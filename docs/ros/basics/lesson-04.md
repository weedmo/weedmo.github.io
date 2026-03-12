# 강의_3기_ROS2_기초_4차시


ROS2 기초-4차시
훈련일정
오전
오후
1차시

- 로봇의역사
- 컴퓨터구조(Booting, CPU 작동원리, POST)
- 리눅스와운영체계
- 리눅스CLI 실습(디렉토리, 계정, 기본명령어등), Terminator, 커널, 쉘, gedit, bash
- Application 작동원리(마이크로프로세서, 메모리, 저장장치)
- 리눅스 CLI 실습
2차시

- 리눅스 CLI 실습
- 네트워크와통신(IPV4, IPV6, 소켓, 노드, Hub, TCP, UDP)
- API, Library, Framework, 프로세스와Thread
- 인터프리터, 컴파일러(소스코드→ Build → 실행파일)
- 소켓프로그래밍실습
- OSI7 Layer, 프로토콜(RS-232C, RS-485, Ethernet, TCP/UDP, IP)
3차시

- 센서 기초, IoT와Embedded
- 로봇기초, 좌표계
- 로봇센서활용및로봇의 구성(기계기구, 전기전자, 소프트웨어)
- ROS2 소개및활용
- ROS2 설치(ros.org) 및demo_node
4차시

- ROS2 소개및활용
- ROS2 실습(Talker, Listener)
- ROS2 패키지설명
- ROS2 실습(Turtlesim, teleop_key)
5차시

- ROS2 실습(Turtlesim, Teleop_key 여러개만들기)
- Topic, Service, Action, Parameter, RQT, RQT_Graph 이론및실습
- ROS2 실습(Turtlesim, Namespace 여러개만들기)
- Ros bag and play 실습, my first package build 실습
- Turtlesim subscribing 실습, ROS의 중요한개발도구(Rviz, GAZEBO 소개)


ROS2 turtlesim 복습
$ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist “{linear:{x: 2.0, y: 0.0, z: 0.0},
angular:{x: 0.0, y: 0.0, z: 0.0}}”
이동
Turtle 다시 생성해보기

ROS2 turtlesim 복습
$ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist “{linear:{x: 2.0, y: 0.0, z: 0.0},
angular:{x: 0.0, y: 0.0, z: 1.8}}”
이동


![Image 7](../../assets/images/ros/basics/lesson-04/img_004_007.webp)


ROS2 turtlesim 복습
$ros2 topic pub --rate 1 /turtle1/cmd_vel geometry_msgs/msg/Twist “{linear:{x: 0.0, y: 0.0, z: 0.0},
angular:{x: 0.0, y: 0.0, z: 1.8}}”
제자리회전
$ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist “{linear:{x: 0.0, y: 0.0, z: 0.0},
angular:{x: 0.0, y: 0.0, z: 1.8}}”
※ Tip : ctrl + 화살표눌러서cli 빠른이동

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
ROS 소개및활용
●
OS

- Ubuntu 22.04 (Jammy Jellyfish)
●
ROS

- ROS 2 Humble
●
에디터

- Visual Studio Code, gedit
●
설치매뉴얼

- ROS 2 Installation (Humble)
●
환경설정및간단튜토리얼

- ROS 2 Configuring environment
- ROS 2 Turtlesim Tutorial

ROS 소개및활용
메타운영체계
ROS는메타운영체제로, 메타운영체제란애플리케이션과분산컴퓨팅
자원간의가상화레이어로분산컴퓨팅자원을활용하여, 스케줄링,로드,
감시, 에러처리등을실행하는시스템이다.
ROS 소개및활용

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
- LTS, supported until May, 2025
ROS 2 Jazzy Jalisco
[출처] https://github.com/ros-infrastructure/artwork/tree/master/distributions

![Image 18](../../assets/images/ros/basics/lesson-04/img_011_018.webp)


![Image 19](../../assets/images/ros/basics/lesson-04/img_011_019.webp)


![Image 20](../../assets/images/ros/basics/lesson-04/img_011_020.webp)

![Image 22](../../assets/images/ros/basics/lesson-04/img_011_022.webp)


![Image 23](../../assets/images/ros/basics/lesson-04/img_011_023.webp)

![Image 26](../../assets/images/ros/basics/lesson-04/img_011_026.webp)

ROS
ROS란무엇인가?
ROS는로봇을위한오픈소스메타운영체제
메타운영체제란기존의운영체제위에로봇개발에필요한기능을추가한것을말합니다.
ROS는로봇의하드웨어추상화, 프로세스간통신, 패키지관리등로봇개발에필요한다양한기능을제공합니다.
Open Source
모듈구조
확장성
ROS는기존의윈도우나리눅스같은운영체계가아니며, 기존운영체계에추가적인설치를동반하는미들웨어이다.
ROS의데이터통신은서로다른운영체제, 하드웨어시스템에서도데이터를주고받을수있기때문에로봇개발에적합하다.
ROS와Linux를사용하는이유
1.
운영체계라이선스
2.
개발시간단축
3.
편리한디버깅도구및시각화도구
4.
많은사용자및생태계


![Image 36](../../assets/images/ros/basics/lesson-04/img_013_036.webp)


ROS2 실습
ROS 구성요소
구성요소
설명
마스터

- 노드와노드사이연결및메시지통신의네임서버역할
- Roscore로실행이되며, URI 주소는기본적으로는현재의로컬IP 사용
노드

- ROS에서실행되는최소단위의프로세스를말함
- ROS에서는하나의목적에하나의노드작성을권장함
- 노드가구동될때, 노드의역할(토리그서비스등), 메시지형태등이등록됨
패키지

- ROS를구성하는기본단위
- ROS 응용프로그램은패키지단위로개발되며최소한하나의노드를가짐
메시지

- 노드와노드는서로메시지를통해서데이터를주고받음
- 메시지는integer, float, Boolean 등의변수형태임
- 메시지 안에메시지를품는데이터구조가가능
- 단방향은토픽(topic), 양방향은서비스(service)
토픽

- 토픽은ROS의노드사이의데이터통신의한종류
- 단방향통신으로, 데이터를메시지에담아서방송을함
- 방송을하는퍼블리셔(publisher)와수신을하는서브스크라이버(subscriber)로 구성됨


ROS 소개및활용
ROS1
ROS2
단일로봇
복수대의로봇
실시간제어지원하지않음
실시간제어
안정된네트워크환경요구
불안정한네트워크환경에서도동작할수있는유연함
단일플랫폼(Linux)
멀티플랫폼(Linux, Windows, MacOS)
-
최신기술지원(Zeroconf, Protocon Buffers, ZeroMQ, WedSockets, DDS등)
주로대학이나연구소등의아카데믹연구용도
상업용제품지원


ROS 소개및활용
앞시간에서임베디드와역할을잘분배해야한다는설명이있었습니다.

ROS 소개및활용
(1) 글로벌커뮤니티
ROS 커뮤니티는10년이상ROS 프로젝트는소프트웨어에기여하고개선하는수십만명의개발자와사용자로구성된글로벌커뮤니티를
육성함으로써로봇공학을위한방대한소프트웨어에코시스템을만들어왔다. ROS 2는커뮤니티를위해, 커뮤니티에의해개발되었다.
(2) 검증된사용사례
ROS는로봇산업전반에걸쳐사용되고있다. 로봇공학교육을위한표준이다. 단일프로젝트부터여러기관의협업및대규모경연대회에
이르기까지대부분의로봇공학연구의기반이되었다. 그리고오늘날전세계에서생산중인로봇의내부에도이기술이적용되고있다. 자율
이동로봇(AMR)에서만ROS는수십억달러의가치를창출하는데기여했다.
(3) 시장출시시간단축
ROS는로봇응용프로그램을개발하는데필요한도구, 라이브러리및기능을제공하므로본연의중요한로봇개발작업에더많은시간을
할애할수있다는것이가장큰장점이다. 특정로봇개발을위해처음부터프레임워크를만들고통신방법을선정하고디버깅툴과시각화툴을
다시만드는비효율적인방법에서벗어날수있게한다. 더불어ROS는상용소프트웨어가아닌ROS 커뮤니티에서개발해오고있는
오픈소스이기때문에ROS를사용할부분과사용방법을유연하게결정할수있을뿐만아니라필요에따라자유롭게수정할수있다.
(4) 다중도메인
ROS는실내에서실외, 가정에서자동차, 수중에서우주, 소비자에서산업에이르기까지다양한로봇공학애플리케이션에서사용할수있다.
(5) 멀티플랫폼
ROS 2는Linux, Windows, macOS에서개발, 지원, 테스트진행하고있기에자율성, 백엔드관리및사용자인터페이스의원활한개발및
배포가가능하다. 계층형지원모델을사용하고있기에실시간운영체제(Real-time OS) 및임베디드OS(Embedded OS)와같은새로운
플랫폼으로의포팅에대한관심과투자를통해도입및홍보도할수있다.


