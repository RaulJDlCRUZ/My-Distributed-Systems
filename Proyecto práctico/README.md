# Proyecto de Prácticas: **Gestor de archivos distribuido**

El objetivo principal del proyecto es diseñar un sistema cliente-servidor que permita la subida y descarga de ficheros. En los siguientes apartados se describirán los detalles de cada uno de los componentes que componen el sistema, así como las interfaces que determinarán los métodos que deberán implementar.<br>
También se darán pautas para facilitar el proceso de desarrollo, dividiendo el proyecto en varias fases.

## 1\. Componentes e interacciones
El sistema estará formado por cinco tipos de componentes: los sirvientes de tipo **`Uploader`**, que funcionarán como manejadores del proceso de subida de un fichero; los de tipo **`Downloader`**, que se encargarán de la descarga de ficheros; los de tipo **`FileManager`**, que se encargarán de la gestión de los `Uploader` y `Downloader`, y del borrado de ficheros; y los de tipo **`Frontend`**, que harán de intermediarios entre las peticiones de los clientes y los FileManager, llevando un registro de los ficheros existents en el sistema. Por supuesto, también habrá **clientes**, que serán los encargados de solicitar la subida y descarga de ficheros.
### 1.1. Cliente
El cliente es el componente que se encarga de solicitar la subida, la descarga, o el borrado de ficheros. Para ello, se proporciona el nombre del fichero a subir, o el _hash_ del fichero a borrar o descargar. Como se verá en la [Sección 1.2](#12-frontend), el `Frontend`, que es el tipo de sirviente con el que interacciona directamente el cliente, también permite listar todos los ficheros existentes en el sistema distribuido. La aplicación cliente debe implementar una forma cómoda de interactuar con el sistema, y debe permitir al usuario realizar las acciones mencionadas.
### 1.2. Frontend
El `Frontend` es el componente encargado de gestionar las peticiones de los clientes y de llevar un registro de los ficheros que existen en el sistema, que pueden estar distribuidos en diferentes nodos y ser accesibles por medio de distintos `FileManager`. Para ello, el Frontend debe ser capaz de:

1) de comunicarse con todos los `FileManager` existentes en el sistema
2) de llevar un control de qué ficheros se añaden y se borran del sistema (solo cuando la tarea haya terminado)
3) de sincronizarse con otros `Frontend` para mantener el registro de ficheros actualizado. Concretamente:
    - El `Frontend` siempre está a la espera de recibir peticiones de subida, descarga o borrado de ficheros, o de listar todos los ficheros existentes en el sistema, por parte de aplicaciones cliente.
    - Cuando se solicita el listado de ficheros disponibles, el Frontendretorna una lista de tipo `FileList` con todos los ficheros que figuran en su registro en estructuras `FileInfo`, que contienen el nombre del fichero y su hash.

        <pre>
        struct FileInfo {
            string name;
            string hash;
        };

        sequence<FileInfo> FileList;
        FileList getFileList();</pre>
    
    - Cuando se solicita la subida de un fichero, indicando el nombre del fichero, el `Frontend` solicita a un `FileManager` (selecciona el que menos ficheros tenga) la creación de un Uploader para dicho fichero, y retorna la referencia del Uploadercreado. Si el nombre del fichero ya figura en el registro, lanza una excepción.

        <pre>
            Uploader* uploadFile(string filename) throws FileNameInUseError;</pre>
    
    - Cuando se solicita la _descarga_ de un fichero, indicando el hash del fichero, el `Frontend` solicita a un `FileManager` (selecciona el que contiene el fichero de interés) la creación de un `Downloader` para dicho fichero, y retorna la referencia del `Downloader` creado. Si el fichero no figura en el registro, lanza una excepción.

        <pre>
            Downloader* downloadFile(string hash) throws FileNotFoundError;</pre>

    - Cuando se solicita el _borrado_ de un fichero, indicando el hash del fichero, el `Frontend` solicita a un `FileManager` (selecciona el que contiene el fichero de interés) el borrado de dicho fichero. Si el fichero no figura en el registro, lanza una excepción.

        <pre>
            void removeFile(string hash) throws FileNotFoundError;</pre>
    
