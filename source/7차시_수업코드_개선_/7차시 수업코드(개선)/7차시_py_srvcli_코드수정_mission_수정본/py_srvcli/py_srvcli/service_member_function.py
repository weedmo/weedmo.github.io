from example_interfaces.srv import AddTwoInts

import rclpy
from rclpy.node import Node


class MotorControlServer(Node):

    def __init__(self):
        super().__init__("motor_control_server")
        self.srv = self.create_service(
            AddTwoInts, "motor_start", self.motor_start_callback
        )

    def motor_start_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(
            "Motor control(숫자 입력)\nleft(1:start, 2:stop): %d right(1:start, 2: stop): %d"
            % (request.a, request.b)
        )

        return response


def main():
    rclpy.init()

    motor_control_server = MotorControlServer()

    rclpy.spin(motor_control_server)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
