# 02_로키 - 두산 프로젝트 교안(GAZEBO)_0305


Version
V1.0
최종수정일
2025.02.18
작성자
김루진
시뮬레이션
프로젝트교안

가제보(gazebo)가상환경구축
- ROS 시뮤레이션툴인가제보를이용하여테스트환경구축하기
- 터틀봇3를사용하여실제시뮬레이션구축및실제환경테스트
- 가상의공장에서Pick and Place를구현하는시뮬레이션구축하기
가제보

HUMAN AI ROBOTICS
3
주제2.1 기초
가제보이해

HUMAN AI ROBOTICS
4
가제보이해
가제보신버전정보
로봇시뮬레이션은모든로봇공학자의도구상자에서필수적인도구. 
잘설계된시뮬레이터를사용하면현실적인시나리오를사용하여알고리즘을신속하게
테스트하고, 로봇을설계하고, 회귀테스트를수행하고, AI 시스템을훈련.
Gazebo Classic과Ignition Gazebo (현재는Gazebo로통합)라는두가지주요버전
신규버전(Ignition Gazebo)
모듈화된아키텍처. 
여러독립된모듈(Ignition Physics, Ignition Rendering, Ignition Transport 등)로구성, 특정기능만교체, 확장
물리엔진
•구버전(Gazebo Classic): 
•기본물리엔진은ODE (Open Dynamics Engine)를사용
•다른엔진을지원하기위해플러그인을사용할수있었습니다. Bullet, Simbody, DART 등과도통합
•신규버전(Ignition Gazebo): 
•다양한물리엔진과의더나은통합을제공하며, TPE (Trivial Physics Engine)와같은새로운엔진도입 성능과유연성 향상
HUMAN AI ROBOTICS
5
가제보이해
가제보이해
▪
설치하기싸이트
▪
Classic버전설치
▪
Gazebo : Tutorial : Ubuntu (gazebosim.org)
1. 셋업
2. 최소설치사양
# Install Gazebo Classic 11
sudo apt install gazebo11 -y
# Install ROS2-Gazebo integration packages
sudo apt install ros-humble-gazebo-ros-pkgs -y
# Source ROS2 setup script
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
# Install additional tools (optional but recommended)
sudo apt install python3-colcon-common-extensions -y
3. 설치하기
HUMAN AI ROBOTICS
6
가제보이해
신버전가제보
Ubuntu 22.04와ROS2 Humble에맞는Gazebo 설치방법
ROS2 Humble은Gazebo 11과호환되며, 이는'gz'로시작하는새로운Gazebo 버전
$sudo apt update
$sudo apt install -y ros-humble-gazebo-ros-pkgs
gz sim -v 4 /path/to/your/world/file.sdf
특정월드로Gazebo 실행

![Image 10](../../assets/images/ros/projects/gazebo/img_006_010.webp)


HUMAN AI ROBOTICS
7
가제보이해
SDF(Simulation Description Format)
URDF는RViz, Moveit! 그리고Gazebo에서모두사용


HUMAN AI ROBOTICS
8
주제2.2.3 시뮬레이터상Machine Tending동작실습
가제보이해
3. 가제보다양한기능
HUMAN AI ROBOTICS
9
가제보이해
가제보프로젝트디렉토리구조
•launch 폴더는시뮬레이션을시작하는데사용되는launch 파일 저장
•worlds 폴더에는가제보환경을정의하는.world 파일 저장
•models 폴더에는로봇이나객체와같은개별모델 파일 저장
•meshes 폴더는3D 모델의시각적및물리적표현을위한파일 저장
•config 폴더에는컨트롤러나기타설정파일 저장
•scripts 폴더는로봇제어나시뮬레이션관련스크립트파일 저장
•plugins 폴더에는가제보의기능을확장하는사용자정의플러그인
가제보로봇모델을spawn하고ROS를통해제어하기위해필요한폴더 및파일구조
가제보모델데이터베이스폴더구조에따른포맷의규칙을따라야한다.

![Image 17](../../assets/images/ros/projects/gazebo/img_009_017.webp)


HUMAN AI ROBOTICS
10
가제보이해
가제보프로젝트디렉토리구조
mkdir -p ~/.gazebo/models/my_robot
gedit ~/.gazebo/models/my_robot/model.config
gedit ~/.gazebo/models/my_robot/model.sdf
가제보GUI 인터페이스의Insert Model을통해당신의모델을불러올수있다


HUMAN AI ROBOTICS
11
가제보이해
가제보툴이해
1. 툴바(toolbars)
Upper Toolbar
Bottom Toolbar

![Image 22](../../assets/images/ros/projects/gazebo/img_011_022.webp)


![Image 23](../../assets/images/ros/projects/gazebo/img_011_023.webp)


HUMAN AI ROBOTICS
12
가제보이해
가제보화면용어
1. 씬(scene)
2. 판넬(panel)
![Image 26](../../assets/images/ros/projects/gazebo/img_012_026.webp)


![Image 27](../../assets/images/ros/projects/gazebo/img_012_027.webp)

HUMAN AI ROBOTICS
13
가제보이해
가상환경만들기
1. 샤시(Chassis)
2. 샤시크기조정
3. 싸이즈줄이기(파란색으로납작하게)
![Image 31](../../assets/images/ros/projects/gazebo/img_013_031.webp)

HUMAN AI ROBOTICS
14
가제보이해
가상환경만들기
4. Body 사시만들기
5. Front Wheels

![Image 34](../../assets/images/ros/projects/gazebo/img_014_034.webp)


![Image 35](../../assets/images/ros/projects/gazebo/img_014_035.webp)


HUMAN AI ROBOTICS
15
가제보이해
가상환경만들기
6. 싸이즈조절및복사

![Image 37](../../assets/images/ros/projects/gazebo/img_015_037.webp)


![Image 38](../../assets/images/ros/projects/gazebo/img_015_038.webp)


![Image 39](../../assets/images/ros/projects/gazebo/img_015_039.webp)


HUMAN AI ROBOTICS
16
가제보이해
가상환경만들기
7. 관절(Joint) 추가
상단도구모음에서조인트아이콘을클릭하여조인트생성대화상자를표시

![Image 41](../../assets/images/ros/projects/gazebo/img_016_041.webp)


![Image 42](../../assets/images/ros/projects/gazebo/img_016_042.webp)


HUMAN AI ROBOTICS
17
가제보이해
가상환경만들기
6. 휠축맞추기
조인트축섹션을변경하고축을Z(0, 0, 1)로변경합니다.

![Image 44](../../assets/images/ros/projects/gazebo/img_017_044.webp)


HUMAN AI ROBOTICS
18
가제보이해
가상환경만들기
7. 휠을샤시와어라인하기그리고왼쪽바퀴도만들기

![Image 46](../../assets/images/ros/projects/gazebo/img_018_046.webp)


![Image 47](../../assets/images/ros/projects/gazebo/img_018_047.webp)