Es importante tener en cuenta que las tareas de adición y borrado de ficheros que se han listado anteriormente no añaden o eliminan los ficheros del registro del `Frontend`, solo del almacenamiento (en el lado del `FileManager`). El registro del Frontendse actualiza cuando el `FileManager` le notifica que la tarea, de adición o de borrado, ha terminado por medio de un canal de eventos denominado `FileUpdates`. Este canal de eventos, que se implementa por medio de sirvientes con el mismo nombre, `FileUpdates`, permite al `Frontend` mantener su registro de ficheros actualizado.<br>
Concretamente, esta actualización consiste en:

1. Cuando se termina la tarea de subida o de borrado de un fichero, el `Uploader` o el `FileManager`, respectivamente, notifica que la tarea ha terminado enviando un evento con una estructura `FileData` al canal de eventos `FileUpdates` con la información del archivo y la referencia del `FileManager` que lo gestiona.

    <pre>
    struct FileData {
        FileInfo fileInfo;
        FileManager* fileManager;
    };<br>
    interface FileUpdates {
        void new(FileData file);
        void removed(FileData file);
    };</pre>

2. Cuando los objetos suscriptores `FileUpdates` existentes en cada servidor reciben el evento, se lo hacen llegar a los `Frontend`.
3. Cuando al `Frontend` le llega la información, actualiza su registro de ficheros.

De la misma forma, para actualizar los registros de ficheros de los `Frontend` que se lancen una vez el sistema ya esté en marcha, se implementa un canal de eventos denominado `FrontendUpdates`.
Este canal de eventos, que se implementa por medio de sirvientes con el mismo nombre, `FrontendUpdates`, permite al `Frontend` nuevo poner su registro de ficheros al día. Concretamente, esta actualización consiste en:

1. Cuando se lanza un nuevo `Frontend`, este publica un evento con su proxy directo en el canal de eventos `FrontendUpdates`. Es decir, invocando el método `newFrontend` del _publisher_ `FrontendUpdates`.

    <pre>
    interface FrontendUpdates {
        void newFrontend(Frontend* newFrontend);
    };</pre>

2. Cuando los objetos suscriptores `FrontendUpdates` existentes en cada servidor reciben el evento, se lo hacen llegar a los `Frontend`, incluido el nuevo (tendrá que filtrar su propio evento), y estos responden al nuevo `Frontend` con su proxy directo por medio de una _invocación remota_.

    <pre>
    void replyNewFrontend(Frontend* oldFrontend);</pre>

3. Una vez los `Frontend` responden al nuevo objeto, envían su registro de ficheros al nuevo `Frontend` por medio de eventos publicados en el canal de eventos `FileUpdates`.

Esta forma de actualizar el registro de ficheros, aunque eficaz, **no es eficiente**, ya que yodos los sirvientes `Frontendexistentes` envían su registro completo de ficheros cada vez que se lanza un nuevo `Frontend`. Se propondrá la implementación de una mejora más adelante.

### 1.3. FileManager

El `FileManager` es el componente localizado en el lugar donde se almacenarán los archivos, y es el encargado de crear sirvientes `Downloader` y `Uploader` a demanda. Cada vez que se solicita la subida o la descarga de un fichero, se crea un sirviente de estos tipos, que se encargará de gestionar la tarea y será destruido al terminar. El `FileManager` también gestiona el borrado de ficheros, y solamente interacciona de forma directa con los Frontend. Concretamente:

- Está siempre a la espera de recibir peticiones de creación de sirvientes `Uploader` y `Downloader` por parte de los `Frontend`.
- Cuando se solicita la subida de un fichero, indicando el nombre del fichero, crea un sirviente `Uploader` y retorna su referencia.

    <pre>
    Uploader* createUploader(string filename);</pre>

