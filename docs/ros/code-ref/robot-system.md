# Robot System

센서 노드, 쿨러 서비스, 액션 서버를 포함한 로봇 시스템 제어


[View full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/my_robot_/){ .md-button }

#### `my_robot_/my_robot_system/my_robot_system/manager_node.py`

```python
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

# ... (11 more lines)
```

#### `my_robot_/my_robot_system/my_robot_system/sensor_node.py`

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random


class SensorNode(Node):
    def __init__(self):
        super().__init__("sensor_node")
        self.publisher = self.create_publisher(Float32, "temperature", 10)
        self.timer = self.create_timer(1.0, self.publish_temperature)

    def publish_temperature(self):
        temp = random.uniform(25.0, 35.0)
        self.get_logger().info(f"Publishing Temperature: {temp:.2f}")
        msg = Float32()
        msg.data = temp
        self.publisher.publish(msg)


def main():
    rclpy.init()
    sensor_node = SensorNode()
    rclpy.spin(sensor_node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()

```

#### `my_robot_/my_robot_system/launch/system.launch.py`

```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="my_robot_system",
                executable="sensor_node",
                name="sensor_node",
                output="screen",
            ),
            Node(
                package="my_robot_system",
                executable="manager_node",
                name="manager_node",
                output="screen",
            ),
            Node(
                package="my_robot_system",
                executable="cooler_service",
                name="cooler_service",
                output="screen",
            ),
            Node(
                package="my_robot_system",
                executable="switch_action_server",
                name="switch_action_server",
                output="screen",
            ),
        ]
    )

```

#### `my_robot_/my_robot_system/launch/system.launch.py`

```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="my_robot_system",
                executable="sensor_node",
                name="sensor_node",
                output="screen",
            ),
            Node(
                package="my_robot_system",
                executable="manager_node",
                name="manager_node",
                output="screen",
            ),
            Node(
                package="my_robot_system",
                executable="cooler_service",
                name="cooler_service",
                output="screen",
            ),
            Node(
                package="my_robot_system",
                executable="switch_action_server",
                name="switch_action_server",
                output="screen",
            ),
        ]
    )

```

#### `my_robot_/my_robot_system/my_robot_system/__init__.py`

```python

```


*... and 6 more files. [See full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/my_robot_/)*
