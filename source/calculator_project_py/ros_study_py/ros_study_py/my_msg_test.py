import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from ros_study_msgs.msg import MyMsg


class MyMsgTest(Node):
    def __init__(self):
        super().__init__('my_msg_test')
        qos_profile = QoSProfile(depth=10)
        self.publisher_ = self.create_publisher(MyMsg, 'MyMsg', qos_profile)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0.0

    def timer_callback(self):
        msg = MyMsg()
        msg.num = self.i
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.num}')
        self.i += 1


def main(args=None):
    rclpy.init(args=args)
    node = MyMsgTest()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
