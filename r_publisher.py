import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class PublisherNode(Node):

    def __init__(self):
        super().__init__('publisher_node')
        self.publisher = self.create_publisher(String, '/communication_topic', 10)
        timer_period = 1.0  # Change this to the desired publishing frequency
        self.timer = self.create_timer(timer_period, self.publish_data)

    def publish_data(self):
        msg = String()
        msg.data = "Hello from Computer 1!"
        self.publisher.publish(msg)
        self.get_logger().info("Message published: %s" % msg.data)

def main():
    rclpy.init()
    node = PublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()