# 강의_3기_ROS2_기초_3차시


ROS2 기초-3차시
훈련일정
오전
오후
1차시

- 로봇의역사
- 컴퓨터구조(Booting, CPU 작동원리, POST)
- 리눅스와운영체계
- 리눅스CLI 실습(디렉토리, 계정, 기본명령어등), Terminator, 커널, 쉘, gedit, bash
- Application 작동원리(마이크로프로세서, 메모리, 저장장치)
- 리눅스 CLI 실습 2차시
- 리눅스 CLI 실습
- 네트워크와통신(IPV4, IPV6, 소켓, 노드, Hub, TCP, UDP)
- API, Library, Framework, 프로세스와Thread
- 인터프리터, 컴파일러(소스코드→ Build → 실행파일)
- 소켓프로그래밍실습
- OSI7 Layer, 프로토콜(RS-232C, RS-485, Ethernet, TCP/UDP, IP) 3차시
- 센서 기초, IoT와Embedded
- 로봇기초, 좌표계
- 로봇센서활용및로봇의 구성(기계기구, 전기전자, 소프트웨어)
- ROS2 소개및활용
- ROS2 설치(ros.org) 및demo_node 4차시
- ROS2 소개및활용
- ROS2 실습(Talker, Listener)
- ROS2 패키지설명
- ROS2 실습(Turtlesim, teleop_key) 5차시
- ROS2 실습(Turtlesim, Teleop_key 여러개만들기)
- Topic, Service, Action, Parameter, RQT, RQT_Graph 이론및실습
- ROS2 실습(Turtlesim, Namespace 여러개만들기)
- Ros bag and play 실습, my first package build 실습
- Turtlesim subscribing 실습, ROS의 중요한개발도구(Rviz, GAZEBO 소개)


로봇과센서
센서(Sensor)란무엇인가?
Sense는인간의감각작용을가리킨다. 센서는측정대상으로부터정보를검지또는측정하여그측정량을인식가능한유용한신호로
변하는장치, 물리, 화학량등외계의정보를감지하여신호처리하기쉬운전기나빛의신호로변화하는기능을가진소자, 신호나
자극에반응하고, 수신하는장치, 모든정보및에너지의검출장치등으로정의한다.
인간의오감
센서
측정대상
시각
광센서, 이미지센서
빛, 명암, 색, 패턴, 위치, 속도
청각
마이크, 초음파센서
음성, 음계
후각
가스센서, 연기센서
냄새
미각
이온센서, 바이오센서
맛
촉각
자기센서, 온도센서, 압력센서, 습도센서
온도, 압력, 위치


신호체계
PWM
PWM
PWM 신호를통해위그림과같이우리가작업하는프로그램과입력, 혹은프로그램과출력사이에서주고받을수있다.
마치우리가대화를할때소리를사용하는것처럼 다만우리가의사소통을할때공기중의소리를쓸수도있고메신저를
쓸수있는것처럼 신호를회로간의유선연결혹은앞서배운무선연결, 네트워크를통해쓸수도있다.
참고로본교육과정에서우리가주로다루는것은가운데처리부분이며, 처리부분에서의수행으로양끝단의센서, 출력에
어떤영향을미치는지이해하도록해보자.
입력(Sensors)
출력(Actuator)
Processing
(H/W, S/W, F/W, M/W, OS, etc)

![Image 7](../../assets/images/ros/basics/lesson-03/img_004_007.webp)


![Image 8](../../assets/images/ros/basics/lesson-03/img_004_008.webp)

![Image 10](../../assets/images/ros/basics/lesson-03/img_004_010.webp)

![Image 12](../../assets/images/ros/basics/lesson-03/img_004_012.webp)


![Image 13](../../assets/images/ros/basics/lesson-03/img_004_013.webp)


![Image 14](../../assets/images/ros/basics/lesson-03/img_004_014.webp)


신호체계
4mA
20mA
-100℃
+100℃
제품명: 온도센서
[Specifications]

- 측정범위: -100℃ ~ +100℃
- Analog 출력: 4~ 20mA 12mA 0℃


![Image 15](../../assets/images/ros/basics/lesson-03/img_005_015.webp)


![Image 16](../../assets/images/ros/basics/lesson-03/img_005_016.webp)

로봇과센서
센서의신호
인간의감각이뇌에전달되고행동에명령을내리듯이센서의신호또한회로를통해연결, CPU나메모리에연결되어로봇에명령을내리게된다.
PWM 신호
PWM은디지털신호중특정한형태를띈신호를일컷는용어이다. 이PWM은회로제어에다양한용도로활용되고있다. 가장손쉽게PWM을사용한
예는RGB LED의색상변경이나서보모터의방향전환에서목격할수있다. 양쪽의예모두디지털신호일지라도PWM을사용하면아날로그신호와
유사한효과를낼수있다는점에기인한방법이다. 이방법은일정한주기의디지털신호의출력이HIGH인시간과LOW인시간의비율을조정해서
아날로그효과를내는방법이므로디지털신호만을사용하는마이크로컨트롤러에서아날로그신호를만들필요가있을때매우유용하게사용된다.
이런형태의펄스신호가PWM이며, 펄스의길이로값을측정하거나혹은제어명령을내릴수있다


