import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from std_srvs.srv import Trigger
from rclpy.action import ActionClient
from my_robot_interfaces.action import SwitchControl


class ManagerNode(Node):
    def __init__(self):
        super().__init__("manager_node")
        self.subscriber = self.create_subscription(
            Float32, "temperature", self.temp_callback, 10
        )
        self.cooler_client = self.create_client(Trigger, "cooler_motor")
        self.switch_client = ActionClient(self, SwitchControl, "switch_control")

    def temp_callback(self, msg):
        temp = msg.data
        self.get_logger().info(f"Received temperature(현재 보드온도): {temp:.2f}")
        if temp > 30.0:
            self.call_cooler_service()
            self.send_switch_goal(True)

    def call_cooler_service(self):
        while not self.cooler_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("Waiting for cooler_motor service...")
        req = Trigger.Request()
        future = self.cooler_client.call_async(req)

        def callback(future):
            try:
                res = future.result()
                self.get_logger().info(
                    f"Cooler service called : 팬 동작: {res.success}, 스위치: {res.message}"
                )
            except Exception as e:
                self.get_logger().error(f"Service call failed: {e}")

        future.add_done_callback(callback)

    def send_switch_goal(self, turn_on):
        if not self.switch_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().warn("Switch control action server not available!")
            return

        goal_msg = SwitchControl.Goal()
        goal_msg.turn_on = ["Switch ON"]
        self.switch_client.send_goal_async(goal_msg)


def main():
    rclpy.init()
    manager_node = ManagerNode()
    rclpy.spin(manager_node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