![Image 48](../../assets/images/ros/projects/gazebo/img_018_048.webp)


![Image 49](../../assets/images/ros/projects/gazebo/img_018_049.webp)


HUMAN AI ROBOTICS
19
가제보이해
가상환경만들기
8. 케스트볼만들기
기하학섹션으로스크롤하여반경을0.2m로변경합니다.

![Image 51](../../assets/images/ros/projects/gazebo/img_019_051.webp)


![Image 52](../../assets/images/ros/projects/gazebo/img_019_052.webp)


HUMAN AI ROBOTICS
20
가제보이해
가상환경만들기
9. 휠을샤시와어라인하기
Y Align Center option to center the two links in the Y axis, and select the X Align Min option
조인트유형섹션에서볼조인트옵션을선택하세요.

![Image 54](../../assets/images/ros/projects/gazebo/img_020_054.webp)


![Image 55](../../assets/images/ros/projects/gazebo/img_020_055.webp)


HUMAN AI ROBOTICS
21
가제보이해
가상환경만들기
3D 맵만들기
Edit 메뉴에서building editor 를클릭, 다음과같은building editor화면이나타난다.
화면에서왼쪽에는벽, 문, 계단등을만들수있는항목들이있고, 모눈종이처럼생긴구역에서위에서내려다보는평면도
관점의맵을볼수있다. 이모눈종이구역에서벽, 계단등을생성, 배치할수있다아래쪽구역은실제gazebo 공간상에
생성된3차원맵을보여준다.

![Image 57](../../assets/images/ros/projects/gazebo/img_021_057.webp)


![Image 58](../../assets/images/ros/projects/gazebo/img_021_058.webp)


HUMAN AI ROBOTICS
22
가제보이해
가상환경만들기
왼쪽의Create Walls의Wall을클릭하고모눈종이영역에서직선을그려주면, 벽이생성된다.  직선의길이, 위치
등을변경하면벽의길이, 위치를변경할수있다.
왼쪽에서Stairs 를클릭하고, 모눈종이영역을클릭해주면계단이생성된다.

![Image 60](../../assets/images/ros/projects/gazebo/img_022_060.webp)


![Image 61](../../assets/images/ros/projects/gazebo/img_022_061.webp)


HUMAN AI ROBOTICS
23
가제보이해
가상환경만들기
Add texture 기능으로물체의표면질감을바꿔줄수있다.
building editor 에서맵을다만들었다면왼쪽상단의File 탭에서Save as..를클릭,이름을바꿔준뒤, 저장한다.
저장한뒤File -> exit building editor 를눌러buildig editor 화면에서나간다.
저장한뒤building editor에서나가면, 가제보공간에, 우리가만든구조물들이
나타나있다.
위사진은building editor에서간단한계단, 벽등으로만든구조물이다.
이제이3D 맵을*.world 파일로저장하자.
왼쪽상단의File -> save world as 를클릭한다.
참고: https://www.youtube.com/watch?v=7McYSJFAqlU

![Image 63](../../assets/images/ros/projects/gazebo/img_023_063.webp)


HUMAN AI ROBOTICS
24
가제보이해
자동차모델만들기
10. 저장및리로드
ROS2 환경에서가제보모델다음의경로에저장
1.
시스템전체에서접근가능한공용가제보모델저장소
         `~/.gazebo/models/`: 사용자의홈디렉토리내`.gazebo/models/` 폴더
2. 특정ROS2 패키지내에속한모델들을저장하는공간
          `<ros2_workspace>/src/<package_name>/models/`: ROS2 워크스페이스의패키지내`models/` 폴더
11. 저장된모델을로드
1. ros2 run gazebo_ros spawn_entity.py -entity robot_name -file /path/to/your/robot.urdf -x 0 -y 0 -z 1

HUMAN AI ROBOTICS
25
가제보이해
자동차모델만들기
from gazebo_ros.node import GazeboRosPaths
# 1.번경로의모델로드
gazebo.spawn_sdf_model('my_model', model_xml, '', initial_pose, 'world')
# 2.번경로의모델로드
pkg_path = GazeboRosPaths.get_model_path('my_package', 'my_model')
gazebo.spawn_urdf_model('my_model', pkg_path, '', initial_pose, 'world')
11. 저장된모델을로드
2. launch 파일, `gazebo.spawn_sdf_model()` 또는`gazebo.spawn_urdf_model()` 함수사용

![Image 66](../../assets/images/ros/projects/gazebo/img_025_066.webp)


HUMAN AI ROBOTICS
26
메니퓨레이션시뮬레이션

HUMAN AI ROBOTICS
27
메니퓨레이션시뮬레이션
로봇모델패키지만들기
1. 워크스페이스폴더를만들고그안으로이동
$ cd ~
$ mkdir -p .gazebo/models/gongjang
$ cd .gazebo/models/gongjang/
<?xml version="1.0"?>
 <model>
   <name>ganzang</name>
   <version>1.0</version>
   <sdf version='1.4'>model.sdf</sdf>
   <author>
     <name>sj kim</name>
     <email>*@gmail.com</email>
   </author>
   <description>project ganzang</description>
</model>
2. 로봇모델의설정파일을만들고편집
Model.config
sudo apt-get install ros-humble-gazebo-ros
참고: 가제보설치

HUMAN AI ROBOTICS
28
메니퓨레이션시뮬레이션
모델설계하기
3. 로봇모델의실제내용이될파일을만들고설계
<link name="link1">
<pose>0 0.1 0.125 0 0 0</pose>
<collision name="collision">
<geometry>
<box>
<size>.05 .3 .05</size>
</box>
</geometry>
</collision>
<visual name="visual">
<geometry>
<box>
<size>.05 .3 .05</size>
</box>
</geometry>
</visual>
</link>
<joint type="revolute" name="joint0">
<pose>0 0 0 0 0 0</pose>
<child>link0</child>
<parent>world</parent>
<axis>
<xyz>0 0 0</xyz>
</axis>
</joint>
<joint type="revolute" name="joint1">
<pose>0 -0.1 0 0 0 0</pose>
<child>link1</child>
<parent>link0</parent>
<axis>
<limit>
<lower>-1</lower>
<upper>1</upper>
</limit>
<xyz>0 0 10</xyz>
</axis>
</joint>
</model>
<?xml version='1.0'?>
<sdf version='1.4'>
<model name="ganzang">
<static>false</static>
<link name='link0'>
<pose>0 0 0.05 0 0 0</pose>
  <collision name='collision'>
<geometry>
  <box>
<size>.1 .1 .1</size>
  </box>
</geometry>
</collision>
<visual name='visual'> 
<geometry>
<box>
<size>.1 .1 .1</size>
</box>
</geometry>
</visual>
</link>

HUMAN AI ROBOTICS
29
메니퓨레이션시뮬레이션
모델불러오기
4. 가제보의왼쪽페널에서gongjang 모델을마우스로끌어온다.
여러가지기능을메뉴를선택해서학습하시기바랍니다.

