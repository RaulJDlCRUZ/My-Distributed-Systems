# Tema 3: Invocación Remota

Paradigmas de programación que permiten llamar a bloques de código pertenecientes a un proceso (remoto).

## Remote Procedure Call (RPC)

RPC intenta simplificar la programación de aplicaciones distribuidas haciendo que la distribución sea transparente, es decir, hacer que se parezca lo más posible a la programación convencional. El tiempo de ejecución de RPC oculta la mayoría de los detalles de la comunicación:

- Conexión/desconexión
- _Marshalling_ (serialización) / _Unmarshalling_
- Paso de mensajes

### RPC desde cero

La explicación completa de la implementación o bosquejo RPC se encuentra [aquí](./Ejemplos/RPC/rpc-from-scratch/README.md)
- [`client.py`](./Ejemplos/RPC/rpc-from-scratch/client.py)
- [`server.py`](./Ejemplos/RPC/rpc-from-scratch/server.py)

### ONC RPC: XDR

También denominado Sun RPC, permite usar llamadas a procedimientos remotos a través de UDP o TCP. Emplea semántica at-least-once. Proporciona un lenguaje de interfaz llamado XDR y un compilador de interfaz llamado `rpcgen`, que está diseñado para usarse con el lenguaje de programación C.

- El compilador `rpcgen` toma un archivo XDR para generar _stubs_ (códigos auxiliares) para usar en el servidor y el cliente.
- La mayoría de los idiomas permiten especificar nombres de interfaz, pero Sun RPC no; en lugar de esto, se proporcionan un número de programa y un número de versión:

**`hello.x`**
```
program MESSAGE_PROG {
    version PRINTMESSAGE_VERS {
    int PRINTMESSAGE(string) = 1;
    int PRINT_MESSAGE_COLOR(string, string) = 2;
    } = 2;
    version PRINTMESSAGE_VERS {
        int PRINTMESSAGE(string) = 1; /* procedure number */
    } = 1;                            /* version number */
} = 600000000;                        /* program number */
```

### gRPC

#### Hola Mundo! con gRPC

**`hello.proto`**
```
syntax = "proto3";

package hello;

service Hello {
  rpc write (PrintRequest) returns (PrintReply) {}
}

message PrintRequest {
  string message = 1;
}

message PrintReply {}
```

**Cliente**
```python
server = sys.argv[1]
port = sys.argv[2]
channel = grpc.insecure_channel(f'{server}:{port}')
stub = hello_pb2_grpc.HelloStub(channel)
message = hello_pb2.PrintRequest(message='hello')
stub.write(message)
```

**Servidor**
```python
class Hello(hello_pb2_grpc.HelloServicer):
    def write(self, request, context):
        print("Client sent: '{}'".format(request.message))
        return hello_pb2.PrintReply()


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
hello_pb2_grpc.add_HelloServicer_to_server(Hello(), server)
server.add_insecure_port('0.0.0.0:2000')
server.start()
```

## Remote Method Invocation (RMI)

RMI es la contraparte orientada a objetos de RPC. En RMI, un objeto que llama puede invocar un método en un objeto potencialmente remoto. Al igual que con RPC, los detalles subyacentes generalmente están ocultos para el usuario. _Es la base del Middlewares Orientado a Objetos_.

### Hola Mundo! ZeroC Ice

>:warning: Para ejecutar este ejemplo se requiere `python3-zeroc-ice` (paquete debian)

**Interfaz**
- Característica clave en RMI Middlewares. Especificado en un IDL (lenguaje de definición de interfaz)
    ```
    module Example {
        interface Printer {
            void write(string message);
        };
    };
    ```

**Cliente**

```console
$ ./Client.py "<proxy>"
 ...por ejemplo:
  ./Client.py 'printer1 -t -e 1.1:tcp -h 192.168.8.120 -p 7070
```

```python
Ice.loadSlice('Printer.ice')
import Example

class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        printer = Example.PrinterPrx.checkedCast(proxy)

        if not printer:
            raise RuntimeError('Invalid proxy')

        printer.write('Hello World!')

        return 0

sys.exit(Client().main(sys.argv))
```

