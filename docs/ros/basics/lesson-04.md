# 강의_3기_ROS2_기초_4차시


ROS2 기초-4차시
훈련 일정
오전
오후
1차시

- 로봇의 역사
- 컴퓨터 구조(Booting, CPU 작동 원리, POST)
- 리눅스와 운영 체계
- 리눅스CLI 실습(디렉토리, 계정, 기본 명령어 등), Terminator, 커널, 쉘, gedit, bash
- Application 작동 원리(마이크로프로세서, 메모리, 저장 장치)
- 리눅스 CLI 실습 2차시
- 리눅스 CLI 실습
- 네트워크와 통신(IPV4, IPV6, 소켓, 노드, Hub, TCP, UDP)
- API, Library, Framework, 프로세스와Thread
- 인터프리터, 컴파일러(소스 코드→ Build → 실행 파일)
- 소켓 프로그래밍 실습
- OSI7 Layer, 프로토콜(RS-232C, RS-485, Ethernet, TCP/UDP, IP) 3차시
- 센서 기초, IoT와Embedded
- 로봇 기초, 좌표계
- 로봇 센서 활용 및 로봇의 구성(기계 기구, 전기 전자, 소프트웨어)
- ROS2 소개 및 활용
- ROS2 설치(ros.org) 및demo_node 4차시
- ROS2 소개 및 활용
- ROS2 실습(Talker, Listener)
- ROS2 패키지 설명
- ROS2 실습(Turtlesim, teleop_key) 5차시
- ROS2 실습(Turtlesim, Teleop_key 여러 개 만들기)
- Topic, Service, Action, Parameter, RQT, RQT_Graph 이론 및 실습
- ROS2 실습(Turtlesim, Namespace 여러 개 만들기)
- Ros bag and play 실습, my first package build 실습
- Turtlesim subscribing 실습, ROS의 중요한 개발 도구(Rviz, GAZEBO 소개)


ROS2 turtlesim 복습
$ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist “{linear:{x: 2.0, y: 0.0, z: 0.0},
angular:{x: 0.0, y: 0.0, z: 0.0}}”
이동
Turtle 다시 생성해 보기

ROS2 turtlesim 복습
$ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist “{linear:{x: 2.0, y: 0.0, z: 0.0},
angular:{x: 0.0, y: 0.0, z: 1.8}}”
이동


![Image 7](../../assets/images/ros/basics/lesson-04/img_004_007.webp)


ROS2 turtlesim 복습
$ros2 topic pub --rate 1 /turtle1/cmd_vel geometry_msgs/msg/Twist “{linear:{x: 0.0, y: 0.0, z: 0.0},
angular:{x: 0.0, y: 0.0, z: 1.8}}”
제자리 회전
$ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist “{linear:{x: 0.0, y: 0.0, z: 0.0},
angular:{x: 0.0, y: 0.0, z: 1.8}}”
※ Tip : ctrl + 화살표 눌러서cli 빠른 이동

ROS2 turtlesim 복습
$ros2 topic pub --rate 1 /turtle1/cmd_vel geometry_msgs/msg/Twist “{linear:{x: 2.0, y: 0.0, z: 0.0},
angular:{x: 0.0, y: 0.0, z: 1.8}}”
원운동
(회전)
Rate 1(초당1회)

ROS2 turtlesim 복습
$ros2 topic pub --rate 1 /turtle1/cmd_vel geometry_msgs/msg/Twist “{linear:{x: 2.0, y: 0.0, z: 0.0},
angular:{x: 0.0, y: 0.0, z: 3.6}}”
원운동
(회전)
ROS2 turtlesim 복습
ROS 소개 및 활용
●
OS

- Ubuntu 22.04 (Jammy Jellyfish) ● ROS
- ROS 2 Humble ● 에디터
- Visual Studio Code, gedit ● 설치 매뉴얼
- ROS 2 Installation (Humble) ● 환경 설정 및 간단 튜 토 리얼
- ROS 2 Configuring environment
- ROS 2 Turtlesim Tutorial

ROS 소개 및 활용
메타 운영 체계
ROS는 메타 운영 체제로, 메타 운영 체제란 애플리케이션과 분산 컴퓨팅
자원 간의 가상화 레이어로 분산 컴퓨팅 자원을 활용하여, 스케줄링, 로드,
감시, 에러 처리 등을 실행하는 시스템이다.
ROS 소개 및 활용

- 2024.05.23 - ROS 2 Jazzy Jalisco (LTS, 5 years support)
- 2023.05.23 - ROS 2 Iron Irwini
- 2022.05.23 - ROS 2 Humble Hawksbill (LTS, 5 years support)
- 2021.05.23 - ROS 2 Galactic Geochelone
- 2020.06.05 - ROS 2 Foxy Fitzroy (LTS, 3 years support)
- 2019.11.22 - ROS 2 Eloquent Elusor
- 2019.05.31 - ROS 2 Dashing Diademata (First LTS, 2 years support)
- 2018.12.14 - ROS 2 Crystal Clemmys
- 2018.07.02 - ROS 2 Bouncy Bolson
- 2017.12.08 - ROS 2 Ardent Apalone (1st version)
- 2017.09.13 - ROS 2 Beta3 (code name R2B3)
- 2017.07.05 - ROS 2 Beta2 (code name R2B2)
- 2016.12.19 - ROS 2 Beta1 (code name Asphalt)
- 2016.10.04 - ROS 2 Alpha8 (code name Hook.and.Loop)
- 2016.07.14 - ROS 2 Alpha7 (code name Glue Gun)
- 2016.06.02 - ROS 2 Alpha6 (code name Fastener)
- 2016.04.06 - ROS 2 Alpha5 (code name Epoxy)
- 2016.02.17 - ROS 2 Alpha4 (code name Duct tape)
- 2015.12.18 - ROS 2 Alpha3 (code name Cement)
- 2015.11.03 - ROS 2 Alpha2 (code name Baling wire)
- 2015.08.31 - ROS 2 Alpha1 (code name Anchor)
- ROS Noetic Ninjemys
- Released May, 2020
- LTS, supported until May, 2025 ROS 2 Jazzy Jalisco [출처] https://github.com/ros-infrastructure/artwork/tree/master/distributions

![Image 18](../../assets/images/ros/basics/lesson-04/img_011_018.webp)


![Image 19](../../assets/images/ros/basics/lesson-04/img_011_019.webp)


![Image 20](../../assets/images/ros/basics/lesson-04/img_011_020.webp)

![Image 22](../../assets/images/ros/basics/lesson-04/img_011_022.webp)


![Image 23](../../assets/images/ros/basics/lesson-04/img_011_023.webp)

![Image 26](../../assets/images/ros/basics/lesson-04/img_011_026.webp)

ROS
ROS란 무엇인가?
ROS는 로봇을 위한 오픈 소스 메타 운영 체제
메타 운영 체제란 기존의 운영 체제 위에 로봇 개발에 필요한 기능을 추가한 것을 말합니다.
ROS는 로봇의 하드웨어 추상화, 프로세스 간 통신, 패키지 관리 등 로봇 개발에 필요한 다양한 기능을 제공합니다.
Open Source
모듈 구조
확장성
ROS는 기존의 윈도우나 리눅스 같은 운영 체계가 아니며, 기존 운영 체계에 추가적인 설치를 동반하는 미들 웨어이다.
ROS의 데이터 통신은 서로 다른 운영 체제, 하드웨어 시스템에서도 데이터를 주고받을 수 있기 때문에 로봇 개발에 적합하다.
ROS와Linux를 사용하는 이유
1.
운영 체계 라이선스
2.
개발 시간 단축
3.
편리한디버깅도구및시각화도구
4.
많은 사용자 및 생태계


![Image 36](../../assets/images/ros/basics/lesson-04/img_013_036.webp)


ROS2 실습
ROS 구성 요소
구성 요소
설명
마스터

- 노드와 노드 사이 연결 및 메시지 통신의 네임 서버 역할
- Roscore로 실행이 되며, URI 주소는 기본적으로는 현재의 로컬IP 사용 노드
- ROS에서 실행되는 최소 단위의 프로세스를 말함
- ROS에서는 하나의 목적에 하나의 노드 작성을 권장함
- 노드가 구동될 때, 노드의 역할(토 리그 서비스 등), 메시지 형태 등이 등록됨 패키지
- ROS를 구성하는 기본 단위
- ROS 응용 프로그램은 패키지 단위로 개발되며 최소한 하나의 노드를 가짐 메시지
- 노드와 노 드는 서로 메시지를 통해서 데이터를 주고받음
- 메시지는integer, float, Boolean 등의 변수 형태임
- 메시지 안에 메시지를 품는 데이터 구조가 가능
- 단방향은 토픽(topic), 양방향은 서비스(service) 토픽
- 토픽은ROS의노드 사이의 데이터 통신의 한 종류
- 단방향 통신으로, 데이터를 메시지에 담아서 방송을 함
- 방송을 하는 퍼 블 리 셔(publisher)와수신을하는서브스크라이버(subscriber)로 구성됨


ROS 소개 및 활용
ROS1
ROS2
단일 로봇
복수 대의 로봇
실시간 제어 지원하지 않음
실시간 제어
안정된 네트워크 환경 요구
불안정한 네트워크 환경에서도 동작할 수 있는 유연함
단일 플랫폼(Linux)
멀티 플랫폼(Linux, Windows, MacOS)

- 최신 기술 지원(Zeroconf, Protocon Buffers, ZeroMQ, WedSockets, DDS등) 주로 대학이나 연구소 등의 아카데믹 연구용도 상업용 제품 지원


ROS 소개 및 활용
앞 시간에서 임 베 디 드와 역할을 잘 분배해야한다는 설명이 있었습니다.

