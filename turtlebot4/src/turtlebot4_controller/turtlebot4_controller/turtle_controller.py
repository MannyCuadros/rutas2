#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

import pygame
import sys
import time

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

tiempo = 0.1

class TrutleControlerNode(Node):

    def __init__(self, window, font):
        self.window = window
        self.font = font
        self.x = 0.0
        self.z = 0.0
        self.vlinear = 1.0
        self.vangular = 1.0
        super().__init__("control_turtle")
        self.cmd_vel_pub_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        #self.pose_subscriber_ = self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)
        self.timer = self.create_timer(0.1,self.send_velocity_command)
        self.get_logger().info("Turtle Controller has been started.")

    def pose_callback(self, pose: Pose):
        cmd = Twist()

        if pose.x > 9.0 or pose.x < 2.0 or pose.y > 9.0 or pose.y < 2.0:
            cmd.linear.x = 1.0
            cmd.angular.z = 0.9
        else:
            cmd.linear.x = 5.0
            cmd.angular.z = 0.0

        self.cmd_vel_pub_.publish(cmd)
    
    def send_velocity_command(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                time.sleep(0.2)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.x = self.vlinear
                elif event.key == pygame.K_DOWN:
                    self.x = self.vlinear * (-1.0)
                elif event.key == pygame.K_RIGHT:
                    self.z = self.vangular * (-1.0)
                elif event.key == pygame.K_LEFT:
                    self.z = self.vangular
                elif event.key == pygame.K_KP_PLUS:
                    self.vlinear = round(self.vlinear + 0.2, 2)
                    if self.vlinear > 5:
                        self.vlinear = 5.0
                elif event.key == pygame.K_KP_MINUS:
                    self.vlinear = round(self.vlinear - 0.2, 2)
                    if self.vlinear < 0:
                        self.vlinear = 0.0
                elif event.key == pygame.K_KP_MULTIPLY:
                    self.vangular = round(self.vangular + 0.2, 2)
                    if self.vangular > 5:
                        self.vangular = 5.0
                elif event.key == pygame.K_KP_DIVIDE:
                    self.vangular = round(self.vangular - 0.2, 2)
                    if self.vangular < 0:
                        self.vangular = 0.0
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.x = 0.0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    self.z = 0.0

        # Imprimir el estado de las teclas en consola
        print("X = " + str(self.x) + " | Z = " + str(self.z))
        print_key_state(self.window, self.font, self.x, self.z, self.vlinear, self.vangular)
        msg = Twist()
        msg.linear.x = self.x
        msg.angular.z = self.z
        self.cmd_vel_pub_.publish(msg)

# Función para imprimir el estado de las teclas en la ventana
def print_key_state(window, font, x, a, vl, va):
    window.fill(BLACK)
    text_x = font.render("x = {}".format(x), True, WHITE)
    text_a = font.render("a = {}".format(a), True, WHITE)
    text_vl = font.render("vl = {}".format(vl), True, WHITE)
    text_va = font.render("va = {}".format(va), True, WHITE)
    window.blit(text_x, (20, 20))
    window.blit(text_a, (20, 60))
    window.blit(text_vl, (20, 120))
    window.blit(text_va, (20, 160))
    pygame.display.flip()


def main (args=None):
    rclpy.init(args=args)

    # Inicializar pygame
    pygame.init()

    # Definir el tamaño de la ventana
    window_width = 200
    window_height = 200
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Control")


    # Definir fuente
    font = pygame.font.Font(None, 36)

    node = TrutleControlerNode(window,font)
    rclpy.spin(node)

    rclpy.shutdown()
