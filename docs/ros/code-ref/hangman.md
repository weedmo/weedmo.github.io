# Hangman Game

ROS2 Action을 활용한 행맨 게임


[View full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/hangman_game/){ .md-button }

#### `hangman_game/hangman_game/__init__.py`

```python

```

#### `hangman_game/hangman_game/letter_publisher.py`

```python
# hangman_game/letter_publisher.py

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class LetterPublisher(Node):

    def __init__(self):
        super().__init__('letter_publisher')
        self.publisher_ = self.create_publisher(String, 'letter_topic', 10)
        self.timer = self.create_timer(1.0, self.publish_letter)
        self.current_letter = ord('a')

    def publish_letter(self):
        msg = String()
        msg.data = chr(self.current_letter)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data}')
        self.current_letter += 1
        if self.current_letter > ord('z'):
            self.current_letter = ord('a')

def main(args=None):
    rclpy.init(args=args)
    letter_publisher = LetterPublisher()
    rclpy.spin(letter_publisher)
    letter_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

```

#### `hangman_game/hangman_game/progress_action_client.py`

```python
# hangman_game/progress_action_client.py

import rclpy
from rclpy.node import Node
from hangman_interfaces.action import GameProgress
from rclpy.action import ActionClient


class ProgressActionClient(Node):

    def __init__(self):
        super().__init__("progress_action_client")
        self._action_client = ActionClient(self, GameProgress, "game_progress")
        self.result_received = False
        self.send_goal()

    def send_goal(self):
        self.get_logger().info("Action Client: Waiting for action server...")
        self._action_client.wait_for_server()
        goal_msg = GameProgress.Goal()
        self.get_logger().info("Action Client: Sending goal request...")
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        if feedback.game_over:
            self.get_logger().info("Action Client: Game over detected in feedback")

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info("Action Client: Goal rejected")
            self.result_received = True
            return

        self.get_logger().info("Action Client: Goal accepted")
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        if result.won:
            self.get_logger().info("Action Client: Congratulations! You won!")
        else:
            self.get_logger().info("Action Client: Game Over. You lost.")
        self.result_received = True

# ... (15 more lines)
```

#### `hangman_game/hangman_game/progress_action_server.py`

```python
# hangman_game/progress_action_server.py

import rclpy
from rclpy.node import Node
from hangman_interfaces.action import GameProgress
from hangman_interfaces.msg import Progress
from rclpy.action import ActionServer
from rclpy.executors import MultiThreadedExecutor
import time
import threading


class ProgressActionServer(Node):

    def __init__(self):
        super().__init__("progress_action_server")
        self._action_server = ActionServer(
            self, GameProgress, "game_progress", self.execute_callback
        )
        self.current_progress = Progress()
        self.progress_received_event = threading.Event()

        # Subscribe to the 'progress' topic to get game updates
        self.subscription = self.create_subscription(
            Progress, "progress", self.progress_callback, 10
        )
        self.subscription  # prevent unused variable warning

        self.get_logger().info("Action Server Initialized")
        self.get_logger().info(f"GAME OVER: {self.current_progress.game_over}")
        self.get_logger().info(f"WON: {self.current_progress.won}")

    def progress_callback(self, msg):
        self.current_progress = msg
        self.get_logger().info(
            f"Progress updated: {self.current_progress.current_state}"
        )

    def execute_callback(self, goal_handle):
        self.get_logger().info("Action Server: Received goal request")
        feedback_msg = GameProgress.Feedback()
        update_rate = 1.0  # seconds

        while not self.current_progress.game_over:
            # Publish feedback
            feedback_msg.game_over = self.current_progress.game_over
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(
                f"Current State: {self.current_progress.current_state}"
            )
# ... (47 more lines)
```

#### `hangman_game/setup.py`

```python
from setuptools import find_packages, setup

package_name = 'hangman_game'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='mh9716@kookmin.ac.kr',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'letter_publisher = hangman_game.letter_publisher:main',
            'word_service = hangman_game.word_service:main',
            'user_input = hangman_game.user_input:main',
            'progress_action_server = hangman_game.progress_action_server:main',
            'progress_action_client = hangman_game.progress_action_client:main',
        ],
    },
)

```


*... and 3 more files. [See full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/hangman_game/)*


[View full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/hangman_interfaces/){ .md-button }

#### `hangman_interfaces/srv/CheckLetter.srv`

```text
# Empty request
---
string updated_word_state
bool is_correct
string message

```

#### `hangman_interfaces/action/GameProgress.action`

```text
# Goal
# Empty since the client doesn't need to send any data
---
# Result
bool game_over
bool won
---
# Feedback
bool game_over

```

#### `hangman_interfaces/msg/Progress.msg`

```text
string current_state
int32 attempts_left
bool game_over
bool won

```

#### `hangman_interfaces/package.xml`

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>hangman_interfaces</name>
  <version>0.0.0</version>
  <description>TODO: Package description</description>
  <maintainer email="user@gmail.com">user</maintainer>
  <license>TODO: License declaration</license>

  <buildtool_depend>ament_cmake</buildtool_depend>
  <buildtool_depend>rosidl_default_generators</buildtool_depend>

  <exec_depend>builtin_interfaces</exec_depend>
  <exec_depend>rosidl_default_runtime</exec_depend>
  <member_of_group>rosidl_interface_packages</member_of_group>

  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_lint_common</test_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>

```