![Image 18](../../assets/images/ros/basics/lesson-03/img_006_018.webp)


![Image 19](../../assets/images/ros/basics/lesson-03/img_006_019.webp)


로봇과센서
아두이노출력
5V = ON
0V = OFF
5ms동안HIGH이고5ms동안LOW였으므로전체시간은10ms
10ms는0.01초이므로주파수는1/0.01 = 100Hz
1sec = 1000ms
   0.1sec =   100ms
 0.01sec =     10ms
0.001sec =      1ms


![Image 20](../../assets/images/ros/basics/lesson-03/img_007_020.webp)


![Image 21](../../assets/images/ros/basics/lesson-03/img_007_021.webp)


![Image 22](../../assets/images/ros/basics/lesson-03/img_007_022.webp)

![Image 24](../../assets/images/ros/basics/lesson-03/img_007_024.webp)


![Image 25](../../assets/images/ros/basics/lesson-03/img_007_025.webp)


![Image 26](../../assets/images/ros/basics/lesson-03/img_007_026.webp)


![Image 27](../../assets/images/ros/basics/lesson-03/img_007_027.webp)


센서종류
*센서가너무민감한경우PWM 신호의펄스가너무급격히변해오히려측정에어려움을겪는경우가있다.
이때방법중하나가특정구간(시간)의평균값혹은급격한펄스변화를노이즈라판단하고제외하는방법이있다.

![Image 29](../../assets/images/ros/basics/lesson-03/img_008_029.webp)


로봇과센서
센서를선택할때고려해야하는것
로봇을설계할때센서를선택할때고려해야할사항이다.

- 가격: 로봇제품을판매할때고려되는사항
- 크기및무게: 센서의응용분야에따라고려되는부분. 가령작업영역이작다면크고무거운센서를쓸필요는없다.
- 출력형태: 아날로그또는디지털로출력된다. 아날로그신호를택할경우디지털로변환하는컨버터가필요하다.
- 인터페이싱: 제어기나마이크로프로세서등과의연결을지원하는인터페이스가고려된다. 센서가요구하는인터페이스, API가있을수있다.
- 분해능: 센서측정범위내최소크기단위. 즉센서가측정하는최소단위
- 감도: 센서의민감도. 보통가격에영향을준다. 작업에따라민감한감도를요구하기도하지만항시우선되어요구되는부분은아니다.
- 선형성: 일반적으로 입력과출력사이의관계를선형성으로설계한다. 비선형성의출력이라면모델링, 보정식을추가하여선형화한다.
- 범위: 최대출력과최소출력의범위를뜻한다.
- 응답시간:  입력변화에따른출력의응답시간을뜻한다. 감도와는헷갈리기쉽지만엄연히다른개념이다.
- 신뢰성: 시스템이온전히운용된시간을시스템이운용된횟수로나눈비율로신뢰성을측정한다.
- 정확성: 센서의출력이목표치에얼마나접근되어있는지
- 반복정밀도: 반복된횟수에서출력된값의범위. 센서의출력이같은입력에대한각각의출력값이변화한정도를측정함으로써결정됨


로봇과센서


![Image 30](../../assets/images/ros/basics/lesson-03/img_010_030.webp)


![Image 31](../../assets/images/ros/basics/lesson-03/img_010_031.webp)


![Image 32](../../assets/images/ros/basics/lesson-03/img_010_032.webp)


![Image 33](../../assets/images/ros/basics/lesson-03/img_010_033.webp)

![Image 35](../../assets/images/ros/basics/lesson-03/img_010_035.webp)


![Image 36](../../assets/images/ros/basics/lesson-03/img_010_036.webp)


![Image 37](../../assets/images/ros/basics/lesson-03/img_010_037.webp)


![Image 38](../../assets/images/ros/basics/lesson-03/img_010_038.webp)


![Image 39](../../assets/images/ros/basics/lesson-03/img_010_039.webp)


![Image 40](../../assets/images/ros/basics/lesson-03/img_010_040.webp)


![Image 41](../../assets/images/ros/basics/lesson-03/img_010_041.webp)

![Image 43](../../assets/images/ros/basics/lesson-03/img_010_043.webp)


![Image 44](../../assets/images/ros/basics/lesson-03/img_010_044.webp)


![Image 45](../../assets/images/ros/basics/lesson-03/img_010_045.webp)


로봇과센서

- 사람은앞이안보이면손을더듬어가며길을찾을수있지만
- 로봇은각종센서로부터데이터를수집→ 분석, 판단→ 행동(제어)
- 입력→ 처리→ 출력


![Image 46](../../assets/images/ros/basics/lesson-03/img_011_046.webp)


