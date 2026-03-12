# RQT Example

RQT GUI 플러그인 예제


[View full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/rqt_example/){ .md-button }

#### `rqt_example/launch/turtlesim.launch.py`

```python
from launch import LaunchDescription
from launch.actions import LogInfo
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        LogInfo(msg=['Execute the rqt_example with turtlesim node.']),

        Node(
            namespace='turtle1',
            package='rqt_example',
            executable='rqt_example',
            name='rqt_example',
            output='screen'),

        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim',
            output='screen')
    ])

```

#### `rqt_example/launch/turtlesim.launch.py`

```python
from launch import LaunchDescription
from launch.actions import LogInfo
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        LogInfo(msg=['Execute the rqt_example with turtlesim node.']),

        Node(
            namespace='turtle1',
            package='rqt_example',
            executable='rqt_example',
            name='rqt_example',
            output='screen'),

        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim',
            output='screen')
    ])

```

#### `rqt_example/src/rqt_example/__init__.py`

```python

```

#### `rqt_example/src/rqt_example/examples.py`

```python
#!/usr/bin/env python3
# Copyright 2019 OROCA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from rqt_example.examples_widget import ExamplesWidget

from rqt_gui_py.plugin import Plugin


class Examples(Plugin):

    def __init__(self, context):
        super(Examples, self).__init__(context)
        self.setObjectName('RQt example')
        self.widget = ExamplesWidget(context.node)
        serial_number = context.serial_number()
        if serial_number > 1:
            self.widget.setWindowTitle(self.widget.windowTitle() + ' ({0})'.format(serial_number))
        context.add_widget(self.widget)

    def shutdown_plugin(self):
        print('Shutdown the RQt example.')
        self.widget.shutdown_widget()

```

#### `rqt_example/src/rqt_example/examples_widget.py`

```python
import os

from ament_index_python.resources import get_resource
from geometry_msgs.msg import Twist
from python_qt_binding import loadUi
from python_qt_binding.QtCore import Qt
from python_qt_binding.QtCore import QTimer
from python_qt_binding.QtGui import QKeySequence
from python_qt_binding.QtWidgets import QShortcut
from python_qt_binding.QtWidgets import QWidget

import rclpy
from rclpy.qos import QoSProfile
from std_srvs.srv import SetBool

class ExamplesWidget(QWidget):

    def __init__(self, node):
        super(ExamplesWidget, self).__init__()
        self.setObjectName('ExamplesWidget')

        self.node = node

        self.REDRAW_INTERVAL = 30
        self.PUBLISH_INTERVAL = 100
        self.CMD_VEL_X_FACTOR = 1000.0
        self.CMD_VEL_YAW_FACTOR = -10.0

        pkg_name = 'rqt_example'
        ui_filename = 'rqt_example.ui'
        topic_name = 'cmd_vel'
        service_name = 'led_control'

        _, package_path = get_resource('packages', pkg_name)
        ui_file = os.path.join(package_path, 'share', pkg_name, 'resource', ui_filename)
        loadUi(ui_file, self)

        self.pub_velocity = Twist()
        self.pub_velocity.linear.x = 0.0
        self.pub_velocity.angular.z = 0.0
        self.sub_velocity = Twist()
        self.sub_velocity.linear.x = 0.0
        self.sub_velocity.angular.z = 0.0
        self.slider_x.setValue(0)
        self.lcd_number_x.display(0.0)
        self.lcd_number_yaw.display(0.0)

        qos = QoSProfile(depth=10)
        self.publisher = self.node.create_publisher(Twist, topic_name, qos)
        self.subscriber = self.node.create_subscription(Twist, topic_name, self.get_velocity, qos)
# ... (120 more lines)
```


*... and 2 more files. [See full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/rqt_example/)*