![Image 71](../../assets/images/ros/projects/gazebo/img_029_071.webp)


HUMAN AI ROBOTICS
30
메니퓨레이션시뮬레이션
모델설계하기
4. 컨트롤러사용
<?xml version="1.0"?>
<robot name="simple_example">
<link name="base_link">
<inertial>
<mass value="10" />
<inertia ixx="0.4" ixy="0.0" ixz="0.0" iyy="0.4" iyz="0.0" izz="0.2"/>
</inertial>
<collision>
<geometry>
<cylinder radius="0.05" length="0.24" />
</geometry>
</collision>
<visual>
<geometry>
<cylinder radius="0.05" length="0.24" />
</geometry>
</visual>
</link>
<joint name="base_to_second_joint" type="continuous">
<parent link="base_link"/>
<child link="second_link"/>
<axis xyz="1 0 0"/>
<origin xyz="0.0 0.0 0.2" rpy="0.0 0.0 0.0"/> 
</joint>
<!--
GAZEBO RELATED PART                             -->
<!-- ROS Control plugin for Gazebo -->
<gazebo>
<plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
<robotNamespace>/simple_model</robotNamespace>
</plugin>
</gazebo>
<!-- transmission -->
<transmission name="base_to_second_trans">
<type>transmission_interface/SimpleTransmission</type>
<actuator name="motor1">
<mechanicalReduction>1</mechanicalReduction>
</actuator>
<joint name="base_to_second_joint">
<hardwareInterface>EffortJointInterface</hardwareInterface>
</joint>
</transmission>
</robot>
<link name="second_link">
<inertial>
<mass value="0.18" />
<inertia ixx="0.0002835" ixy="0.0" ixz="0.0" iyy="0.0002835" iyz="0.0" izz="0.000324" />
</inertial>
<origin rpy="0.0 0.0 0.0" xyz="0.0 0.0 0.0" />
<collision>
<geometry>
<box size="0.05 0.05 0.15" />
</geometry>
</collision>
<visual>
<geometry>
<box size="0.05 0.05 0.15" />
</geometry>
</visual>
</link>

HUMAN AI ROBOTICS
31
메니퓨레이션시뮬레이션
힘으로동작시켜보기
모델을선택후> Apply Force and Torgue 선택
힘(Force)와토크(Torque) 설정후Play 버튼

![Image 74](../../assets/images/ros/projects/gazebo/img_031_074.webp)


HUMAN AI ROBOTICS
32
World

HUMAN AI ROBOTICS
33
.world 파일
..
•Gazebo 시뮬레이션환경을정의하는파일입니다.
•여러개의모델(로봇, 지형, 센서등)을포함할수있습니다.
•.sdf 파일을불러오는역할을합니다. 
<?xml version="1.0" ?>
<sdf version="1.6">
<world name="my_simulation_world">
<!-- 기본지면추가-->
<include>
<uri>model://ground_plane</uri>
</include>
<!-- 조명추가-->
<include>
<uri>model://sun</uri>
</include>
<!-- 로봇모델추가(외부SDF 파일포함) -->
<include>
<uri>model://my_robot</uri>
</include>
</world>
</sdf>
Gazebo의환경(월드, 조명, 지면, 로봇, 센서등) 을정의
<include> 태그를사용하여외부모델(.sdf) 을불러옴

HUMAN AI ROBOTICS
34
.sdf 파일
..
단일개체(로봇, 센서, 지형등)를정의하는파일입니다.
로봇의링크, 조인트, 센서, 물리적특성등을포함합니다.
.world 파일내에서불러올수도있고, 개별적으로실행할수도있습니다.
<?xml version="1.0" ?>
<sdf version="1.6">
<model name="my_robot">
<static>false</static>
<link name="base_link">
<visual name="visual">
<geometry>
<box>
<size>0.5 0.5 0.5</size>
</box>
</geometry>
</visual>
<collision name="collision">
<geometry>
<box>
<size>0.5 0.5 0.5</size>
</box>
</geometry>
</collision>
</link>
</model>
</sdf>

HUMAN AI ROBOTICS
35
가제보모델
..
Gazebo는기본적으로~/.gazebo/models/ 디렉터리를모델경로로인식
mkdir -p ~/.gazebo/models/my_custom_model
모델폴더구조

![Image 79](../../assets/images/ros/projects/gazebo/img_035_079.webp)


HUMAN AI ROBOTICS
36
.world vs .sdf 핵심차이점
.world 파일을실행하려면ROS2의gazebo_ros 패키지를사용합니다. 
..
ros2 launch gazebo_ros gzserver.launch.py world:=/absolute/path/to/my_world.world

![Image 81](../../assets/images/ros/projects/gazebo/img_036_081.webp)


HUMAN AI ROBOTICS
37
..
Gazebo의.world 파일에서특정모델을직접지정하는방법
특정모델을.world 파일에서지정하는방법
예를들어, TurtleBot3를포함한커스텀월드를생성하려면다음과같은.world 파일을작성합니다.
<?xml version="1.0" ?>
<sdf version="1.6">
<world name="custom_world">
<!-- 바닥평면-->
<include>
<uri>model:ground_plane</uri>
</include>
<!-- 태양조명-->
<include>
<uri>model:sun</uri>
</include>
<!-- TurtleBot3 로봇추가-->
<include>
<uri>model:turtlebot3_burger</uri>
<pose>0 0 0.1 0 0 0</pose>
</include>
</world>
</sdf>

HUMAN AI ROBOTICS
38
…
Gazebo의.world 파일에서특정모델을직접지정하는방법
특정.world 파일을포함하는방법
다른.world 파일을현재월드에포함하려면<include> 태그안에filename 속성을사용합니다.
예를들어, 기존default.world를custom.world에서포함하려면:
<?xml version="1.0" ?>
<sdf version="1.6">
<world name="custom_world">
<!-- 기존default.world 포함-->
<include>
<uri>file://path/to/default.world</uri>
</include>
</world>
</sdf>

HUMAN AI ROBOTICS
39
…
Gazebo의.world 파일에서특정모델을직접지정하는방법
모델파일의위치확인및추가
Gazebo는기본적으로/usr/share/gazebo-11/models/ 디렉터리에서모델을찾습니다.
사용자지정모델을사용하려면GAZEBO_MODEL_PATH를설정해야합니다. 
<include>
<uri>model:my_custom_robot</uri>
</include>
직접.world 파일을실행하는방법
저장한.world 파일을실행하려면
ros2 launch gazebo_ros gzserver.launch.py world:=/absolute/path/to/my_custom_world.world

HUMAN AI ROBOTICS
40
SDF(Scenario Description Format)