![Image 47](../../assets/images/ros/basics/lesson-03/img_011_047.webp)


센서종류

- 일상생활에서우리주변에는어떤센서들이있는지생각해보자


![Image 48](../../assets/images/ros/basics/lesson-03/img_012_048.webp)


![Image 49](../../assets/images/ros/basics/lesson-03/img_012_049.webp)

![Image 51](../../assets/images/ros/basics/lesson-03/img_012_051.webp)

센서종류
참고로여기있는센서들상당수(핀3개있는것들)가RS-485 통신을쓴다.
자세히보면RS-485 통신의Rxd, Txd 표시가있다.
보통핀3개가Rxd, Txd, Gnd(접지)로구성되어있다.
라즈베리파이보드나아두이노보드에는Rxd, Txd 커널이하나만있다. 이때
여러개의 센서를해당보드에연결할때병렬로연결해서해결할수있다.
[RS-485 통신특징]
하나의버스에최대32개의송신기와32개의수신기를연결할수있다.


![Image 53](../../assets/images/ros/basics/lesson-03/img_013_053.webp)


![Image 54](../../assets/images/ros/basics/lesson-03/img_013_054.webp)


![Image 55](../../assets/images/ros/basics/lesson-03/img_013_055.webp)


로봇과센서, 액츄에이터
측정(Input)을위해사람에게는감각이있고 vs 로봇에게센서(Snesor)가있다면,
움직임(Output)을위해서사람에겐근육  vs 로봇에겐액츄에이터(Actuator)가있다.
액츄에이터란전기신호를받아물리적인움직임이나변화를만들어내는장치. 정보를실행하는역할을한다아래는액츄에이터의예이다.
서보모터: 특정각도로회전한다
DC모터: 회전 운동을한다
LED : 빛을발산한다


![Image 56](../../assets/images/ros/basics/lesson-03/img_014_056.webp)


![Image 57](../../assets/images/ros/basics/lesson-03/img_014_057.webp)


![Image 58](../../assets/images/ros/basics/lesson-03/img_014_058.webp)


![Image 59](../../assets/images/ros/basics/lesson-03/img_014_059.webp)


![Image 60](../../assets/images/ros/basics/lesson-03/img_014_060.webp)


센서종류
이중LCD의경우센서와마찬가지로회로를보면RS-485 통신의Rxd, Txd가있다.
즉RS-485 통신으로센서의입력과액츄에이터의출력을모두연결할수도있다.


![Image 61](../../assets/images/ros/basics/lesson-03/img_015_061.webp)


미들웨어(Middleware)와Firmware
Firmware
Middleware
위치

- 하드웨어와가까운저수준소프트웨어
- ROM이나플래시메모리와같은비휘발성메모리에저장
- 소프트웨어와소프트웨어
- 하드웨어와소프트웨어사이의중간계층 역할 하드웨어제어및초기와 시스템간의데이터통신과상호작용관리 사용예 마이크로컨트롤러, 임베디드시스템 네트워크통신, 데이터베이스 접근 여러소프트웨어모듈간의연결 변경용이성 하드웨어에내장되어있어수정이나업데이트가어려움 보통업데이트가가능하며, 시스템간의통신에만영향을미침 사용자와의관계 사용자는거의직접적으로펌웨어를다루지않음 사용자및애플리케이션미들웨어를통해시스템을다룸 특징 하드웨어와의직접적인상호작용 여러시스템간의통신을처리하는소프트웨어 예시
- 마이크로컨트롤러에서실행되는소프트웨어
- 라우터의부팅과정에서작동하는소프트웨어
- 프린터의하드웨어동작을제어하는소프트웨어
- 데이터베이스미들웨어
- 메시징미들웨어
- ROS(다양한하드웨어및소프트웨어모듈간의통신을중개)


미들웨어(Middleware)와Firmware
미들웨어정의
응용소프트웨어가(application software) 운영체제(operation system, OS)로부터제공받는서비스이외에, 추가적인서비스를제공하는
컴퓨터소프트웨어라고정의한다.
미들웨어는양쪽을연결하여데이터를주고받을수있도록중간에서매개역할을하는소프트웨어, 네트워크를통해서연결된여러개의
컴퓨터에있는많은프로세스들에게어떤서비스를사용할수있도록연결해주는소프트웨어를말한다.
데이터를주고받을수있도록중간에서매개역할을하는소프트웨어
우리가공부하는ROS가바로미들웨어에속한다.


![Image 62](../../assets/images/ros/basics/lesson-03/img_017_062.webp)


SBC
Single Board Computer (싱글보드컴퓨터)
SBC는하나의보드에CPU, 메모리, 저장장치등을모두포함한작은컴퓨터를의미합니다.
대표적인예로Raspberry Pi, Arduino, BeagleBone, NBDIA Jetson Nano 등이있습니다.
주로IoT, 임베디드시스템, 소규모서버용도로활용됩니다.
즉주로소형로봇에탑재되는소형컴퓨터이다.
그러나협동로봇처럼크기가크거나무거운연산(프로세스스레드)을요구하는로봇의경우해당SBC 대신우리가
일반적으로생각하는컴퓨터보드나CPU를 탑재하기도한다