ROS 소개 및 활용
(1) 글로벌 커뮤니티
ROS 커뮤니티는10년이상ROS 프로젝트는 소프트웨어에 기여하고 개선하는 수십만 명의 개발자와 사용자로 구성된 글로벌 커뮤니티를
육성함으로써 로봇 공학을 위한 방대한 소프트웨어 에코 시스템을 만들어 왔다. ROS 2는 커뮤니티를 위해, 커뮤니티에 의해 개발되었다.
(2) 검증된 사용 사례
ROS는 로봇 산업 전반에 걸쳐 사용되고 있다. 로봇 공학 교육을 위한 표준이다. 단일 프로젝트부터 여러 기관의 협업 및 대규모 경연 대회에
이르기까지 대부분의 로봇 공학 연구의 기반이 되었다. 그리고 오늘날 전 세계에서 생산 중인 로봇의 내부에도 이 기술이 적용되고 있다. 자율
이동 로봇(AMR)에서만ROS는 수십억 달러의 가치를 창출하는 데 기여했다.
(3) 시장 출시 시간 단축
ROS는 로봇 응용 프로그램을 개발하는 데 필요한 도구, 라이브러리 및 기능을 제공하므로 본연의 중요한 로봇 개발 작업에 더 많은 시간을
할애할 수 있다는 것이 가장 큰 장점이다. 특정로봇개발을위해처음부터프레임워크를만들고통신방법을선정하고디버깅툴과시각화툴을
다시 만드는 비효율적인 방법에서 벗어날 수 있게한다. 더불어ROS는 상용 소프트웨어가 아닌ROS 커뮤니티에서 개발해 오고 있는
오픈 소스이기 때문에ROS를 사용할 부분과 사용 방법을 유연하게 결정할 수 있을 뿐만 아니라 필요에 따라 자유롭게 수정할 수 있다.
(4) 다중 도메인
ROS는 실내에서 실외, 가정에서 자동차, 수중에서 우주, 소비자에서 산업에 이르기까지 다양한 로봇 공학 애플리케이션에서 사용할 수 있다.
(5) 멀티 플랫폼
ROS 2는Linux, Windows, macOS에서 개발, 지원, 테스트 진행하고 있기에 자율성, 백 엔드 관리 및 사용자 인터페이스의 원활한 개발 및
배포가 가능하다. 계층형 지원 모델을 사용하고 있기에 실시간 운영 체제(Real-time OS) 및임베디드OS(Embedded OS)와 같은 새로운
플랫폼으로의 포 팅에 대한 관심과 투자를 통해 도입 및 홍보도 할 수 있다.


ROS 소개 및 활용
(6) 100% 오픈 소스
ROS 2 코드는Apache 2.0 라이센스를 기본 라이센스로 사용하여 지적 재산권에 영향을 주지 않으면서 자유 재량으로 넓은 범위로 사용 가능하다.
(7) 상업 친화성
사용자 커뮤니티의ROS에 대한 오픈 소스 기여를 진심으로 권장하지만, 이를 요구하지는 않는다. 오픈 소스 라이선스에 따라ROS를 배포하며, Apache
2.0이 기본 라이선스이다. ROS를 수정하고, 자신 또는 다른 사람의 비공개 소프트웨어와 혼합하고, 그 결과물을 여러분의 독점 제품에 배포할 수 있으며,
그 사실을 알릴 필요도 없다. 물론 항상 사용자들이ROS를 어떻게 사용하고 있는지 알고 싶기에 커뮤니티에 이를 알려 주길 바란다.
(8) 업계 지원
ROS 2 기술 운영 위원회(ROS 2 Technical Steering Committee)의 멤버 쉽에서 알 수 있듯이ROS 2에 대한 업계 지원은 강력하다. 전 세계의 크고 작은
회사는 제품을 개발할 뿐만 아니라ROS 2에 오픈 소스 기여를 하기 위해 자원을 투입하고 있다.

- ROS Package Documentation
- Robotics Stack Exchange
- ROS Discourse Forums
- Open Robotics Discord Server
- ROS Index
- Issue Trackers


ROS 소개 및 활용
로봇 문제에 대한 솔루션을 제공하는ROS
이름과는 달리ROS는 사실 운영 체제가 아니다. 그보다는 로봇 애플리케이션을 구축하는 데 필요한 빌딩 블록을 제공하는
SDK(소프트웨어 개발 키트)이다.
수업 프로젝트, 과학 실험, 연구 프로토타입, 최종 제품 등 어떤 애플리케이션이든ROS를 사용하면 목표를 더 빨리 달성할 수 있다.
그리고, 모두 오픈 소스이다.

ROS 소개 및 활용
1) Plumbing
ROS의 핵심은 흔히"미들웨어" 또는"배관"이라고 불리는 메시지 전달 시스템을 제공한다. 커뮤니케이션은 새로운 로봇 애플리케이션이나 하드웨어와
상호 작용하는 모든 소프트웨어 시스템을 구현할 때 가장 먼저 해결해야할 문제 중 하나이다. ROS에 내장되어 있고 충분한 테스트를 거친 메시징
시스템은 퍼 블 리 시/서브스크 라이브 패턴을 통해 분산 노드 간의 통신 세부 사항을 관리함으로써 시간을 절약해 준다. 이러한 접근 방식은 결함 격리,
우려 사항 분리, 명확한 인터페이스 등 소프트웨어 개발의 어려운 부분들을 해결할 수 있게 돕는다. ROS를 사용하면 유지 관리, 기여, 재사용이 더 쉬운
시스템을 만들 수 있다.
그 과정에서 방대한 커뮤니티 경험을 활용하여 표준ROS 메시지 형식을 만들 수 있으며, 이러한 표준은LIDAR 및 카메라부터 현지화 알고리즘 및
사용자 인터페이스에 이르기까지 모든 것과 상호 작용하는 데 사용된다.
2) Tools
로봇 애플리케이션을 구축하는 일은 쉽지 않다. 센서와 액추에이터를 통해 물리적 세계와 비동기적으로 상호 작용해야한다는 점과 소프트웨어 개발의
모든 어려움이 결합되어 있다. 애플리케이션을 효율적으로 구축하려면 우수한 개발자 도구가 필요하다. ROS에는 실행, 상태, 디버깅, 시각화, 플로 팅,
로깅, 재생 등 다양한 개발 도구가 포함되어 있다. 이러한 도구는 개발 팀의 진행 속도를 높여 주며, 제품 출시 시 함께 제공될 수 있다.


ROS 소개 및 활용
3) Capabilities
ROS 에코 시스템은 로봇 소프트웨어의 보고이다. GPS용 디바이스 드라이버, 4족 보행 로봇을 위한 보행 및 균형 컨트롤러, 모바일 로봇을 위한 매핑
시스템 등 어떤 것이 필요하든ROS는 여러분을 위한 모든 것을 제공하고 있다. 드라이버부터 알고리즘, 사용자 인터페이스에 이르기까지ROS는
애플리케이션에 집중할 수 있는 빌딩 블록을 제공한다.
ROS 프로젝트의 목표는 당연하게 여겨지는 것에 대한 기준을 지속적으로 높여 로봇 애플리케이션 구축에 대한 진입 장벽을 낮추는 것이다. 유용
하거나 재미있고 흥미로운 로봇에 대한 좋은 아이디어가 있는 사람이라면 누구나 기본 하드웨어와 소프트웨어에 대한 모든 것을 이해하지 않고도
그 아이디어를 현실화할 수 있어야한다.
4) Community
ROS 커뮤니티는 규모가 크고 다양하며 글로벌하다. 학생과 취미 활동가부터 다국적 기업, 정부 기관에 이르기까지 다양한 사람과 조직이ROS
프로젝트를 계속 이어 가고 있다.
이 프로젝트의 커뮤니티 허브이자 중립적인 관리자는 이 웹 사이트와 같은 공유 온라인 서비스를 호스팅하고, 사용자가 설치하는 바이너리
패키지를 포함한 배포 릴리스를 생성 및 관리하며, ROS 내 대부분의 핵심 소프트웨어를 개발 및 유지 관리하는Open Robotics이다. 오픈
로보 틱 스는ROS와 관련된 엔지니어링 서비스도 제공하고 있다.


ROS 소개 및 활용
ROS 1은2007년에 개발이 시작되어 지금은 대학, 연구 기관, 산업계, 로봇 자작의 취미 활동까지 폭넓게 이용되고 있다. 원래ROS 1은
Willow Garage사가 개인 서비스 로봇인PR2개발에 필요한 미들 웨어 형태의 로봇 개발 프레임워크를 다양한 개발 툴과 함께 오픈 소스로
공개한 것으로 시작하였다. 따라서 개발 환경으로는PR2의 초기 컨셉을 그대로 이어받아 다음과 같은 제한 사항이 있었다.

- 단일 로봇
- 워크스테이션 급 컴퓨터
- Linux 환경
- 실시간 제어 지원하지 않음
- 안정된 네트워크 환경이 요구됨
- 주로 대학이나 연구소와 같은 아카데믹 연구용도 ROS1과ROS2의 차이점


ROS 소개 및 활용


![Image 39](../../assets/images/ros/basics/lesson-04/img_023_039.webp)


ROS 소개 및 활용
오늘날 요구되는 로봇 개발 환경과는 큰 차이가 있다. 예를 들어, 최근의ROS 1은 종래 가장 많이 이용되고 있던 학술 분야뿐만 아니라, 제조 로봇, 농업 로봇,
드론, 소셜 로봇과 같은 상용 로봇 등으로 이용되고 있다. 극단적인 예로NASA가 국제우주정거장에서 사용한Robonaut에는ROS 1가채용되고 있지만,
거기에서는 실시간 제어가 요구되었고 이를 위해서ROS 1을 수정하여 사용하였다. 이러한 새로운 로봇 개발 환경 및 요구되는 기능을 정리하면 다음과 같다.

- 복수 대의 로봇
- 임베디드 시스템에서의ROS 사용
- 실시간 제어
- 불안정한 네트워크 환경에서도 동작할 수 있는 유연함
- 멀티 플랫폼(Linux, Windows, macOS)
- 최신 기술 지원(Zeroconf, Protocol Buffers, ZeroMQ, WebSockets, DDS 등)
- 상업용 제품 지원 ROS 1에서 이러한 새롭게 요구되는 기능을 제공하려면 대규모API의 변경이 필요하다. 그러나 기존의ROS 1과의 호환성을 유지하면서 수많은 새로운 기능을 추가하는 것은 쉽지 않았다. 또한, 기존의ROS 1을 문제 없이 이용하고 있는 사용자에게는 큰API의 변경은 바람직하지 않다. 그래서ROS의 차세대 기능을 도입한 버전을ROS 2라고, ROS 1에서 분리하여 개발하게 된 것이다. 기존의ROS 1 사용자는 필요하다면 그대로ROS 1을 이용할 수 있다. 한편, 새로운 기능이 필요한 사용자는ROS 2를 선택하면 된다. 또한, ROS 1과ROS 2 사이에서 서로 메시지 통신이 가능한 브리지 프로그램 (ros1_bridge) 제공되므로 두 버전 모두를 함께 사용하는 것도 가능하다.


ROS 소개 및 활용

