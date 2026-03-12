# Camera Pub/Sub

카메라 이미지 Publisher/Subscriber 노드


[View full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/my_cam_pubsub/){ .md-button }

#### `my_cam_pubsub/my_cam_pubsub/__init__.py`

```python

```

#### `my_cam_pubsub/my_cam_pubsub/cam_pub.py`

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class CameraPublisher(Node):

    def __init__(self):
        super().__init__("camera_publisher")
        self.publisher = self.create_publisher(Image, "camera/image_raw", 10)
        self.timer = self.create_timer(0.1, self.timer_callback)  # 10Hz
        self.cap = cv2.VideoCapture(0)
        self.bridge = CvBridge()

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().error("Failed to read from camera")
            return

        msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
        self.publisher.publish(msg)
        self.get_logger().info("Published image")


def main():
    rclpy.init()
    node = CameraPublisher()
    rclpy.spin(node)
    node.cap.release()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

```

#### `my_cam_pubsub/my_cam_pubsub/cam_sub.py`

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class CameraSubscriber(Node):

    def __init__(self):
        super().__init__("camera_subscriber")
        self.subscription = self.create_subscription(
            Image, "camera/image_raw", self.listener_callback, 10
        )
        self.bridge = CvBridge()

    def listener_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        # cv2.imshow("Camera Feed", frame)
        cv2.waitKey(1)


def main():
    rclpy.init()
    node = CameraSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    # cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

```

#### `my_cam_pubsub/setup.py`

```python
from setuptools import find_packages, setup

package_name = 'my_cam_pubsub'

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
    maintainer='i',
    maintainer_email='i@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'cam_pub = my_cam_pubsub.cam_pub:main',
            'cam_sub = my_cam_pubsub.cam_sub:main',
        ],
    },
)

```

#### `my_cam_pubsub/package.xml`

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>my_cam_pubsub</name>
  <version>0.0.0</version>
  <description>TODO: Package description</description>
  <maintainer email="i@todo.todo">i</maintainer>
  <license>TODO: License declaration</license>

  <depend>rclpy</depend>
  <depend>cv_bridge</depend>
  <depend>sensor_msgs</depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>

```