ROS 소개및활용
(6) 100% 오픈소스
ROS 2 코드는Apache 2.0 라이센스를기본라이센스로사용하여지적재산권에영향을주지않으면서자유재량으로넓은범위로사용가능하다.
(7) 상업친화성
사용자커뮤니티의ROS에대한오픈소스기여를진심으로권장하지만, 이를요구하지는않는다. 오픈소스라이선스에따라ROS를배포하며, Apache
2.0이기본라이선스이다. ROS를수정하고, 자신또는다른사람의비공개소프트웨어와혼합하고, 그결과물을여러분의독점제품에배포할수있으며,
그사실을알릴필요도없다. 물론항상사용자들이ROS를어떻게사용하고있는지알고싶기에커뮤니티에이를알려주길바란다.
(8) 업계지원
ROS 2 기술운영위원회(ROS 2 Technical Steering Committee)의멤버쉽에서알수있듯이ROS 2에대한업계지원은강력하다. 전세계의크고작은
회사는제품을개발할뿐만아니라ROS 2에오픈소스기여를하기위해자원을투입하고있다.

- ROS Package Documentation
- Robotics Stack Exchange
- ROS Discourse Forums
- Open Robotics Discord Server
- ROS Index
- Issue Trackers


ROS 소개및활용
로봇문제에대한솔루션을제공하는ROS
이름과는달리ROS는사실운영체제가아니다. 그보다는로봇애플리케이션을구축하는데필요한빌딩블록을제공하는
SDK(소프트웨어개발키트)이다.
수업프로젝트, 과학실험, 연구프로토타입, 최종제품등어떤애플리케이션이든ROS를사용하면목표를더빨리달성할수있다.
그리고, 모두오픈소스이다.

ROS 소개및활용
1) Plumbing
ROS의핵심은흔히"미들웨어" 또는"배관"이라고불리는메시지전달시스템을제공한다. 커뮤니케이션은새로운로봇애플리케이션이나하드웨어와
상호작용하는모든소프트웨어시스템을구현할때가장먼저해결해야할문제중하나이다. ROS에내장되어있고충분한테스트를거친메시징
시스템은퍼블리시/서브스크라이브패턴을통해분산노드간의통신세부사항을관리함으로써시간을절약해준다. 이러한접근방식은결함격리,
우려사항분리, 명확한인터페이스등소프트웨어개발의어려운부분들을해결할수있게돕는다. ROS를사용하면유지관리, 기여, 재사용이더쉬운
시스템을만들수있다.
그과정에서방대한커뮤니티경험을활용하여표준ROS 메시지형식을만들수있으며, 이러한표준은LIDAR 및카메라부터현지화알고리즘및
사용자인터페이스에이르기까지모든것과상호작용하는데사용된다.
2) Tools
로봇애플리케이션을구축하는일은쉽지않다. 센서와액추에이터를통해물리적세계와비동기적으로상호작용해야한다는점과소프트웨어개발의
모든어려움이결합되어있다. 애플리케이션을효율적으로구축하려면우수한개발자도구가필요하다. ROS에는실행, 상태, 디버깅, 시각화, 플로팅,
로깅, 재생등다양한개발도구가포함되어있다. 이러한도구는개발팀의진행속도를높여주며, 제품출시시함께제공될수있다.


ROS 소개및활용
3) Capabilities
ROS 에코시스템은로봇소프트웨어의보고이다. GPS용디바이스드라이버, 4족보행로봇을위한보행및균형컨트롤러, 모바일로봇을위한매핑
시스템등어떤것이필요하든ROS는여러분을위한모든것을제공하고있다. 드라이버부터알고리즘, 사용자인터페이스에이르기까지ROS는
애플리케이션에집중할수있는빌딩블록을제공한다.
ROS 프로젝트의목표는당연하게여겨지는것에대한기준을지속적으로높여로봇애플리케이션구축에대한진입장벽을낮추는것이다. 유용
하거나재미있고흥미로운로봇에대한좋은아이디어가있는사람이라면누구나기본하드웨어와소프트웨어에대한모든것을이해하지않고도
그아이디어를현실화할수있어야한다.
4) Community
ROS 커뮤니티는규모가크고다양하며글로벌하다. 학생과취미활동가부터다국적기업, 정부기관에이르기까지다양한사람과조직이ROS
프로젝트를계속이어가고있다.
이프로젝트의커뮤니티허브이자중립적인관리자는이웹사이트와같은공유온라인서비스를호스팅하고, 사용자가설치하는바이너리
패키지를포함한배포릴리스를생성및관리하며, ROS 내대부분의핵심소프트웨어를개발및유지관리하는Open Robotics이다. 오픈
로보틱스는ROS와관련된엔지니어링서비스도제공하고있다.


ROS 소개및활용
ROS 1은2007년에개발이시작되어지금은대학, 연구기관, 산업계, 로봇자작의취미활동까지폭넓게이용되고있다. 원래ROS 1은
Willow Garage사가개인서비스로봇인PR2개발에필요한미들웨어형태의로봇개발프레임워크를다양한개발툴과함께오픈소스로
공개한것으로시작하였다. 따라서개발환경으로는PR2의초기컨셉을그대로이어받아다음과같은제한사항이있었다.

- 단일로봇
- 워크스테이션급컴퓨터
- Linux 환경
- 실시간제어지원하지않음
- 안정된네트워크환경이요구됨
- 주로대학이나연구소와같은아카데믹연구용도
ROS1과ROS2의차이점


ROS 소개및활용


![Image 39](../../assets/images/ros/basics/lesson-04/img_023_039.webp)


ROS 소개및활용
오늘날요구되는로봇개발환경과는큰차이가있다. 예를들어, 최근의ROS 1은종래가장많이이용되고있던학술분야뿐만아니라, 제조로봇, 농업로봇,
드론, 소셜로봇과같은상용로봇등으로이용되고있다. 극단적인예로NASA가국제우주정거장에서사용한Robonaut에는ROS 1가채용되고있지만,
거기에서는실시간제어가요구되었고이를위해서ROS 1을수정하여사용하였다. 이러한새로운로봇개발환경및요구되는기능을정리하면다음과같다.

- 복수대의로봇
- 임베디드시스템에서의ROS 사용
- 실시간제어
- 불안정한네트워크환경에서도동작할수있는유연함
- 멀티플랫폼(Linux, Windows, macOS)
- 최신기술지원(Zeroconf, Protocol Buffers, ZeroMQ, WebSockets, DDS 등)
- 상업용제품지원
ROS 1에서이러한새롭게요구되는기능을제공하려면대규모API의변경이필요하다. 그러나기존의ROS 1과의호환성을유지하면서수많은새로운
기능을추가하는것은쉽지않았다. 또한, 기존의ROS 1을문제없이이용하고있는사용자에게는큰API의변경은바람직하지않다.
그래서ROS의차세대기능을도입한버전을ROS 2라고, ROS 1에서분리하여개발하게된것이다. 기존의ROS 1 사용자는필요하다면그대로ROS 1을
이용할수있다. 한편, 새로운기능이필요한사용자는ROS 2를선택하면된다. 또한, ROS 1과ROS 2 사이에서서로메시지통신이가능한브리지프로그램
(ros1_bridge) 제공되므로두버전모두를함께사용하는것도가능하다.


ROS 소개및활용

