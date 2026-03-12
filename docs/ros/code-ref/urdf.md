# URDF & Xacro

로봇 모델 기술을 위한 URDF와 Xacro 파일


[View full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/my_urdf/){ .md-button }

#### `my_urdf/launch/robot.launch.py`

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time")

    pkg_path = os.path.join(get_package_share_directory("my_urdf"))
    xacro_file = os.path.join(pkg_path, "urdf", "robot_fixed.xacro")
    # xacro_file = os.path.join(pkg_path, "urdf", "robot_revolute.xacro")
    robot_description = xacro.process_file(xacro_file)
    params = {"robot_description": robot_description.toxml(), "use_sim_time": use_sim_time}

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time", default_value="false", description="use sim time"
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                output="screen",
                parameters=[params],
            ),
            # move_robot.py에서 /joint_state를 publish하므로
            # 별도의 /joint_state_publisher 노드를 추가할 필요가 없습니다.
            # 아래의 joint_state_publisher_gui를 이용하여 move_robot.py를 실행하기 전에 간단하게 확인해볼 수 있습니다.
            # Node(package='joint_state_publisher_gui',
            #                     executable='joint_state_publisher_gui',
            #                     name='joint_state_publisher_gui'),
            Node(
                package="rviz2",
                executable="rviz2",
                output="screen",
                parameters=[params],
            ),
        ]
    )

```

#### `my_urdf/launch/robot.launch.py`

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time")

    pkg_path = os.path.join(get_package_share_directory("my_urdf"))
    xacro_file = os.path.join(pkg_path, "urdf", "robot_fixed.xacro")
    # xacro_file = os.path.join(pkg_path, "urdf", "robot_revolute.xacro")
    robot_description = xacro.process_file(xacro_file)
    params = {"robot_description": robot_description.toxml(), "use_sim_time": use_sim_time}

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time", default_value="false", description="use sim time"
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                output="screen",
                parameters=[params],
            ),
            # move_robot.py에서 /joint_state를 publish하므로
            # 별도의 /joint_state_publisher 노드를 추가할 필요가 없습니다.
            # 아래의 joint_state_publisher_gui를 이용하여 move_robot.py를 실행하기 전에 간단하게 확인해볼 수 있습니다.
            # Node(package='joint_state_publisher_gui',
            #                     executable='joint_state_publisher_gui',
            #                     name='joint_state_publisher_gui'),
            Node(
                package="rviz2",
                executable="rviz2",
                output="screen",
                parameters=[params],
            ),
        ]
    )

```

#### `my_urdf/my_urdf/__init__.py`

```python

```

#### `my_urdf/my_urdf/move_robot.py`

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math

class MoveRobot(Node):
    def __init__(self):
        super().__init__('move_robot')

        self.publisher_ = self.create_publisher(JointState, 'joint_states', 10)

        timer_period = 0.05  # 20Hz로 부드럽게 퍼블리시
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.start_time = self.get_clock().now()

    def timer_callback(self):
        now = self.get_clock().now()
        t = (now - self.start_time).nanoseconds * 1e-9  # 초 단위 시간

        msg = JointState()
        msg.header.stamp = now.to_msg()
        # 로봇의 joint 이름
        msg.name = [
            'neck',
            'left_shoulder',
            'right_shoulder',
            'left_hip',
            'right_hip',
        ]

        # 시간에 따라 각 joint를 sinusoidal하게 움직이기
        msg.position = [
            0.3 * math.sin(t),        # neck: 좌우로 부드럽게 흔들기
            0.5 * math.sin(t * 0.5),  # left_shoulder: 천천히 팔 들기
            0.5 * math.sin(t * 0.5),  # right_shoulder: 천천히 팔 들기
            0.4 * math.sin(t * 0.7),  # left_hip: 다리 앞뒤로 움직이기
            0.4 * math.sin(t * 0.7),  # right_hip: 다리 앞뒤로 움직이기
        ]

        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = MoveRobot()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
