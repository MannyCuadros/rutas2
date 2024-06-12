#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import socket

class DrawCircleNode(Node):

    def __init__(self):
        super().__init__("dibujar_circulo")
        self.cmd_vel_pub_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer = self.create_timer(0.5,self.send_velocity_command)
        self.get_logger().info("Draw circle node has been started")

        # Connect to the middle program's socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Replace with appropriate socket type if needed
        self.socket.connect(('localhost', 12345))  # Replace with middle program's IP and port

    def send_velocity_command(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 1.0

        # Define message format based on your protocol
        message = f"CMD:forward {msg.linear.x}\n"  # Example for forward command

        # Send message through socket
        self.socket.sendall(message.encode())

        # Optional: Receive response from middle program
        response = self.socket.recv(1024)  # Adjust buffer size as needed
        print(response.decode())

    def __del__(self):
        self.socket.close()  # Close socket upon program exit

def main (args=None):
    rclpy.init(args=args)

    node = DrawCircleNode()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == '__main__':
    main()
