# Lane Detection

슬라이딩 윈도우 알고리즘을 활용한 차선 검출


[View full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/lane_detect/){ .md-button }

#### `lane_detect/src/lane_detect/lane_detect/publisher_node.py`

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os

class VideoPublisher(Node):
    def __init__(self, fps=10):
        super().__init__('video_publisher')
        self.declare_and_fetch_parameters()
        self.fps = fps
        self.bridge = CvBridge()
        self.publisher = self.create_publisher(Image, 'video_frames', 10)
        self.setup_timer(self.fps)
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            self.get_logger().error(f'Failed to open video file: {self.video_path}')
            rclpy.shutdown()

    def declare_and_fetch_parameters(self):
        self.declare_parameter('video_path', '')
        video_path_param = self.get_parameter('video_path').get_parameter_value().string_value
        if not video_path_param:
            self.get_logger().error(
                'No video path provided. Use "--ros-args -p video_path:=<path_to_video>"'
            )
            rclpy.shutdown()
        script_dir = os.path.dirname(os.path.realpath(__file__))
        script_dir = '/'.join(script_dir.split('/')[:4])
        self.video_path = f'{script_dir}/{video_path_param}'

    def setup_timer(self, fps):
        timer_interval = 1.0 / fps
        self.timer = self.create_timer(timer_interval, self.timer_callback)

    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            img_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
            self.publisher.publish(img_msg)
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

def main():
    rclpy.init()
    video_publisher = VideoPublisher(fps=30)
    rclpy.spin(video_publisher)
    video_publisher.cap.release()
    video_publisher.destroy_node()
# ... (5 more lines)
```

#### `lane_detect/src/lane_detect/lane_detect/subscriber_node.py`

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from visualization_msgs.msg import Marker
from cv_bridge import CvBridge
import cv2
import numpy as np
from lane_detect import slide_window
from lane_detect import camera_processing

class VideoSubscriber(Node):
    def __init__(self):
        super().__init__('video_subscriber')
        self.subscription = self.create_subscription(
            Image,
            'video_frames',
            self.listener_callback,
            10
        )
        self.image_publisher = self.create_publisher(Image, 'processed_frames', 10)
        self.marker_publisher = self.create_publisher(Marker, 'lane_info_marker', 10)
        self.bridge = CvBridge()

        self.camera_processor = camera_processing.CameraProcessing()
        self.slide_window_processor = slide_window.SlideWindow()

    def listener_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        detected, left, right, processed = self.lane_detect(frame)
        
        processed_msg = self.bridge.cv2_to_imgmsg(processed, encoding='bgr8')
        self.image_publisher.publish(processed_msg)

        info_text = f'Left position: {left}, Right position: {right}'

        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD
        marker.pose.position.z = 2.0
        marker.scale.z = 0.5
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 1.0
        marker.text = info_text
        self.marker_publisher.publish(marker)

# ... (23 more lines)
```

#### `lane_detect/src/lane_detect/lane_detect/__init__.py`

```python

```

#### `lane_detect/src/lane_detect/lane_detect/camera_processing.py`

```python
import numpy as np
import cv2

class CameraProcessing:
    def __init__(self):
        self.GaussianBlur = 3 # 커질수록 더 부드러워짐
        self.LightRemove = 15 # 조명 제거 강도(작아질 수록 많이 없어짐)
        self.MedianBlur = 3
        self.bin_threshold = 10
        self.kernels = {
            'vertical': np.array([[-1,  0,  1],
                                  [-2,  0,  2],
                                  [-1,  0,  1]]),
            'diagonal_1': np.array([[ 0,  1,  2],
                                    [-1,  0,  1],
                                    [-2, -1,  0]]),
            'diagonal_2': np.array([[ 2,  1,  0],
                                    [ 1,  0, -1],
                                    [ 0, -1, -2]])
        }

    def process_image(self, img):
        if img is None:
            return None

        img = self.remove_lighting(img)
        _, img = cv2.threshold(img, self.bin_threshold, 255, cv2.THRESH_BINARY)

        img = cv2.medianBlur(img, self.MedianBlur)

        img = self.warp(img)
        filtered, img = self.choose_filtered_img(img)
        return img, filtered

    def choose_filtered_img(self, img):
        max_edge_strength = -1
        best_filtered_img = None
        best_kernel_name = None

        for kernel_name, kernel in self.kernels.items():
            filtered_img = cv2.filter2D(img, -1, kernel)
            edge_strength = np.sum(np.abs(filtered_img))

            if edge_strength > max_edge_strength:
                max_edge_strength = edge_strength
                best_filtered_img = filtered_img
                best_kernel_name = kernel_name

        return best_kernel_name, best_filtered_img

# ... (25 more lines)
```

#### `lane_detect/src/lane_detect/setup.py`

```python
from setuptools import setup

package_name = 'lane_detect'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sjs',
    maintainer_email='wordok38@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
    'console_scripts': [
        'publisher_node = lane_detect.publisher_node:main',
        'subscriber_node = lane_detect.subscriber_node:main',
    ],
},
)

```


*... and 2 more files. [See full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/lane_detect/)*