HUMAN AI ROBOTICS
41
가제보이해
SDF(Scenario Description Format, Simulation Description Format)
SDF: Gazebo에서로봇, 센서, 환경등을정의하는XML 기반의파일형식입니다. 
SDF는URDF보다더정밀한시뮬레이션을지원하며, Gazebo의물리엔진과긴밀하게연결됩니다.
ROS2와함께사용하면로봇의구조, 물리적특성, 센서모델등을정의하고시뮬레이션환경을설정할수있습니다.
SDF 주요요소
1) <world> - 월드정의
월드는Gazebo에서시뮬레이션할전체환경을정의하는요소입니다.
<model> - 로봇및오브젝트정의
•로봇이나오브젝트를정의하는요소로, <link>, <joint> 등을포함할수있습니다.
•static이true이면해당오브젝트는고정된상태가됩니다.
<link> - 모델의물리적요소
•로봇의구성요소(바퀴, 몸체등) 또는오브젝트의물리적특성을정의합니다.
•<collision>과<visual>을포함할수있습니다.

HUMAN AI ROBOTICS
42
가제보이해
SDF
SDF 주요요소
<joint> - 링크간연결
•링크들사이의구동방식(회전, 이동)을정의하는요소입니다.
•type="revolute"는회전조인트, type="prismatic"는선형조인트입니다.
<sensor> - 센서모델정의
•카메라, LIDAR, IMU 등의센서를정의할수있습니다.
<include> - 외부모델추가
•Gazebo의기본모델을불러오거나외부SDF 파일을로드할때사용됩니다.
ros2 launch gazebo_ros gazebo.launch.py world:=/path/to/my_world.sdf

HUMAN AI ROBOTICS
43
SDF
Sdf 만들기실습
로봇모델만들기준비
폴더를만들고시작
 cd ~
mkdir –p .gazebo/models/myrobot
cd .gazebo/models/myrobot
vi model.config
<?xml version="1.0"?>
 <model>
   <name>myrobot</name>
   <version>1.0</version>
   <sdf version='1.4'>model.sdf</sdf>
   <author>
     <name>kim rujin</name>
     <email>rujinkim32@gmail.com</email>
   </author>
   <description>project rokey</description>
</model>
model.config

HUMAN AI ROBOTICS
44
SDF
Sdf 파일모델파일
<?xml version='1.0'?>
<sdf version='1.4'>
<model name=“myrobot"> 
<static>false</static>
<link name='link0'> 
<pose>0 0 0.05 0 0 0</pose> 
<collision name='collision'> 
<geometry> 
<box>
<size>.1 .1 .1</size>
</box> 
</geometry>
</collision>
<visual name='visual'>  
<geometry>
<box>
<size>.1 .1 .1</size>
</box>
</geometry>
</visual>
</link>
<link name="link1">
<pose>0 0.1 0.125 0 0 0</pose>
<collision name="collision">
<geometry>
<box>
<size>.05 .3 .05</size>
</box>
</geometry>
</collision>
<visual name="visual">
<geometry>
<box>
<size>.05 .3 .05</size>
</box>
</geometry>
</visual>
</link>
<joint type="revolute" name="joint0">
<pose>0 0 0 0 0 0</pose>
<child>link0</child>
<parent>world</parent>
<axis>
<xyz>0 0 0</xyz>
</axis>
</joint>
<joint type="revolute" name="joint1">
<pose>0 -0.1 0 0 0 0</pose>
<child>link1</child>
<parent>link0</parent>
<axis>
<limit>
<lower>-1</lower>
<upper>1</upper>
</limit>
<xyz>0 0 10</xyz>
</axis>
</joint>
</model>
</sdf>
Model.sdf
static은이모델이움직이는것인지아닌지를표시,앞으로움직일'로봇'인지바닥위에놓여질'장애물'인지를설정. 
True이면이후에플러그인이나파라메터를전달해도움직이 않음.
로봇모델일경우엔false로입력

HUMAN AI ROBOTICS
45
SDF
Sdf 만들기실습
world, static, dynamic 객체

![Image 91](../../assets/images/ros/projects/gazebo/img_045_091.webp)


![Image 92](../../assets/images/ros/projects/gazebo/img_045_092.webp)


![Image 93](../../assets/images/ros/projects/gazebo/img_045_093.webp)

HUMAN AI ROBOTICS
46
SDF
Inertial
<inertial>
<mass value="2.275"/>
<origin rpy="0 0 0" xyz="0.0 0.0 0.25"/>
<inertia ixx="0.049443313556" ixy="0.0" ixz="0.0" iyy="0.049443313556" iyz="0.0" izz="0.004095"/>
</inertial>
Gazebo는로봇부품(즉, 링크)의무게와관성을알아야하는데, 이는이무게가어떻게분포되는지를측정
effort로봇에적용할수있는최대힘(또는토크)을결정하는데, 이는주로모터의힘에
따라달라집니다.
태그<origin>는각각링크의질량중심또는중력중심을정의합니다. 
이는질량에따라가중치가부여된시스템의모든부분의평균위치입니다. 가속도를
계산할때유용한속성입니다.
HUMAN AI ROBOTICS
47
실습과제2 –라이다시뮬레이션

HUMAN AI ROBOTICS
48
라이다시뮬레이션
라이다정보시각화
라이다(LIDAR/LiDAR, light detection and ranging” 또는“laser imaging, detection, and ranging”의약자))는레이저
펄스를쏘고반사되어돌아오는시간을측정하여반사체의위치좌표를측정하는레이다시스템
2D LiDAR는관찰지점으로부터2차원상의평면정보를제공합니다. 
즉센서와평행한평면을기준으로물체와의거리가얼마나떨어져있는지확인
![Image 100](../../assets/images/ros/projects/gazebo/img_048_100.webp)


HUMAN AI ROBOTICS
49
라이다시뮬레이션
패키지만들기, 기본모델만들기
라이다기능을모델에추가하고gazebo에서실행하고그정보를Rviz2에서시각화확인할수있다.
$ cd ~/sim_ws 
$ cp src/urdf_tutorial/urdf/robot_3.xacro src/urdf_tutorial/urdf/robot_4.xacro
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
import xacro
def generate_launch_description():
use_sim_time = LaunchConfiguration("use_sim_time")
pkg_path = os.path.join(get_package_share_directory("urdf_tutorial"))
xacro_file = os.path.join(pkg_path, "urdf", "robot_4.xacro")
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
]
)
Robot_state_publisher는robot_description을토픽으로

HUMAN AI ROBOTICS
50
라이다시뮬레이션
런치파일만들기
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
def generate_launch_description():
package_name = "urdf_tutorial"
rsp = IncludeLaunchDescription(
PythonLaunchDescriptionSource(
[os.path.join(get_package_share_directory(package_name), "launch", "robot_4.launch.py")]
),
launch_arguments={"use_sim_time": "true"}.items(),
)
# Include the Gazebo launch file, provided by the gazebo_ros package
gazebo = IncludeLaunchDescription(
PythonLaunchDescriptionSource(
[os.path.join(get_package_share_directory("gazebo_ros"), "launch", "gazebo.launch.py")]
),
)
# Run the spawner node from the gazebo_ros package. 
spawn_entity = Node(
package="gazebo_ros",
executable="spawn_entity.py",
arguments=["-topic", "robot_description", "-entity", "with_robot"],
output="screen",
)
# Launch them all!
return LaunchDescription(
[
rsp,
gazebo,
spawn_entity,
]
)