- Cuando se solicita la descarga de un fichero, indicando el _hash_ del fichero, crea un sirviente `Downloader` y retorna su referencia. Si el fichero no existe, no crea el objeto y lanza una excepción.

    <pre>
    Downloader* createDownloader(string hash) throws FileNotFoundError;</pre>

- Cuando se solicita el borrado de un fichero, indicando el hash del fichero, le indica al `FileManager` que lo contiene que borre el fichero. Si el fichero no existe, lanza una excepción.

    <pre>
    void removeFile(string hash) throws FileNotFoundError;</pre>

### 1.4. Uploader

El `Uploader` es el componente encargado de gestionar la subida de un fichero al sistema. Cuando estos objetos se crean, abren el fichero en el que se va a escribir, y se quedan a la espera de recibir los datos del fichero. Cuando se termina de escribir el fichero, se cierra y se notifica mediante un evento de que la tarea ha terminado. Concretamente:

- Cuando es creado, queda a la espera de recibir los datos del fichero que se desea almacenar.
- Cuando se recibe un bloque de datos, que se ha enviado directamente desde el cliente, se escribe en el fichero.

    <pre>
    void send(string data);</pre>

- Cuando no hay más datos que mandar, el cliente guarda el archivo. En este momento, el archivo se almacena con el hash del fichero como nombre. En caso de que ya exista un fichero con ese hash (es decir, el archivo ya ha sido subido, pero con otro nombre), se lanza una excepción que contiene el hash del fichero que ya existe. Si el fichero es almacenado sin problemas, se publica un evento en el canal de eventos `FileUpdates` para notificar que la tarea ha terminado y para que los Frontendpuedan actualizar sus registros, y se retorna al cliente una estructura FileInfocon el nombre del fichero y su hash.

    <pre>
    FileInfo save() throws FileAlreadyExistsError;</pre>

- Finalmente, el `Uploader` se destruye bajo petición explícita del cliente.

    <pre>
    void destroy();</pre>

### 1.5. Downloader

El `Downloader` es el componente encargado de gestionar la descarga de un fichero del sistema. Cuando estos objetos se crean, abren el fichero que se va a leer, y se quedan a la espera de recibir peticiones de lectura de datos. El cliente debe detectar cuándo ha terminado de leer el fichero, y destruir el objeto explícitamente. Concretamente:

- Cuando es creado, abre el fichero que se desea leer y queda a la espera de recibir peticiones de lectura de datos.
- Cuando se recibe una petición de lectura de datos, se lee un bloque de datos del fichero de un tamaño concreto y se retorna al cliente.

    <pre>
    string recv(int size);</pre>

- Cuando el cliente ha terminado de leer el fichero, destruye el objeto explícitamente.

    <pre>
    void destroy();</pre>

## 2\. Fases de desarrollo

Con el objetivo de facilitar el desarrollo de la aplicación, el proceso de implementación se divide en tres fases, cada una de las cuales añade funcionalidades nuevas al sistema. En la primera fase se debe implementar el funcionamiento básico del sistema; en la segunda fase, una versión que soporte múltiples servidores con sirvientes de diverso tipo; y, finalmente, en la tercera fase se ha de configurar la gestión de la aplicación con IceGrid.

### 2.1. FASE 1: Funcionamiento básico

En esta fase se debe implementar el funcionamiento básico del sistema, que consiste en la subida, descarga y borrado de ficheros. Para ello, es necesario habilitar con _icegridregistry_ transparencia de localización, y se debe implementar una primera versión del código del `Frontend`, del
`FileManager`, del `Uploader` y del `Downloader`, así como el código de la aplicación cliente. En concreto, en esta fase se debe conseguir:

- Un cliente capaz de subir, descargar y borrar ficheros.
- Un `Frontend` capaz de gestionar las peticiones de los clientes, y de crear `Uploader` y `Downloader` en los `FileManager`.
- Un `FileManager` capaz de crear `Uploader` y `Downloader` a demanda, y de gestionar el borrado de ficheros.
- Un `Uploader` capaz de recibir los datos de un fichero y de almacenarlos en el sistema.
- Un `Downloader` capaz de leer los datos de un fichero y de enviarlos al cliente.

