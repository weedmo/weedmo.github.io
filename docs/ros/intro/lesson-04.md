# 강의_3기_ROS2입문_4차시


ROS2 프로그래밍 입문(4차시)

4. 인터페이스 프로그래밍(응용- 2)


## 인터페이스프로그래밍(응용_2)
1. 인터페이스 프로그래밍(hangman)
Python을 이용한 패키지 생성 실습

## Python을이용한행맨게임_실습
- Topic, Service, Action을 이용하여 행 맨(Hang-man) 게임 만들기


Hang-man - 실습

## Hang-man
1. Hangman은 단어나 문구를 추측하는 고전적인 단어 게임
2. 게임의 목적은 플레이어가 주어진 단어를 맞추는 것
3. 단어 선택: 한 명의 플레이어(또는 시스템)가 특정 단어를 선택
4. 추측: 다른 플레이어는 이 단어를 맞추기 위해 알파벳 한 글자씩 추측
맞는 글자를 추측하면, 해당 글자가 단어에 위치한 곳에 표시됨. 틀린 글자를 추측할
때마다 기회가 줄어듦

5. 목숨(기회) : 보통 틀린 추측이 반복될 때마다 목숨이 하나씩 줄어들어 모든 목숨 소진
시 게임에서 패배

6. 게임 종료: 단어를 모두 맞추거나, 기회가 다 소진될 때까지 추측을 반복 모든 글자를
맞추면 승리, 모든 기회가 소진되면 패배


Hang-man - 실습

## Hang-man 구조도
Letter
publisher
User input
Word
service
Action
client
Action
server
topic publish
progress
game_progress
request

Hang-man - 실습

## Letter Publisher
- a부터z까지의 알파벳을 순서대로publish

![Image 10](../../assets/images/ros/intro/lesson-04/img_006_010.webp)


Hang-man - 실습

## Word Service
- 임의의 단어를 선택, 행 맨 게임 진행, 진행 상황publish Hang-man - 실습

## Action Client
- Goal 설정, action server와의 상호 작용을 통해 행 맨 게임 진행 상태 업데이트 Hang-man - 실습

## Action Server
- 사용자의 진행 상황을 관리, 임의 진행 상태를 추적, 게임 결과를 클라이언트에게 전달 Hang-man - 실습

## 코드구조
- 패키지 생성

Hang-man - 실습

## 코드구조
- 전체 코드의 구조는 다음과 같음
- 일부 파일은 지금부터 생성 예정

![Image 22](../../assets/images/ros/intro/lesson-04/img_011_022.webp)


Hang-man - 실습

## hangman_interfaces
- hangman_interfaces/srv/CheckLetter.srv
- updated_word_state: 현재 상태ex) p y _ _ o n
- is_correct : 현재user input으로 들어온 글자가 선택된 단어 내에 존재하는지에 대한 bool 타입 자료형
- message : 맞았으면“Correct”를 띄우고 틀리면“WRONG”을띄움 Hang-man - 실습

## hangman_interfaces
- hangman_interfaces/msg/Progress.msg
- current_state : 현재 상태ex) p y _ _ o n
- attempts_left : 목숨(남은 시도 횟수)
- game_over : 목숨이 다 소진되었는지
- won : 게임에서 이겼는지(목숨 소진 이전에 정답을 맞추었는지)

![Image 26](../../assets/images/ros/intro/lesson-04/img_013_026.webp)


Hang-man - 실습

## hangman_interfaces
- hangman_interfaces/action/GameProgress.action
- game_over : 목숨이 다 소진되었는지
- won : 게임에서 이겼는지(목숨 소진 이전에 정답을 맞추었는지) Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/letter _publisher.py의 전체 코드


