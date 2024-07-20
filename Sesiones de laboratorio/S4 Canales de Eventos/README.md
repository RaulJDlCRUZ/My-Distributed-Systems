# Sesión 4: Canales de eventos
Estudia y ejecuta el ejemplo [_IceStorm_](./icestorm/README) del repositorio de ejemplos para ver cómo puedes implementar canales de eventos con ZeroC Ice. 

Como ejercicio, adapta el ejemplo del repositorio para que cada vez que el objeto Printer recibe un evento write, en vez de imprimirlo, notifique a otro objeto PrintRegister con esa cadena. Este último objeto almacenará todas las cadenas enviadas al objeto Printer, e imprimirá la lista de cadenas recibidas cada vez que llegue una nueva una notificación.