Sin embargo, en esta fase no se debe utilizar _IceStorm_, ni es necesaria la gestión de múltiples servidores. Es decir, que **solamente deben ser funcionales un cliente, un `Frontend`, y un `FileManager`**. Por tanto, el `Frontend` **no** tiene que sincronizarse con otros `Frontend` y, puesto que no se usan canales de eventos, no mantiene un registro de ficheros. En este contexto, el `Frontend` aún no implementa el listado de ficheros y, por ello, _el cliente debe conocer los ficheros que ha subido para poder hacer peticiones de descarga y borrado_.

### 2.2 FASE 2: IceStorm y Múltiples servidores

En esta fase se debe implementar la gestión de múltiples servidores, y se debe utilizar IceStorm para la comunicación asíncrona entre los Frontendy los FileManager. En concreto, en esta fase se debe conseguir:

- Un cliente capaz de subir, descargar, borrar y listar ficheros.
- Un `Frontend` capaz de gestionar las peticiones de los clientes, creando objetos `Uploader` y `Downloader` en los `FileManager`, y manteniendo un registro de ficheros actualizado (sincronización de `Frontends`).
- Un `FileManager` capaz de crear `Uploader` y `Downloader` a demanda, y de gestionar el borrado de ficheros. Debe poder notificar que la tarea de borrado ha terminado por medio de eventos.
- Un `Uploader` capaz de recibir los datos de un fichero y de almacenarlos en el sistema. Debe poder notificar que la tarea ha terminado por medio de eventos.
- Un `Downloader` capaz de leer los datos de un fichero y de enviarlos al cliente.
- Objetos `FrontendUpdates` y `FileUpdates` que permitan la sincronización de `Frontends` y la actualización de los registros de ficheros.

En esta fase debe ser posible ejecutar más de un `Frontend` y más de un `FileManager`. El cliente podrá utilizar cualquiera de los `Frontend` disponibles, y los `Frontend` deben conocer todos los `FileManager` en marcha para distribuir las tareas de subida de ficheros y para saber a quién asignar tareas de descarga o de borrado.

### 2.3. FASE 3: Gestión de la aplicación con IceGrid

En esta fase la aplicación debe implementarse de modo que sea posible llevar a cabo su despliegue con _IceGrid_. La aplicación se debe llamar _URFSApp_, y debe quedar configurada en tres nodos de la siguiente manera:

- **Nodo 1**: Aloja el binder, un servidor _IcePatch2_, y un servidor de _IceStorm_.
- **Nodo 2**: Aloja tres servidores `Frontend`, definidos mediante una plantilla. Estos servidores deberán pertenecer a un grupo de réplica alcanzable por medio del identificador _frontend_.
- **Nodo 3**: Aloja dos servidores `FileManager`, definidos mediante una plantilla. Sus proxies indirectos serán conocidos por los `Frontend`.

Configura los servidores `Frontend` para que arranquen solo bajo demanda, y configura los servidores `FileManager` para que arranquen automáticamente. El cliente debe conectar con los `Frontend` por medio del proxy del grupo de réplica _frontend_, no a través de los proxies directos/indirectos de cada sirviente.

-----

Actualmente, sólo tienes a tu disposición algunos archivos iniciales para implementar el proyecto URFS.

- Un `Makefile` que te indica cómo ejecutar cada elemento del sistema (estos comandos se utilizarán durante la evaluación, por lo que debes desarrollar el sistema de acuerdo con ellos).
- Un archivo Slice llamado `urfs.ice`, donde se han especificado las interfaces.
- Una implementación básica del script `Client.py` (proporcionando sólo el proceso de carga).
- Una imagen `example.png` para pruebas.

Desarrolla la aplicación de acuerdo con las especificaciones, y recuerda que **no puedes modificar `urfs.ice` y el `Makefile`**.

#### Implementación

**Nivel básico**, no se considera el desarrollo de un frontend web mínimo para el cliente ni la mejora del método de actualización/sincronización de registros de ficheros de los Frontend.