1. Platforms
ROS 2부터는3대 운영 체제인Linux, Windows, macOS를 모두 지원한다. 이는 바이너리 파일로 설치가 가능하다는 의미로Windows
사용자가 많은 한국의 경우에는 반가운 소식으로 받아들이는 분들이 많을 것 같다. ROS 2 Jazzy Jalisco 기준으로 보았을 때Linux는Ubuntu
Noble (24.04), Windows는Windows 10 버전, macOS는Mojave (10.14)버전을 지원하고 있다.
Linux의 경우에는Linux 배포 판 중 일반 사용자가 가장 많은Canonical의Ubuntu 진영에서ROS 2 TSC로 가입되어 있어서 관련된 내용을
많이 볼 수 있다. 리눅스 이용자라면Canonical에서 연재 중인 아래 참고 자료Ubuntu Robotics, Ubuntu Robotics Blogs의 내용을 참고하면
ROS 2 사용에 도움이 될 듯 싶다. 그리고Linux, macOS는ROS 1 부터 지원하고 있었는데 이번ROS 2에서는Microsoft가ROS 2 TSC로
들어오고Windows용 패키지 및 테스트, Visual Studio Code Extension for ROS 까지 준비하는 등 굉장한 노력을 기울여Windows
사용자들도ROS 2를 쉽게 사용할 수 있게 되었다. Windows 사용자라면Win ROS Landing Page, WSL 2(Windows Subsystem For Linux 2)의
Windows 관련 문서를 참고하기를 추천한다.

2. Real-time
ROS 2는Real-time을 지원한다. 단, 선별된 하드웨어 사용, 리얼타임 운영 체제 사용, DDS의RTPS(Real-time Publish-Subscribe Protocol)와
같은 통신 프로토콜을 사용, 매우 잘 짜여진 리얼타임 코드 사용을 전제로 실시간성을 지원하고 있다. 이 부분은ROSCon2019의Pre-
conference Workshops으로 진행되었던`Doing real-time with ROS 2: Capabilities and challenges`에서 자세히 설명되었는데 이 부분의
내용은 이 강좌에서 설명하기에는 내용이 많아 상당히 길어질 것 같으므로 추후 해당 내용 및 더 자세히 알아보려면 해당 워크샵의 페이지를
참고하도록하자.


ROS 소개 및 활용

3. Security
ROS 1에서는 항상 보안이 문제였다. 노드를 관리하는ROS master의 하나의IP와 포트만 노출되면 모든 시스템을 죽일 수 있었으
며, 보안 입장에서는TCPROS는 뻥 뚫린 큰 구멍에 가까웠다. 하지만ROS 1은 이러한 부족한 부분을 매우기보다는 로봇 개발에
사용되는 다양한 하드웨어와 소프트웨어를 평가하고 작동하는 유연성에 더 무게를 두었고 이러한 유연성은 보안에 대한 기회 비
용보다 더 중요하게 여겼다. 즉, 보안 이슈는 개발 우선순위에서 뒤져 있었다. 당연히ROS 초창기에는 이 선택은 옳았다.
하지만 시간이 흘러 이러한 취약점은 상용 로봇에ROS를 도입할 수 없게 만드는 첫 번째 이유이자 가장 큰 걸림돌이 되었다. 이에
ROS 2에서는 디자인 설계부터 이 부분을 명확히 짚고 넘어갔다. 우선, TCP 기반의 통신은OMG(Object Management Group)에
서 산업용으로 사용 중인DDS(Data Distribution Service)를 도입하였고, 자연스럽게DDS-Security 이라는DDS 보안 사양을
ROS에 적용하여 보안에 대한 이슈를 통신 단부터 해결하였다. 또한ROS 커뮤니티에서는SROS 2(Secure Robot Operating
System 2)라는 툴을 개발하였고 보안 관련RCL 서포트 및 보안 관련 프로그래밍에 익숙지 않은 로보 틱 스 개발자를 위해 보안을
위한 툴 킷 을 만들어 배포하고 있다. 이 부분에 대한 더 자세한 내용은ROS 2 디자인 문서(DDS-Security integration, Access
Control Policies, Security Enclaves, Robotic Systems Threat Model)의`Security` 관련 부분을 참고하길 바라며 지난ROSCon에서
의 워크샵에서 진행한`Is your robot secure? ROS 1 & ROS 2 Security Workshop`의문 서도 참고하면 도움이 될 것 같다. 우리는
추후 강좌를 통해 직접 보안 설정 및 프로그램하는 실습을 진행해 보기로 하자.


ROS 소개 및 활용

4. Communication
ROS 1에서는 자체 개발한TCPROS와 같은 통신 라이브러리를 사용하고 있던 반면, ROS 2은리얼타임퍼블리시와서브스크라이브
프로토콜인RTPS(Real Time Publish Subscribe)를 지원하는 통신 미들 웨어DDS를 사용하고 있다. DDS는OMG(Object Management
Group)에 의해 표준화가 진행되고 있으며, 상업적인 용도에도 적합하다는 평가가 지배적이다. DDS에서는IDL(Interface Description
Language)를 사용하여 메시지 정의 및 직렬화를 더 쉽게, 더 포괄적으로 다룰 수 있다. 또한 통신 프로토콜로는RTPS을 채용하여 실시간
데이터 전송을 보장하고 임 베 디 드 시스템에도 사용할 수 있다. DDS는 노드 간의 자동 감지 기능을 지원하고 있어서 기존ROS 1에서각
노드들의 정보를 관리하였던ROS마스터가 없어도 여러DDS 프로그램 간에 통신할 수 있다. 또한 노드 간의 통신을 조정하는QoS(Quality
of Service) 매개변수를 설정할 수 있어서TCP 처럼 데이터 손실을 방지함으로써 신뢰도를 높이거나, UDP 처럼 통신 속도를 최우선하여
사용할 수도 있다. 이러한 다양한 기능을 갖춘DDS를 이용하여ROS 1의퍼블리시, 서브스크 라이브형 메세지 전달은 물론, 실시간 데이터
전송, 불안정한 네트워크에 대한 대응, 보안 강화 등이 강화되었다. DDS의 채용은ROS 1에서ROS 2로 바뀌면서 가장 큰 변화 점이다.

5. Middleware interface
앞서 설명한DDS는 다양한 기업에서 통신 미들 웨어 형태로 제공하고 있다. 그 벤더로는10 곳이 있는데 이 중ROS 2를 지원하는 업체는
ADLink, Eclipse Foundation, Eprosima, Gurum Network, RTI로총5 곳이다. DDS 제품명으로는Eclipse Foundation의Cyclone DDS,
Eprosima의Fast DDS, Gurum Network의Gurum DDS, RTI의Connext DDS가 있다. 참고로 이 중Gurum Network는 유일하게 대한민국
기업으로DDS를 순수 국산 기술로 개발하여 상용화에 성공한 기업이다.
ROS 2에서는 이러한 벤더들의 미들 웨어를 유저가 원하는 사용 목적에 맞게 선택하여 사용할 수 있도록ROS Middleware(RMW)형태로
지원하고 있다. 이는 각 벤더들의 미들 웨어마다API가 약간씩 달라도ROS 2 유저들은 이를 생각하지 않고 통일된 코드로 쉽게 바꿔서 사용할
수 있도록 것으로, RMW는여러DDS 구현을 지원하기 위하여API의 추상화 인터페이스로 지원하고 있다.


ROS 소개 및 활용

6. Node manager (discovery)
ROS 1에서의 필수 실행 프로그램으로는roscore가 있다. 이를 실행시키면ROS Master, ROS Parameter Server, rosout logging node가 실행되었다.
특히ROS Master는ROS 시스템의 노드들의 이름 지정 및 등록 서비스를 제공하였고, 각 노드에서 퍼 블 리 시 또는 서브 스 크 라이브하는 메시지를 찾아서
연결할 수 있도록 정보를 제공해 주었다. 즉, 각각 독립되어 실행되는 노드들의 정보를 관리하여 서로 연결해야하는 노드들에게 상대방 노드의 정보를
건네 주어 연결할 수 있게해 주는 매우 중요한 중매 역할을 수행했었다. 이 때문에ROS 1에서는 노드 사이의 연결을 위해 네임 서비스를 마스터에서
실행했었어야했고, 이ROS Master가 연결이 끓기거나 죽는 경우 모든 시스템이 마비되는 단점이 있었다.
ROS 2에서는roscore가 없어지고3가지 프로그램이 각각 독립 수행으로 바뀌었다. 특히, ROS Master의 경우 완전히 삭제되었는데 이는DDS를
사용함에 따라 노드를DDS의Participant개념으로 취급하게 되었으며, Dynamic Discovery기능을 이용하여DDS 미들 웨어를 통해 직접 검색하여
노드를 연결할 수 있게 되었다. 이제ROS 2에서는roscore는Bye~ Bye~ 다.

7. Languages
ROS 2의 프로그램 언어로는ROS 1과 마찬가지로 다양한 프로그래밍 언어를 지원할 예정이다. 아직까지는C++, Python이 주력 언어라고 볼 수 있는데
이 주력 언어도 아래와 같이 큰 변화가 있었다. ROS 2 배포 판마다 조금씩 다르기는하지만Jazzy를 기준으로 보았을 때, C++은C++17, 파이썬은
Python 3.8이 기본 요구 사항으로 되어 있다. 이다. 같은 언어를 쓰더라도ROS 1을 사용했을 때에는 뭔가 올드한 느낌이었고 최신 언어들이 제공하는
기능들을 못 쓰고 그림에 떡이였는데 이제는 최신의 아름다운 언어를 쓰는 기분이다. 이는 사용해 보면 알게 될 것이다. 물론 새로운 걸 배운다는 것은
어쩔 수 없는 엔지니어의 숙명이다.

- ROS 1: C++03, Python 2.7
- ROS 2: C++17, Python 3.8


ROS 소개 및 활용

8. Build system
ROS 2에서는 새로운 빌 드 시스템인ament를 사용한다. ament는ROS 1에서 사용되는 빌 드 시스템인catkin의 업그레이드 버전이다. ROS 1의
catkin이CMake만을 지원했던 반면, ament는CMake를 사용하지 않는Python 패키지 관리도 가능하다. 즉, ROS 2에 와서는Python 패키지는
비로서 처음으로 완전 독립을 이루게 되었는데ROS 1에서Python 코드가 있는 패키지는setup.py 파일이CMake 내에서 사용자 정의
로직으로 처리되었다. 하지만ROS 2에서Python 패키지는setup.py 파일의 모든 기능을 순수Python 모듈과 동등한 수준으로 개발할 수 있게
되었다. 마지막으로TMI일 수 있으나catkin과ament는 이음 동의어로 버드나무의 화수를 의미하며ROS 1의 개발 주체인Willow Garage 뒷
마당에 있던 버드나무 화수를 보고 지었다고 한다. 즉, 뭔가 심오한 뜻이 있는 것은 아니다.