1. Platforms
ROS 2부터는3대운영체제인Linux, Windows, macOS를모두지원한다. 이는바이너리파일로설치가가능하다는의미로Windows
사용자가많은한국의경우에는반가운소식으로받아들이는분들이많을것같다. ROS 2 Jazzy Jalisco 기준으로보았을때Linux는Ubuntu
Noble (24.04), Windows는Windows 10 버전, macOS는Mojave (10.14)버전을지원하고있다.
Linux의경우에는Linux 배포판중일반사용자가가장많은Canonical의Ubuntu 진영에서ROS 2 TSC로가입되어있어서관련된내용을
많이볼수있다. 리눅스이용자라면Canonical에서연재중인아래참고자료Ubuntu Robotics, Ubuntu Robotics Blogs의내용을참고하면
ROS 2 사용에도움이될듯싶다. 그리고Linux, macOS는ROS 1 부터지원하고있었는데이번ROS 2에서는Microsoft가ROS 2 TSC로
들어오고Windows용패키지및테스트, Visual Studio Code Extension for ROS 까지준비하는등굉장한노력을기울여Windows
사용자들도ROS 2를쉽게사용할수있게되었다. Windows 사용자라면Win ROS Landing Page, WSL 2(Windows Subsystem For Linux 2)의
Windows 관련문서를참고하기를추천한다.

2. Real-time
ROS 2는Real-time을지원한다. 단, 선별된하드웨어사용, 리얼타임운영체제사용, DDS의RTPS(Real-time Publish-Subscribe Protocol)와
같은통신프로토콜을사용, 매우잘짜여진리얼타임코드사용을전제로실시간성을지원하고있다. 이부분은ROSCon2019의Pre-
conference Workshops으로진행되었던`Doing real-time with ROS 2: Capabilities and challenges`에서자세히설명되었는데이부분의
내용은이강좌에서설명하기에는내용이많아상당히길어질것같으므로추후해당내용및더자세히알아보려면해당워크샵의페이지를
참고하도록하자.


ROS 소개및활용

3. Security
ROS 1에서는항상보안이문제였다. 노드를관리하는ROS master의하나의IP와포트만노출되면모든시스템을죽일수있었으
며, 보안입장에서는TCPROS는뻥뚫린큰구멍에가까웠다. 하지만ROS 1은이러한부족한부분을매우기보다는로봇개발에
사용되는다양한하드웨어와소프트웨어를평가하고작동하는유연성에더무게를두었고이러한유연성은보안에대한기회비
용보다더중요하게여겼다. 즉, 보안이슈는개발우선순위에서뒤져있었다. 당연히ROS 초창기에는이선택은옳았다.
하지만시간이흘러이러한취약점은상용로봇에ROS를도입할수없게만드는첫번째이유이자가장큰걸림돌이되었다. 이에
ROS 2에서는디자인설계부터이부분을명확히짚고넘어갔다. 우선, TCP 기반의통신은OMG(Object Management Group)에
서산업용으로사용중인DDS(Data Distribution Service)를도입하였고, 자연스럽게DDS-Security 이라는DDS 보안사양을
ROS에적용하여보안에대한이슈를통신단부터해결하였다. 또한ROS 커뮤니티에서는SROS 2(Secure Robot Operating
System 2)라는툴을개발하였고보안관련RCL 서포트및보안관련프로그래밍에익숙지않은로보틱스개발자를위해보안을
위한툴킷을만들어배포하고있다. 이부분에대한더자세한내용은ROS 2 디자인문서(DDS-Security integration, Access
Control Policies, Security Enclaves, Robotic Systems Threat Model)의`Security` 관련부분을참고하길바라며지난ROSCon에서
의워크샵에서진행한`Is your robot secure? ROS 1 & ROS 2 Security Workshop`의문서도참고하면도움이될것같다. 우리는
추후강좌를통해직접보안설정및프로그램하는실습을진행해보기로하자.


ROS 소개및활용

4. Communication
ROS 1에서는자체개발한TCPROS와같은통신라이브러리를사용하고있던반면, ROS 2은리얼타임퍼블리시와서브스크라이브
프로토콜인RTPS(Real Time Publish Subscribe)를지원하는통신미들웨어DDS를사용하고있다. DDS는OMG(Object Management
Group)에의해표준화가진행되고있으며, 상업적인용도에도적합하다는평가가지배적이다. DDS에서는IDL(Interface Description
Language)를사용하여메시지정의및직렬화를더쉽게, 더포괄적으로다룰수있다. 또한통신프로토콜로는RTPS을채용하여실시간
데이터전송을보장하고임베디드시스템에도사용할수있다. DDS는노드간의자동감지기능을지원하고있어서기존ROS 1에서각
노드들의정보를관리하였던ROS마스터가없어도여러DDS 프로그램간에통신할수있다. 또한노드간의통신을조정하는QoS(Quality
of Service) 매개변수를설정할수있어서TCP 처럼데이터손실을방지함으로써신뢰도를높이거나, UDP 처럼통신속도를최우선하여
사용할수도있다. 이러한다양한기능을갖춘DDS를이용하여ROS 1의퍼블리시, 서브스크라이브형메세지전달은물론, 실시간데이터
전송, 불안정한네트워크에대한대응, 보안강화등이강화되었다. DDS의채용은ROS 1에서ROS 2로바뀌면서가장큰변화점이다.

5. Middleware interface
앞서설명한DDS는다양한기업에서통신미들웨어형태로제공하고있다. 그벤더로는10 곳이있는데이중ROS 2를지원하는업체는
ADLink, Eclipse Foundation, Eprosima, Gurum Network, RTI로총5 곳이다. DDS 제품명으로는Eclipse Foundation의Cyclone DDS,
Eprosima의Fast DDS, Gurum Network의Gurum DDS, RTI의Connext DDS가있다. 참고로이중Gurum Network는유일하게대한민국
기업으로DDS를순수국산기술로개발하여상용화에성공한기업이다.
ROS 2에서는이러한벤더들의미들웨어를유저가원하는사용목적에맞게선택하여사용할수있도록ROS Middleware(RMW)형태로
지원하고있다. 이는각벤더들의미들웨어마다API가약간씩달라도ROS 2 유저들은이를생각하지않고통일된코드로쉽게바꿔서사용할
수있도록것으로, RMW는여러DDS 구현을지원하기위하여API의추상화인터페이스로지원하고있다.


ROS 소개및활용

6. Node manager (discovery)
ROS 1에서의필수실행프로그램으로는roscore가있다. 이를실행시키면ROS Master, ROS Parameter Server, rosout logging node가실행되었다.
특히ROS Master는ROS 시스템의노드들의이름지정및등록서비스를제공하였고, 각노드에서퍼블리시또는서브스크라이브하는메시지를찾아서
연결할수있도록정보를제공해주었다. 즉, 각각독립되어실행되는노드들의정보를관리하여서로연결해야하는노드들에게상대방노드의정보를
건네주어연결할수있게해주는매우중요한중매역할을수행했었다. 이때문에ROS 1에서는노드사이의연결을위해네임서비스를마스터에서
실행했었어야했고, 이ROS Master가연결이끓기거나죽는경우모든시스템이마비되는단점이있었다.
ROS 2에서는roscore가없어지고3가지프로그램이각각독립수행으로바뀌었다. 특히, ROS Master의경우완전히삭제되었는데이는DDS를
사용함에따라노드를DDS의Participant개념으로취급하게되었으며, Dynamic Discovery기능을이용하여DDS 미들웨어를통해직접검색하여
노드를연결할수있게되었다. 이제ROS 2에서는roscore는Bye~ Bye~ 다.

7. Languages
ROS 2의프로그램언어로는ROS 1과마찬가지로다양한프로그래밍언어를지원할예정이다. 아직까지는C++, Python이주력언어라고볼수있는데
이주력언어도아래와같이큰변화가있었다. ROS 2 배포판마다조금씩다르기는하지만Jazzy를기준으로보았을때, C++은C++17, 파이썬은
Python 3.8이기본요구사항으로되어있다. 이다. 같은언어를쓰더라도ROS 1을사용했을때에는뭔가올드한느낌이었고최신언어들이제공하는
기능들을못쓰고그림에떡이였는데이제는최신의아름다운언어를쓰는기분이다. 이는사용해보면알게될것이다. 물론새로운걸배운다는것은
어쩔수없는엔지니어의숙명이다.

