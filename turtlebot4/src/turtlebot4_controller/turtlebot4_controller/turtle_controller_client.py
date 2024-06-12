#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

from comunicacion import *
from logger import *
from protocol import *

import sys
import time

tiempo = 0.01
ip = "127.0.0.1"
puerto = 5000

class TrutleClientNode(Node):

    def __init__(self):
        self.x = 0.0
        self.z = 0.0
        self.vlinear = 1.0
        self.vangular = 1.0
        self.count_send = 0
        self.count_received = 0
        self.cliente = Comunicacion()
        
        super().__init__("control_turtle_client")
        self.cmd_vel_pub_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer = self.create_timer(0.01,self.subscribe_velocity)
        self.get_logger().info("Turtle Controller Client has been started.")

    def pose_callback(self, pose: Pose):
        cmd = Twist()
              
        if pose.x > 9.0 or pose.x < 2.0 or pose.y > 9.0 or pose.y < 2.0:
            cmd.linear.x = 1.0
            cmd.angular.z = 0.9
        else:
            cmd.linear.x = 5.0
            cmd.angular.z = 0.0
        
        self.cmd_vel_pub_.publish(cmd)
    
    def subscribe_velocity(self):
        
        self.cliente.conectar_cliente(ip, puerto)

        #%pc001#turtle2#ROS2#cmd_vel#p#0.0/0.0/0.0/0.0/0.0/0.0%
        datos = ["pc001", "turtle1", "ROS2", "cmd_vel", "s"]
        mensaje_enviar = codificar(datos)
        print(str(count_send) + ": " + mensaje_enviar + "\n")
        self.cliente.enviar_mensaje(mensaje_enviar)
        count_send += 1
        time.sleep(tiempo)
        mensaje_recibido = self.cliente.recibir_mensaje()
        count_received += 1
        print("recibiendo...")
        print(str(count_received) + ": " + mensaje_recibido)
        mensaje = decodificar(mensaje_recibido)
        parametros = mensaje[5]
        velocidad = parametros.split("/")
        self.x = float(velocidad[0])
        self.z = float(velocidad[5])
        
        print("X = " + str(self.x) + " | Z = " + str(self.z))
        msg = Twist()
        msg.linear.x = self.x
        msg.angular.z = self.z
        self.cmd_vel_pub_.publish(msg)

        self.cliente.__del__()

# Función para imprimir el estado de las teclas en la ventana

def main (args=None):
    rclpy.init(args=args)

    node = TrutleClientNode()
    #node.subscribe_velocity()
    rclpy.spin(node)

    rclpy.shutdown()

#if __name__ == "__main__":
#    main()