HUMAN AI ROBOTICS
51
라이다시뮬레이션
패키지빌드후가제보실행
<material name="red">
<color rgba="1 0 0 1"/>
</material>
<!-- LiDAR -->
<joint name="laser_joint" type="fixed">
<parent link="body"/>
<child link="laser_frame"/>
<origin xyz="0.1 0 0.075" rpy="0 0 0"/>
</joint>
<link name="laser_frame">
<visual>
<geometry>
<cylinder radius="0.03" length="0.03"/>
</geometry>
<material name="red"/>
</visual>
<collision>
<geometry>
<cylinder radius="0.03" length="0.03"/>
</geometry>
</collision>
</link>
$ cd ~/sim_ws/
$ colcon build --symlink-install
$ source install/setup.bash
$ ros2 launch urdf_tutorial lidar.launch.py

![Image 104](../../assets/images/ros/projects/gazebo/img_051_104.webp)


HUMAN AI ROBOTICS
52
라이다시뮬레이션
라이다정보모델만들기
‘src/urdf_tutorial/urdf/lidar.xacro’ 파일
◦update_rate: 초당10회정보를제공합니다.
◦samples: 검색구간내에서4개의광선을발사합니다. 
◦min_angle, max_angle: 2D LiDAR가스캔할구간입니다. 
◦range min/max: 2D LiDAR가스캔가능한거리의최소, 최대값입니다.
◦argument: ros에전달할topic 이름입니다.
◦output_type: 출력형식입니다.
◦frame_name: 2D LiDAR가부착된센서이름입니다.
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">
<gazebo reference="laser_frame">
<material>Gazebo/Red</material>
<sensor name="laser" type="ray">
<pose>0 0 0 0 0 0</pose>
<visualize>true</visualize>
<update_rate>10</update_rate>
<ray>
<scan>
<horizontal>
<samples>4</samples>
<min_angle>-3.14</min_angle>
<max_angle>3.14</max_angle>
</horizontal>
</scan>
<range>
<min>0.3</min>
<max>12</max>
</range>
</ray>
<plugin name="laser_controller" filename="libgazebo_ros_ray_sensor.so">
<ros>
<argument>~/out:=scan</argument>
</ros>
<output_type>sensor_msgs/LaserScan</output_type>
<frame_name>laser_frame</frame_name>
</plugin>
</sensor>
</gazebo>
</robot>
<xacro:include filename="lidar.xacro"/>
로봇모델에라이다모델추가

HUMAN AI ROBOTICS
53
라이다시뮬레이션
가제보이해
•Gazebo에서‘Insert’ 탭을누르고‘Insert model …’을누른상태로5분정도기다리면설치가능한모델목록이나타납니다.
시뮬레이션을위한월드만들기, 로봇제거후월드저장

![Image 107](../../assets/images/ros/projects/gazebo/img_053_107.webp)


HUMAN AI ROBOTICS
54
라이다시뮬레이션
가제보이해
•목록에서‘with-bot’을선택후마우스메뉴버튼을누른후팝업메뉴에서‘Delete’를눌러서with-bot을제거
•'src/urdf_tutorial/config' 폴더에‘with_robot.world’라는파일명으로저장합니다.

![Image 109](../../assets/images/ros/projects/gazebo/img_054_109.webp)


HUMAN AI ROBOTICS
55
라이다시뮬레이션
RVIZ2 실행하기
$ ros2 launch urdf_tutorial lidar.launch.py world:=src/urdf_tutorial/config/with_robot.world

![Image 111](../../assets/images/ros/projects/gazebo/img_055_111.webp)


![Image 112](../../assets/images/ros/projects/gazebo/img_055_112.webp)


HUMAN AI ROBOTICS
56
카메라시뮬레이션
/scan 토픽확인
•2D LiDAR의samples 수를4에서360으로늘려보고수신되는정보를기반으로키보드로주행을해보는과정
•우선모든터미널에서‘CTRL+C’를눌러서실행중인모든프로그램을종료.
•‘src/urdf_tutorial/urdf/lidar.xacro’ 파일에서‘laser_frame’의samples를360으로변경.
$ cd ~/Workspace/ros_ws/ $ ros2 topic echo /scan

![Image 114](../../assets/images/ros/projects/gazebo/img_056_114.webp)


HUMAN AI ROBOTICS
57
카메라시뮬레이션
시뮬레이선수행하기
•2D LiDAR의samples 수를4에서360으로늘려보고수신되는정보를기반으로키보드로주행을해보는과정
•우선모든터미널에서‘CTRL+C’를눌러서실행중인모든프로그램을종료합니다.
•‘src/urdf_tutorial/urdf/lidar.xacro’ 파일에서‘laser_frame’의samples를360으로변경합니다.
$ colcon build --symlink-install $ ros2 launch urdf_tutorial 
lidar.launch.py world:=src/urdf_tutorial/config/with_robot.world
$ ros2 run teleop_twist_keyboard 
teleop_twist_keyboard

![Image 116](../../assets/images/ros/projects/gazebo/img_057_116.webp)

HUMAN AI ROBOTICS
58
실습과제3- Moveit2

HUMAN AI ROBOTICS
59
Moveit2 실습
Moveit2 실습
https://kolkemboi.medium.com/simulate-6-dof-robot-arm-in-ros2-gazebo-and-moveit2-a171c7e9b0ad
시뮬레이션및시각화를위한Gazebo, 모션계획을위한MoveIt2, 프로그래밍을위한Python을통합하여로봇
개발을위한포괄적인환경을제공
아래링크는내GitHub에있는파일의공개저장소
필수구성요소
Ubuntu 22.04
ROS2 Humble
Gazebo
Moveit2

HUMAN AI ROBOTICS
60
Moveit2 실습
Moveit2 실습
시스템아키텍처
6개DoF 로봇은관절을위한6개관절을특징으로하는로봇팔구성을사용합니다.
ROS 2 아키텍처내에서여러노드를사용하여관절컨트롤러, 센서인터페이스, 모션계획모듈을포함한
시스템의다양한측면을제어합니다.
Gazebo는시뮬레이션환경역할을하며현실적인물리및센서피드백을제공합니다.
Autodesk Fusion을사용하여Gazebo에서시뮬레이션
로봇모델을개발하고ROS2용URDF 내보내기기능을사용하여URDF로내보냈습니다.

![Image 121](../../assets/images/ros/projects/gazebo/img_060_121.webp)