- ROS 1: C++03, Python 2.7
- ROS 2: C++17, Python 3.8


ROS 소개및활용

8. Build system
ROS 2에서는새로운빌드시스템인ament를사용한다. ament는ROS 1에서사용되는빌드시스템인catkin의업그레이드버전이다. ROS 1의
catkin이CMake만을지원했던반면, ament는CMake를사용하지않는Python 패키지관리도가능하다. 즉, ROS 2에와서는Python 패키지는
비로서처음으로완전독립을이루게되었는데ROS 1에서Python 코드가있는패키지는setup.py 파일이CMake 내에서사용자정의
로직으로처리되었다. 하지만ROS 2에서Python 패키지는setup.py 파일의모든기능을순수Python 모듈과동등한수준으로개발할수있게
되었다. 마지막으로TMI일수있으나catkin과ament는이음동의어로버드나무의화수를의미하며ROS 1의개발주체인Willow Garage 뒷
마당에있던버드나무화수를보고지었다고한다. 즉, 뭔가심오한뜻이있는것은아니다.

- ROS 1: rosbuild → catkin (CMake)
- ROS 2: ament (CMake), Python setuptools (Full support)

9. Build tools
ROS 1의경우여러가지다른도구, 즉catkin_make, catkin_make_isolated 및catkin_tools가지원되었다. ROS 2에서는알파, 베타, 그리고
Ardent 릴리스까지빌드도구로ament_tools이이용되었고지금에와서는colcon을추천하고있다.
colcon은ROS 2 패키지를작성, 테스트, 빌드등ROS 2 기반의프로그램할때빼놓을수없는툴로작업흐름을향상시키는CLI 타입의명령어
도구이다. 사용방법은`colcon test`와`colcon build` 와같이터미널창에서수행하게되며다양한옵션을사용할수있다. 이는추후이어지는
강좌들에서더자세히다루도록하겠다.


ROS 소개및활용

10. Build options
ROS 2에서는빌드관련내용들이모두변경되면서빌드옵션에도새로운변화가생겼다. 그중사용하면서가장좋았던3가지를꼽자면
아래와같다.
우선`Multiple workspace` 이다.
이는ROS 1에서는`catkin_ws`와같이특정워크스페이스를확보하고하나의워크스페이스에서모든작업을다했는데ROS 2에서는복수의
독립된워크스페이스를사용할수있어서작업목적및패키지종류별로관리할수있게되었다.
둘째는`No non-isolated build` 이다.
ROS 1에서는하나의CMake 파일로여러개의패키지를동시에빌드할수있었다. 이렇게하면빌드속도가빨라지지만모든패키지의
종속성에신경을많이써야하고빌드순서가매우중요하게된다. 또한모든패키지가동일네임스페이스사용하게되므로이름에서충돌이
발생할수있었다. ROS 2에서는이전빌드시스템인catkin에서일부기능으로사용되었던`catkin_make_isolated` 형태와같은격리빌드만을
지원함으로써모든패키지를별도로빌드하게되었다. 이기능변화를통해설치용폴더를분리하거나병합할수있게되었다.
셋째는`No devel space`이다.
catkin은패키지를빌드한후devel 이라는폴더에코드를저장한다. 이폴더는패키지를설치할필요없이패키지를사용할수있는환경을
제공한다. 이를통해파일복사를피하면서사용자는파이썬코드를편집하고즉시코드실행할수있었다. 단이러한기능은매우편리한
기능이지만패키지를관리하는측면에서복잡성을크게증가시켰다.
이에ROS 2에서는패키지를빌드한후설치해야패키지를사용할수있도록바뀌었다. 단쉬운사용성도고려하여colcon 사용시에`colcon
build --symlink-install` 와같은옵션을사용하여심벌릭링크설치의선택적기능을사용하여동일한이점을제공하고있다.


ROS 소개및활용

11. Version control system
ROS는수많은소스코드공여자로부터만들어가는코드의집합이기때문에개인은물론소속도정말다양하고각코드들의리포지토리도제각각이다.
예를들어어느패키지는GitHub를이용하고어떤것은Bitbucket를이용한다. 그리고사용하는버전관리시스템(Version Control System, VCS)도Git,
Mercurial, Subversion, Bazaar 등다양하다.

- ROS 1: rosws → wstool, rosinstall (*.rosinstall)
- ROS 2: vcstool (*.repos)
ROS 커뮤니티에서는이러한다양한리포지토리와혼재된버전관리시스템을사용하더라도ROS를사용함에있어서불편함이없도록통합적인툴이
필요했다. ROS 1에서는처음에rosws이라는툴에서wstool을이용하였다가최근ROS 2에서는vcstool으로통합하였다.
현재ROS 1에서도vcstool를사용하고있는상황이다. vcstool은여러리포지토리작업을보다쉽게관리할수있도록설계된버전관리시스템(VCS) 툴이다.
이툴은ROS 2를소스코드로부터설치해본사람이라면자신도모르게사용했을것이다. 아래의명령어2줄을살펴보자. 우선wget을통하여
ros2.repos라는파일을받게되는데이파일에는vcs 타입은무었이고, 리포지토리주소는어떻게되며, 설치해야하는브랜치는어떤것인지가명시된
파일이다. 이러한정보가기재된*.repos 파일을이용하여다양한리포지토리, 다양한vcs를지원하며패키지들을관리할수있도록하는것을의미한다.
특히ROS 2에서는기존vcs 툴을통폐합하여vcstool 이라는이름으로제공되어사용에매우편리하게되었다. 자세한사용법은README 파일을
참고하도록하자.
wget https://raw.githubusercontent.com/ros2/ros2/humble/ros2.repos
vcs import src < ros2.repos


ROS 소개및활용

12. Client library
ROS 기반의프로그래밍을작성한다는것은ROS Middleware Interface에서유저코드영역(user land)을다룬다는것으로그밑에는ROS 클라이언트라이브러리
(ROS Client Library)이있고, 이클라이언트라이브러리는앞서설명한미들웨어(middleware interface)를사용하고있다는것을알고있어야한다. 여기서유저는
개발목적에따라C/C++, Python, Java, Node.js 등을사용할것이다. ROS 에서는초창기부터이러한멀티프로그래밍언어를지원하고있는데ROS 1에서는
roscpp, rospy, roslisp 등각프로그래밍언어에대해클라이언트라이브러리(Client Library)를제공했다. 한편, ROS 2에서는ROS 클라이언트라이브러리를
RCL(ROS Client Library)이라는이름으로제공한다. 그리고프로그래밍언어별로rclcpp, rclc, rclpy, rcljava, rclobjc, rclada, rclgo, rclnodejs 등으로제공된다.
또한ROS 2는앞서설명한바와같이C이면C99, C++ 이라면C++ 14/17, Python라면Python 3 (3.5+) 등최신기술사양에대응하고있다. 각C++/Python ROS
Client Library API는rclcpp, rclpy을미리봐둔다면도움일될것이다.

13. Life cycle
로봇개발에있어서로봇의현재상태를파악하고현재상태에서다른상태로변경되는상태천이제어는수십년간로봇공학에서도주요연구주제로다루었던중
요한부분중에하나이다. 특히태스크수행측면에서현재의상태파악과천이는멀티태스크수행에서빠질수없는중요한부분일것이고복수의로봇복수의
복합태스크, 서비스수행과같은상위레벨의프로그램일수록더중요하게다루어지는부분이다. ROS 1에서는이러한기능을구현하기위해서는SMACH과같은
상태천이를관리하는독립적인패키지를사용했어야했고클라이언트라이브러리에서는상태관리하는부분이없었기에사용자가임의로클라이언트라이브러
리부분까지수정하여사용했어야했다.
ROS 2에서는이러한니즈를반영하여패키지의각노드들의현재상태를모니터링하고상태를제어가능한lifecycle을클라이언트라이브러리에포함시켰으며
이를통해ROS 시스템상태를보다효과적으로제어할수있게되었다. 이를이용하게되면기존ROS 1에서는할수없었던노드의상태를모니터링하고상태를
천이시키거나노드를상태에따라재시작하거나교체할수도있게된다.