![Image 29](../../assets/images/ros/intro/lesson-04/img_015_029.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/letter_publisher.py 모듈별 설명
- __init__함수: Node 클래스를 상속받아LetterPublisher 클래스를 정의하고 필요한 퍼 블 리 셔 와 타이머를 설정

Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/letter_publisher.py 모듈별 설명
- publish_letter 함수: 현재 알파벳 문자를letter_topic 토픽에 퍼 블 리시하는 함수


![Image 31](../../assets/images/ros/intro/lesson-04/img_017_031.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/letter_publisher.py 모듈별 설명
- main 함수: ROS2 시스템을 초기화하고, LetterPublisher 노드를 실행


![Image 32](../../assets/images/ros/intro/lesson-04/img_018_032.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/word _service.py의 전체 코드


![Image 33](../../assets/images/ros/intro/lesson-04/img_019_033.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/word _service.py의 전체 코드


![Image 34](../../assets/images/ros/intro/lesson-04/img_020_034.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/word _service.py의 전체 코드


![Image 35](../../assets/images/ros/intro/lesson-04/img_021_035.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/word_service.py 모듈별 설명
- __init__함수: ROS2의Node 클래스를 상속받아WordService라는 이름의 노드를 정의 후 내부에 서비스서버와퍼블리셔, 서브스크라이버를정의


![Image 36](../../assets/images/ros/intro/lesson-04/img_022_036.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/word_service.py 모듈별 설명
- letter_callback함수: letter_topic 토픽에서 수신된 메시지를 처리하여self.current_letter에저장


![Image 37](../../assets/images/ros/intro/lesson-04/img_023_037.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/word _service.py 모듈별 설명
- check_letter_callback 함수: 서비스 요청을 처리하며, 수신한 문자가 현재 단어에 포함되어 있는지 확인하고 게임 상태를 업데이트. 업데이트된 상태는Progress 메시지를 통해 퍼 블 리 시


![Image 38](../../assets/images/ros/intro/lesson-04/img_024_038.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/word_service.py 모듈별 설명
- main 함수: ROS2 시스템을 초기화하고WordService 노드를 실행


![Image 39](../../assets/images/ros/intro/lesson-04/img_025_039.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/user_ input.py 전체 코드

Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/user_input.py 모듈별 설명
- __init__ 함수: Node 클래스를 상속받아UserInput이라는 노드를 정의. 이노 드는CheckLetter 서비스에 문자 확인 요청을 보냄

![Image 42](../../assets/images/ros/intro/lesson-04/img_027_042.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/user_input.py 모듈별 설명
- input_thread 함수: 사용자로부터Enter 키 입력을 기다리며, 입력이 들어오면send_request 메서드를 호출하여 현재 요청을 서비스로 보냄

![Image 44](../../assets/images/ros/intro/lesson-04/img_028_044.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/user_input.py 모듈별 설명
- send_request 함수: CheckLetter 서비스에 비동기적으로 요청을 보내어, 현재 선택된 문자가 단어에 포함되어 있는지 확인

![Image 46](../../assets/images/ros/intro/lesson-04/img_029_046.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/user_input.py 모듈별 설명
- main 함수: ROS2 시스템을 초기화하고UserInput 노드를 실행하여 사용자 입력을 기다리며, 서비스 요청을 반복적으로 보낼 수 있는 구조를 만듦

![Image 48](../../assets/images/ros/intro/lesson-04/img_030_048.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/ progress_action_client.py 전체 코드

![Image 50](../../assets/images/ros/intro/lesson-04/img_031_050.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/ progress_action_client.py 전체 코드

![Image 52](../../assets/images/ros/intro/lesson-04/img_032_052.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/progress_action_client.py 모듈별 설명
- __init__ 함수: 노드를 초기화하고 액션 클라이언트를 생성하여, 게임 진행 목표를 서버에 전송할 준비를 함

![Image 54](../../assets/images/ros/intro/lesson-04/img_033_054.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/progress_action_client.py 모듈별 설명
- send_goal 함수: GameProgress 액션 서버에 목표를 전송하고, 목표 전송 후에 피드백 콜백과 완료 콜백을 설정하여 서버 응답을 처리

![Image 56](../../assets/images/ros/intro/lesson-04/img_034_056.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/progress_action_client.py 모듈별 설명
- Feedback_callback 함수: 서버에서 수신한 피드백 메시지를 처리하여, 게임 종료 상태를 확인하고로깅

![Image 58](../../assets/images/ros/intro/lesson-04/img_035_058.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/progress_action_client.py 모듈별 설명
- goal_response_callback 함수: 서버가 목표를 수락했는지 확인하고, 수락된 경우 최종 결과를 비동기적으로 요청하며 결과 콜백 을 설정

![Image 60](../../assets/images/ros/intro/lesson-04/img_036_060.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/progress_action_client.py 모듈별 설명
- get_result_callback 함수: 서버에서 수신한 최종 결과를 확인하고, 승리 또는 패배에 따라로 깅 을 진행

![Image 62](../../assets/images/ros/intro/lesson-04/img_037_062.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/progress_action_client.py 모듈별 설명
- main 함수: ROS2 시스템을 초기화하고ProgressActionClient 노드를 실행하여 목표를 전송하고 결과가 수신될 때까지 이벤트루프를 유지

![Image 64](../../assets/images/ros/intro/lesson-04/img_038_064.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/ progress_action_server.py 전체 코드

![Image 66](../../assets/images/ros/intro/lesson-04/img_039_066.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/ progress_action_server.py 전체 코드

![Image 68](../../assets/images/ros/intro/lesson-04/img_040_068.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/ progress_action_server.py 전체 코드

![Image 70](../../assets/images/ros/intro/lesson-04/img_041_070.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/progress_action_server.py 모듈별 설명
- __init__ 함수: 노드를 초기화하고GameProgress 액션 서버와progress 토픽을 구독하여 게임 진행 상태를 관리

![Image 72](../../assets/images/ros/intro/lesson-04/img_042_072.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/progress_action_server.py 모듈별 설명
- progress_callback 함수: progress 토픽으로부터 수신한 메시지를 처리하여, current_progress에 게임 상태를 업데이트하고로깅

![Image 74](../../assets/images/ros/intro/lesson-04/img_043_074.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/pro gress_action_server.py 모듈별 설명
- execute_callback 함수: 클라이언트의 목표 요청을 수신하고, 게 임 진행 상황을 주기적으로 피드백하며, 게임 종료 시 최종 결과를 반환. 주기적으로feedback_msg를 통해 게임 상태를 클라이언트에 전달

![Image 76](../../assets/images/ros/intro/lesson-04/img_044_076.webp)


Hang-man - 실습

## hangman_game
- hangman_game/hangman_game/progress_action_server.py 모듈별 설명
- main 함수: ROS2 시스템을 초기화하고ProgressActionServer 노드를 실행하여 목표 요청과 토픽 구독을 동시에 처리할 수 있도록 멀티 스레드 실행자를 사용

![Image 78](../../assets/images/ros/intro/lesson-04/img_045_078.webp)


Hang-man - 실습

## hangman_game
- hangman_game/setup.py
- entry_points를 다음과 같이 변경

![Image 80](../../assets/images/ros/intro/lesson-04/img_046_080.webp)


Hang-man - 실습

## hangman_game
- hangman_interfaces/CMakeLists.txt

![Image 82](../../assets/images/ros/intro/lesson-04/img_047_082.webp)

![Image 84](../../assets/images/ros/intro/lesson-04/img_047_084.webp)


Hang-man - 실습

## hangman_game
- hangman_interfaces/package.xml

![Image 86](../../assets/images/ros/intro/lesson-04/img_048_086.webp)


Hang-man - 실습

## hangman_game
1. colcon 빌드후setup.bash 적용
2. letter publisher 실행
3. 새로운 터미널에서word service 실행


![Image 87](../../assets/images/ros/intro/lesson-04/img_049_087.webp)


![Image 88](../../assets/images/ros/intro/lesson-04/img_049_088.webp)


![Image 89](../../assets/images/ros/intro/lesson-04/img_049_089.webp)


Hang-man - 실습

## hangman_game
4. 새로운 터미널에서action server 실행
5. 새로운 터미널에서action client 실행
6. 새로운 터미널에서user input 실행


![Image 90](../../assets/images/ros/intro/lesson-04/img_050_090.webp)


![Image 91](../../assets/images/ros/intro/lesson-04/img_050_091.webp)


![Image 92](../../assets/images/ros/intro/lesson-04/img_050_092.webp)


Hang-man - 실습

## hangman_game
- 실행 화면 user_input word_service


![Image 93](../../assets/images/ros/intro/lesson-04/img_051_093.webp)


![Image 94](../../assets/images/ros/intro/lesson-04/img_051_094.webp)


Hang-man - 실습

## hangman_game
- 실행 화면 action_server action_client


![Image 95](../../assets/images/ros/intro/lesson-04/img_052_095.webp)


![Image 96](../../assets/images/ros/intro/lesson-04/img_052_096.webp)


Hang-man - 실습

## hangman_game
- 실행 화면 user_input


![Image 97](../../assets/images/ros/intro/lesson-04/img_053_097.webp)


---

## Jupyter Notebooks


### ros2_function

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/ros/jupyter_ros/ros2_function.ipynb)

다음은 **ROS 2 Humble**에서 자주 사용하는 **Topic, Service, Action** 관련 Python API 함수들을 정리한 노트. 개발할 때 빠르게 참고할 수 있도록 요약.

### Topic 관련 함수
#### 퍼블리셔(Publisher)


```python
publisher = self.create_publisher(MsgType, 'topic_name', qos_profile)
publisher.publish(msg)
```

- `create_publisher(MsgType, topic_name, qos_profile)`: 퍼블리셔 생성
- `publish(msg)`: 메시지 전송

#### 서브스크라이버(Subscriber)


```python
self.subscription = self.create_subscription(
    MsgType,
    'topic_name',
    self.callback,
    qos_profile)
```

- `create_subscription(MsgType, topic_name, callback, qos_profile)`: 서브스크라이버 생성
- `callback(msg)`: 수신 메시지 처리 함수

### Service 관련 함수
#### 클라이언트(Client)


```python
self.cli = self.create_client(SrvType, 'service_name')

# 서비스 요청 준비
req = SrvType.Request()
req.param = value

# 서버가 준비될 때까지 대기
while not self.cli.wait_for_service(timeout_sec=1.0):
    self.get_logger().info('Waiting for service...')

# 요청 보내기
future = self.cli.call_async(req)
future.add_done_callback(response_callback)
```

- `create_client(SrvType, service_name)`: 서비스 클라이언트 생성
- `SrvType.Request()`: 요청 메시지 생성
- `call_async(req)`: 비동기 요청

#### 서버(Server)


```python
self.srv = self.create_service(SrvType, 'service_name', self.callback)
```

- `create_service(SrvType, service_name, callback)`: 서비스 서버 생성
- `callback(request, response)`: 요청 처리 함수
- `response.param = value` → 응답 내용 설정

### Action 관련 함수
#### 액션 클라이언트(Action Client)


```python
self._action_client = ActionClient(self, ActionType, 'action_name')

# 서버 대기
self._action_client.wait_for_server()

# goal 생성
goal_msg = ActionType.Goal()
goal_msg.param = value

# goal 전송
self._send_goal_future = self._action_client.send_goal_async(
    goal_msg,
    feedback_callback=self.feedback_callback)

# 결과 기다리기
self._send_goal_future.add_done_callback(self.goal_response_callback)
```

- `ActionClient(self, ActionType, action_name)`: 액션 클라이언트 생성
- `send_goal_async(goal_msg, feedback_callback)`: 목표 전송
- `goal_response_callback(future)`: 응답 처리
- `feedback_callback(feedback_msg)`: 피드백 수신 처리
- `get_result_async()`: 결과 요청

#### 액션 서버(Action Server)


```python
self._action_server = ActionServer(
    self,
    ActionType,
    'action_name',
    execute_callback=self.execute_callback)
```

- `ActionServer(self, ActionType, action_name, execute_callback)`: 액션 서버 생성
- `execute_callback(goal_handle)`: goal 처리 함수
- 내부에서 `goal_handle.publish_feedback()`으로 피드백 전송
- `goal_handle.succeed()` 또는 `goal_handle.abort()`
- `return result` 로 결과 전달

#### 참고용 예시 메시지 타입
- Topic: `std_msgs.msg.String`, `sensor_msgs.msg.Image`
- Service: `example_interfaces.srv.AddTwoInts`
- Action: `example_interfaces.action.Fibonacci`


---

## Code Examples


### `py_pubsub_qos/`

[View full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/py_pubsub_qos/){ .md-button }

#### `py_pubsub_qos/py_pubsub_qos/__init__.py`

```python

```

#### `py_pubsub_qos/py_pubsub_qos/publisher_member_function.py`

```python
# Copyright 2016 Open Source Robotics Foundation, Inc.
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

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

from std_msgs.msg import String
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSHistoryPolicy
from rclpy.qos import QoSProfile
from rclpy.qos import QoSReliabilityPolicy

qos_profile = QoSProfile(reliability=QoSReliabilityPolicy.RELIABLE, history=QoSHistoryPolicy.KEEP_ALL, depth=10, durability=QoSDurabilityPolicy.TRANSIENT_LOCAL)


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__("minimal_publisher")
        self.publisher_ = self.create_publisher(String, "topic", qos_profile)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = "Hello World: %d" % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

# ... (12 more lines)
```

#### `py_pubsub_qos/setup.py`

```python
from setuptools import find_packages, setup

package_name = "py_pubsub_qos"

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
    maintainer="sparkx",
    maintainer_email="mh9716@naver.com",
    description="TODO: Package description",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "talker = py_pubsub_qos.publisher_member_function:main",
            "listener = py_pubsub_qos.subscriber_member_function:main",
        ],
    },
)

```