HUMAN AI ROBOTICS
61
Moveit2 실습
Moveit2 실습
시뮬레이션을위해Gazebo로가져왔습니다. 월드링크를추가하여월드의땅에고정
로봇은시뮬레이션된세계에서제어가부족하므로ros2_control을사용하여제어를추가
조인트, 명령및상태인터페이스를정의하고gazebo.launch.py에컨트롤러런처를추가하여모델을생성하고로봇의컨트롤러를시작

![Image 123](../../assets/images/ros/projects/gazebo/img_061_123.webp)


HUMAN AI ROBOTICS
62
Moveit2 실습
Moveit2 실습

![Image 125](../../assets/images/ros/projects/gazebo/img_062_125.webp)

HUMAN AI ROBOTICS
63
Moveit2 실습
Moveit2 실습
MoveIt2를사용한모션플래닝
MoveIt2는모션플래닝및조작작업을위한강력한프레임워크를제공
로봇의운동학모델은MoveIt2와인터페이스되어구성공간에서경로플래닝이가능
Rapidly-exploring Random Trees(RRT)를포함한다양한모션플래닝알고리즘이구현되어충돌없는궤적을생성
HUMAN AI ROBOTICS
64
Moveit2 실습
Moveit2 실습
시스템이어떤링크가충돌하는지에대한계산을줄이기
위해충돌행렬을생성합니다.
HUMAN AI ROBOTICS
65
Moveit2 실습
Moveit2 실습
RRT와KDLkinematic 솔버를사용하여계획그룹을생성합니다. 
이단계에서는Moveit에서제어할링크를선택합니다.

![Image 132](../../assets/images/ros/projects/gazebo/img_065_132.webp)

HUMAN AI ROBOTICS
66
Moveit2 실습
Moveit2 실습
로봇에휴식포즈와시작포즈의두가지포즈를제공합니다.

![Image 135](../../assets/images/ros/projects/gazebo/img_066_135.webp)


HUMAN AI ROBOTICS
67
Moveit2 실습
Moveit2 실습
moveit config 폴더에ros2_control 인터페이스추가

![Image 137](../../assets/images/ros/projects/gazebo/img_067_137.webp)


HUMAN AI ROBOTICS
68
가제보이해
SRDF (Semantic Robot Description Format)
•
URDF와같은로봇의의미론적정보(semantic information)를정의하는XML 파일포맷 
•
주로MoveIt!과같은로봇모션계획소프트웨어에서사용
•
SRDF는로봇의움직임에대한의미론적정보
      - 어떤조인트를그룹으로묶을지, 플래닝그룹, 엔드이펙터정의등
•  플래닝그룹 - 로봇의특정조인트들을그룹화하여모션플래닝을위해사용하는데, 이를SRDF에서정의.
•  자유도제약및제한 - 특정조인트에대한운동범위제한및제약조건을정의.
•  MoveIt!와통합 - 주로MoveIt!에서모션플래닝을위해사용.
▪SRDF
▪SRDF 특징

HUMAN AI ROBOTICS
69
가제보이해
SDF (Simulation Description Format)
•  복잡한시뮬레이션환경지원:
     로봇뿐만아니라전체시뮬레이션환경(장애물, 지형등) 정의
•  다양한물리적특성:
     URDF보다더복잡한물리엔진지원및모델정의가능
     (예: 다양한마찰력, 관성모멘트등을정교하게설정)
•  Gazebo에서주로사용:
     Gazebo 시뮬레이터와통합
     고급물리시뮬레이션을위해설계
▪SDF
<sdf version="1.6">
  <model name="example_robot">
      <link name="base_link">
        <visual>
          <geometry>
            <box size="1 1 1"/>
          </geometry>
        </visual>
        <collision>
          <geometry>
            <box size="1 1 1"/>
          </geometry>
        </collision>
      </link>
      <joint name="joint1" type="revolute">
        <parent>base_link</parent>
        <child>link1</child>
        <axis>
          <xyz>0 0 1</xyz>
        </axis>
      </joint>
  </model>
</sdf>

HUMAN AI ROBOTICS
70
Moveit2 실습
Moveit2 실습
생성된Moveit 파일을RVIZ에서시각화하고로봇과상호작용하며다양한위치에서포즈
Python 스크립트는ROS 2 환경내에서로봇의동작을제어하는데활용
궤적생성, 역운동학계산및피드백제어를위한함수는Python으로구현
이를통해프로그래밍의유연성과ROS 2 노드와의쉬운통합이가능
스크립트는각관절의관절위치에대한6개인수와지속시간에대한2개인수를포함하여8개의인수를필요
Python으로프로그래밍하기
HUMAN AI ROBOTICS
71
Moveit2

HUMAN AI ROBOTICS
72
GAZEBO
Moveit 시스템구조
MoveIt은모션플래닝을위해다양한알고리즘과플러그인기반구조를사용하며, 로봇의경로계획, 제어, 시각화
등의작업을통합하여수행
•로봇모델및환경(URDF, SRDF)
로봇의구조와환경을정의하는파일들을바탕으로MoveIt이로봇과환경을이해하고작업.
•Planning Scene
로봇과환경의상태를유지하고, 충돌감지및환경변화를실시간반영.
•Motion Planning Pipeline
경로를계획하고최적화하며, 키네마틱솔버와충돌감지시스템을통해안전한경로를계산.
•Controller Manager
경로를실제로봇에적용하여움직임을제어.
•Rviz 및사용자상호작용
사용자에게로봇의상태를시각적으로보여주고, 목표를설정하거나경로를모니터링
•Perception과Grasping
환경인식을통해동적으로경로를수정하고, 물체조작.
MoveIt은로봇의모션플래닝, 제어, 시뮬레이션, 충돌감지등을지원하는강력한로봇소프트웨어플랫폼으로, 
ROS(로봇운영체제) 기반에서동작

![Image 144](../../assets/images/ros/projects/gazebo/img_072_144.webp)


HUMAN AI ROBOTICS
73
GAZEBO
Moveit 기능
1. Robot Model (로봇모델)
•MoveIt은로봇의모델을기반으로작업을수행.
•URDF(Unified Robot Description Format) 또는SRDF(Semantic Robot Description Format) 정의.
•URDF는로봇의물리적구조(링크, 조인트등)를정의, SRDF는로봇의키네마틱체인, 그룹화된링크, 
제약사항등을설명.
•모션플래닝, 경로생성, 충돌감지등다양한작업에사용.
2. Motion Planning (모션플래닝)
•OMPL (Open Motion Planning Library)를사용하여다양한알고리즘기반으로경로를계획.
•로봇의목표위치에도달하는최적경로를계산
•이과정에서충돌을피하고, 로봇의운동학적제약을고려.
•사용가능한플래닝알고리즘에는RRT, RRT*, PRM, CHOMP, STOMP, TrajOpt 등

