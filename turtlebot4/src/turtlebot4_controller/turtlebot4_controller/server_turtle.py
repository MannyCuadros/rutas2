#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class ServerControl(Node):
  
    def __init__(self):
        
        super().__init__("server_turtle")

        # Define publisher for velocity commands
        self.move_pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer = self.create_timer(0.5, self.enviar_mensaje)
        self.get_logger().info("Enviando mensaje")
        
    # Set desired linear velocity for straight line movement
    def enviar_mensaje(self):
        velocity = Twist()
        velocity.linear.x = 1.0  # Set forward speed (m/s)
        velocity.angular.z = 0.0  # Set angular velocity to 0 for straight line
        self.move_pub.publish(velocity)

def main (args=None):

    rclpy.init(args=args)

    node = ServerControl()
    rclpy.spin(node)

    rclpy.shutdown()