- ROS 1: rosbuild → catkin (CMake)
- ROS 2: ament (CMake), Python setuptools (Full support)

9. Build tools
ROS 1의 경우 여러 가지 다른 도구, 즉catkin_make, catkin_make_isolated 및catkin_tools가지원되었다. ROS 2에서는 알파, 베타, 그리고
Ardent 릴리스까지 빌 드 도구로ament_tools이 이용되었고 지금에 와서는colcon을 추천하고 있다.
colcon은ROS 2 패키지를 작성, 테스트, 빌 드 등ROS 2 기반의 프로그램할 때 빼놓을 수 없는 툴로 작업 흐름을 향상시키는CLI 타입의 명령어
도구이다. 사용 방법은`colcon test`와`colcon build` 와 같이 터미널 창에서 수행하게 되며 다양한 옵션을 사용할 수 있다. 이는 추후 이어지는
강좌들에서 더 자세히 다루도록하겠다.


ROS 소개 및 활용

10. Build options
ROS 2에서는 빌 드 관련 내용들이 모두 변경되면서 빌 드 옵션에도 새로운 변화가 생겼다. 그 중 사용하면서 가장 좋았던3가지를 꼽자면
아래와 같다.
우선`Multiple workspace` 이다.
이는ROS 1에서는`catkin_ws`와 같이 특정 워크 스페이스를 확보하고 하나의 워크 스페이스에서 모든 작업을 다 했는데ROS 2에서는 복수의
독립된 워크 스페이스를 사용할 수 있어서 작업 목적 및 패키지 종류별로 관리할 수 있게 되었다.
둘째는`No non-isolated build` 이다.
ROS 1에서는 하나의CMake 파일로 여러 개의 패키지를 동시에 빌 드할 수 있었다. 이렇게 하면 빌 드 속도가 빨라지지만 모든 패키지의
종속성에 신경을 많이 써야하고 빌 드 순서가 매우 중요하게 된다. 또한 모든 패키지가 동일 네임 스페이스 사용하게 되므로 이름에서 충돌이
발생할 수 있었다. ROS 2에서는 이 전 빌 드 시스템인catkin에서 일부 기능으로 사용되었던`catkin_make_isolated` 형태와 같은 격리 빌드만을
지원함으로써 모든 패키지를 별도로 빌 드하게 되었다. 이 기능 변화를 통해 설치용 폴더를 분리하거나 병합할 수 있게 되었다.
셋째는`No devel space`이다.
catkin은 패키지를 빌 드한 후devel 이라는 폴더에 코드를 저장한다. 이 폴더는 패키지를 설치할 필요 없이 패키지를 사용할 수 있는 환경을
제공한다. 이를 통해 파일 복사를 피하면서 사용자는 파이썬 코드를 편집하고 즉시 코드 실행할 수 있었다. 단 이러한 기능은 매우 편리한
기능이지만 패키지를 관리하는 측면에서 복잡성을 크게 증가시켰다.
이에ROS 2에서는 패키지를 빌 드한 후 설치해야 패키지를 사용할 수 있도록 바뀌었다. 단 쉬운 사용성도 고려하여colcon 사용 시에`colcon
build --symlink-install` 와 같은 옵션을 사용하여 심벌 릭 링크 설치의 선택적 기능을 사용하여 동일한 이점을 제공하고 있다.


ROS 소개 및 활용

11. Version control system
ROS는 수많은 소스 코드 공여자로부터 만들어 가는 코드의 집합이기 때문에 개인은 물론 소속도 정말 다양하고 각 코드들의 리 포 지 토 리도 제각각이다.
예를 들어 어느 패키지는GitHub를 이용하고 어떤 것은Bitbucket를 이용한다. 그리고 사용하는 버전 관리 시스템(Version Control System, VCS)도Git,
Mercurial, Subversion, Bazaar 등 다양하다.

- ROS 1: rosws → wstool, rosinstall (*.rosinstall)
- ROS 2: vcstool (*.repos) ROS 커뮤니티에서는 이러한 다양한 리 포 지 토 리와 혼재된 버전 관리 시스템을 사용하더라도ROS를 사용함에 있어서 불편함이 없도록 통합적인 툴이 필요했다. ROS 1에서는 처음에rosws이라는 툴에서wstool을 이용하였다가 최근ROS 2에서는vcstool으로 통합하였다. 현재ROS 1에서도vcstool를 사용하고 있는 상황이다. vcstool은 여러 리 포 지 토 리 작업을 보다 쉽게 관리할 수 있도록 설계된 버전 관리 시스템(VCS) 툴이다. 이 툴은ROS 2를 소스 코드로부터 설치해 본 사람이라면 자신도 모르게 사용했을 것이다. 아래의 명령어2줄을 살펴보자. 우선wget을 통하여 ros2.repos라는 파일을 받게 되는데 이 파일에는vcs 타입은 무었이고, 리포지토리 주소는 어떻게 되며, 설치해야하는 브랜치는 어떤 것인지가 명시된 파일이다. 이러한 정보가 기재된*.repos 파일을 이용하여 다양한 리 포 지 토 리, 다양한vcs를 지원하며 패키지들을 관리할 수 있도록하는 것을 의미한다. 특히ROS 2에서는 기존vcs 툴을 통폐합하여vcstool 이라는 이름으로 제공되어 사용에 매우 편리하게 되었다. 자세한 사용법은README 파일을 참고하도록하자. wget https://raw.githubusercontent.com/ros2/ros2/humble/ros2.repos vcs import src < ros2.repos


ROS 소개 및 활용

12. Client library
ROS 기반의 프로그래밍을 작성한다는 것은ROS Middleware Interface에서 유저 코드 영역(user land)을 다룬다는 것으로 그 밑에는ROS 클라이언트 라이브러리
(ROS Client Library)이 있고, 이 클라이언트 라이브러리는 앞서 설명한 미들 웨어(middleware interface)를 사용하고 있다는 것을 알고 있어야한다. 여기서 유저는
개발 목적에 따라C/C++, Python, Java, Node.js 등을 사용할 것이다. ROS 에서는 초창기부터 이러한 멀티 프로그래밍 언어를 지원하고 있는데ROS 1에서는
roscpp, rospy, roslisp 등각 프로그래밍 언어에 대해 클라이언트 라이브러리(Client Library)를 제공했다. 한편, ROS 2에서는ROS 클라이언트 라이브러리를
RCL(ROS Client Library)이라는 이름으로 제공한다. 그리고 프로그래밍 언어별로rclcpp, rclc, rclpy, rcljava, rclobjc, rclada, rclgo, rclnodejs 등으로 제공된다.
또한ROS 2는 앞서 설명한 바와 같이C이면C99, C++ 이라면C++ 14/17, Python라면Python 3 (3.5+) 등 최신 기술 사양에 대응하고 있다. 각C++/Python ROS
Client Library API는rclcpp, rclpy을 미리 봐 둔다면 도움 일 될 것이다.

13. Life cycle
로봇 개발에 있어서 로봇의 현재 상태를 파악하고 현재 상태에서 다른 상태로 변경되는 상태 천이 제어는 수십 년 간 로봇 공학에서도 주요 연구 주제로 다루었던 중
요한 부분 중에 하나이다. 특히 태스크 수행 측면에서 현재의 상태 파악과 천 이는 멀티 태스크 수행에서 빠질 수 없는 중요한 부분일 것이고 복수의 로봇 복수의
복합 태스크, 서비스 수행과 같은 상위 레벨의 프로그램일수록 더 중요하게 다루어지는 부분이다. ROS 1에서는 이러한 기능을 구현하기 위해서는SMACH과같은
상태 천 이를 관리하는 독립적인 패키지를 사용했어야했고 클라이언트 라이브러리에서는 상태 관리하는 부분이 없었기에 사용자가 임의로 클라이언트 라이브러
리 부분까지 수정하여 사용했어야했다.
ROS 2에서는 이러한 니즈를 반영하여 패키지의 각 노드들의 현재 상태를 모니터링하고 상태를 제어 가능한lifecycle을 클라이언트 라이브러리에 포함시켰으며
이를 통해ROS 시스템 상태를 보다 효과적으로 제어할 수 있게 되었다. 이를 이용하게 되면 기존ROS 1에서는 할 수 없었던 노드의 상태를 모니터링하고 상태를
천이 시키거나 노 드를 상태에 따라 재시작하거나 교체할 수도 있게 된다.


ROS 소개 및 활용

14. Multiple nodes
ROS 1의 초기에는 하나의 프로세스에서 여러 노드를 실행할 수 없었다. 하지만 이러한 요구는 지속적으로 제기되었고 하나의 프로세스에서 여러 노드를 작
성하기 위해nodelet라는 새로운 기능이ROS 1에 추가되었다. 이는 하드웨어 리 소스가 제한적이거나 노드 간에 수많은 메시지를 보내야할 때 유용하게 사
용되었다.
ROS 2에서nodelet이 사용되지는 않고RCL에 포함되어 있다. 이름은 컴포넌트(components)라고 부르며ROS 2에서는 이 컴포넌트를 사용하여 동일한 실행
파일에서 복수의 노드를 수행할 수 있게 되었다. 이를 사용하게 되면 노드의 실행 파일 수준은 더 세분화시킬 수 있으며 프로세스 내 통신IPC(intra-
process communication)기능을 이용하여ROS 2의 통신 오버 헤드를 제거할 수 있어서 더 효율적인ROS 2 응용 프로그램을 작성 가능하다.

15. Threading model
ROS 1에서 개발자는 단일스레 드 실행 또는 다중 스레드 실행 중 하나만 선택할 수 있었다. ROS 2에서는 더 세분화된 실행 모델(executor)을C++과
Python에서 사용할 수 있으며 사용자가 정의한 실행 기도 제공되는RCL API를 이용하여 쉽게 구현할 수 있다. Single Threaded Executor, Multi Threaded
Executor는 각 클라이언트 라이브러리마다 구현 방식이 다르기에 관련 설명은rclcpp executors, rclpy executors 문서를 참고하도록하자.


ROS 소개 및 활용

