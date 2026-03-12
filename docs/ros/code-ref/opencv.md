# OpenCV (Hough Transform)

OpenCV를 활용한 Hough 변환 예제


[View full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/opencv/){ .md-button }

#### `opencv/src/hough_transform/hough_transform/__init__.py`

```python

```

#### `opencv/src/hough_transform/hough_transform/hough_transform.py`

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np


class HoughTransform(Node):
    def __init__(self):
        super().__init__("hough_transform")
        self.method = (
            self.declare_parameter("method", "").get_parameter_value().string_value
        )
        self.bridge = CvBridge()
        self.subscriber = self.create_subscription(
            Image, "original_image", self.process_image, 10
        )
        self.publisher = self.create_publisher(Image, "hough_transform", 10)
        if not self.method:
            self.get_logger().error(
                "No method provided. Use '--ros-args -p method:=<method>'"
            )
            rclpy.shutdown()

    def process_image(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        if self.method == "circle":
            processed_image = self.detect_circles(cv_image)
        elif self.method == "line":
            processed_image = self.detect_lines(cv_image)
        else:
            self.get_logger().error(f"Invalid method: {self.method}")
            return
        self.publisher.publish(
            self.bridge.cv2_to_imgmsg(processed_image, encoding="bgr8")
        )

    def detect_circles(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(
            cv2.GaussianBlur(gray, (9, 9), 2),
            cv2.HOUGH_GRADIENT,
            1,
            20,
            param1=50,
            param2=37,
            minRadius=80,
            maxRadius=100,
        )
# ... (25 more lines)
```

#### `opencv/src/hough_transform/hough_transform/img_pub.py`

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class ImagePublisher(Node):
    def __init__(self):
        super().__init__("image_publisher")
        self.declare_and_fetch_parameters()
        self.bridge = CvBridge()
        self.publisher = self.create_publisher(Image, "original_image", 10)
        self.setup_timer()

    def declare_and_fetch_parameters(self):
        """Declare and fetch the image path parameter."""
        self.declare_parameter("image_path", "")
        image_path_param = (
            self.get_parameter("image_path").get_parameter_value().string_value
        )
        if not image_path_param:
            self.get_logger().error(
                "No image path provided. Use '--ros-args -p image_path:=<path_to_image>'"
            )
            rclpy.shutdown()
        self.image_path = image_path_param

    def setup_timer(self):
        """Set up a timer to publish images at regular intervals."""
        self.timer = self.create_timer(0.1, self.publish_image)

    def publish_image(self):
        """Read an image from file and publish it."""
        cv_image = cv2.imread(self.image_path)
        if cv_image is None:
            self.get_logger().error(f"Failed to load image from {self.image_path}")
            return

        ros_image = self.bridge.cv2_to_imgmsg(cv_image, encoding="bgr8")
        self.publisher.publish(ros_image)
        self.get_logger().info(
            f"Published image: {self.image_path} with shape {cv_image.shape}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = ImagePublisher()
    rclpy.spin(node)
# ... (6 more lines)
```

#### `opencv/src/hough_transform/setup.py`

```python
from setuptools import find_packages, setup

package_name = "hough_transform"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="user",
    maintainer_email="user@todo.todo",
    description="TODO: Package description",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "image_publisher = hough_transform.img_pub:main",
            "hough_transform = hough_transform.hough_transform:main",
        ],
    },
)

```

#### `opencv/src/hough_transform/package.xml`

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>hough_transform</name>
  <version>0.0.0</version>
  <description>TODO: Package description</description>
  <maintainer email="user@todo.todo">user</maintainer>
  <license>TODO: License declaration</license>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>

```