![Image 63](../../assets/images/ros/basics/lesson-03/img_018_063.webp)


![Image 64](../../assets/images/ros/basics/lesson-03/img_018_064.webp)


![Image 65](../../assets/images/ros/basics/lesson-03/img_018_065.webp)


![Image 66](../../assets/images/ros/basics/lesson-03/img_018_066.webp)


![Image 67](../../assets/images/ros/basics/lesson-03/img_018_067.webp)


SBC
ROS의통신을로봇과의통신이라고하지만엄밀히말하면, SBC나로봇에탑재된컴퓨터통신하는것이다.
즉우리가이전에통신했던네트워크, 소켓통신이컴퓨터(데스크탑 혹은노트북)와컴퓨터 (데스크탑 혹은노트북)이통신하는것이라면
ROS는 컴퓨터(데스크탑 혹은노트북)와 SBC 혹은로봇에탑재된컴퓨터 간의통신이다


![Image 68](../../assets/images/ros/basics/lesson-03/img_019_068.webp)


![Image 69](../../assets/images/ros/basics/lesson-03/img_019_069.webp)


![Image 70](../../assets/images/ros/basics/lesson-03/img_019_070.webp)


![Image 71](../../assets/images/ros/basics/lesson-03/img_019_071.webp)


![Image 72](../../assets/images/ros/basics/lesson-03/img_019_072.webp)


## SBC vs 제어기

터틀봇의 경우에는 SBC(라즈베리파이)와 OpenCR이라는 보드가 탑재되어 있다.

### 제어기란?

특정 작업이나 장비를 제어하는 데 사용되는 장치로, 보통 임베디드 시스템에서 마이크로컨트롤러(MCU)를 사용하며 간단한 작업을 수행하도록 설계된다.

- 예: 산업용 PLC(Programmable Logic Controller), 자동차 ECU(Electronic Control Unit), IoT 디바이스의 내장형 제어 시스템

제어기는 로봇의 두뇌 역할을 하는 장치로써 다양한 센서와 액추에이터를 연결할 수 있다. 로봇 개발자는 제어기에 다양한 프로그래밍 방법을 통해서 원하는 형태의 로봇을 제어할 수 있게 된다.

### SBC vs 제어기 비교

| 구분 | SBC | 제어기 |
|------|-----|--------|
| **용도** | 더 복잡하고 다양한 작업 수행 (예: 동영상 처리, 네트워크 서버 운영, 프로그래밍 학습) | 특정한 작업을 효율적으로 수행 (예: 온도 제어, 로봇팔 움직임 제어, 센서 데이터 수집 및 처리) |
| **범용성** | 일반적인 컴퓨터처럼 다목적 사용이 가능 | 실시간 작업과 빠른 반응이 중요한 경우에 적합 |
| **효율성** | 운영체제와 소프트웨어를 실행할 수 있어 복잡한 데이터 처리와 멀티태스킹에 적합 | 에너지 소모가 적고, 비용이 저렴하며, 단순한 시스템에 최적화 |
| **운영체제** | 보통 Linux, Windows IoT, Android와 같은 범용 운영체제를 실행할 수 있음. 복잡한 소프트웨어와 GUI 기반의 애플리케이션 실행 가능 | 대부분 운영체제가 없거나, RTOS(Real-Time Operating System)와 같은 경량 운영체제 사용. 작업이 운영체제에 의존하지 않고 펌웨어 수준에서 직접 작동 |
| **하드웨어** | CPU, GPU, RAM 등의 사양이 훨씬 높음. USB, HDMI, 이더넷 포트 등 다양한 연결 옵션 제공. 복잡한 연산과 데이터 처리가 가능하며 고해상도 디스플레이 출력도 지원 | CPU 성능과 메모리가 상대적으로 낮음. GPIO(General Purpose Input/Output)와 같은 간단한 하드웨어 인터페이스 제공. 저전력 및 소형화에 최적화 |
| **활용 분야** | 비디오 스트리밍, 머신러닝 응용 프로그램, 웹 서버, 로봇공학에서 활용. 교육용, 프로토타이핑, 개발자 커뮤니티에서 널리 사용 | 온도, 압력, 습도 등 센서 데이터를 기반으로 간단한 제어 작업 수행. 산업용 자동화, IoT 장치, 스마트 가전 등에서 주로 사용 |


![Image 73](../../assets/images/ros/basics/lesson-03/img_020_073.webp)


IoT(사물인터넷)
IoT (Internet of Things)또는사물인터넷이라는용어는연결된디바이스의공통네트워크를의미하며, 디바이스와클라우드및디바이스간
통신을용이하게하는기술을의미하기도합니다. 저렴한컴퓨터칩과고대역폭통신의출현덕분에이제수십억개의디바이스가인터넷에
연결되어있습니다. 이는칫솔, 진공청소기, 자동차및기계와같은일상적인디바이스가센서를사용하여데이터를수집하고사용자에게
지능적으로응답할수있음을의미합니다.
IoT의구성요소