ROS 소개및활용

14. Multiple nodes
ROS 1의초기에는하나의프로세스에서여러노드를실행할수없었다. 하지만이러한요구는지속적으로제기되었고하나의프로세스에서여러노드를작
성하기위해nodelet라는새로운기능이ROS 1에추가되었다. 이는하드웨어리소스가제한적이거나노드간에수많은메시지를보내야할때유용하게사
용되었다.
ROS 2에서nodelet이사용되지는않고RCL에포함되어있다. 이름은컴포넌트(components)라고부르며ROS 2에서는이컴포넌트를사용하여동일한실행
파일에서복수의노드를수행할수있게되었다. 이를사용하게되면노드의실행파일수준은더세분화시킬수있으며프로세스내통신IPC(intra-
process communication)기능을이용하여ROS 2의통신오버헤드를제거할수있어서더효율적인ROS 2 응용프로그램을작성가능하다.

15. Threading model
ROS 1에서개발자는단일스레드실행또는다중스레드실행중하나만선택할수있었다. ROS 2에서는더세분화된실행모델(executor)을C++과
Python에서사용할수있으며사용자가정의한실행기도제공되는RCL API를이용하여쉽게구현할수있다. Single Threaded Executor, Multi Threaded
Executor는각클라이언트라이브러리마다구현방식이다르기에관련설명은rclcpp executors, rclpy executors 문서를참고하도록하자.


ROS 소개및활용

16. Messages (topic, service, action)
ROS 2에서도기존ROS 1의메시지(Messages)과마찬가지로단일데이터구조를메시지라고정의하며정해진또는사용자가정의한메시지를사용할수있으며,
각패키지이름과마찬가지로이름과각지정된형식으로메시지를고유하게식별할수있다. 사용처도기존과마찬가지로Topic, Service, Action 등에서사용하며
기존과비슷한형태(Interface definition, interface file)로사용가능하다.
여기에ROS 2에서는OMG(Object Management Group)에서정의된IDL(Interface Description Language)을사용하여메시지정의및직렬화를더쉽게, 더포괄적
으로다룰수있게되었다. IDL을이용하게되면기존ROS 메시지컨셉과마찬가지로다양한프로그래밍언어로작성된메시지를사용할수있다. 이전에CORBA
(일명, 코바)를써본사람들은IDL이친숙할것이다. ROS 2에서는기존msg, srv, action 파일이외에도IDL을지원한다. 그리고ROS 2가DDS를채용하게되면서
기존메시지들과DDS 규칙을맞추는작업이진행되었다. ROS 인터페이스유형과DDS IDL 유형간의맵핑은Mapping between ROS interface types and DDS
IDL types 자료를참고하면좋을듯싶으며전체적으로다듬어진정리표는Interfaces 글을참고하도록하자.
그리고, ROS 2에서는DDS를사용하면서메시지를이용한Topic, Service, Action 등의컨셉은변하지않으나사용방법은상당히많이바뀌었다. 이부분에대한설
명은이어지는강좌를통해예제와함께하나하나알아가보자.

17. Command Line Interface
대부분의CLI 타입의명령어사용법은기존ROS 1과매우비슷해서약간의이름변경과일부옵션사용법만익힌다면사용시큰차이는없다. 자주사용되는명령
어를예를들어보자면아래와같은차이정도이다. ROS 1 명령어에비해명령어가약간길어진듯보이긴하지만자주쓰는명령어는"alias rt='ros2 topic list'"와
같이설정하여사용하면되기에큰무리는없다. 더욱이ROS 2의CLI 형태의명령어는ROS 2 TSC 멤버이자Ubuntu 개발업체인Canonical이담당하고있어서더
욱믿음이간다. 자세한설명은ROS 2 Command Line Interface 를참고하기바라며실습을해보고싶다면발표자료를참고하면좋다.

- ROS 1: 'rostopic list'
- ROS 2: 'ros2 topic list'


ROS 소개및활용

18. roslaunch
ROS의실행시스템은대표적으로`run`과`launch`가있는데`run`은단일프로그램실행, `launch`는사용자지정프로그램실행을수행한다. 사용면에서
는`run`에비해다양한설정을할수있는`launch` 사용이월등히사용빈도가높다. `launch`는사용자가실행하고자하는프로그램의각종설정을기술
하고기술된설정에맞추어각종프로그램을실행하도록도와준다. 사용자가지정하는설정에는실행할프로그램, 실행할위치, 전달할인수등시스템
전체의구성요소를쉽게재사용할수있도록하고있다. 그목적과컨셉은ROS 2에서도크게다르지않다.
launch의ROS 1과ROS 2의차이점을살펴보면다양한파일사용이다. ROS 1에서는`roslaunch` 파일이특정`XML` 형식을사용해었다. 이형식을이용
해도다양한설정을추가하여프로그램을실행시킬수있어서매우편했는데, ROS 2에서는`XML`, `YAML` 형식이외에도`Python`이새롭게채용되어
조건문및Python 모듈을추가로사용하여보다복잡한논리와기능을사용할수있게되었다. 어떤방식으로사용하는지에대한추가설명은튜토리얼
을참고하도록하자.

19. Graph API
ROS는메타패키지, 패키지, 노드그리고노드간의데이터교환을위한토픽등으로구성되어있다. 이때의각노드와토픽, 메시지등이고유의이름을
가지고있고, 매핑이이루어져각노드와노드간의토픽, 메시지의관계를그래프화시킬수있도록되어있다. 이러한그래프구조를시각화하는툴인
rqt_graph를제공하고있어서현재네트워크상의각구성요소의연결성을시각적으로확인할수있다.


ROS 소개및활용

20. Embedded Systems
로봇개발에있어서실시간성을담보받으며모터및센싱을제어하는부분은매우중요하게다루어져왔다. 이강좌초반에서언급했듯이ROS 커뮤니티에서도
이를위해ROS 2에서는선별된하드웨어사용, 리얼타임운영체제사용, DDS의RTPS(Real-time Publish-Subscribe Protocol)와같은통신프로토콜을사용, 매우
잘짜여진리얼타임코드사용을전제로실시간성을지원하고있다. 하지만실시간성이라는것은상위소프트웨어에서다루기에는제약이많다. 오히려
Embedded Systems 안에서해결하는게더적합하다고보고있다.
이에ROS 2 개발초기부터Embedded Systems에대한관심이높았는데초기개발컨셉은ROS의창시자인Morgan Quigley가ROSCon2015에서`ROS 2 on
“small” embedded systems`이라는이름으로발표한자료및영상를보면도움이될것이다. ROS 1에서도Embedded Systems을지원하지않는것은아니였다.
단, 매우기초적인수단이라고볼수있는임베디드보드와메시지를주고받을때시리얼(rosserial)로통하여통신하였다. ROS 2에서는한발더나아가기존시리
얼통신, 블루투스및와이파이통신을지원하거나RTOS (Real-Time Operating System)를사용하고기존DDS 대신eXtremely Resource Constrained
Environments (DDS-XRCE)를사용하는등임베디드보드에서직접ROS 프로그래밍을하여하드웨어펌웨어로구현된노드를실행할수도있다. 이방법론에
는여러가지가있을수있는데현재ARM 사를포함한다양한MCU 제조업체에서이를지원하기위하여다양한방법론을내놓고있는상태이고, eProsima,
BOSCH, ROBOTIS, FIWARE, Amazon, Renesas 등에서다음참고자료와같이다양한임베디드지원방법에대해개발, 공개하고있다.
임베디드환경에서DDS 및ROS 메시지통신등에관심있는사람은아래참고자료를참고하도록하자.

- ROS 1: rosserial, mROS
- ROS 2: micro-ROS, XEL Network, ros2arduino, Renesas, DDS-XRCE(Micro-XRCE-DDS), AWS ARCLM
[참고자료]

- https://micro-ros.github.io/
- http://xelnetwork.robotis.com/
- https://github.com/ROBOTIS-GIT/ros2arduino
- https://www.renesas.com/us/en/solutions/key-technology/robot/robot-operating-system.html
- https://micro-xrce-dds.docs.eprosima.com/en/latest/


