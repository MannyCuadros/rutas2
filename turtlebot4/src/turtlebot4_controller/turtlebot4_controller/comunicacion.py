import socket
import threading

from logger import logs

# caracteres de separación
delimitador = "%"
separadorm = "#"
separadorp = "/"

#variables de protocolo
id_cliente = ""     #código t-turtlebot, p-pepper, a-alice, ... + 001-999
nombre_sistema = "" #nombre del robot al que publica o el que subscribe
tipo_sistema = ""   #ROS1, ROS2, sockets, otro...
tipo_mensaje = ""   #p: publicación, s: subscripción
topico = ""
parametros = ""
fin_mensaje = ""


class Comunicacion(threading.Thread):

    # Dirección de servidor
    servidor_ip = "127.0.0.1"
    servidor_puerto = 5000

    def __init__(self, socket=None, direccion=(servidor_ip,servidor_puerto)):
        threading.Thread.__init__(self)
        self.ip = direccion[0]
        self.puerto = direccion[1]
        self.socket_servidor = None
        self.socket_cliente = socket
        print("conexión creada")
    
    def crear_servidor(self):
        # Crear comunicación con el servidor por el puerto 5000
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Enlazar el socket a una dirección y puerto
        self.socket_servidor.bind(('', self.puerto))

        # Escuchar conexiones
        self.socket_servidor.listen()
        logs("Servidor ejecutándose. Esperando conexiones...")


    def conectar_cliente(self, ip_servidor, puerto_servidor):
        self.socket_cliente =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Conectarse al servidor
            self.socket_cliente.connect((ip_servidor,puerto_servidor))
        except:
            mi_ip = self.obtener_ip()
            print(f"Error: {mi_ip} No se pudo conectar al servidor {ip_servidor}:{puerto_servidor}")
            exit(1)
        print("cliene creado")

    def obtener_ip(self):
        try:
            # Crear un socket temporal
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Conectarse a una dirección externa (no se envían datos)
            sock.connect(("8.8.8.8", 80))
            # Obtener la IP local
            ip_address = sock.getsockname()[0]
        except Exception as e:
            print(f"Error al obtener la IP: {e}")
            ip_address = "127.0.0.1"
        finally:
            sock.close()
    
        return ip_address
    
    def enviar_mensaje(self, mensaje):
        if self.socket_servidor is not None:
            self.socket_servidor.send(mensaje.encode())
        if self.socket_cliente is not None:
            self.socket_cliente.send(mensaje.encode())  

    def recibir_mensaje(self):
        if self.socket_servidor is not None:
            return self.socket_servidor.recv(1024).decode()
        if self.socket_cliente is not None:
            return self.socket_cliente.recv(1024).decode()

    def modo(self):
        if self.socket_servidor is not None:
            return (0,"servidor")
        if self.socket_cliente is not None:
            return (1,"cliente")

    def __del__(self):
        if self.socket_servidor is not None:
            self.socket_servidor.close()  # Cerrar la conexión
            print("Se cerró la conexión del servidor")
        if self.socket_cliente is not None:
            self.socket_cliente.close()  # Cerrar la conexión
            print("Se cerró la conexión del cliente")