- 스마트디바이스 컴퓨터기능이부여된텔레비전, 보안카메라또는운동장비와같은 디바이스입니다. 환경, 사용자입력또는사용패턴에서데이터를수집하고 인터넷을통해IoT 애플리케이션과데이터를주고받습니다.
- IoT 애플리케이션 IoT 애플리케이션은다양한IoT 디바이스에서수신한데이터를통합하는 서비스및소프트웨어의모음입니다. 머신러닝/딥러닝기술을사용하여이 데이터를분석하고정보에입각한결정을내립니다. 이러한결정은IoT 디바이스로다시전달되고IoT 디바이스는입력에지능적으로응답합니다.
- 그래픽사용자인터페이스 그래픽사용자인터페이스를통해IoT 디바이스나디바이스플릿(Fleet)을 관리할수있습니다. 일반적인예로스마트디바이스를등록하고제어하는데 사용할수있는모바일애플리케이션또는웹사이트가있습니다.


![Image 74](../../assets/images/ros/basics/lesson-03/img_021_074.webp)


IoT(사물인터넷)
IoT (Internet of Things)의예
스마트팜
스마트홈(삼성smart thing 앱의모니터, 에어컨제어화면)
스마트시티
그외스마트공급망관리, 스마트헬스케어시스템, 스마트바코드리더, 스마트팩토리, 스마트그리드등


![Image 75](../../assets/images/ros/basics/lesson-03/img_022_075.webp)


![Image 76](../../assets/images/ros/basics/lesson-03/img_022_076.webp)


![Image 77](../../assets/images/ros/basics/lesson-03/img_022_077.webp)


임베디드(Embedded)
내장형시스템이라는뜻으로 시스템'내부에탑재된' 컴퓨터를뜻한다.

- 시스템을동작시키는소프트웨어를하드웨어에내장하여특수한기능만을수행하는컴퓨터시스템
- 즉, 디바이스를직접적으로제어하는프로그램을말한다.
- 디바이스를제어하기위해서메모리영역에서리소스를제어하는것이필요하여강력한메모리조작성능을갖추고C/C++ 언어를권장한다.
- 또한임베디드개발에서메모리리소스영역을제대로정리하지못하고침범하면하드웨어의심각한오작동을유발할수있기때문이다. 때문에 컴파일언어의빌드동작으로메모리리소스를효율적으로확보해야한다.
- 그리고기기에탑재되는프로그램리소스가제한될수있어최적화는반드시필요하다. 파이썬으로임베디드개발이가능한가?
- 일반적으로파이썬으로임베디드시스템을개발하는것은부적절하다.
- 이유는파이썬의메모리할당되어메모리를사용자가직접적으로통제하기어렵기때문이다.
- 파이썬에서는가비지컬렉션을자체적으로메모리를관리해주는부분이있어, 메모리리소스관리는생소한개념일수있다.
- 하지만고급개발자가되기위해해당개념을숙지하도록한다 Garbage Collection(가비지컬렉션)은메모리관리기법중하나로, 더이상사용되지않는메모리(즉, 객체들)를자동으로해제하여메모리누수를방지하고시스템의효율적인메모리사용을돕습니다.


![Image 78](../../assets/images/ros/basics/lesson-03/img_023_078.webp)


임베디드(Embedded)
임베디드는SBC 같은로봇내부의컴퓨터에탑재된다.
즉우리가그동안코딩했던프로그램이우리가쓰는데스크탑 혹은노트북에서돌아가는것이라면임베디드는로봇안에들어가는프로그램이다.
로봇안에서각종프로세스, 스레드를처리하고그러기위해메모리를통제해서
로봇이해당임베디드프로그램에의해안정적으로돌아가야하므로C/C++이선호된다.


![Image 79](../../assets/images/ros/basics/lesson-03/img_024_079.webp)


![Image 80](../../assets/images/ros/basics/lesson-03/img_024_080.webp)


![Image 81](../../assets/images/ros/basics/lesson-03/img_024_081.webp)


![Image 82](../../assets/images/ros/basics/lesson-03/img_024_082.webp)


![Image 83](../../assets/images/ros/basics/lesson-03/img_024_083.webp)