ROS 소개및활용
ROS2와DDS (Data Distribution Service)


ROS 소개및활용
로봇운영체제ROS에서중요시여기는몇가지용어정의및메시지, 메시지통신에대해먼저알아보도록하자. 특히, 메시지통신은ROS 프로그래밍에
있어서ROS 1과2의공통된중요한핵심개념이기에ROS 프로그래밍에들어가기전에꼭이해하고넘어가야할부분이다.
ROS에서는프로그램의재사용성을극대화하기위하여최소단위의실행가능한프로세스라고정의하는노드(node) 단위의프로그램을작성하게된다.
이는하나의실행가능한프로그램으로생각하면된다. 그리고하나이상의노드또는노드실행을위한정보등을묶어놓은것을패키지(package)라고
하며, 패키지의묶음을메타패키지(metapackage)라하여따로분리한다.
여기서제일중요한것은실제실행프로그램인노드인데앞서이야기한것과마찬가지로ROS에서는최소한의실행단위로프로그램을나누어프로그
래밍하기때문에노드는각각별개의프로그램이라고이해하면된다. 이에수많은노드들이연동되는ROS 시스템을위해서는노드와노드사이에입력
과출력데이터를서로주고받게설계해야만한다.
여기서주고받는데이터를ROS에서는메시지(message)라고하고주고받는방식을메시지통신이라고한다. 여기서데이터에해당되는메시지
(message)는integer, floating point, boolean, string 와같은변수형태이며메시지안에메시지를품고있는간단한데이터구조및메시지들의배열과
같은구조도사용할수있다. 그리고메시지를주고받는통신방법에따라토픽(topic), 서비스(service), 액션(action), 파라미터(parameter)로구분된다.


![Image 40](../../assets/images/ros/basics/lesson-04/img_038_040.webp)


ROS 소개및활용
ROS에서사용되는메시지통신방법으로는토픽(topic), 서비스(service), 액션(action), 파라미터(parameter)가있다. 각메시지통신방법의
목적과사용방법은다르기는하지만토픽의발간(publish)과구독(subscribe)의개념을응용하고있다. 이데이터를보내고받는발간, 구독개
념은ROS 1은물론ROS 2에서도매우중요한개념으로변함이없는데이기술에사용된통신라이브러리는ROS 1, 2에서조금씩다르다.
ROS 1에서는자체개발한TCPROS와같은통신라이브러리를사용하고있던반면, ROS 2에서는OMG(Object Management Group)에의해표
준화된DDS(Data Distribution Service)의리얼타임퍼블리시와서브스크라이브프로토콜인DDSI-RTPS(Real Time Publish Subscribe)를사
용하고있다. ROS 2 개발초기에는기존TCPROS를개선하거나ZeroMQ, Protocol Buffers 및Zeroconf 등을이용하여미들웨어처럼사용하는
방법도제안되었으나무엇보다산업용시장을위해표준방식사용을중요하게여겼고, ROS 1때와같이자체적으로만들기보다는산업용표
준을만들고생태계를꾸려가고있었던DDS를통신미들웨어로써사용하기로하였다. DDS 도입에따라다음그림과같이ROS의레이아웃은
크게바뀌게되었다. 처음에는DDS 채용에따른장점과단점에대한팽팽한줄다리기토론으로걱정의목소리도높였지만지금에와서는ROS
2에서의DDS 도입은상업적인용도로ROS를사용할수있게발판을만들었다는것에가장큰역할을했다는평가가지배적이다.


![Image 41](../../assets/images/ros/basics/lesson-04/img_039_041.webp)


ROS 소개및활용
DDS 도입으로기존메시지형태이외에도OMG의CORBA 시절부터사용되던IDL(Interface Description Language, )를사용하여메시
지정의및직렬화를더쉽게, 더포괄적으로다룰수있게되었다. 또한DDS의중요컨셉인DCPS(data-centric publish-subscribe),
DLRL(data local reconstruction layer)의내용을담아재정한통신프로토콜로인DDSI-RTPS을채용하여실시간데이터전송을보장하
고임베디드시스템에도사용할수있게되었다. DDS의사용으로노드간의동적검색기능을지원하고있어서기존ROS 1에서각노
드들의정보를관리하였던ROS Master가없어도여러DDS 프로그램간에통신할수있다. 또한노드간의데이터통신을세부적으로
조정하는QoS(Quality of Service)를매개변수형태로설정할수있어서TCP처럼데이터손실을방지함으로써신뢰도를높이거나, UDP
처럼통신속도를최우선시하여사용할수도있다. 그리고산업용으로사용되는미들웨어인만큼DDS-Security 도입으로보안측면에서
도큰혜택을얻을수있었다. 이러한다양한기능을갖춘DDS를이용하여ROS 1의퍼블리시, 서브스크라이브형메시지전달은물론,
실시간데이터전송, 불안정한네트워크에대한대응, 보안등이강화되었다. DDS의채용은ROS 1에서ROS 2로바뀌면서가장큰변
화점이자다음그림과같이개발자및사용자로하여금통신미들웨어에대한개발및이용부담을줄여진짜로집중해야할부분에더
많은시간을쏟을수있게되었다.
[출처]  ROS 2 Update (ROSCon2016)


![Image 42](../../assets/images/ros/basics/lesson-04/img_040_042.webp)


ROS 소개및활용
자~ 이제본격적으로DDS에대해알아보자. 처음DDS를ROS 2에도입하자는이야기가나왔을때, DDS라는단어자체를처음
들어봤기에너무어려웠다. 결론부터말하자면DDS는데이터분산시스템이라는용어로OMG에서표준을정하고자만든트레이드
마크(TM)였다. 그냥용어이고그실체는데이터통신을위한미들웨어이다.
DDS가ROS 2의미들웨어로사용하는만큼그자체에대해너무자세히알필요는없을듯싶고ROS 프로그래밍에필요한개념만알고
넘어가면될듯싶다. 우선정의부터알아보자. DDS는Data Distribution Service, 즉데이터분산서비스의약자이다.
DDS는데이터분산시스템이라는개념을나타내는단어이고실제로는데이터를중심으로연결성을갖는미들웨어의프로토콜(DDSI-
RTPS)과같은DDS 사양을만족하는미들웨어API가그실체이다. 이미들웨어는ISO 7 계층레이어에서호스트계층(Host layers)에
해당되는4~7 계층에해당되고ROS 2에서는위에서언급한다음그림과같이운영체제와사용자애플리케이션사이에있는
소프트웨어계층으로이를통해시스템의다양한구성요소를보다쉽게통신하고데이터를공유할수있게된다.


![Image 43](../../assets/images/ros/basics/lesson-04/img_041_043.webp)


ROS 소개및활용
DDS의특징은다양하겠지만DDS를ROS 2의미들웨어로사용해보면서느낀장점은아래와같이10가지이다. 여기서는이10
가지에대해하나씩정리해보고각기능들은이어지는강좌에서실습을통해더자세히알아보자.
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


ROS 소개및활용

1. 산업표준
DDS는분산객체에대한기술표준을제정하기위해1989년에설립된비영리단체인OMG(Object Management Group, 객체관리그룹)가관
리하고있는만큼산업표준으로자리잡고있다. 지금까지OMG가진행하여ISO 승인된표준으로는UML, SysML, CORBA 등이있다. 2001년
에시작된DDS 표준화작업도잘진행되어지금에와서는OpenFMB, Adaptive AUTOSAR, MD PnP, GVA, NGVA, ROS 2와같은시스템들에서
DDS를사용하며산업표준의기반이되고있다. ROS 1에서의TCPROS는독자적인미들웨어라는성격이짙었는데ROS 2에와서는DDS 사용
으로더넓은범위로사용가능하게되었으며산업표준을지키고있는만큼로봇운영체제ROS가IoT, 자동차, 국방, 항공, 우주분야로넓혀갈
수있는발판이마련되었다고생각한다.

2. 운영체제독립
DDS는Linux, Windows, macOS, Android, VxWorks 등다양한운영체제를지원하고있기에사용자가사용하던운영체제를변경할필요가
없다. 멀티운영체제지원을컨셉으로하고있는ROS 2에도매우적합하다고볼수있다.