16. Messages (topic, service, action)
ROS 2에서도 기존ROS 1의 메시지(Messages)과 마찬가지로 단일 데이터 구조를 메시지라고 정의하며 정해진 또는 사용자가 정의한 메시지를 사용할 수 있으며,
각 패키지 이름과 마찬가지로 이름과 각 지정된 형식으로 메시지를 고유하게 식별할 수 있다. 사용처도 기존과 마찬가지로Topic, Service, Action 등에서 사용하며
기존과 비슷한 형태(Interface definition, interface file)로 사용 가능하다.
여기에ROS 2에서는OMG(Object Management Group)에서 정의된IDL(Interface Description Language)을 사용하여 메시지 정의 및 직렬화를 더 쉽게, 더 포괄적
으로 다룰 수 있게 되었다. IDL을 이용하게 되면 기존ROS 메시지 컨셉과 마찬가지로 다양한 프로그래밍 언어로 작성된 메시지를 사용할 수 있다. 이전에CORBA
(일 명, 코바)를 써 본 사람들은IDL이 친숙할 것이다. ROS 2에서는 기존msg, srv, action 파일 이외에도IDL을 지원한다. 그리고ROS 2가DDS를 채용하게 되면서
기존 메시지들과DDS 규칙을 맞추는 작업이 진행되었다. ROS 인터페이스 유형과DDS IDL 유형 간의 맵핑은Mapping between ROS interface types and DDS
IDL types 자료를 참고하면 좋을 듯 싶으며 전체적으로 다듬어진 정리 표는Interfaces 글을 참고하도록하자.
그리고, ROS 2에서는DDS를 사용하면서 메시지를 이용한Topic, Service, Action 등의 컨셉은 변하지 않으나 사용 방법은 상당히 많이 바뀌었다. 이 부분에 대한 설
명은 이어지는 강좌를 통해 예제와 함께 하나하나 알아 가 보자.

17. Command Line Interface
대부분의CLI 타입의 명령어 사용법은 기존ROS 1과 매우 비슷해서 약간의 이름 변경과 일부 옵션 사용법만 익힌다면 사용 시 큰 차이는 없다. 자주 사용되는 명령
어를 예를 들어 보자면 아래와 같은 차이 정도이다. ROS 1 명령어에 비해 명령어가 약간 길어진 듯 보이긴하지만 자주 쓰는 명령어는"alias rt='ros2 topic list'"와
같이 설정하여 사용하면 되기에 큰 무리는 없다. 더욱이ROS 2의CLI 형태의 명령어는ROS 2 TSC 멤버이자Ubuntu 개발 업체인Canonical이 담당하고 있어서 더
욱 믿음이 간다. 자세한 설명은ROS 2 Command Line Interface 를 참고하기 바라며 실습을 해 보고 싶다면 발표 자료를 참고하면 좋다.

- ROS 1: 'rostopic list'
- ROS 2: 'ros2 topic list'


ROS 소개 및 활용

18. roslaunch
ROS의 실행 시스템은 대표적으로`run`과`launch`가 있는데`run`은 단일 프로그램 실행, `launch`는 사용자 지정 프로그램 실행을 수행한다. 사용 면에서
는`run`에 비해 다양한 설정을 할 수 있는`launch` 사용이 월등히 사용 빈도가 높다. `launch`는 사용자가 실행하고자하는 프로그램의 각종 설정을 기술
하고 기술된 설정에 맞추어 각종 프로그램을 실행하도록 도와준다. 사용자가 지정하는 설정에는 실행할 프로그램, 실행할 위치, 전달할 인수 등 시스템
전체의 구성 요소를 쉽게 재사용할 수 있도록하고 있다. 그 목적과 컨셉은ROS 2에서도 크게 다르지 않다.
launch의ROS 1과ROS 2의 차이점을 살펴보면 다양한 파일 사용이다. ROS 1에서는`roslaunch` 파일이 특정`XML` 형식을 사용해었다. 이 형식을 이용
해도 다양한 설정을 추가하여 프로그램을 실행시킬 수 있어서 매우 편했는데, ROS 2에서는`XML`, `YAML` 형식 이외에도`Python`이 새롭게 채용되어
조건문 및Python 모듈을 추가로 사용하여 보다 복잡한 논리와 기능을 사용할 수 있게 되었다. 어떤 방식으로 사용하는지에 대한 추가 설명은 튜 토 리얼
을 참고하도록하자.

19. Graph API
ROS는 메타 패키지, 패키지, 노드 그리고 노드 간의 데이터 교환을 위한 토픽 등으로 구성되어 있다. 이 때의 각 노드와 토픽, 메시지 등이 고유의 이름을
가지고 있고, 매핑이 이루어져 각 노드와 노드 간의 토픽, 메시지의 관계를 그래프화시킬 수 있도록 되어 있다. 이러한 그래프 구조를 시각화하는 툴인
rqt_graph를 제공하고 있어서 현재 네트워크상의 각 구성 요소의 연결성을 시각적으로 확인할 수 있다.


ROS 소개 및 활용

20. Embedded Systems
로봇 개발에 있어서 실시간성을 담보 받으며 모터 및 센 싱을 제어하는 부분은 매우 중요하게 다루어져 왔다. 이 강좌 초반에서 언급했듯이ROS 커뮤니티에서도
이를 위해ROS 2에서는 선별된 하드웨어 사용, 리얼타임 운영 체제 사용, DDS의RTPS(Real-time Publish-Subscribe Protocol)와 같은 통신 프로토콜을 사용, 매우
잘 짜여진 리얼타임 코드 사용을 전제로 실시간성을 지원하고 있다. 하지만 실시간성이라는 것은 상위 소프트웨어에서 다루기에는 제약이 많다. 오히려
Embedded Systems 안에서 해결하는 게 더 적합하다고 보고 있다.
이에ROS 2 개발 초기부터Embedded Systems에 대한 관심이 높았는데 초기 개발 컨셉은ROS의 창시자인Morgan Quigley가ROSCon2015에서`ROS 2 on
“small” embedded systems`이라는 이름으로 발표한 자료 및 영상 를 보면 도움이 될 것이다. ROS 1에서도Embedded Systems을지 원하지 않는 것은 아니였다.
단, 매우 기초적인 수단이라고 볼 수 있는 임 베 디 드 보드와 메시지를 주고받을 때 시리얼(rosserial)로 통하여 통신하였다. ROS 2에서는 한 발 더 나아가 기존 시리
얼 통신, 블루투스 및 와이파이 통신을 지원하거나RTOS (Real-Time Operating System)를 사용하고 기존DDS 대신eXtremely Resource Constrained
Environments (DDS-XRCE)를 사용하는 등 임 베 디 드 보드에서 직접ROS 프로그래밍을 하여 하드웨어 펌 웨어로 구현된 노드를 실행할 수도 있다. 이 방법론에
는 여러 가지가 있을 수 있는데 현재ARM 사를 포함한 다양한MCU 제조 업체에서 이를 지원하기 위하여 다양한 방법론을 내놓고 있는 상태이고, eProsima,
BOSCH, ROBOTIS, FIWARE, Amazon, Renesas 등에서 다음 참고 자료와 같이 다양한 임 베 디 드 지원 방법에 대해 개발, 공개하고 있다.
임베디드 환경에서DDS 및ROS 메시지 통신 등에 관심 있는 사람은 아래 참고 자료를 참고하도록하자.

- ROS 1: rosserial, mROS
- ROS 2: micro-ROS, XEL Network, ros2arduino, Renesas, DDS-XRCE(Micro-XRCE-DDS), AWS ARCLM [참고 자료]
- https://micro-ros.github.io/
- http://xelnetwork.robotis.com/
- https://github.com/ROBOTIS-GIT/ros2arduino
- https://www.renesas.com/us/en/solutions/key-technology/robot/robot-operating-system.html
- https://micro-xrce-dds.docs.eprosima.com/en/latest/


ROS 소개 및 활용
ROS2와DDS (Data Distribution Service)


ROS 소개 및 활용
로봇 운영 체제ROS에서 중요시 여기는 몇 가지 용어 정의 및 메시지, 메시지 통신에 대해 먼저 알아보도록하자. 특히, 메시지 통신은ROS 프로그래밍에
있어서ROS 1과2의 공통된 중요한 핵심 개념이기에ROS 프로그래밍에 들어가기 전에 꼭 이해하고 넘어가야할 부분이다.
ROS에서는 프로그램의 재사용성을 극대화하기 위하여 최소 단위의 실행 가능한 프로세스라고 정의하는 노드(node) 단위의 프로그램을 작성하게 된다.
이는 하나의 실행 가능한 프로그램으로 생각하면 된다. 그리고 하나 이상의 노드 또는 노드 실행을 위한 정보 등을 묶어 놓은 것을 패키지(package)라고
하며, 패키지의 묶음을 메타 패키지(metapackage)라하여 따로 분리한다.
여기서 제일 중요한 것은 실제 실행 프로그램인 노드인데 앞서 이야기한 것과 마찬가지로ROS에서는 최소한의 실행 단위로 프로그램을 나누어 프로 그
래밍하기 때문에 노 드는 각각 별개의 프로그램이라고 이해하면 된다. 이에 수많은 노드들이 연동되는ROS 시스템을 위해서는 노드와 노드 사이에 입력
과출력 데이터를 서로 주고받게 설계해야만한다.
여기서 주고 받는 데이터를ROS에서는 메시지(message)라고 하고 주고받는 방식을 메시지 통신이라고 한다. 여기서 데이터에 해당되는 메시지
(message)는integer, floating point, boolean, string 와 같은 변수 형태이며 메시지 안에 메시지를 품고 있는 간단한 데이터 구조 및 메시지들의 배열과
같은 구조도 사용할 수 있다. 그리고 메시지를 주고받는 통신 방법에 따라 토픽(topic), 서비스(service), 액션(action), 파라미터(parameter)로 구분된다.


![Image 40](../../assets/images/ros/basics/lesson-04/img_038_040.webp)