임베디드(Embedded)
임베디드설계시고려해야할사항을고민해보자.
임베디드에어디까지프로그램을넣느냐?
지금까지AI 실습을할때컴퓨터가발열되거나팬이계속작동되는상황을접한적이있다.
학습하는데Epoch 한번에상당한시간을소비하게되어colab 프로까지사용했던경험을떠올려보자.
이때우리는컴퓨터의리소스가아닌구글에서제공해주는리소스를사용했다.
ROKEY 친구들중에서GPU가있는수강생은빠르게처리되어크게불편함이없었을것같다.
이유는컴퓨터하드웨어의사양이좋다면colab 프로는필요없었을것이다.
마찬가지로 아두이노, 라즈베리파이는작은보드에무거운임베디드를돌린다면어떻게될까?
많은리소스를필요하게되어오히려기기의성능을저하시킬수있다.
하지만임베디드에최소한의기기작동에대한프로그램만넣고AI에의한연산은중앙에서제어하는컴퓨터에서실행한후
컴퓨터에서임베디드에명령을내린다면우리가그동안컴퓨터에GPU가없어colab 프로를썼던것처럼
SBC의리소스가아닌중앙제어의리소스를사용해기기의리소스를절약하게된다.
물론기기에탑재하는SBC나컴퓨터를고성능으로넣어중앙에서제어하는PC에의존하지않는것이더좋은경우도있다.
가령통신이원활하지않는상황에자주노출되는디바이스라면그런고성능리소스를탑재하는것이좋다.
하지만기기에고성능리소스를탑재한다는것은곧가격의상승을의미하게되니상황과여건을고려하여기기의사양이정해지면
임베디드의역할을어디까지정할지고민하는게좋겠다.
이는임베디드개발자뿐만아니라임베디드와통신하는프로그램을만드는개발자도마찬가지이다.


![Image 84](../../assets/images/ros/basics/lesson-03/img_025_084.webp)


로봇의센서활용구성


![Image 85](../../assets/images/ros/basics/lesson-03/img_026_085.webp)


로봇의구성

로봇의구성


![Image 87](../../assets/images/ros/basics/lesson-03/img_028_087.webp)

![Image 89](../../assets/images/ros/basics/lesson-03/img_028_089.webp)


로봇의구성


![Image 90](../../assets/images/ros/basics/lesson-03/img_029_090.webp)


![Image 91](../../assets/images/ros/basics/lesson-03/img_029_091.webp)


로봇의조인트(Joint, 관절)
DOF(Degree of Freedom)

- DOF는물체가독립적으로움직일수있는방향의수
- 즉, 어떤객체가공간에서위치와방향을바꾸는방법의수
- 이개념은특히로봇의움직임을정의할때매우중요


![Image 92](../../assets/images/ros/basics/lesson-03/img_030_092.webp)


좌표계
우리가흔히알고있는X, Y, Z로이루어진좌표이다
해당좌표는직선이동을할때계산이편하다
X, Y 축에서원점과해당좌표까지의거리(r)와해당점에서
원점으로이은선이X축과의이루는각(θ)으로좌표를
표시한다. (z축은동일), X, Y 평면에서회전을계산할때
용이하다
한점을원점까지의거리를r이라정의하고원점까지이은선과
Z축과의각을θ라한다. 그리고원점과해당좌표를이은선을X, Y
평면에수직으로내린선과X축과의각을ϕ라정의하여좌표를(r, θ,
ϕ)라정의한다회전운동을계산하기용이하다.
직교좌표, 데카르트좌표계
(Cartesian Coordinate System)
원통 좌표좌표계
(r, θ, z), rho-theta
구면좌표계
(r, θ, ϕ)
눈으로사물을위치(좌표)를파악하고이동후물체를잡는등의행위를하는것처럼로봇에게명령을수행할좌표를
로봇기술자가입력/파악후제어할수있어야한다. 기본적인좌표계에대한수학적인지식을정리해보았습니다.


![Image 93](../../assets/images/ros/basics/lesson-03/img_031_093.webp)


![Image 94](../../assets/images/ros/basics/lesson-03/img_031_094.webp)


![Image 95](../../assets/images/ros/basics/lesson-03/img_031_095.webp)


![Image 96](../../assets/images/ros/basics/lesson-03/img_031_096.webp)


좌표계
앞서좌표계에대한수학적인배경지식을잠깐설명했지만, 해당좌표계산에민감해하지말자. 로봇에서의좌표는다음과같이생각해볼수있다


![Image 97](../../assets/images/ros/basics/lesson-03/img_032_097.webp)


좌표계


![Image 98](../../assets/images/ros/basics/lesson-03/img_033_098.webp)


좌표계


![Image 99](../../assets/images/ros/basics/lesson-03/img_034_099.webp)


![Image 100](../../assets/images/ros/basics/lesson-03/img_034_100.webp)


좌표계
Gimber Lock

- 하나의축이다른축과동일하게되어축에대한자유도를상실하게되는현상
- 오일러각은X, Y, Z의회전값을각각의행렬이순차적으로계산됨. 이로인해Gimber Lock 발생됨
- 가장바깥쪽(보라색)이Yaw, 가운데초록색Pitch, 파란색Roll
- 초록색(pitch)가90도또는-90도의회전을진행하면,
- 보라색(yaw)과파란색(roll)이같은축을회전하는방향이되어1개축에대한자유도가사라짐 → 3차원방향표시못하고2차원방향만표현


![Image 101](../../assets/images/ros/basics/lesson-03/img_035_101.webp)


