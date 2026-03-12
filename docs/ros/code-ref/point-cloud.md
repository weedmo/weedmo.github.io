# Point Cloud

PCD 파일 기반 포인트 클라우드 처리


[View full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/point_cloud/){ .md-button }

#### `point_cloud/launch/pcd_publisher_demo.launch.py`

```python
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    rviz_config_dir = os.path.join(get_package_share_directory(
        'point_cloud'), 'config', 'config.rviz')
    assert os.path.exists(rviz_config_dir)

    ply_path = os.path.join(get_package_share_directory(
        'point_cloud'), 'resource', 'fragment.ply')
    assert os.path.exists(ply_path)

    return LaunchDescription([
        Node(package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            output='screen'
        ),
        Node(package='point_cloud',
            executable='pcd_publisher_node',
            name='pcd_publisher_node',
            output='screen',
            arguments=[ply_path],
        ),
    ])
```

#### `point_cloud/launch/pcd_publisher_demo.launch.py`

```python
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    rviz_config_dir = os.path.join(get_package_share_directory(
        'point_cloud'), 'config', 'config.rviz')
    assert os.path.exists(rviz_config_dir)

    ply_path = os.path.join(get_package_share_directory(
        'point_cloud'), 'resource', 'fragment.ply')
    assert os.path.exists(ply_path)

    return LaunchDescription([
        Node(package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            output='screen'
        ),
        Node(package='point_cloud',
            executable='pcd_publisher_node',
            name='pcd_publisher_node',
            output='screen',
            arguments=[ply_path],
        ),
    ])
```

#### `point_cloud/point_cloud/pcd_publisher/pcd_publisher_node.py`

```python
import sys
import os
import struct
import rclpy
import sensor_msgs.msg as sensor_msgs
import std_msgs.msg as std_msgs
import numpy as np
import open3d as o3d
from rclpy.node import Node


class PCDPublisher(Node):
    #PCD 데이터를 퍼블리시하는 ROS2 노드
    def __init__(self, voxel_size, pcd_path):
        super().__init__('pcd_publisher_node')
        self.voxel_size = voxel_size
        self.pcd_path = pcd_path

        self.load_point_cloud()
        self.points = self.rotate_points_90(self.points)
        self.points[:, 2] += 2.5

        self.pcd_publisher = self.create_publisher(sensor_msgs.PointCloud2, 'pcd', 10)
        self.timer = self.create_timer(1 / 30.0, self.timer_callback)

    def load_point_cloud(self):
        #포인트 클라우드 파일을 로드
        if not os.path.exists(self.pcd_path):
            raise FileNotFoundError("File doesn't exist.")

        pcd = o3d.io.read_point_cloud(self.pcd_path)
        if self.voxel_size > 0:
            pcd = pcd.voxel_down_sample(self.voxel_size)

        self.points = np.asarray(pcd.points)
        self.colors = np.asarray(pcd.colors)

    def timer_callback(self):
        #타이머 콜백 : points와 colors 데이터를 이용해 PointCloud 메시지를 생성
        #좌표계 : map을 기준으로 함
        pcd_msg = self.create_point_cloud_message(self.points, self.colors, 'map')
        self.pcd_publisher.publish(pcd_msg)

    def rotate_points_90(self, points):
        #포인트 클라우드를 X축 기준으로 90도 회전
        theta = np.radians(90)
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(theta), -np.sin(theta)],
            [0, np.sin(theta), np.cos(theta)]
# ... (50 more lines)
```

#### `point_cloud/launch/pcd_pubsub_demo.launch.py`

```python
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():


    ply_path = os.path.join(get_package_share_directory(
        'point_cloud'), 'resource', 'fragment.ply')
    assert os.path.exists(ply_path)

    return LaunchDescription([
        Node(package='point_cloud',
            executable='pcd_publisher_node',
            name='pcd_publisher_node',
            output='screen',
            arguments=[ply_path],
        ),
        Node(package='point_cloud',
            executable='pcd_subscriber_node',
            name='pcd_subscriber_node',
            output='screen',
            arguments=[ply_path],
        ),
    ])
```

#### `point_cloud/launch/pcd_pubsub_demo.launch.py`

```python
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():


    ply_path = os.path.join(get_package_share_directory(
        'point_cloud'), 'resource', 'fragment.ply')
    assert os.path.exists(ply_path)

    return LaunchDescription([
        Node(package='point_cloud',
            executable='pcd_publisher_node',
            name='pcd_publisher_node',
            output='screen',
            arguments=[ply_path],
        ),
        Node(package='point_cloud',
            executable='pcd_subscriber_node',
            name='pcd_subscriber_node',
            output='screen',
            arguments=[ply_path],
        ),
    ])
```


*... and 6 more files. [See full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/point_cloud/)*
