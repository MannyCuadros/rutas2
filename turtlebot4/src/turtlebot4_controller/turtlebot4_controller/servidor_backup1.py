
import socket
import threading
import signal

from logger import logs
from record import *
from pythonmongo import *
from protocol import *


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

socket_servidor = None
socket_cliente = None

class Comunicacion(threading.Thread):
    def __init__(self, socket_cliente, direccion_cliente, db):
        threading.Thread.__init__(self)
        self.socket_cliente = socket_cliente
        self.direccion_cliente = direccion_cliente
        self.db = db
        logs("Se conectó el cliente: " + 
              str(direccion_cliente[0]) + ":" + str(direccion_cliente[1]) + "\n")
        

    def run(self):

        while True:
            try:
                # Recibir mensaje del cliente
                # El mensaje llegará en los siguientes formato:
                # %id_cliente#mensaje%                                          # en caso mensaje sea "exit", la conexión termina
                # %id_cliente#nombre_sistema#tipo_sistema#topico%               # en caso topico sea "s", el cliente se subscribe al servidor
                # %id_cliente#nombre_sistema#tipo_sistema#topico#parametros%    # en caso topico sea "p", el cliente se publica en servidor
                mensaje_recibido = self.socket_cliente.recv(1024).decode()
                logs("Cliente: " +  str(self.direccion_cliente[0]) + " -> " + mensaje_recibido)
                
                mensaje = decodificar(mensaje_recibido)

                id_cliente = mensaje[0]

                if len(mensaje) <= 2:
                    if mensaje[1] == "exit":        # fin_mensaje
                        logs("Conexión terminada con " + id_cliente)
                        Comunicacion.__del__()
                        break

                else:
                    nombre_sistema = mensaje[1]
                    tipo_sistema = mensaje[2]
                    topico = mensaje[3]

                    if mensaje[4] == "s":
                        tipo_mensaje = "Subscriber"

                        # Buscar en base de datos por el nombre de sistema y tópico
                        parametros = search_data(self.db, nombre_sistema, topico)

                        # Enviar mensaje al cliente
                        mensaje_enviar = codificar(mensaje, 'p', parametros)
                        logs("Enviando mensaje: " + mensaje_enviar)
                        #mensaje_enviar = input("Servidor: ")
                        self.socket_cliente.send(mensaje_enviar.encode())
                        logs(f"Mensaje enviado a cliente {id_cliente}: {str(self.direccion_cliente[0])}\n" )

                    elif mensaje[4] == "p":
                        tipo_mensaje = "Publisher"
                        parametros = mensaje[5]
                                                
                        create_or_update_collection(self.db, 
                                                    nombre_sistema, 
                                                    tipo_sistema, 
                                                    topico, 
                                                    parametros)

                        datos = {
                            "id_cliente": id_cliente,
                            "nombre_sistema": nombre_sistema,
                            "tipo_sistema": tipo_sistema,
                            "tipo_mensaje": tipo_mensaje,
                            "topico": topico,
                            "parametros": parametros
                        }
                        
                        saveToFile(datos)

                # Enviar mensaje al cliente
                #mensaje_enviar = input("Servidor: ")
                #self.socket_cliente.send(mensaje_enviar.encode())
            except:
                # El cliente ha cerrado la conexión
                logs("Se ha perdido la conexión con el cliente " + 
                      str(self.direccion_cliente[0]) + 
                      ":" + str(self.direccion_cliente[1])+ "\n")
                self.socket_cliente.close()
                break
           

def manejar_senal_sigint(senal, frame):
    print("\n")
    logs("Se ha recibido la señal SIGINT para salir del programa.")
    # Cerrar el socket del servidor
    if socket_servidor is not None:
        socket_servidor.close()

    logs("Fin de programa\n\n\n")
    # Salir del programa
    exit()


def main():
    
    logs("Inicio de programa\n")

    #se conecta a la base de datos de MongoDB
    logs("Servidor ejecutándose. Conectando a MongoDB...")
    d_b = connect_to_database()
    
    # Importar la señal SIGINT
    signal.signal(signal.SIGINT, manejar_senal_sigint)

    global socket_servidor

    # Crear socket
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Enlazar el socket a una dirección y puerto
    socket_servidor.bind(('', 5000))

    # Escuchar conexiones
    socket_servidor.listen()

    logs("Servidor ejecutándose. Esperando conexiones...")
    
    while True:
        global socket_cliente

        # Aceptar la conexión
        socket_cliente, direccion_cliente = socket_servidor.accept()

        # Crear una instancia de la clase "Comunicacion"
        comunicacion = Comunicacion(socket_cliente, direccion_cliente, d_b)

        # Iniciar el hilo
        comunicacion.start()

if __name__ == "__main__":
    main()