ROS 소개 및 활용
ROS에서 사용되는 메시지 통신 방법으로는 토픽(topic), 서비스(service), 액션(action), 파라미터(parameter)가 있다. 각 메시지 통신 방법의
목적과 사용 방법은 다르기는하지만 토픽의 발간(publish)과구독(subscribe)의 개념을 응용하고 있다. 이 데이터를 보내고 받는 발간, 구독 개
념은ROS 1은물론ROS 2에서도 매우 중요한 개념으로 변함이 없는 데 이 기술에 사용된 통신 라이브러리는ROS 1, 2에서 조금씩 다르다.
ROS 1에서는 자체 개발한TCPROS와 같은 통신 라이브러리를 사용하고 있던 반면, ROS 2에서는OMG(Object Management Group)에 의해 표
준화된DDS(Data Distribution Service)의 리얼 타임 퍼 블 리 시와 서브 스 크 라이브 프로토콜인DDSI-RTPS(Real Time Publish Subscribe)를사
용하고 있다. ROS 2 개발 초기에는 기존TCPROS를 개선하거나ZeroMQ, Protocol Buffers 및Zeroconf 등을 이용하여 미들 웨어처럼 사용하는
방법도 제안되었으나 무엇보다 산업용 시장을 위해 표준 방식 사용을 중요하게 여겼고, ROS 1때와 같이 자체적으로 만들기보다는 산업용 표
준을 만들고 생태계를 꾸려 가고 있었던DDS를 통신 미들 웨어로써 사용하기로 하였다. DDS 도입에 따라 다음 그림과 같이ROS의 레이아웃은
크게 바뀌게 되었다. 처음에는DDS 채용에 따른 장점과 단점에 대한 팽팽한 줄다리기 토론으로 걱정의 목소리도 높였지만 지금에 와서는ROS
2에서의DDS 도입은 상업적인 용도로ROS를 사용할 수 있게 발판을 만들었다는 것에 가장 큰 역할을 했다는 평가가 지배적이다.


![Image 41](../../assets/images/ros/basics/lesson-04/img_039_041.webp)


ROS 소개 및 활용
DDS 도입으로 기존 메시지 형태 이외에도OMG의CORBA 시절부터 사용되던IDL(Interface Description Language, )를 사용하여 메시
지정의 및 직렬화를 더 쉽게, 더 포괄적으로 다룰 수 있게 되었다. 또한DDS의 중요 컨셉인DCPS(data-centric publish-subscribe),
DLRL(data local reconstruction layer)의 내용을 담아 재정한 통신 프로토콜로 인DDSI-RTPS을 채용하여 실시간 데이터 전송을 보장하
고임베디드 시스템에도 사용할 수 있게 되었다. DDS의사용으로 노드 간의 동적 검색 기능을 지원하고 있어서 기존ROS 1에서각노
드들의 정보를 관리하였던ROS Master가없어도 여러DDS 프로그램 간에 통신할 수 있다. 또한 노드 간의 데이터 통신을 세부적으로
조정하는QoS(Quality of Service)를 매개 변수 형태로 설정할 수 있어서TCP처럼 데이터 손실을 방지함으로써 신뢰도를 높이거나, UDP
처럼 통신 속도를 최우선시하여 사용할 수도 있다. 그리고 산업용으로 사용되는 미들 웨어인 만큼DDS-Security 도입으로 보안 측면에서
도 큰 혜택을 얻을 수 있었다. 이러한 다양한 기능을 갖춘DDS를 이용하여ROS 1의퍼블리시, 서브스크 라이브형 메시지 전달은 물론,
실시간 데이터 전송, 불안정한 네트워크에 대한 대응, 보안 등이 강화되었다. DDS의 채용은ROS 1에서ROS 2로 바뀌면서 가장 큰 변
화점이자 다음 그림과 같이 개발자 및 사용자로 하여금 통신 미들 웨어에 대한 개발 및 이용 부담을 줄여 진짜로 집중해야할 부분에 더
많은 시간을 쏟을 수 있게 되었다.
[출처] ROS 2 Update (ROSCon2016)


![Image 42](../../assets/images/ros/basics/lesson-04/img_040_042.webp)


ROS 소개 및 활용
자~ 이제 본격적으로DDS에 대해 알아보자. 처음DDS를ROS 2에 도입하자는 이야기가 나왔을 때, DDS라는 단어 자체를 처음
들어 봤기에 너무 어려웠다. 결론부터 말하자면DDS는 데이터 분산 시스템이라는 용어로OMG에서 표준을 정하고자 만든 트레이드
마크(TM)였다. 그냥 용어이고 그 실체는 데이터 통신을 위한 미들 웨어이다.
DDS가ROS 2의미들 웨어로 사용하는 만큼 그 자체에 대해 너무 자세히 알 필요는 없을 듯 싶고ROS 프로그래밍에 필요한 개념만 알고
넘어가면 될 듯 싶다. 우선 정의부터 알아보자. DDS는Data Distribution Service, 즉 데이터 분산 서비스의 약자이다.
DDS는 데이터 분산 시스템이라는 개념을 나타내는 단어이고 실제로는 데이터를 중심으로 연결성을 갖는 미들 웨어의 프로토콜(DDSI-
RTPS)과같은DDS 사양을 만족하는 미들 웨어API가 그 실체이다. 이 미들 웨어는ISO 7 계층 레이어에서 호스트 계층(Host layers)에
해당되는4~7 계층에 해당되고ROS 2에서는 위에서 언급한 다음 그림과 같이 운영 체제와 사용자 애플리케이션 사이에 있는
소프트웨어 계층으로 이를 통해 시스템의 다양한 구성 요소를 보다 쉽게 통신하고 데이터를 공유할 수 있게 된다.


![Image 43](../../assets/images/ros/basics/lesson-04/img_041_043.webp)


ROS 소개 및 활용
DDS의 특징은 다양하겠지만DDS를ROS 2의미들 웨어로 사용해 보면서 느낀 장점은 아래와 같이10가지이다. 여기서는 이10
가지에 대해 하나씩 정리해 보고 각 기능들은 이어지는 강좌에서 실습을 통해 더 자세히 알아보자.
1.
Industry Standards
2.
OS Independent
3.
Language Independent
4.
Transport on UDP/IP
5.
Data Centricity
6.
Dynamic Discovery
7.
Scalable Architecture
8.
Interoperability
9.
Quality of Service (QoS)

10. Security


![Image 44](../../assets/images/ros/basics/lesson-04/img_042_044.webp)


ROS 소개 및 활용

1. 산업 표준
DDS는 분산 객체에 대한 기술 표준을 제정하기 위해1989년에 설립된 비영리 단체인OMG(Object Management Group, 객체 관리 그룹)가관
리하고 있는 만큼 산업 표준으로 자리 잡고 있다. 지금까지OMG가 진행하여ISO 승인된 표준으로는UML, SysML, CORBA 등이 있다. 2001년
에 시작된DDS 표준화 작업도 잘 진행되어 지금에 와서는OpenFMB, Adaptive AUTOSAR, MD PnP, GVA, NGVA, ROS 2와 같은 시스템들에서
DDS를 사용하며 산업 표준의 기반이 되고 있다. ROS 1에서의TCPROS는 독자적인 미들 웨어라는 성격이 짙었는데ROS 2에 와서는DDS 사용
으로 더 넓은 범위로 사용 가능하게 되었으며 산업 표준을 지키고 있는 만큼 로봇 운영 체제ROS가IoT, 자동차, 국방, 항공, 우주 분야로 넓혀 갈
수 있는 발판이 마련되었다고 생각한다.

2. 운영 체제 독립
DDS는Linux, Windows, macOS, Android, VxWorks 등 다양한 운영 체제를 지원하고 있기에 사용자가 사용하던 운영 체제를 변경할 필요가
없다. 멀티 운영 체제 지원을 컨셉으로 하고 있는ROS 2에도 매우 적합하다고 볼 수 있다.


ROS 소개 및 활용

3. 언어 독립
DDS는 미들 웨어이기에 그 상위 레벨이라고 볼 수 있는 사용자 코드 레벨에서는DDS 사용
을 위해 기존에 사용하던 프로그래밍 언어를 바꿀 필요가 없다. ROS 2에서도 이 특징을 충
분히 살려하기 그림과 같이DDS를RMW(ROS middleware)으로 디자인되었으며 벤더별
로각RMW가제작되었으며, 그 위에 사용자 코드를 위해rclcpp, rclc, rclpy, rcljava,
rclobjc, rclada, rclgo, rclnodejs 같이 다양한 언어를 지원하는ROS 클라이언트 라이브러
리(ROS Client Library)를 제작하여 멀티 프로그래밍 언어를 지원하고 있다.

4. UDP 기반의 전송 방식
DDS 벤더별로DDS Interoperability Wire Protocol (DDSI-RTPS)의 구현 방식에 따라 상이할 수 있으나 일반적으로UDP 기반의 신뢰성
있는 멀티 캐스트(reliable multicast)를 구현하여 시스템이 최신 네트워킹 인프라의 이점을 효율적으로 활용할 수 있도록 돕고 있다. UDP
기반이라는 것이ROS 1에서의TCPROS가TCP 기반이었던 것에 비해 매우 큰 변화인데UDP의 멀티 캐스트(multicast)는 브로드 캐스트
(broadcast)처럼 여러 목적지로 동시에 데이터를 보낼 수 있지만, 불특정 목적지가 아닌 특정된 도메인 그룹에 대해서만 데이터를 전송하게
된다. 참고로ROS 2에서는`ROS_DOMAIN_ID`라는 환경 변수로 도메인을 설정하게 된다. 이 멀티 캐스트의 방식 도입으로ROS 2에서는 전
역 공간이라 불리는DDS Global Space이라는 공간에 있는 토픽들에 대해 구독 및 발행을 할 수 있게 된다. Best effort 개념인UDP는
reliable을 보장하는TCP에 비해 장단점이 있는데 이 또한 후에 설명하는QoS(Quality of Service)를 통해 보완 및 해결되었다.
​* 참고로 일부RMW 기능에는TCP 기반으로 구현되는 경우도 있다.


![Image 45](../../assets/images/ros/basics/lesson-04/img_044_045.webp)


ROS 소개 및 활용

5. 데이터 중심적 기능
다양한 미들 웨어가 있겠지만 그 중DDS를 사용하면서 제일 많이 듣는 말 중에 하나는`Data Centric`이라는 것이다. 우리말로는데 이
터 중심적이라는 것인데 실제로DDS를 사용하다 보면 이 말이 이해가 된다. DDS 사양에도DCPS(data-centric publish-subscribe)이
라는 개념이 나오는데 이는 적절한 수신자에게 적절한 정보를 효율적으로 전달하는 것을 목표로 하는 발간 및 구독 방식이라는 것이
다. DDS의미들 웨어를 사용자 입장에서 본다면 어떤 데이터인지, 이 데이터가 어떤 형식인지, 이 데이터를 어떻게 보낼 것인지, 이
데이터를 어떻게 안전하게 보낼 것인지에 대한 기능이DDS 미들 웨어에 녹여 있기 때문이다.


![Image 46](../../assets/images/ros/basics/lesson-04/img_045_046.webp)


ROS 소개 및 활용