# ... (2 more lines)
```

#### `my_urdf/setup.py`

```python
import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'my_urdf'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
                (os.path.join('share', package_name, 'urdf'), glob('urdf/*.xacro')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='victor',
    maintainer_email='victor@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
        ],
    },
)

```


*... and 3 more files. [See full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/my_urdf/)*


[View full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/urdf_revolution/){ .md-button }

#### `urdf_revolution/launch/demo.launch.py`

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    use_sim_time = LaunchConfiguration("use_sim_time", default="false")

    urdf_file_name = "r2d2.urdf.xml"
    urdf = os.path.join(
        get_package_share_directory("urdf_revolution"), urdf_file_name
    )
    with open(urdf, "r") as infp:
        robot_desc = infp.read()

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Use simulation (Gazebo) clock if true",
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="robot_state_publisher",
                output="screen",
                parameters=[
                    {"use_sim_time": use_sim_time, "robot_description": robot_desc}
                ],
                arguments=[urdf],
            ),
            Node(
                package="urdf_revolution",
                executable="state_publisher",
                name="state_publisher",
                output="screen",
            ),
        ]
    )

```

#### `urdf_revolution/launch/demo.launch.py`

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    use_sim_time = LaunchConfiguration("use_sim_time", default="false")

    urdf_file_name = "r2d2.urdf.xml"
    urdf = os.path.join(
        get_package_share_directory("urdf_revolution"), urdf_file_name
    )
    with open(urdf, "r") as infp:
        robot_desc = infp.read()

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Use simulation (Gazebo) clock if true",
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="robot_state_publisher",
                output="screen",
                parameters=[
                    {"use_sim_time": use_sim_time, "robot_description": robot_desc}
                ],
                arguments=[urdf],
            ),
            Node(
                package="urdf_revolution",
                executable="state_publisher",
                name="state_publisher",
                output="screen",
            ),
        ]
    )

```

#### `urdf_revolution/urdf_revolution/__init__.py`

```python

```

#### `urdf_revolution/setup.py`

```python
from setuptools import find_packages, setup
import os
from glob import glob
from setuptools import setup
from setuptools import find_packages

package_name = "urdf_revolution"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (
            os.path.join("share", package_name, "launch"),
            glob(os.path.join("launch", "*launch.[pxy][yma]*")),
        ),
        (os.path.join("share", package_name), glob("urdf/*")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="user",
    maintainer_email="choonghyunlee@naver.com",
    description="TODO: Package description",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "state_publisher = urdf_revolution.state_publisher:main",
        ],
    },
)

```

#### `urdf_revolution/urdf_revolution/state_publisher.py`

```python
from math import sin, cos, pi
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformStamped


class StatePublisher(Node):

    def __init__(self):
        rclpy.init()
        super().__init__("state_publisher")

        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, "joint_states", qos_profile)
        self.broadcaster = TransformBroadcaster(self, qos=qos_profile)
        self.nodeName = self.get_name()
        self.get_logger().info("{0} started".format(self.nodeName))

        degree = pi / 180.0
        loop_rate = self.create_rate(30)

        # robot state
        tilt = 0.0
        tinc = degree
        swivel = 0.0
        angle = 0.0
        height = 0.0
        hinc = 0.005

        # message declarations
        odom_trans = TransformStamped()
        odom_trans.header.frame_id = "odom"
        odom_trans.child_frame_id = "axis"
        joint_state = JointState()

        try:
            while rclpy.ok():
                rclpy.spin_once(self)

                # update joint_state
                now = self.get_clock().now()
                joint_state.header.stamp = now.to_msg()
                joint_state.name = ["swivel", "tilt", "periscope"]
                joint_state.position = [swivel, tilt, height]

                # update transform
                # (moving in a circle with radius=2)
# ... (52 more lines)
```


*... and 2 more files. [See full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/urdf_revolution/)*
