from comunicacion import Comunicacion
from logger import *
from record import *
from pythonmongo import *
from protocol import *
import signal

ip = "127.0.0.1"
puerto = 5000


def manejar_senal_sigint(senal, frame):
    
    logs("Se ha recibido la señal SIGINT para salir del programa.")
    # Cerrar el socket del servidor
    #print(comm.socket_servidor)
    #if comm.socket_servidor is not None:
    #    comm.__del__()

    logs("Fin de programa\n\n\n")
    # Salir del programa
    exit()

def ejecutar(comm:Comunicacion, db):

    while True:
        try:
            # Recibir mensaje del cliente
            # El mensaje llegará en los siguientes formato:
            # %id_cliente#mensaje%                                          # en caso mensaje sea "exit", la conexión termina
            # %id_cliente#nombre_sistema#tipo_sistema#topico%               # en caso topico sea "s", el cliente se subscribe al servidor
            # %id_cliente#nombre_sistema#tipo_sistema#topico#parametros%    # en caso topico sea "p", el cliente se publica en servidor
            mensaje_recibido = comm.recibir_mensaje()
            logs("Cliente: " +  str(comm.ip) + " -> " + mensaje_recibido)
                
            mensaje = decodificar(mensaje_recibido)

            id_cliente = mensaje[0]

            if len(mensaje) <= 2:
                if mensaje[1] == "exit":        # fin_mensaje
                    logs("Conexión terminada con " + id_cliente)
                    comm.__del__()
                    break

            else:
                nombre_sistema = mensaje[1]
                tipo_sistema = mensaje[2]
                topico = mensaje[3]

                if mensaje[4] == "s":
                    tipo_mensaje = "Subscriber"
            
                    # Buscar en base de datos por el nombre de sistema y tópico
                    parametros = search_data(db, nombre_sistema, topico)
                    # Enviar mensaje al cliente
                    mensaje_enviar = codificar(mensaje, 'p', parametros)
                    logs("Enviando mensaje: " + mensaje_enviar)
                    #mensaje_enviar = input("Servidor: ")
                    comm.enviar_mensaje(mensaje_enviar)
                    logs(f"Mensaje enviado a cliente {id_cliente}: {str(comm.ip)}\n")

                elif mensaje[4] == "p":
                    tipo_mensaje = "Publisher"
                    parametros = mensaje[5]
                                                
                    create_or_update_collection(db, 
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
            # mensaje_enviar = input("Servidor: ")
            # self.socket_cliente.send(mensaje_enviar.encode())
        except:
            # El cliente ha cerrado la conexión
            logs("Se ha perdido la conexión con el cliente " + 
                 str(comm.ip) + 
                 ":" + str(comm.puerto)+ "\n")
            comm.__del__()
            break



def main():
    
    logs("Inicio de programa\n")

    #se conecta a la base de datos de MongoDB
    logs("Conectando a MongoDB...")
    db = connect_to_database()

    #Se crea el servidor. Por defecto se usa el puerto 5000
    logs("Abriendo conexiones...")
    servidor = Comunicacion()
    servidor.crear_servidor()

    # Importar la señal SIGINT
    signal.signal(signal.SIGINT, manejar_senal_sigint)

    while True:

        # Aceptar la conexión
        socket_cliente, direccion_cliente = servidor.socket_servidor.accept()
        
        # Crear una instancia de la clase "Comunicacion"
        cliente = Comunicacion(socket_cliente, direccion_cliente)
        logs("Se conectó el cliente: " + 
             str(direccion_cliente[0]) + ":" + 
             str(direccion_cliente[1]) + "\n")

        # Iniciar hilo
        ejecutar(cliente, db)
        socket_cliente.close()

if __name__ == "__main__":
    main()