HUMAN AI ROBOTICS
74
GAZEBO
Moveit 기능
3. Kinematics Solver (키네마틱솔버)
•MoveIt은정방향키네마틱스(Forward Kinematics)와역방향키네마틱스(Inverse Kinematics, IK) 솔버를
사용로봇의위치와자세계산.
•정방향키네마틱스는로봇의조인트값을기반으로각링크의위치를계산, 역방향키네마틱스는목표
위치에도달하기위해각조인트의값계산.
•MoveIt은IKFast, KDL 등다양한IK 솔버를지원.
4. MoveIt Setup Assistant
•MoveIt을설정하고URDF 파일을기반으로시스템구성을쉽게할수있도록돕는GUI 도구.
•로봇모델을설정하고, 키네마틱체인및그룹설정, 플래닝그룹설정, 충돌감지설정.
•시뮬레이션및실제로봇에서사용할수있도록MoveIt의주요구성요소들을자동으로생성.

HUMAN AI ROBOTICS
75
GAZEBO
Moveit 기능
5. Motion Planning Pipeline (모션플래닝파이프라인)
•모션플래닝은파이프라인구조로처리. 
•로봇의현재상태와목표상태를입력받아, 플래닝요청시다양한플래닝알고리즘을통해경로계산.
•이파이프라인에는경로필터링, 경로수정, 키네마틱계산, 충돌감지등의단계가포함.
•최종적으로안전한경로를만들어로봇이실행할수있도록명령전달.
6. Controller Manager (컨트롤러매니저)
•MoveIt은플래닝된경로를로봇이실제로따를수있도록로봇컨트롤러와통신.
•ROS 2의controller_manager를통해제어명령을로봇의하드웨어로전송, 로봇이경로따라
동작시킴.
•로봇의조인트트레저(Joint Trajectory Controller)와같은컨트롤러를사용하여경로제어.

HUMAN AI ROBOTICS
76
Moveit 기능
7. Planning Scene (플래닝씬)
•로봇과환경을정의하는데이터구조. 
•로봇모델, 환경의장애물, 그리고이들이상호작용하는방식등을정의.
•로봇의현재상태(포즈, 링크의위치등)와환경의상태를포함하여실시간으로로봇의상태를추적하며, 
충돌감지및모션플래닝에사용.
8. Collision Detection (충돌감지)
•로봇이경로를계획할때주변환경및로봇자신의다른링크와충돌하지않도록확인하는중요한기능
•MoveIt은FCL(Flexible Collision Library)와Bullet 같은충돌감지라이브러리를사용.
•경로계획중에실시간으로충돌여부를감지하고, 충돌을피하는경로생성.
GAZEBO

HUMAN AI ROBOTICS
77
GAZEBO
Moveit 기능
9. Perception (인식)
•카메라또는LIDAR 등의센서데이터를이용해주변환경을인식하고, 이를모션플래닝반영
•Octomap과같은맵핑라이브러리를통해3D 환경에서장애물을감지하고, 로봇의경로계획에
반영.
10. Rviz와의통합
•사용자는Rviz의인터페이스를통해경로계획과시각화를직관적으로수행. 
•move_group은Rviz와상호작용하여실시간경로계획및상태업데이트를처리.

HUMAN AI ROBOTICS
78
TF 이해
ROS에서기본적으로제공해주는메세지타입중, 공간과관련된메세지타입
#!/usr/bin/python
import rospy
import random
import math
from tf.transformations import quaternion_from_euler
from geometry_msgs.msg import PoseStamped
if __name__ == '__main__':
rospy.init_node("tf_test")
pub = rospy.Publisher("pose", PoseStamped, queue_size=1)
r = rospy.Rate(1)
while not rospy.is_shutdown():
msg = PoseStamped()
msg.header.stamp = rospy.Time.now()
msg.header.frame_id = "frame1"
msg.pose.position.x = random.randint(0, 5)
msg.pose.position.y = random.randint(0, 5)
msg.pose.position.z = 0
quat = quaternion_from_euler(
0., 0., math.radians(random.randint(0, 180)))
msg.pose.orientation.x = quat[0]
msg.pose.orientation.y = quat[1]
msg.pose.orientation.z = quat[2]
msg.pose.orientation.w = quat[3]
pub.publish(msg)
r.sleep()
GAZEBO
![Image 152](../../assets/images/ros/projects/gazebo/img_078_152.webp)


HUMAN AI ROBOTICS
79
GAZEBO
TF 이해
tf_broadcaster = 
tf.TransformBroadcaster()
r = rospy.Rate(1)
while not rospy.is_shutdown():
tf_broadcaster.sendTransform(
translation=[10, 10, 0],
rotation=[0., 0., 0., 1],
time=rospy.Time.now(),
child="home",
parent="world"
)
robot.publishPose()
r.sleep()
import rospy
import tf
from geometry_msgs.msg import PoseStamped
class Robot(object):
def __init__(self):
position = PoseStamped()
position.header.frame_id = "home"
position.pose.position.x = -5
position.pose.position.y = 10
position.pose.orientation.w = 1
self.position = position
self.pub = rospy.Publisher("robot_pose", PoseStamped, queue_size=1)
def publishPose(self):
self.position.header.stamp = rospy.Time.now()
self.pub.publish(self.position)
if __name__ == '__main__':
rospy.init_node("tf_pub")
robot = Robot()
r = rospy.Rate(1)
while not rospy.is_shutdown():
robot.publishPose()
r.sleep()

![Image 154](../../assets/images/ros/projects/gazebo/img_079_154.webp)


![Image 155](../../assets/images/ros/projects/gazebo/img_079_155.webp)


