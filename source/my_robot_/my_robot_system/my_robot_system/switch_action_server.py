import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from my_robot_interfaces.action import SwitchControl
import time


class SwitchActionServer(Node):
    def __init__(self):
        super().__init__("switch_action_server")
        self._action_server = ActionServer(
            self, SwitchControl, "switch_control", self.execute_callback
        )

    async def execute_callback(self, goal_handle):
        turn_on = goal_handle.request.turn_on
        status = ["Switch ON"] if turn_on else ["Switch OFF"]
        self.get_logger().info(f"[Action]서버 상태: {status}")

        feedback_msg = SwitchControl.Feedback()
        feedback_msg.status = status
        goal_handle.publish_feedback(feedback_msg)

        time.sleep(2)

        goal_handle.succeed()
        result = SwitchControl.Result()
        result.success = True
        return result


def main():
    rclpy.init()
    switch_action_server = SwitchActionServer()
    rclpy.spin(switch_action_server)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