6. 동적 검색
DDS는 동적 검색(Dynamic Discovery)을 제공한다. 즉, 응용 프로그램은DDS의 동적 검색을 통하여 어떤 토픽이 지정 도메인 영역에 있으며어
떤노드가이를 발신하고 수신하는지 알 수 있게 된다. 이는ROS 프로그래밍할 때 데이터를 주고받을 노드들의IP 주소 및 포트를 미리 입력하 거
나 따로 구성하지 않아도 되며 사용하는 시스템 아키텍처의 차이점을 고려할 필요가 없기 때문에 모든 운영 체제 또는 하드웨어 플랫폼에서 매
우 쉽게 작업할 수 있다.
ROS 1에서는ROS Master에서ROS 시스템의 노드들의 이름 지정 및 등록 서비스를 제공하였고, 각 노드에서 퍼 블 리 시 또는 서브 스 크 라이브 하는
메시지를 찾아서 연결할 수 있도록 정보를 제공해 주었다. 즉, 각각 독립되어 실행되는 노드들의 정보를 관리하여 서로 연결해야하는 노드들에
게 상대방 노드의 정보를 건네 주어 연결할 수 있게해 주는 매우 중요한 중매 역할을 수행했었다. 이 때문에ROS 1에서는 노드 사이의 연결을 위
해 네임 서비스를 마스터에서 실행했었어야했고, 이ROS Master가 연결이 끊기거나 죽는 경우 모든 시스템이 마비되는 단점이 있었다.
ROS 2에서는ROS Master가 없어지고DDS의 동적 검색 기능을 사용함에 따라 노드를DDS의Participant 개념으로 취급하게 되었으며, 동적
검색 기능을 이용하여DDS 미들 웨어를 통해 직접 검색하여 노드를 연결할 수 있게 되었다.

7. 확장 가능한 아키텍처
OMG의DDS 아키텍처는IoT 디바이스와 같은 소형 디바이스부터 인프라, 국방, 항공, 우주 산업과 같은 초대형 시스템으로까지 확장할 수 있도
록 설계되었다. 그렇다고 사용하기 복잡한 것도 아니다. DDS의Participant 형태의 노드는 확장 가능한 형태로 제공되어 사용할 수 있으며 단일
표준 통신 계층에서 많은 복잡성을 흡수하여 분산 시스템 개발을 더욱 단순화시켜 편의성을 높였다.
특히ROS와 같이 최소 실행 가능한 노드 단위로 나누어 수백, 수천 개의 노드를 관리해야하는 시스템에서는 이 부분이 강점으로 보이며 한 대의
로봇이 아닌 복수의 로봇, 주변 인프라와 다양한IT 기술, 데이터베이스, 클라우드로 연결 및 확장해야하는ROS 시스템에 매우 적합한 기능이다.


ROS 소개 및 활용

8. 상호 운용성
ROS 2에서 통신 미들 웨어로 사용하고 있는DDS는 상호 운용성을 지원하고 있다. 즉, DDS의 표준 사양을 지키고 있는 벤더 제품을
사용한다면A라는 회사의 제품을 사용하였다가도B라는 회사 제품으로 변경이 가능하고, A 제품과B 제품을 혼용하여 서로 다른
제품의DDS 제품을 사용하더라도A 제품과B 제품 간의 상호 통신도 지원한다는 것이다. 현재DDS 벤더로는10 곳이 있는데 이 중
ROS 2를 지원하는 업체는ADLink, Eclipse Foundation, Eprosima, Gurum Network, RTI로총5 곳이며DDS 제품명으로는Eclipse
Foundation의Cyclone DDS, Eprosima의Fast DDS, Gurum Network의Gurum DDS, RTI의Connext DDS가 있다. 이 중Fast DDS
와Cyclone DDS는 오픈 소스를 지향하고 있기에 자유롭게 사용 가능하며 기술 지원을 개별적으로 받기 원한다면 상용 제품인
Connext DDS, Gurum DDS를 사용하면 된다.


![Image 47](../../assets/images/ros/basics/lesson-04/img_047_047.webp)


ROS 소개 및 활용

10. 보안
ROS 1의 가장 큰 구멍이었던 보안 부분은ROS 2 개발에서DDS으로 해결되었다. DDS의사 양에는DDS-Security이라는DDS 보안 사양을
ROS에 적용하여 보안에 대한 이슈를 통신 단부터 해결하였다. 또한ROS 커뮤니티에서는SROS 2(Secure Robot Operating System 2)라는
툴을 개발하였고 보안 관련RCL 서포트 및 보안 관련 프로그래밍에 익숙지 않은 로보 틱 스 개발자를 위해 보안을 위한 툴 킷 을 만들어 배포하
고 있다. 이 부분에 대한 설명도 추후 이어지는 강좌에서 실습을 통해 더 자세히 알아보기로 하자.
$ ros2 run demo_nodes_cpp listener
[INFO]: I heard: [Hello World: 1]
[INFO]: I heard: [Hello World: 2]
[INFO]: I heard: [Hello World: 3]
[INFO]: I heard: [Hello World: 4]
[INFO]: I heard: [Hello World: 5]
$ ros2 run demo_nodes_cpp talker
[INFO]: Publishing: 'Hello World: 1'
[INFO]: Publishing: 'Hello World: 2'
[INFO]: Publishing: 'Hello World: 3'
[INFO]: Publishing: 'Hello World: 4'
[INFO]: Publishing: 'Hello World: 5'
$ rqt_graph
DDS 사용 예시


![Image 48](../../assets/images/ros/basics/lesson-04/img_048_048.webp)


ROS2 실습
rViz : ROS시각화 도구
rqt_graph : ROS 노드 간 데이터 통신 구조 블럭도
GAZEBO : 로봇 시뮬레이터
로봇 기구학 역 기구학 계산 및 모션 플래닝 프레임워크
ROS2 도구


![Image 49](../../assets/images/ros/basics/lesson-04/img_049_049.webp)


![Image 50](../../assets/images/ros/basics/lesson-04/img_049_050.webp)


![Image 51](../../assets/images/ros/basics/lesson-04/img_049_051.webp)


![Image 52](../../assets/images/ros/basics/lesson-04/img_049_052.webp)


로봇의 기술적 측면에서 로봇의3가지 중요한 기능
인식
센서 정보 수집
인터페이스로
광범위한 정보 활용
분석
정확도 향상
지능 향상
동작
정밀도 고도화
R2X간
상호 운용성 중심
ROS2 - 노드와 메시지 통신
노드(node)는 아래 그림처럼Node A, Node B, Node C라는 노드가 있을 때 각각의 노드들은 서로 유기적으로
Message로 연결되어 사용된다. 지금은 단순히3개의 노드만 표시하였지만 수행하고자하는 태스크가 많아질수록
메시지로 연결되는 노드가 늘어나며 시스템이 확장할 수 있게 된다.
Node


![Image 55](../../assets/images/ros/basics/lesson-04/img_051_055.webp)


ROS2 - 노드와 메시지 통신
토픽(topic)은 아래 그림의`Node A - Node B`, `Node A - Node C`처럼 비동기식 단방향 메시지 송수신 방식으로msg
메시지 형태의 메시지를 발간하는Publisher와 메시지를 구독하는Subscriber 간의 통신이라고 볼 수 있다. 이는1:N, N:1,
N:N 통신도 가능하며ROS 메시지 통신에서 가장 널리 사용되는 통신 방법이다.
Topic


![Image 56](../../assets/images/ros/basics/lesson-04/img_052_056.webp)


ROS2 - 노드와 메시지 통신
서비스(Service)는 아래 그림의`Node B - Node C`처럼 동기식 양방향 메시지 송수신 방식으로 서비스의
요청(Request)을 하는 쪽을Service client라고 하며 서비스의 응답(Response)을 하는 쪽을Service server라고 한다.
결국 서비스는 특정 요청을 하는 클라이언트 단과 요청 받은 일을 수행 후에 결과 값을 전달하는 서버 단과의 통신이라고
볼 수 있다. 서비스 요청 및 응답(Request/Response) 또한 위에서 언급한msg 메시지의 변형으로srv 메시지라고 한다.
Service


![Image 57](../../assets/images/ros/basics/lesson-04/img_053_057.webp)


ROS2 - 노드와 메시지 통신
액션(Action)은 아래 그림의`Node A - Node B`처럼 비동기식+동기식 양방향 메시지 송수신 방식으로 액션 목표Goal를
지정하는Action client과액션 목표를 받아 특정 태스크를 수행하면서 중간 결과 값에 해당되는 액션
피드백(Feedback)과 최종 결과 값에 해당되는 액션 결과(Result)를 전송하는Action server 간의 통신이라고 볼 수 있다.
Action


![Image 58](../../assets/images/ros/basics/lesson-04/img_054_058.webp)


ROS2 - 노드와 메시지 통신
액션의 구현 방식을 더 자세히 살펴보면 아래 그림과 같이 토픽(topic)과 서비스(service)의 혼합이라고 볼 수 있는데 액션
목표 및 액션 결과를 전달하는 방식은 서비스와 같으며 액션 피드백은 토픽과 같은 메시지 전송 방식이다.
액션 목표/피드백/결과(Goal/Feedback/Result) 메시지 또한 위에서 언급한msg 메시지의 변형으로action 메시지라고 한다.
Action


![Image 59](../../assets/images/ros/basics/lesson-04/img_055_059.webp)


ROS2 - 노드와 메시지 통신
파라미터(Parameter)는 아래 그림의 각 노드에 파라미터 관련Parameter server를 실행시켜 외부의Parameter client
간의 통신으로 파라미터를 변경하는 것으로 서비스와 동일하다고 볼 수 있다. 단노드내 매개 변수 또는 글로벌
매개변수를 서비스 메시지 통신 방법을 사용하여 노드 내부 또는 외부에서 쉽게 지정(Set) 하거나 변경할 수 있고, 쉽게
가져(Get)와서 사용할 수 있게하는 점에서 목적이 다르다고 볼 수 있다.
Parameter


![Image 60](../../assets/images/ros/basics/lesson-04/img_056_060.webp)