HUMAN AI ROBOTICS
80
GAZEBO
터틀봇3 자기위치찾기
#include <ros/ros.h>
#include <geometry_msgs/PoseWithCovarianceStamped.h>
#include <nav_msgs/Odometry.h>
#include <tf/transform_listener.h>
class TurtlebotLocationTracker {
private:
ros::NodeHandle nh;
ros::Subscriber amcl_pose_sub;
ros::Subscriber odom_sub;
tf::TransformListener tf_listener;
void amclPoseCallback(const
geometry_msgs::PoseWithCovarianceStamped::ConstPtr& msg) {
ROS_INFO("AMCL Position:");
ROS_INFO("  Position: (x: %.2f, y: %.2f)", 
msg->pose.pose.position.x, 
msg->pose.pose.position.y);
// 쿼터니언을RPY로변환
tf::Quaternion q(
msg->pose.pose.orientation.x,
msg->pose.pose.orientation.y,
msg->pose.pose.orientation.z,
msg->pose.pose.orientation.w
);
tf::Matrix3x3 m(q);
double roll, pitch, yaw;
m.getRPY(roll, pitch, yaw);
ROS_INFO("  Orientation (yaw): %.2f degrees", yaw * 180.0 / M_PI);
}
void getTFTransform() {
try {
tf::StampedTransform transform;
tf_listener.lookupTransform("/map", "/base_footprint", 
ros::Time(0), transform);
ROS_INFO("TF Transform:");
ROS_INFO("  Position: (x: %.2f, y: %.2f, z: %.2f)", 
transform.getOrigin().x(),
transform.getOrigin().y(),
transform.getOrigin().z());
// 쿼터니언을RPY로변환
tf::Quaternion q = transform.getRotation();
tf::Matrix3x3 m(q);
double roll, pitch, yaw;
m.getRPY(roll, pitch, yaw);
ROS_INFO("  Orientation:");
ROS_INFO("    Roll: %.2f degrees", roll * 180.0 / M_PI);
ROS_INFO("    Pitch: %.2f degrees", pitch * 180.0 / M_PI);
ROS_INFO("    Yaw: %.2f degrees", yaw * 180.0 / M_PI);
} catch (tf::TransformException &ex) {
ROS_ERROR("TF Transform error: %s", ex.what());
}
}
void odometryCallback(const
nav_msgs::Odometry::ConstPtr& msg) {
ROS_INFO("Odometry Position:");
ROS_INFO("  Position: (x: %.2f, y: %.2f, z: %.2f)", 
msg->pose.pose.position.x, 
msg->pose.pose.position.y,
msg->pose.pose.position.z);
// 쿼터니언을RPY로변환
tf::Quaternion q(
msg->pose.pose.orientation.x,
msg->pose.pose.orientation.y,
msg->pose.pose.orientation.z,
msg->pose.pose.orientation.w
);
tf::Matrix3x3 m(q);
double roll, pitch, yaw;
m.getRPY(roll, pitch, yaw);
ROS_INFO("  Orientation:");
ROS_INFO("    Roll: %.2f degrees", roll * 180.0 / M_PI);
ROS_INFO("    Pitch: %.2f degrees", pitch * 180.0 / M_PI);
ROS_INFO("    Yaw: %.2f degrees", yaw * 180.0 / M_PI);
}

HUMAN AI ROBOTICS
81
GAZEBO
터틀봇3 자기위치찾기
public:
TurtlebotLocationTracker() {
// AMCL 포즈구독
amcl_pose_sub = nh.subscribe("/amcl_pose", 10, 
&TurtlebotLocationTracker::amclPoseCallback, this);
// 오도메트리구독
odom_sub = nh.subscribe("/odom", 10, 
&TurtlebotLocationTracker::odometryCallback, this);
}
void run() {
ros::Rate rate(1.0);  // 1Hz로위치업데이트
while (ros::ok()) {
ros::spinOnce();
// TF 변환확인
getTFTransform();
rate.sleep();
}
}
};
int main(int argc, char** argv) {
ros::init(argc, argv, "turtlebot3_location_tracker");
TurtlebotLocationTracker tracker;
tracker.run();
return 0;
}

HUMAN AI ROBOTICS
82
GAZEBO
FT로서로위치추종
두개의터틀봇이서로를따라가도록한다.
#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <turtlesim/Pose.h>
#include <tf/transform_broadcaster.h>
#include <tf/transform_listener.h>
#include <cmath>
class TurtleFollower {
private:
ros::NodeHandle nh;
ros::Publisher turtle1_vel_pub;
ros::Publisher turtle2_vel_pub;
ros::Subscriber turtle1_pose_sub;
ros::Subscriber turtle2_pose_sub;
tf::TransformBroadcaster br;
tf::TransformListener listener;
turtlesim::Pose turtle1_pose;
turtlesim::Pose turtle2_pose;
void turtle1PoseCallback(const turtlesim::Pose::ConstPtr& msg) {
turtle1_pose = *msg;
// Broadcast turtle1's transform
tf::Transform transform;
transform.setOrigin(tf::Vector3(msg->x, msg->y, 0.0));
tf::Quaternion q;
q.setRPY(0, 0, msg->theta);
transform.setRotation(q);
br.sendTransform(tf::StampedTransform(transform, ros::Time::now(), "world", "turtle1"));
}
void turtle2PoseCallback(const turtlesim::Pose::ConstPtr& msg) {
turtle2_pose = *msg;
// Broadcast turtle2's transform
tf::Transform transform;
transform.setOrigin(tf::Vector3(msg->x, msg->y, 0.0));
tf::Quaternion q;
q.setRPY(0, 0, msg->theta);
transform.setRotation(q);
br.sendTransform(tf::StampedTransform(transform, ros::Time::now(), "world", "turtle2"));
}
double getDistance(double x1, double y1, double x2, double y2) {
return std::sqrt(std::pow(x1 - x2, 2) + std::pow(y1 - y2, 2));
}
double getAngleBetweenPoses(const turtlesim::Pose& pose1, const turtlesim::Pose& pose2) {
return std::atan2(pose2.y - pose1.y, pose2.x - pose1.x);
}
public:
TurtleFollower() {
// Subscribers for pose
turtle1_pose_sub = nh.subscribe("/turtle1/pose", 10, &TurtleFollower::turtle1PoseCallback, this);
turtle2_pose_sub = nh.subscribe("/turtle2/pose", 10, &TurtleFollower::turtle2PoseCallback, this);
// Publishers for velocity
turtle1_vel_pub = nh.advertise<geometry_msgs::Twist>("/turtle1/cmd_vel", 10);
turtle2_vel_pub = nh.advertise<geometry_msgs::Twist>("/turtle2/cmd_vel", 10);
}

HUMAN AI ROBOTICS
83
GAZEBO
FT로서로위치추종
int main(int argc, char** argv) {
ros::init(argc, argv, "turtle_follower");
TurtleFollower follower;
ros::Rate rate(10);
while (ros::ok()) {
ros::spinOnce();
follower.update();
rate.sleep();
}
return 0;
}
void update() {
// Turtle2 follows Turtle1
if (turtle1_pose.x != 0 && turtle2_pose.x != 0) {
double distance = getDistance(turtle1_pose.x, turtle1_pose.y, 
turtle2_pose.x, turtle2_pose.y);
double target_angle = getAngleBetweenPoses(turtle2_pose, turtle1_pose);
geometry_msgs::Twist cmd_vel;
// Linear velocity proportional to distance
cmd_vel.linear.x = distance * 0.5;
// Angular velocity to align with target
double angle_diff = target_angle - turtle2_pose.theta;
// Normalize angle
while (angle_diff > M_PI) angle_diff -= 2 * M_PI;
while (angle_diff < -M_PI) angle_diff += 2 * M_PI;
cmd_vel.angular.z = angle_diff * 1.0;
// Limit velocities
cmd_vel.linear.x = std::min(cmd_vel.linear.x, 1.0);
cmd_vel.angular.z = std::min(std::max(cmd_vel.angular.z, -1.5), 1.5);
turtle2_vel_pub.publish(cmd_vel);
}
}
};

HUMAN AI ROBOTICS
84
수고하셨습니다.