![Image 102](../../assets/images/ros/basics/lesson-03/img_035_102.webp)


좌표계


![Image 103](../../assets/images/ros/basics/lesson-03/img_036_103.webp)


ROS 소개및활용


![Image 104](../../assets/images/ros/basics/lesson-03/img_037_104.webp)


ROS 소개및활용


![Image 105](../../assets/images/ros/basics/lesson-03/img_038_105.webp)


![Image 106](../../assets/images/ros/basics/lesson-03/img_038_106.webp)


ROS 소개및활용


![Image 107](../../assets/images/ros/basics/lesson-03/img_039_107.webp)


ROS 소개및활용


![Image 108](../../assets/images/ros/basics/lesson-03/img_040_108.webp)


ROS 소개및활용


![Image 109](../../assets/images/ros/basics/lesson-03/img_041_109.webp)


ROS2 참고자료
vmayoral/ros-robotics-companies: A list of robotics companies using the Robot Operating System (ROS and ROS 2).
https://github.com/vmayoral/ros-robotics-companies
ROS Robotics Companies
ROS 2
https://github.com/ros2
ROS2 설치매뉴얼
https://teamsparkx.notion.site/ROS2-1137ad24f8c04bffb7f958b8486b89f8
ROS설치파일.zip


![Image 110](../../assets/images/ros/basics/lesson-03/img_042_110.webp)


![Image 111](../../assets/images/ros/basics/lesson-03/img_042_111.webp)


![Image 112](../../assets/images/ros/basics/lesson-03/img_042_112.webp)


![Image 113](../../assets/images/ros/basics/lesson-03/img_042_113.webp)


ROS2 실습설치
https://teamsparkx.notion.site/ROS2-1137ad24f8c04bffb7f958b8486b89f8?pvs=4
*위링크참고해서파일을다운로드하세요.(링크에서복사CLI 명령어복사도가능해요)


![Image 114](../../assets/images/ros/basics/lesson-03/img_043_114.webp)


![Image 115](../../assets/images/ros/basics/lesson-03/img_043_115.webp)


![Image 116](../../assets/images/ros/basics/lesson-03/img_043_116.webp)


ROS2 실습설치


![Image 117](../../assets/images/ros/basics/lesson-03/img_044_117.webp)


ROS2 실습설치


![Image 118](../../assets/images/ros/basics/lesson-03/img_045_118.webp)


ROS2 실습


![Image 119](../../assets/images/ros/basics/lesson-03/img_046_119.webp)


![Image 120](../../assets/images/ros/basics/lesson-03/img_046_120.webp)


ROS2 실습


![Image 121](../../assets/images/ros/basics/lesson-03/img_047_121.webp)


![Image 122](../../assets/images/ros/basics/lesson-03/img_047_122.webp)


ROS2 실습


![Image 123](../../assets/images/ros/basics/lesson-03/img_048_123.webp)


![Image 124](../../assets/images/ros/basics/lesson-03/img_048_124.webp)


ROS2 실습
→ 실행가능한binary 파일
→ 헤더파일
→ 패키지의빌드, 환경설정파일
→ 소스코드가저장되는디렉토리
→ 다양한유틸리티도구들
→ 공유라이브러리
→ 패키지와 의존성(Dependency) 관리
→ 빌드설정파일
→ 환경설정파일들


![Image 125](../../assets/images/ros/basics/lesson-03/img_049_125.webp)


ROS2 실습


![Image 126](../../assets/images/ros/basics/lesson-03/img_050_126.webp)


![Image 127](../../assets/images/ros/basics/lesson-03/img_050_127.webp)


![Image 128](../../assets/images/ros/basics/lesson-03/img_050_128.webp)


ROS2 실습

1. ros2 run demo_nodes_cpp talker
2. ros2 run demo_nodes_cpp listener
3. 해당디렉토리로이동
4. source /opt/ros/humble/setup.bash
5. ./talker
6. ./listener


![Image 129](../../assets/images/ros/basics/lesson-03/img_051_129.webp)


![Image 130](../../assets/images/ros/basics/lesson-03/img_051_130.webp)


![Image 131](../../assets/images/ros/basics/lesson-03/img_051_131.webp)


ROS2 실습
1.
./turtlesim_node 실행시에러발생
2.
source /opt/ros/humble/setup.bash 실행후(또는~/.bashrc 확인)
3.
./turtlesim_node 실행하면정상실행됨


![Image 132](../../assets/images/ros/basics/lesson-03/img_052_132.webp)


![Image 133](../../assets/images/ros/basics/lesson-03/img_052_133.webp)


![Image 134](../../assets/images/ros/basics/lesson-03/img_052_134.webp)


![Image 135](../../assets/images/ros/basics/lesson-03/img_052_135.webp)


![Image 136](../../assets/images/ros/basics/lesson-03/img_052_136.webp)


ROS2 실습
1.
Echo 명령어실행및.bashrc 추가된내용확인
2.
Ros2 run tab + tab + tab 키입력(자동완성되는지확인)