ROS2 - 노드와 메시지 통신
지금까지 강좌에서 다루었던 토픽, 서비스, 액션은ROS의 중요 컨셉이자 앞으로 강좌에서 다룰ROS 프로그래밍에 있어서 매우 중요한 부분이기에 다시
한번 비교를 해 보도록하겠다. 여기서 비교한 연속성, 방향성, 동기성, 다자간 연결, 노드 역할, 동작 트리거, 인터페이스를 각 토픽, 서비스, 액션의 서로 다른
특징이라고 볼 수 있고 노드 간의 데이터 전송에 있어서 특성에 맞게 선택하여ROS 프로그래밍을 하게 된다.
토픽(topic)​
서비스(service)
액션(action)
연속성
연속성
일회성
복합(토픽+서비스)
방향성
단방향
양방향
양방향
동기성
비동기
동기
동기+ 비동기
다자 간 연결
1:1, 1:N, N:1, N:N
(publisher:subscriber)
1:1
(server:client)
1:1
(server:client)
노드 역할
발행자(publisher)
구독자(subscriber)
서버(server)
클라 언 트(client)
서버(server)
클라 언 트(client)
동작 트리거
발행자
클라 언 트
클라 언 트
인터페이스
msg 인터페이스
srv 인터페이스
action 인터페이스
CLI 명령어
ros2 topic
ros2 interface
ros2 service
ros2 interface
ros2 action
ros2 interface
사용예
센서 데이터, 로봇 상태,
로봇 좌표, 로봇 속도 명령 등
LED 제어, 모터 토크On/Off,
IK/FK 계산, 이동 경로 계산 등
목적지로 이동,
물건 파지, 복합 태스크 등


ROS2 패키지 설명
Node 노드 메시지를 주고받는 객체의 단위,
ROS에서 가장 기본이 되는 단위


![Image 61](../../assets/images/ros/basics/lesson-04/img_058_061.webp)


ROS2 패키지 설명
CMakeLists.txt : 빌 드 설정 파일입니다.
혹시나VSCODE가아닌VS STUDIO에서 개발을 해 본 경험자라면 빌 드 옵션을 설정하는 파일입니다.
*빌 드에 대한 것은2차시 강의 자료 참고


![Image 62](../../assets/images/ros/basics/lesson-04/img_059_062.webp)


ROS2 패키지 설명


![Image 63](../../assets/images/ros/basics/lesson-04/img_060_063.webp)


ROS2 패키지 설명
폴더 경로 생성1차시의우분투CLI 참고
*터미널에 입력하는 명령어입니다.


![Image 64](../../assets/images/ros/basics/lesson-04/img_061_064.webp)


ROS2 패키지 설명
*터미널에 입력하는 명령어입니다.
빌 드 후 빌 드한 파일을 실행(클릭해서 실행하는 것이 아니다)


![Image 65](../../assets/images/ros/basics/lesson-04/img_062_065.webp)


ROS2 패키지 설명
*터미널에 입력하는 명령어입니다.


![Image 66](../../assets/images/ros/basics/lesson-04/img_063_066.webp)


ROS2 Alias 설정
*터미널에 입력하는 명령어입니다.


![Image 67](../../assets/images/ros/basics/lesson-04/img_064_067.webp)


ROS2 Turtlesim


![Image 68](../../assets/images/ros/basics/lesson-04/img_065_068.webp)


인터페이스(토픽) 리스트 보기


![Image 69](../../assets/images/ros/basics/lesson-04/img_066_069.webp)


![Image 70](../../assets/images/ros/basics/lesson-04/img_066_070.webp)


인터페이스(서비스) 리스트 보기


![Image 71](../../assets/images/ros/basics/lesson-04/img_067_071.webp)


ROS2 실습


![Image 72](../../assets/images/ros/basics/lesson-04/img_068_072.webp)


![Image 73](../../assets/images/ros/basics/lesson-04/img_068_073.webp)


ROS2 실습- turtlesim 1단계
Turtlesim 실행후node 확인


![Image 74](../../assets/images/ros/basics/lesson-04/img_069_074.webp)


ROS2 실습

- turtlesim_node
- turtle_teleop_key
- 프로그램 위치 확인


![Image 78](../../assets/images/ros/basics/lesson-04/img_070_078.webp)


![Image 79](../../assets/images/ros/basics/lesson-04/img_070_079.webp)


ROS2 실습


![Image 80](../../assets/images/ros/basics/lesson-04/img_071_080.webp)


![Image 81](../../assets/images/ros/basics/lesson-04/img_071_081.webp)


![Image 82](../../assets/images/ros/basics/lesson-04/img_071_082.webp)


![Image 83](../../assets/images/ros/basics/lesson-04/img_071_083.webp)


ROS2 실습
multisim.launch.py 파일 위치


![Image 84](../../assets/images/ros/basics/lesson-04/img_072_084.webp)


![Image 85](../../assets/images/ros/basics/lesson-04/img_072_085.webp)


ROS2 실습
Turtle 2개 동시 이동


![Image 86](../../assets/images/ros/basics/lesson-04/img_073_086.webp)


![Image 87](../../assets/images/ros/basics/lesson-04/img_073_087.webp)


![Image 88](../../assets/images/ros/basics/lesson-04/img_073_088.webp)


![Image 89](../../assets/images/ros/basics/lesson-04/img_073_089.webp)


ROS2 실습
Service/spawn 선택
Name에turtle1 입력→ call 버튼 클릭
Name에turtle2 입력→ call 버튼 클릭
Name에turtle3 입력→ call 버튼 클릭
Teleop_key실행해서turtle1 or turtle2 or turtle3 입력후turtle 제어


![Image 90](../../assets/images/ros/basics/lesson-04/img_074_090.webp)


![Image 91](../../assets/images/ros/basics/lesson-04/img_074_091.webp)


![Image 92](../../assets/images/ros/basics/lesson-04/img_074_092.webp)


![Image 93](../../assets/images/ros/basics/lesson-04/img_074_093.webp)


ROS2 실습- Topic
$ros2 run turtlesim turtlesim_node
$ ros2 topic list
topic list 확인
/cmd_vel
/color_sensor
/pose


![Image 94](../../assets/images/ros/basics/lesson-04/img_075_094.webp)


ROS2 실습
topic중 pose의 데이터type 확인
/turtle1/pose    [turtlesim/msg/Pose]
topic이름
데이터type


![Image 95](../../assets/images/ros/basics/lesson-04/img_076_095.webp)


ROS2 실습
$ros2 topic info /turtle1/pose
$ros2 topic list -v
Publisher count : 1
Subscriber count : 0
Ready to listen
Now publishing


![Image 96](../../assets/images/ros/basics/lesson-04/img_077_096.webp)


ROS2 실습
$ros2 interface show turtlesim/msg/Pose
$ros2 topic echo /turtle1/pose


![Image 97](../../assets/images/ros/basics/lesson-04/img_078_097.webp)


ROS2 실습
5개 데이터가Echo 출력됨


![Image 98](../../assets/images/ros/basics/lesson-04/img_079_098.webp)


ROS2 실습
$rqt_graph
Terminal로 메시지가 송신되고 있음
Termina
l


![Image 99](../../assets/images/ros/basics/lesson-04/img_080_099.webp)


ROS2 실습
Terminal
Turtlesim
1단계
1개
(Default Namespace)
1개
(Default Namespace)
2단계
1개
(Namespace 지정)
1개
(Namespace 지정)
3단계
1개
2개
4단계
2개
1개씩
5단계
2개
2개씩


ROS2 실습- turtlesim 1단계
Turtlesim 실행후node 확인


![Image 100](../../assets/images/ros/basics/lesson-04/img_082_100.webp)

ROS2 실습
ROKEY
GO!


![Image 106](../../assets/images/ros/basics/lesson-04/img_083_106.webp)


ROS2 실습- turtlesim
Turtlesim 실행후node 확인

![Image 107](../../assets/images/ros/basics/lesson-04/img_084_107.webp)


![Image 108](../../assets/images/ros/basics/lesson-04/img_084_108.webp)


![Image 109](../../assets/images/ros/basics/lesson-04/img_084_109.webp)


![Image 110](../../assets/images/ros/basics/lesson-04/img_084_110.webp)


![Image 111](../../assets/images/ros/basics/lesson-04/img_084_111.webp)


![Image 115](../../assets/images/ros/basics/lesson-04/img_084_115.webp)


ROS2 실습
Turtlesim 실행후node 확인
Namespace 설정(p101)

![Image 116](../../assets/images/ros/basics/lesson-04/img_085_116.webp)


![Image 117](../../assets/images/ros/basics/lesson-04/img_085_117.webp)


![Image 118](../../assets/images/ros/basics/lesson-04/img_085_118.webp)


![Image 119](../../assets/images/ros/basics/lesson-04/img_085_119.webp)


![Image 120](../../assets/images/ros/basics/lesson-04/img_085_120.webp)

ROS2 실습
Turtlesim 실행후node 확인
Namespace + Node 이름 설정

![Image 125](../../assets/images/ros/basics/lesson-04/img_086_125.webp)


![Image 126](../../assets/images/ros/basics/lesson-04/img_086_126.webp)


![Image 127](../../assets/images/ros/basics/lesson-04/img_086_127.webp)

ROS2 실습
Turtlesim 실행후node 확인
Namespace + Node 이름 설정

![Image 130](../../assets/images/ros/basics/lesson-04/img_087_130.webp)


![Image 131](../../assets/images/ros/basics/lesson-04/img_087_131.webp)


![Image 132](../../assets/images/ros/basics/lesson-04/img_087_132.webp)

ROS2 실습

![Image 135](../../assets/images/ros/basics/lesson-04/img_088_135.webp)


![Image 136](../../assets/images/ros/basics/lesson-04/img_088_136.webp)

![Image 139](../../assets/images/ros/basics/lesson-04/img_088_139.webp)


![Image 140](../../assets/images/ros/basics/lesson-04/img_088_140.webp)


![Image 141](../../assets/images/ros/basics/lesson-04/img_088_141.webp)

ROS2 실습

![Image 144](../../assets/images/ros/basics/lesson-04/img_089_144.webp)

![Image 146](../../assets/images/ros/basics/lesson-04/img_089_146.webp)

ROS2 실습
Namespace와Name 설정

![Image 149](../../assets/images/ros/basics/lesson-04/img_090_149.webp)


![Image 150](../../assets/images/ros/basics/lesson-04/img_090_150.webp)

![Image 153](../../assets/images/ros/basics/lesson-04/img_090_153.webp)


![Image 154](../../assets/images/ros/basics/lesson-04/img_090_154.webp)


![Image 155](../../assets/images/ros/basics/lesson-04/img_090_155.webp)

ROS2 실습


![Image 158](../../assets/images/ros/basics/lesson-04/img_091_158.webp)

ROS2 실습


![Image 161](../../assets/images/ros/basics/lesson-04/img_092_161.webp)


![Image 162](../../assets/images/ros/basics/lesson-04/img_092_162.webp)


ROS2 실습
노트북2대로Turtlesim와teleop_key 실행해서 각각의 노트북에서turtlesim 동작 확인


![Image 163](../../assets/images/ros/basics/lesson-04/img_093_163.webp)


수고하셨습니다.