**Servidor**

```console
$ ./Server.py --Ice.Config=Server.config
printer1 -t -e 1.1:tcp -h 192.168.8.120 -p 7070
0: Hello World!
```
Donde la configuración del servidor es del estilo:

    PrinterAdapter.Endpoints=tcp -p 7070

```python
Ice.loadSlice('Printer.ice')
import Example


class PrinterI(Example.Printer):
    n = 0

    def write(self, message, current=None):
        print("{0}: {1}".format(self.n, message))
        sys.stdout.flush()
        self.n += 1


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = PrinterI()

        adapter = broker.createObjectAdapter("PrinterAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("printer1"))

        print(proxy)
        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))
```

### Java RMI

Es un sistema de un solo lenguaje: las interfaces remotas se definen en el lenguaje Java. _Esto significa que no hay un IDL_. Las interfaces remotas se definen extendiendo una interfaz llamada _Remote_ proporcionado en el paquete `java.rmi` (y `java.rmi.server`).

- Los métodos deben lanzar `RemoteException`, pero también se pueden generar excepciones específicas de la aplicación.

**Interfaz**

```java
import java.rmi.Remote;
import java.rmi.RemoteException;

public interface Hello extends Remote {
    String sayHello() throws RemoteException;
}
```

```console
java-rmi$ rmiregistry &
```

**Cliente**

```java
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class Client {
    private Client() {}

    public static void main(String[] args) {
        String host = (args.length < 1) ? null : args[0];
        try {
            Registry registry = LocateRegistry.getRegistry(host);
            Hello stub = (Hello) registry.lookup("Hello");
            String response = stub.sayHello();
            System.out.println("response: " + response);

        } catch (Exception e) {
            System.err.println("Client exception: " + e.toString());
            e.printStackTrace();
        }
    }
}
```

```console
java-rmi$ make run-client
response: Hello, world!
```

**Servidor**

```java
import java.rmi.registry.Registry;
import java.rmi.registry.LocateRegistry;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class Server implements Hello {
    public String sayHello() {
        return "Hello, world!";
    }

    public static void main(String args[]) {
        try {
            Server obj = new Server();
            Hello stub = (Hello) UnicastRemoteObject.exportObject(obj, 5000);

            // Bind the remote object's stub in the registry
            Registry registry = LocateRegistry.getRegistry();
            registry.rebind("Hello", stub);

            System.err.println("Server ready");

        } catch (Exception e) {
            System.err.println("Server exception: " + e.toString());
            e.printStackTrace();
        }
    }
}
```

```console
java-rmi$ make run-server
Server ready
```

## REST

Es un estilo arquitectónico. Una API que cumple con los principios de este estilo es una API
'RESTful'. REST transfiere representaciones de estados de recursos:

- Cada recurso se identifica mediante una URL única.
- Los cambios de estado son impulsados por métodos de recursos (normalmente HTTP)

### Flask

**Cliente**

```python
from requests import put, get

print(get('http://localhost:5000/').json())

device_id = "door1"
response = get(f'http://localhost:5000/{device_id}')
print(response.json())

put(f'http://localhost:5000/{device_id}', data={'status': 'disabled'})
print(get(f'http://localhost:5000/{device_id}').json())
```

**Servidor**

```python
from flask import Flask, request
from flask_restful import Resource, Api, abort

app = Flask(__name__)
api = Api(app)

devices = {
    'switch1': 'enabled',
    'light1': 'disabled',
}


class Device(Resource):
    def get(self, device_id):
        if device_id not in devices:
            abort(404)

        return {device_id: devices.get(device_id)}

    def put(self, device_id):
        devices[device_id] = request.form['status']
        return {device_id: devices[device_id]}


class DeviceList(Resource):
    def get(self):
        return devices


api.add_resource(DeviceList, '/')
api.add_resource(Device, '/<string:device_id>')


if __name__ == '__main__':
    app.run(debug=True)
```

> pip install Flask