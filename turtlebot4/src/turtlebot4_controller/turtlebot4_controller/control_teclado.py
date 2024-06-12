#!/usr/bin/env python3

import pygame
import sys
import time

#libreria de socket
import socket

ip = "127.0.0.1"
#ip = "192.168.1.111"
#ip = "192.168.0.156"
#ip = "192.168.1.109"
#ip = "64.23.166.80"
puerto = 5000

# caracteres de separación
delimitador = "%"
separadorm = "#"
separadorp = "/"

# variables de mensaje
id_cliente = ""     #código t-turtlebot, p-pepper, a-alice, ... + 001-999
nombre_sistema = "" #nombre del robot al que publica o el que subscribe
tipo_sistema = ""   #ROS1, ROS2, sockets, otro...
tipo_mensaje = ""   #p: publicación, s: subscripción
topico = ""
parametros = ""
fin_mensaje = ""

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

tiempo = 0.01
n = 0

#Colocar clase para iniciar comunicación
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

    def conectar(self, ip, puerto):
        try:
            # Conectarse al servidor
            self.socket.connect((ip, puerto))
        except:
            print("Error: No se pudo conectar al servidor " + 
                  ip + ":" + str(puerto))
            exit(1)

    def desconectar(self):
        self.socket.close()
        print("Se ha cerrado la conexión del servidor")

    def recibir_mensaje(self):
        return self.socket.recv(1024).decode()
    
    def __del__(self):
        self.socket.close()  # Cerrar la conexión


# Función para imprimir el estado de las teclas en la ventana
def print_key_state(window, font, x, a):
    window.fill(BLACK)
    text_x = font.render("x = {}".format(x), True, WHITE)
    text_a = font.render("a = {}".format(a), True, WHITE)
    window.blit(text_x, (20, 20))
    window.blit(text_a, (20, 60))
    pygame.display.flip()

def main():
    # Inicializar pygame
    pygame.init()

    # Definir el tamaño de la ventana
    window_width = 200
    window_height = 100
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Control")


    # Definir fuente
    font = pygame.font.Font(None, 36)

    # Definir las variables para el estado de las teclas
    x = 0.0
    a = 0.0

    n = 0
    key_flag = 0
    com_flag = 0
    
    teclas_presionadas = {
    pygame.K_UP: False,
    pygame.K_DOWN: False,
    pygame.K_LEFT: False,
    pygame.K_RIGHT: False
    }   

    # Crear una instancia de la clase "Comunicacion"
    #comunicacion = Comunicacion()
    
    # Bucle principal
    while True:
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                time.sleep(0.2)
                id_cliente = "pc001"
                fin_mensaje = "exit"
                mensaje_enviar = (delimitador +
                                  id_cliente + separadorm + 
                                  fin_mensaje + delimitador)
                comunicacion = Comunicacion()
                #comunicacion.conectar(ip,puerto)
                comunicacion.enviar_mensaje(mensaje_enviar)
                time.sleep(tiempo)
                #comunicacion.desconectar()

                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                key_flag = 1
                if event.key == pygame.K_UP:
                    x = 2.0
                elif event.key == pygame.K_DOWN:
                    x = -2.0
                elif event.key == pygame.K_RIGHT:
                    a = -1.0
                elif event.key == pygame.K_LEFT:
                    a = 1.0
            elif event.type == pygame.KEYUP:
                key_flag = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    x = 0.0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    a = 0.0

        # Imprimir el estado de las teclas en consola
        print_key_state(window, font, x, a)

        if not key_flag and not com_flag:

            id_cliente = "pc001"        #código t-turtlebot, p-pepper, a-alice, ... + 001-999
            nombre_sistema = "turtle1"  #robot al que se desea publicar o el que subscribe
            tipo_sistema = "ROS2"       #ROS1, ROS2, sockets, otro...
            tipo_mensaje = "p"          #p: publicación, s: subscripción
            topico = "cmd_vel"
            parametros = (str(x) + separadorp + 
                        str(0.0) + separadorp +
                        str(0.0) + separadorp +
                        str(0.0) + separadorp +
                        str(0.0) + separadorp + 
                        str(a))
            fin_mensaje = ""

            msg = ("ID cliente" + "\t=\t" + id_cliente + "\n" + 
                    "Nombre sistema" + "\t=\t" + nombre_sistema + "\n" +
                    "Tipo de sistema" + "\t=\t" + tipo_sistema + "\n" + 
                    "Tópico" + "\t\t=\t" + topico + "\n" +
                    "Tipo de mensaje" + "\t=\t" + tipo_mensaje + "\n" +
                    "Parámetros" + "\t=\t" + parametros + "\n")
            print(msg)

            mensaje_enviar = (delimitador + 
                            id_cliente + separadorm + 
                            nombre_sistema + separadorm + 
                            tipo_sistema + separadorm + 
                            topico + separadorm + 
                            tipo_mensaje + separadorm + 
                            parametros + delimitador)
            print(str(n) + " -> " + mensaje_enviar + "\n")
            n = n + 1

            comunicacion = Comunicacion()
            #comunicacion.conectar(ip,puerto)
            comunicacion.enviar_mensaje(mensaje_enviar)
            time.sleep(tiempo)
            #comunicacion.desconectar()
            com_flag = 1

        elif key_flag:
            id_cliente = "pc001"        #código t-turtlebot, p-pepper, a-alice, ... + 001-999
            nombre_sistema = "turtle1"  #robot al que se desea publicar o el que subscribe
            tipo_sistema = "ROS2"       #ROS1, ROS2, sockets, otro...
            tipo_mensaje = "p"          #p: publicación, s: subscripción
            topico = "cmd_vel"
            parametros = (str(x) + separadorp + 
                        str(0.0) + separadorp +
                        str(0.0) + separadorp +
                        str(0.0) + separadorp +
                        str(0.0) + separadorp + 
                        str(a))
            fin_mensaje = ""

            msg = ("ID cliente" + "\t=\t" + id_cliente + "\n" + 
                    "Nombre sistema" + "\t=\t" + nombre_sistema + "\n" +
                    "Tipo de sistema" + "\t=\t" + tipo_sistema + "\n" + 
                    "Tópico" + "\t\t=\t" + topico + "\n" +
                    "Tipo de mensaje" + "\t=\t" + tipo_mensaje + "\n" +
                    "Parámetros" + "\t=\t" + parametros + "\n")
            print(msg)

            mensaje_enviar = (delimitador + 
                            id_cliente + separadorm + 
                            nombre_sistema + separadorm + 
                            tipo_sistema + separadorm + 
                            topico + separadorm + 
                            tipo_mensaje + separadorm + 
                            parametros + delimitador)
            print(str(n) + " -> " + mensaje_enviar + "\n")
            n = n + 1
            
            comunicacion = Comunicacion()
            #comunicacion.conectar(ip,puerto)
            comunicacion.enviar_mensaje(mensaje_enviar)
            time.sleep(tiempo)
            #comunicacion.desconectar()
            com_flag = 0
    
        #time.sleep(tiempo)
        

if __name__ == "__main__":
    main()