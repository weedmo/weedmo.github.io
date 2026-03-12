import sys

from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node


class MotorControlClient(Node):

    def __init__(self):
        super().__init__("motor_control_client")
        self.cli = self.create_client(AddTwoInts, "motor_start")
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("서버연결이 어렵습니다. 잠시만 기다려주세요...")
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        return self.cli.call_async(self.req)


def main():

    rclpy.init()

    motor_control_client = MotorControlClient()
    future = motor_control_client.send_request(int(sys.argv[1]), int(sys.argv[2]))
    rclpy.spin_until_future_complete(motor_control_client, future)
    response = future.result()
    
    if int(sys.argv[1]) == 1:
        motor_control_client.get_logger().info("왼쪽 모터가 회전을 시작했습니다.")
    else:
        motor_control_client.get_logger().info("왼쪽 모터가 정지 했습니다. ")

    if int(sys.argv[2]) == 1:
        motor_control_client.get_logger().info("오른쪽 모터가 회전을 시작했습니다.")
    else:
        motor_control_client.get_logger().info("오른쪽 모터가 정지 했습니다.  ")

    motor_control_client.destroy_node()
    rclpy.shutdown()