ROS 소개및활용

3. 언어독립
DDS는미들웨어이기에그상위레벨이라고볼수있는사용자코드레벨에서는DDS 사용
을위해기존에사용하던프로그래밍언어를바꿀필요가없다. ROS 2에서도이특징을충
분히살려하기그림과같이DDS를RMW(ROS middleware)으로디자인되었으며벤더별
로각RMW가제작되었으며, 그위에사용자코드를위해rclcpp, rclc, rclpy, rcljava,
rclobjc, rclada, rclgo, rclnodejs 같이다양한언어를지원하는ROS 클라이언트라이브러
리(ROS Client Library)를제작하여멀티프로그래밍언어를지원하고있다.

4. UDP 기반의전송방식
DDS 벤더별로DDS Interoperability Wire Protocol (DDSI-RTPS)의구현방식에따라상이할수있으나일반적으로UDP 기반의신뢰성
있는멀티캐스트(reliable multicast)를구현하여시스템이최신네트워킹인프라의이점을효율적으로활용할수있도록돕고있다.  UDP
기반이라는것이ROS 1에서의TCPROS가TCP 기반이었던것에비해매우큰변화인데UDP의멀티캐스트(multicast)는브로드캐스트
(broadcast)처럼여러목적지로동시에데이터를보낼수있지만, 불특정목적지가아닌특정된도메인그룹에대해서만데이터를전송하게
된다. 참고로ROS 2에서는`ROS_DOMAIN_ID`라는환경변수로도메인을설정하게된다. 이멀티캐스트의방식도입으로ROS 2에서는전
역공간이라불리는DDS Global Space이라는공간에있는토픽들에대해구독및발행을할수있게된다. Best effort 개념인UDP는
reliable을보장하는TCP에비해장단점이있는데이또한후에설명하는QoS(Quality of Service)를통해보완및해결되었다.
​* 참고로일부RMW 기능에는TCP 기반으로구현되는경우도있다.


![Image 45](../../assets/images/ros/basics/lesson-04/img_044_045.webp)


ROS 소개및활용

5. 데이터중심적기능
다양한미들웨어가있겠지만그중DDS를사용하면서제일많이듣는말중에하나는`Data Centric`이라는것이다. 우리말로는데이
터중심적이라는것인데실제로DDS를사용하다보면이말이이해가된다. DDS 사양에도DCPS(data-centric publish-subscribe)이
라는개념이나오는데이는적절한수신자에게적절한정보를효율적으로전달하는것을목표로하는발간및구독방식이라는것이
다. DDS의미들웨어를사용자입장에서본다면어떤데이터인지, 이데이터가어떤형식인지, 이데이터를어떻게보낼것인지, 이
데이터를어떻게안전하게보낼것인지에대한기능이DDS 미들웨어에녹여있기때문이다.


![Image 46](../../assets/images/ros/basics/lesson-04/img_045_046.webp)


ROS 소개및활용

6. 동적검색
DDS는동적검색(Dynamic Discovery)을제공한다. 즉, 응용프로그램은DDS의동적검색을통하여어떤토픽이지정도메인영역에있으며어
떤노드가이를발신하고수신하는지알수있게된다. 이는ROS 프로그래밍할때데이터를주고받을노드들의IP 주소및포트를미리입력하거
나따로구성하지않아도되며사용하는시스템아키텍처의차이점을고려할필요가없기때문에모든운영체제또는하드웨어플랫폼에서매
우쉽게작업할수있다.
ROS 1에서는ROS Master에서ROS 시스템의노드들의이름지정및등록서비스를제공하였고, 각노드에서퍼블리시또는서브스크라이브하는
메시지를찾아서연결할수있도록정보를제공해주었다. 즉, 각각독립되어실행되는노드들의정보를관리하여서로연결해야하는노드들에
게상대방노드의정보를건네주어연결할수있게해주는매우중요한중매역할을수행했었다. 이때문에ROS 1에서는노드사이의연결을위
해네임서비스를마스터에서실행했었어야했고, 이ROS Master가연결이끊기거나죽는경우모든시스템이마비되는단점이있었다.
ROS 2에서는ROS Master가없어지고DDS의동적검색기능을사용함에따라노드를DDS의Participant 개념으로취급하게되었으며, 동적
검색기능을이용하여DDS 미들웨어를통해직접검색하여노드를연결할수있게되었다.

7. 확장가능한아키텍처
OMG의DDS 아키텍처는IoT 디바이스와같은소형디바이스부터인프라, 국방, 항공, 우주산업과같은초대형시스템으로까지확장할수있도
록설계되었다. 그렇다고사용하기복잡한것도아니다. DDS의Participant 형태의노드는확장가능한형태로제공되어사용할수있으며단일
표준통신계층에서많은복잡성을흡수하여분산시스템개발을더욱단순화시켜편의성을높였다.
특히ROS와같이최소실행가능한노드단위로나누어수백, 수천개의노드를관리해야하는시스템에서는이부분이강점으로보이며한대의
로봇이아닌복수의로봇, 주변인프라와다양한IT 기술, 데이터베이스, 클라우드로연결및확장해야하는ROS 시스템에매우적합한기능이다.


ROS 소개및활용

8. 상호운용성
ROS 2에서통신미들웨어로사용하고있는DDS는상호운용성을지원하고있다. 즉, DDS의표준사양을지키고있는벤더제품을
사용한다면A라는회사의제품을사용하였다가도B라는회사제품으로변경이가능하고, A 제품과B 제품을혼용하여서로다른
제품의DDS 제품을사용하더라도A 제품과B 제품간의상호통신도지원한다는것이다. 현재DDS 벤더로는10 곳이있는데이중
ROS 2를지원하는업체는ADLink, Eclipse Foundation, Eprosima, Gurum Network, RTI로총5 곳이며DDS 제품명으로는Eclipse
Foundation의Cyclone DDS, Eprosima의Fast DDS, Gurum Network의Gurum DDS, RTI의Connext DDS가있다. 이중Fast DDS
와Cyclone DDS는오픈소스를지향하고있기에자유롭게사용가능하며기술지원을개별적으로받기원한다면상용제품인
Connext DDS, Gurum DDS를사용하면된다.


![Image 47](../../assets/images/ros/basics/lesson-04/img_047_047.webp)


ROS 소개및활용

10. 보안
ROS 1의가장큰구멍이었던보안부분은ROS 2 개발에서DDS으로해결되었다. DDS의사양에는DDS-Security이라는DDS 보안사양을
ROS에적용하여보안에대한이슈를통신단부터해결하였다. 또한ROS 커뮤니티에서는SROS 2(Secure Robot Operating System 2)라는
툴을개발하였고보안관련RCL 서포트및보안관련프로그래밍에익숙지않은로보틱스개발자를위해보안을위한툴킷을만들어배포하
고있다. 이부분에대한설명도추후이어지는강좌에서실습을통해더자세히알아보기로하자.
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
DDS 사용예시


![Image 48](../../assets/images/ros/basics/lesson-04/img_048_048.webp)


ROS2 실습
rViz : ROS시각화도구
rqt_graph : ROS 노드간데이터통신구조블럭도
GAZEBO : 로봇 시뮬레이터
로봇 기구학 역기구학계산및모션플래닝프레임워크
ROS2 도구


![Image 49](../../assets/images/ros/basics/lesson-04/img_049_049.webp)


![Image 50](../../assets/images/ros/basics/lesson-04/img_049_050.webp)


![Image 51](../../assets/images/ros/basics/lesson-04/img_049_051.webp)


![Image 52](../../assets/images/ros/basics/lesson-04/img_049_052.webp)


로봇의기술적측면에서로봇의3가지중요한기능
인식
센서정보 수집
인터페이스로
광범위한 정보 활용
분석
정확도향상
지능향상
동작
정밀도고도화
R2X간
상호운용성중심
ROS2 - 노드와메시지통신
노드(node)는아래그림처럼Node A, Node B, Node C라는노드가있을때각각의노드들은서로유기적으로
Message로연결되어사용된다. 지금은단순히3개의노드만표시하였지만수행하고자하는태스크가많아질수록
메시지로연결되는노드가늘어나며시스템이확장할수있게된다.
Node