![Image 137](../../assets/images/ros/basics/lesson-03/img_053_137.webp)


![Image 138](../../assets/images/ros/basics/lesson-03/img_053_138.webp)


![Image 139](../../assets/images/ros/basics/lesson-03/img_053_139.webp)


ROS2 실습
   .bashrc에추가되어있는지확인


![Image 140](../../assets/images/ros/basics/lesson-03/img_054_140.webp)


![Image 141](../../assets/images/ros/basics/lesson-03/img_054_141.webp)


![Image 142](../../assets/images/ros/basics/lesson-03/img_054_142.webp)


![Image 143](../../assets/images/ros/basics/lesson-03/img_054_143.webp)


![Image 144](../../assets/images/ros/basics/lesson-03/img_054_144.webp)


ROS2 실습


![Image 145](../../assets/images/ros/basics/lesson-03/img_055_145.webp)


![Image 146](../../assets/images/ros/basics/lesson-03/img_055_146.webp)


![Image 147](../../assets/images/ros/basics/lesson-03/img_055_147.webp)


![Image 148](../../assets/images/ros/basics/lesson-03/img_055_148.webp)


ROS2 실습
Turtlesim 실행후node 확인
turtle_teleop_key 실행후키보드로turtle움직여보기


![Image 149](../../assets/images/ros/basics/lesson-03/img_056_149.webp)


ROS2 실습


![Image 153](../../assets/images/ros/basics/lesson-03/img_057_153.webp)


![Image 154](../../assets/images/ros/basics/lesson-03/img_057_154.webp)


![Image 155](../../assets/images/ros/basics/lesson-03/img_057_155.webp)


![Image 156](../../assets/images/ros/basics/lesson-03/img_057_156.webp)


ROS2 실습
:~$ source /opt/ros/humble/setup.bash

- source 명령어는특정스크립트파일을현재쉘에서실행하고, 그안에설정된환경변수를쉘환경에반영
- bash나zsh 같은셸환경에서특정파일을실행하면해당파일의명령이현재셸에로드되므로, 설정된모든환경변수를현재셸에서도사용
- /opt/ros/humble/setup.bash: 이파일은ROS2가설치된경로인/opt/ros/humble 안에있는환경설정스크립트
- setup.bash는ROS 2 패키지를사용할때필요한환경변수를설정하는역할
- PATH

→ /opt/ros/humble/bin

- LD_LIBRARY_PATH →  /opt/ros/humble/lib
- AMENT_PREFIX_PATH → ament 위치참조
- PYTHONPATH →
- CMAKE_PREFIX_PATH


ROS2 실습


![Image 157](../../assets/images/ros/basics/lesson-03/img_059_157.webp)


![Image 158](../../assets/images/ros/basics/lesson-03/img_059_158.webp)


![Image 159](../../assets/images/ros/basics/lesson-03/img_059_159.webp)


ROS2 실습
Class, 상속, 생성자복습
객체(Object)와인스턴스(Instance)


![Image 160](../../assets/images/ros/basics/lesson-03/img_060_160.webp)


ROS2 실습
talker code 설명


![Image 161](../../assets/images/ros/basics/lesson-03/img_061_161.webp)


ROS2 실습
talker code 설명


![Image 162](../../assets/images/ros/basics/lesson-03/img_062_162.webp)


ROS2 실습


![Image 163](../../assets/images/ros/basics/lesson-03/img_063_163.webp)


![Image 164](../../assets/images/ros/basics/lesson-03/img_063_164.webp)


ROS2 실습
Listener code 설명


![Image 165](../../assets/images/ros/basics/lesson-03/img_064_165.webp)


ROS2 실습
Listener code 설명


![Image 166](../../assets/images/ros/basics/lesson-03/img_065_166.webp)


ROS2 실습
각terminal 창에서ROS_DOMAIN_ID를바꿔가며talker와listener 실행해서메시지주고받는지확인


![Image 167](../../assets/images/ros/basics/lesson-03/img_066_167.webp)


![Image 168](../../assets/images/ros/basics/lesson-03/img_066_168.webp)


![Image 169](../../assets/images/ros/basics/lesson-03/img_066_169.webp)


ROS2 실습
talker와listener등샘플프로그램이있는디렉토리위치
/opt/ros/humble/share/demo_node_cpp/launch/topics


![Image 170](../../assets/images/ros/basics/lesson-03/img_067_170.webp)


![Image 171](../../assets/images/ros/basics/lesson-03/img_067_171.webp)


ROS2 실습


![Image 172](../../assets/images/ros/basics/lesson-03/img_068_172.webp)


![Image 173](../../assets/images/ros/basics/lesson-03/img_068_173.webp)


![Image 174](../../assets/images/ros/basics/lesson-03/img_068_174.webp)


ROS2 실습


![Image 175](../../assets/images/ros/basics/lesson-03/img_069_175.webp)


수고하셨습니다.

