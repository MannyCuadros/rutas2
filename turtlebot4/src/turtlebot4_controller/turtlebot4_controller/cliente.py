import socket
#import sys

#ip = "192.168.0.156"
#ip = "192.168.1.109"
ip = "127.0.0.1"
puerto = 5000

separador =" "
delimitador = "#"
id_cliente = ""     #código t-turtlebot, p-pepper, a-alice, ... + 001-999
nombre_sistema = "" #nombre del robot al que publica o el que subscribe
tipo_sistema = ""   #ROS1, ROS2, sockets, otro...
tipo_mensaje = ""   #p: publicación, s: subscripción
topico = ""
parametros = ""
fin_mensaje = ""

class Comunicacion:
    def __init__(self):

        # Crear socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Conectarse al servidor
            self.socket.connect((ip, puerto))
        except:
            print("Error: No se pudo conectar al servidor " + 
                  ip + ":" + str(puerto))
            exit(1)

    def enviar_mensaje(self, mensaje):
        self.socket.send(mensaje.encode())

    def recibir_mensaje(self):
        return self.socket.recv(1024).decode()
    
    def __del__(self):
        self.socket.close()  # Cerrar la conexión

def main(args=None):
    
    # Crear una instancia de la clase "Comunicacion"
    comunicacion = Comunicacion()

    while True:
        # Enviar mensaje al servidor
        # Mensaje debe estar dividido por # y será en formato
        # id_cliente#sistema#tópico#tipo#parametros
        mensaje_enviar = input("Cliente: ")
        comunicacion.enviar_mensaje(mensaje_enviar)
        encapsulado = mensaje_enviar.split("%")
        mensaje = encapsulado[1].split("#")
        
        id_cliente = mensaje[0]
        if len(mensaje) <= 2:
            fin_mensaje = mensaje[1]
            info = ("ID cliente" + "\t=\t" + id_cliente + "\n" + 
                    "Mensaje" + "\t\t=\t" + fin_mensaje  + "\n")
            print(info)
            
            if fin_mensaje == "exit":
                print("Conexión terminada")
                comunicacion.__del__()
                break

        else:
            nombre_sistema = mensaje[1]
            tipo_sistema = mensaje[2]
            topico = mensaje[3]

            info = ("ID cliente" + "\t=\t" + id_cliente + "\n" + 
                    "Nombre sistema" + "\t=\t" + nombre_sistema + "\n" +
                    "Tipo de sistema" + "\t=\t" + tipo_sistema + "\n" + 
                    "Tópico" + "\t\t=\t" + topico + "\n")

            if mensaje[4] == "p":
                tipo_mensaje = "Publisher"
                parametros = mensaje[5]
                info = (info + 
                       "Tipo de mensaje" + "\t=\t" + tipo_mensaje + "\n" +
                       "Parámetros" + "\t=\t" + parametros + "\n")  
                print(info)
                
            elif mensaje[4] == "s":
                tipo_mensaje = "Subscriber"
                
                info = (info + 
                       "Tipo de mensaje" + "\t=\t" + tipo_mensaje + "\n")
                print(info)

                # Recibir mensaje del servidor
                
                mensaje_recibido = comunicacion.recibir_mensaje()
                print("recibiendo...")
                print(mensaje_recibido)
                encapsulador = mensaje_recibido.split("%")
                recibido = encapsulador[1].split("#")
                parametros = recibido[5]
                print("Parámetros" + "\t=\t" + parametros + "\n")
                
            else:
                tipo_mensaje = " "
                print(info)
        

if __name__ == "__main__":
    main()