![Image 55](../../assets/images/ros/basics/lesson-04/img_051_055.webp)


ROS2 - 노드와메시지통신
토픽(topic)은아래그림의`Node A - Node B`, `Node A - Node C`처럼비동기식단방향메시지송수신방식으로msg
메시지형태의메시지를발간하는Publisher와메시지를구독하는Subscriber 간의통신이라고볼수있다. 이는1:N, N:1,
N:N 통신도가능하며ROS 메시지통신에서가장널리사용되는통신방법이다.
Topic


![Image 56](../../assets/images/ros/basics/lesson-04/img_052_056.webp)


ROS2 - 노드와메시지통신
서비스(Service)는아래그림의`Node B - Node C`처럼동기식양방향메시지송수신방식으로서비스의
요청(Request)을하는쪽을Service client라고하며서비스의응답(Response)을하는쪽을Service server라고한다.
결국서비스는특정요청을하는클라이언트단과요청받은일을수행후에결과값을전달하는서버단과의통신이라고
볼수있다. 서비스요청및응답(Request/Response) 또한위에서언급한msg 메시지의변형으로srv 메시지라고한다.
Service


![Image 57](../../assets/images/ros/basics/lesson-04/img_053_057.webp)


ROS2 - 노드와메시지통신
액션(Action)은아래그림의`Node A - Node B`처럼비동기식+동기식양방향메시지송수신방식으로액션목표Goal를
지정하는Action client과액션목표를받아특정태스크를수행하면서중간결과값에해당되는액션
피드백(Feedback)과최종결과값에해당되는액션결과(Result)를전송하는Action server 간의통신이라고볼수있다.
Action


![Image 58](../../assets/images/ros/basics/lesson-04/img_054_058.webp)


ROS2 - 노드와메시지통신
액션의구현방식을더자세히살펴보면아래그림과같이토픽(topic)과서비스(service)의혼합이라고볼수있는데액션
목표및액션결과를전달하는방식은서비스와같으며액션피드백은토픽과같은메시지전송방식이다.
액션목표/피드백/결과(Goal/Feedback/Result) 메시지또한위에서언급한msg 메시지의변형으로action 메시지라고한다.
Action


![Image 59](../../assets/images/ros/basics/lesson-04/img_055_059.webp)


ROS2 - 노드와메시지통신
파라미터(Parameter)는아래그림의각노드에파라미터관련Parameter server를실행시켜외부의Parameter client
간의통신으로파라미터를변경하는것으로서비스와동일하다고볼수있다. 단노드내매개변수또는글로벌
매개변수를서비스메시지통신방법을사용하여노드내부또는외부에서쉽게지정(Set) 하거나변경할수있고, 쉽게
가져(Get)와서사용할수있게하는점에서목적이다르다고볼수있다.
Parameter


![Image 60](../../assets/images/ros/basics/lesson-04/img_056_060.webp)


ROS2 - 노드와메시지통신
지금까지강좌에서다루었던토픽, 서비스, 액션은ROS의중요컨셉이자앞으로강좌에서다룰ROS 프로그래밍에있어서매우중요한부분이기에다시
한번비교를해보도록하겠다. 여기서비교한연속성, 방향성, 동기성, 다자간연결, 노드역할, 동작트리거, 인터페이스를각토픽, 서비스, 액션의서로다른
특징이라고볼수있고노드간의데이터전송에있어서특성에맞게선택하여ROS 프로그래밍을하게된다.
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
다자간연결
1:1, 1:N, N:1, N:N
(publisher:subscriber)
1:1
(server:client)
1:1
(server:client)
노드역할
발행자(publisher)
구독자(subscriber)
서버(server)
클라언트(client)
서버(server)
클라언트(client)
동작트리거
발행자
클라언트
클라언트
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
센서데이터, 로봇상태,
로봇좌표, 로봇속도명령등
LED 제어, 모터토크On/Off,
IK/FK 계산, 이동경로계산등
목적지로이동,
물건파지, 복합태스크등


ROS2 패키지설명
Node 노드메시지를주고받는객체의단위,
ROS에서가장기본이되는단위


![Image 61](../../assets/images/ros/basics/lesson-04/img_058_061.webp)


ROS2 패키지설명
CMakeLists.txt : 빌드설정파일입니다.
혹시나VSCODE가아닌VS STUDIO에서 개발을해본경험자라면빌드옵션을설정하는파일입니다.
*빌드에대한것은2차시강의자료참고


![Image 62](../../assets/images/ros/basics/lesson-04/img_059_062.webp)


ROS2 패키지설명


![Image 63](../../assets/images/ros/basics/lesson-04/img_060_063.webp)


ROS2 패키지설명
폴더경로생성1차시의우분투CLI 참고
*터미널에입력하는 명령어입니다.


![Image 64](../../assets/images/ros/basics/lesson-04/img_061_064.webp)


ROS2 패키지설명
*터미널에입력하는 명령어입니다.
빌드후빌드한파일을실행(클릭해서실행하는것이아니다)


![Image 65](../../assets/images/ros/basics/lesson-04/img_062_065.webp)


ROS2 패키지설명
*터미널에입력하는 명령어입니다.


![Image 66](../../assets/images/ros/basics/lesson-04/img_063_066.webp)


ROS2 Alias 설정
*터미널에입력하는 명령어입니다.


![Image 67](../../assets/images/ros/basics/lesson-04/img_064_067.webp)


ROS2 Turtlesim


![Image 68](../../assets/images/ros/basics/lesson-04/img_065_068.webp)


인터페이스(토픽) 리스트보기


![Image 69](../../assets/images/ros/basics/lesson-04/img_066_069.webp)


![Image 70](../../assets/images/ros/basics/lesson-04/img_066_070.webp)


인터페이스(서비스) 리스트보기


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
- 프로그램위치확인


![Image 78](../../assets/images/ros/basics/lesson-04/img_070_078.webp)


![Image 79](../../assets/images/ros/basics/lesson-04/img_070_079.webp)


ROS2 실습


![Image 80](../../assets/images/ros/basics/lesson-04/img_071_080.webp)


![Image 81](../../assets/images/ros/basics/lesson-04/img_071_081.webp)


![Image 82](../../assets/images/ros/basics/lesson-04/img_071_082.webp)


![Image 83](../../assets/images/ros/basics/lesson-04/img_071_083.webp)


ROS2 실습
multisim.launch.py 파일위치


![Image 84](../../assets/images/ros/basics/lesson-04/img_072_084.webp)


![Image 85](../../assets/images/ros/basics/lesson-04/img_072_085.webp)


ROS2 실습
Turtle 2개동시이동


![Image 86](../../assets/images/ros/basics/lesson-04/img_073_086.webp)


![Image 87](../../assets/images/ros/basics/lesson-04/img_073_087.webp)


![Image 88](../../assets/images/ros/basics/lesson-04/img_073_088.webp)


![Image 89](../../assets/images/ros/basics/lesson-04/img_073_089.webp)


ROS2 실습
Service/spawn 선택
Name에turtle1 입력→ call 버튼클릭
Name에turtle2 입력→ call 버튼클릭
Name에turtle3 입력→ call 버튼클릭
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
topic중 pose의데이터type 확인
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
5개데이터가Echo 출력됨


![Image 98](../../assets/images/ros/basics/lesson-04/img_079_098.webp)


ROS2 실습
$rqt_graph
Terminal로메시지가송신되고있음
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
Namespace + Node 이름설정

![Image 125](../../assets/images/ros/basics/lesson-04/img_086_125.webp)


![Image 126](../../assets/images/ros/basics/lesson-04/img_086_126.webp)


![Image 127](../../assets/images/ros/basics/lesson-04/img_086_127.webp)

ROS2 실습
Turtlesim 실행후node 확인
Namespace + Node 이름설정

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
노트북2대로Turtlesim와teleop_key 실행해서각각의노트북에서turtlesim 동작확인


![Image 163](../../assets/images/ros/basics/lesson-04/img_093_163.webp)


수고하셨습니다.

