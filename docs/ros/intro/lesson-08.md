# 강의_3기_ROS2입문_8차시


ROS2 프로그래밍입문(8차시)
8. ROS2 복습_2


▶ROS2 복습_2
1.  인터페이스패키지생성및설계
2.  인터페이스프로그래밍실습
Contents
00
00


01
01
토픽, 서비스, 액션인터페이스
패키지설계
▶패키지구성

02
02
•
Node 클래스의create_publisher 함수를사용
하여퍼블리셔선언
•
토픽타입: ArithmeticArgument
•
토픽이름: 'arithmetic_argument
•
'QoS 설정: 이전에설정한QOS_RKL10V 사용
▶ararithmetic_argument_publisher 선언
▶create_timer 함수를이용하여1초마다publish_random_arithmetic_arguments 함수실행설정
▶create_publisher에서의설정들은퍼블리시를위한기본설정
▶실제토픽발행이이루어지는부분은publish_random_arithmetic_arguments 함수
토픽프로그래밍
토픽퍼블리셔코드

![Image 4](../../assets/images/ros/intro/lesson-08/img_004_004.webp)

02
•
타이머콜백함수로1초마다실행
•
msg 변수를ArithmeticArgument() 클래스로생성(지난‘토픽, 서
비스, 액션인터페이스’ 강좌에서작성한msg 인터페이스활용)
•
토픽생성시간을get_clock().now().to_msg()로가져와
msg.stamp에기록
•
랜덤함수로0~9 사이의숫자를float로변환하여
msg.argument_a와msg.argument_b에저장
▶publish_random_arithmetic_arguments 함수
03
•
실제로토픽발행이이루어지는함수로우리가발행시간
및변수a, b를저장한msg 메시지를퍼블리시한다는의미
▶arithmetic_argument_publisher.publish(msg) 함수
•
get_logger().info() 를사용하여디버깅목적으로변수a, b 
값을터미널에표시
▶로그출력
토픽프로그래밍
토픽퍼블리셔코드
02
04
토픽프로그래밍
토픽퍼블리셔코드
•
토픽퍼블리셔노드와마찬가지로Node 클래스상속
•
생성자에서'calculator'라는이름으로노드초기화
•
토픽서브스크라이버, 서비스서버, 액션서버를포함
하여코드가길기때문에전체코드는생략
•
여기서는토픽서브스크라이버관련코드만설명
•
Calculator 클래스설정
•
QoS 설정
•
QoSProfile 클래스를이용하여토픽서브스크라이버의
QoS 설정적용
•
QoS 설정값: RELIABLE, KEEP_LAST, DEPTH 10, VOLATILE 
(토픽퍼블리셔와동일설정)
•
QoS에대한자세한내용은'DDS의QoS(Quality of 
Service)' 강좌참고
02
05
•
제일중요한설정으로Node 클래스의create_subscription
함수를이용하여서브스크라이버로선언
•
get_arithmetic_argument라는콜백함수를지정하여퍼블
리셔로부터메시지를서브스크라이브할때마다실행되
는함수를지정
•
ReentrantCallbackGroup으로callback_group을지정하여
콜백함수를병렬로실행할수있게해주며뒤에서설정
•
이후설명할MultiThreadedExecutor와함께사용됨
•
arithmetic_argument_subscriber 설정
•
callback_group
•
MutuallyExclusiveCallbackGroup이기본설정으로사용됨
•
MutuallyExclusiveCallbackGroup: 한번에하나의콜백함
수만실행하도록제한
•
ReentrantCallbackGroup: 제한없이콜백함수를병렬로
실행가능
토픽프로그래밍
토픽서브스크라이버코드
02
06
토픽프로그래밍
토픽서브스크라이버코드
•
콜백함수인이함수는'arithmetic_argument'이라는토픽
이름에ArithmeticArgument 타입의메시지를서브스크라
이브하게되면실행됨
•
서브스크라이브한msg의argument_a와argument_b를
멤버변수에저장하고, get_logger().info() 함수를이용하여
토픽으로받은시간, 변수a, b 값을화면에표시
•
get_arithmetic_argument
02
07
▶entry_points 설정
•
setup.py의entry_points는실행가능한콘솔스크립트이름과호출함수를지정
•
'ros2 run' 명령어로각노드를실행할수있도록4개의노드entry_points 추가
▶노드파일경로
•
argument 노드: ex_calculator 패키지의arithmetic 폴더의argument.py main문에실행코드포함
•
operator 노드: ex_calculator 패키지의arithmetic 폴더의operator.py main문에실행코드포함
•
calculator 노드: ex_calculator 패키지의calculator 폴더의main.py main문에실행코드포함
•
checker 노드: ex_calculator 패키지의checker 폴더의main.py main문에실행코드포함
토픽프로그래밍
노드실행코드

02
08
▶argument 노드
•
main 함수로rclpy.init를이용하여초기화
•
Argument 클래스를argument라는이름으로
생성
•
rclpy.spin 함수를이용하여생성한노드를spin 
시켜지정된콜백함수실행
•
종료(ctrl + c)와같은인터럽트시그널예외상
황에서는argument를소멸시키고
rclpy.shutdown 함수로노드를종료
토픽프로그래밍
노드실행코드
02
토픽프로그래밍
노드실행코드
▶calculator 노드초기화
•
rclpy.init를이용하여ROS2 초기화
•
Calculator 클래스를calculator라는이름으로생성
•
MultiThreadedExecutor를사용하여4개스레드로구성된executor 생성
▶MultiThreadedExecutor 설정
•
스레드풀(thread pool)을사용하여콜백을병렬로실행
•
num_threads로스레드수를지정가능
•
콜백을병렬로처리가능하여ReentrantCallbackGroup과함께사용시병렬실행
지원
▶콜백함수의병렬처리설정
•
create_subscription(), create_service(), ActionServer(), create_timer() 등의함수로설정
된콜백함수들의병렬처리가능
▶executor와노드실행
•
calculator 노드를MultiThreadedExecutor에추가
•
executor.spin()으로노드를실행하여지정된콜백함수실행가능’
▶종료처리
•
인터럽트시그널(Ctrl + C) 발생시, executor, calculator의액션서버(별도소멸
필요), calculator 노드를소멸
•
rclpy.shutdown으로노드를종료
09

![Image 18](../../assets/images/ros/intro/lesson-08/img_011_018.webp)


03
10
서비스프로그래밍
서비스클라이언트/서버


![Image 19](../../assets/images/ros/intro/lesson-08/img_012_019.webp)

03
서비스프로그래밍
서비스서버코드
11
src/ex_calculator/ex_calculator/calculator/calculator.py
▶calculator 노드초기화
•
변수(a, b)와operator 노드로부터요청값으로받은연산자
를이용해계산수행
•
연산결과를operator 노드에서비스응답값으로전송
▶서비스서버설정코드
•
서비스서버선언: arithmetic_service_server를Node 클래스
의create_service 함수로선언
•
서비스타입: ArithmeticOperator
•
서비스이름: 'arithmetic_operator’
•
콜백함수: get_arithmetic_operator (서비스요청시실행)
•
callback_group 설정: 멀티스레드병렬콜백함수실행지원
•
콜백을병렬로처리가능하여ReentrantCallbackGroup과함께
사용시병렬실행지원
▶콜백함수역할
•
콜백함수인get_arithmetic_operator이실제서비스요청에
해당되는특정수행코드가수행되는부분


![Image 21](../../assets/images/ros/intro/lesson-08/img_013_021.webp)


03
서비스프로그래밍
서비스서버코드
12
src/ex_calculator/ex_calculator/calculator/calculator.py
▶get_arithmetic_operator 함수
•
매개변수:
•
request와response는ArithmeticOperator() 클래스로생성된인터
페이스
•
request: 서비스요청데이터
•
response: 서비스응답데이터
▶함수의역할
•
서비스요청시실행되는콜백함수
•
request에서받은연산자와, 토픽서브스크라이버가전달받아
저장한변수(a, b)를사용해연산수행
•
연산결과를서비스응답값(response)으로반환
▶연산과정
•
request.arithmetic_operator를calculate_given_formula 함수에
전달하여연산수행연산결과를response.arithmetic_result에
저장
•
관련수식을**get_logger().info()**를통해문자열로출력하여
화면에표시


![Image 22](../../assets/images/ros/intro/lesson-08/img_014_022.webp)


03
서비스프로그래밍
서비스클라이언트코드
13
src/ex_calculator/ex_calculator/arithmetic/operator.py
▶Operator 클래스초기화
•
rclpy.node 모듈의Node 클래스상속
•
생성자에서노드이름을'operator'로초기화
▶arithmetic_service_client 설정
•
Node 클래스의create_client 함수를이용하여서비스클라이언트로선언
•
서비스의타입: ArithmeticOperator(서비스서버와동일)로선언하였고
•
서비스이름: ‘arithmetic_operator’로선언하였다
▶wait_for_service 함수
•
서비스요청가능여부를위해0.1초간격으로서비스서버가실행되어있는지확인


![Image 23](../../assets/images/ros/intro/lesson-08/img_015_023.webp)


03
서비스프로그래밍
서비스클라이언트코드
14
src/ex_calculator/ex_calculator/arithmetic/operator.py
▶서비스클라이언트의목적: 서비스서버에게연산에필요한연산자를전달
▶서비스요청설정: 서비스인터페이스ArithmeticOperator.Request() 클래스로
service_request를선언후random.randint() 함수를이용하여특정연산자를
self.request의arithmetic_operator 변수에저장
▶send_request 함수: 실질적인서비스클라이언트의실행코드로서비스요청값을서버에
보내고응답값을수신
▶call_async(self.request) 함수로서비스요청수행
▶서비스상태및응답값을담은futures를반환


![Image 24](../../assets/images/ros/intro/lesson-08/img_016_024.webp)


03
서비스프로그래밍
서비스클라이언트노드실행코드
15
src/ex_calculator/ex_calculator/arithmetic/operator.py
•
rclpy.init를이용하여초기화
•
Operator 클래스를operator라는이름으로생성한
후future = operator.send_request()로서비스요청
을전송후응답값수신
•
rclpy.spin_once 함수로노드를주기적으로spin시켜
지정된콜백함수가실행
•
각spin마다노드의콜백함수가실행
•
서비스응답값을수신시future의done 함수를이용
해요청값을제대로받았는지확인
•
결과값을service_response = future.result()로저장
•
get_logger().info() 함수를이용하여화면에서비스
응답값에해당되는연산결과값을표시
•
‘ctrl + c'와같은인터럽트시그널예외상황에서
operator를소멸시키고rclpy.shutdown 함수로노드
를종료


![Image 25](../../assets/images/ros/intro/lesson-08/img_017_025.webp)


03
서비스프로그래밍
서비스클라이언트노드실행코드
16
src/ex_calculator/ex_calculator/arithmetic/operator.py
•
서비스클라이언트는한번실행후종료되는
방식으로, 토픽과같은지속적인수행은없음
•
다만, 예제에서는원하는시점에서비스요청
을다시보낼수있도록user_trigger 변수와
input(＇xxxxx＇)을사용해반복실행가능하
게구성
•
최초1회에한해서사용자입력없이바로임
의의연산자를서비스요청값으로송신
•
그이후노드가종료되기전까지, 사용자의입
력을받을때마다임의의연산자를랜덤으로
선택해서비스요청값으로송신
•
즉. 최초요청후서비스재요청이필요할경우, 
터미널창에서엔터키를눌러operator 실행
•
연산자선택은사칙연산자(+, -, * , /)  중하나
가랜덤으로선택되어송신됨


![Image 26](../../assets/images/ros/intro/lesson-08/img_018_026.webp)


04
액션프로그래밍
액션클라이언트/서버
17
다음그림과같은액션목표(action goal)를지정하는액션클라이언트와액션목표를받아특
정태스크를수행하면서중간결과값에해당되는액션피드백(action feedback)과최종결과값
에해당되는액션결과(action result)를전송하는액션서버를작성해볼것이다.


![Image 27](../../assets/images/ros/intro/lesson-08/img_019_027.webp)


![Image 28](../../assets/images/ros/intro/lesson-08/img_019_028.webp)


04
액션프로그래밍
액션서버코드
18
src/ex_calculator/ex_calculator/calculator/calculator.py
▶arithmetic_action_server : rclpy.action
모듈의ActionServer 클래스를이용하여
액션서버로선언
•
액션타입: ArithmeticChecker
•
액션이름: 'arithmetic_checker’
•
콜백함수: execute_checker(액션클라이언트로
부터액션목표를받으면실행됨)
•
멀티스레드병렬콜백함수실행을위한
callback_group 설정적용
▶이러한설정들은액션서버를위한기본
설정이고실제액션목표를받은후에
실행되는콜백함수는execute_checker
함수임을알아두자


![Image 29](../../assets/images/ros/intro/lesson-08/img_020_029.webp)


04
액션프로그래밍
액션서버코드
19
src/ex_calculator/ex_calculator/calculator/calculator.py
▶goal_handle 매개변수
•
rclpy.action 모듈의ServerGoalHandle 클래스로
생성된액션상태처리용으로execute, succeed, 
abort, canceled 등액션상태에따른관련함수
호출가능
•
publish_feedback을통해피드백퍼블리시가능
Get_logger().info() 함수를이용해터미널창에
액션서버시작표시
ArithmeticChecker.Feedback()을통해액션피
드백을보낼feedback_msg 변수선언
실제피드백에해당되는
feedback_msg.formula와연산합계값을담을
total_sum 변수초기화
goal_handle를이용하여
goal_handle.request.goal_sum에서액션목표
값을불러옴
▶
▶
▶
▶


![Image 30](../../assets/images/ros/intro/lesson-08/img_021_030.webp)


04
액션프로그래밍
액션서버코드
20
src/ex_calculator/ex_calculator/calculator/calculator.py
▶
•
total_sum: argument_result(매번계산되는
연산결과값)를누적한합계
액션목표값(goal_sum)과total_sum이
액션목표값(goal_sum)을넘을때까지
연산식(argument_formula)을액션피드
백(feedback_msg.formula)에저장
▶피드백값은디버깅을위해
get_logger().info()을통해터미널창에출
력후goal_handle.publish_feedback() 함
수를통해액션클라이언트로전송

04
액션프로그래밍
액션서버코드
21
src/ex_calculator/ex_calculator/calculator/calculator.py
▶액션목표를달성했다는상태전환함수인
goal_handle.succeed()를실행시켜액션
클라이언트에게현재의액션상태를알림
▶액션결과값인all_formula에계산식전체
를저장하고total_sum에연산합계를저
장하여액션결과값인result은리턴

04
액션프로그래밍
액션서버실행코드
22
src/ex_calculator/ex_calculator/calculator/main.py
▶액션서버인calculator 노드는토픽서브
스크라이버, 서비스서버, 액션서버를역
할을하는복합기능의노드
▶해당코드에대한설명은토픽프로그래밍
(Python) 강좌참조

04
액션프로그래밍
액션클라이언트코드
23
src/ex_calculator/ex_calculator/checker/checker.py
▶Checker 클래스
•
rclpy.node 모듈의Node 클래스를상속
•
생성자에서노드이름을‘checker'로초기화
▶액션클라이언트에서수행하는액션목표
는토픽과달리, 필요시에만비정기적으로
실행됨
▶여기서는예시를위해액션목표를main 
함수에서한번만실행
▶rclpy.action모듈의ActionClient 클래스
이용하여액션클라이언트선언
•
액션타입: ArithmeticChecker
•
액션이름: 'arithmetic_checker’

04
액션프로그래밍
액션클라이언트코드
24
src/ex_calculator/ex_calculator/checker/checker.py
▶send_goal_total_sum 함수
•
액션목표를액션서버에게전송하고, 
액션피드백및결과값을받기위한
콜백함수지정
▶액션클라이언트가액션서버에연결
시도를함
▶연결에문제가있을때에while문을
반복하게되고문제없이연결되었을
때에는다음구문으로넘어감
04
액션프로그래밍
액션클라이언트코드
25
src/ex_calculator/ex_calculator/checker/checker.py
▶액션메시지설정
•
ArithmeticChecker.Goal() 클래스로액션메시
지(goal_msg) 선언
•
goal_msg.goal_sum으로액션목푯값설정
▶비동기액션전송및피드백설정
•
ActionClient 클래스의send_goal_async 함수
를이용해설정해둔액션메시지를매개변
수로전달
•
액션피드백을수신을위한콜백함수로
get_arithmetic_action_feedback 지정
▶액션결과수신설정
•
send_goal_async으로선언된비동기작업
(future task)인send_goal_future의
add_done_callback 함수를통해액션결과값
을받을때사용할콜백함수로
get_arithmetic_action_goal를선언
1. 액션클라이언트선언: arithmetic_action_client
2. 액션목푯값전달함수선언: send_goal_future
3. 액션피드백값콜백함수선언: get_arithmetic_action_feedback
4. 액션상태값콜백함수선언: get_arithmetic_action_goal
5. 액션결과값콜백함수선언: get_arithmetic_action_result


![Image 37](../../assets/images/ros/intro/lesson-08/img_027_037.webp)


04
액션프로그래밍
액션클라이언트코드
26
src/ex_calculator/ex_calculator/checker/checker.py
▶액션피드백값콜백함수
•
액션피드백을액션서버로부터전달받
으면get_arithmetic_action_feedback 콜백
함수실행
•
피드백인feedback_msg.feedback.formula
값을받아get_logger().info()으로터미널창
에출력
▶액션상태값콜백함수
•
비동기작업(future task)으로생성된
send_goal_future에대해add_done_callback
함수를사용해콜백함수설정
•
이콜백함수는액션서버가액션목푯값을
수신했을때Goal State Machine의상태가
accepted인지확인하여처리
•
액션목푯값을문제없이전달된경우, 액션
결과를받을콜백함수를
get_arithmetic_action_result로설정


![Image 38](../../assets/images/ros/intro/lesson-08/img_028_038.webp)


04
액션프로그래밍
액션클라이언트코드
27
src/ex_calculator/ex_calculator/checker/checker.py
▶앞서지정한"액션결과값콜백함수"
는비동기future task로현재의상태값
(status)과결과값(result)을수신
▶상태값이STATUS_SUCCEEDED 일때
액션서버로부터전달받은액션결과값
인계산식(action_result.all_formula)과
연산합계(action_result.total_sum)를
터미널창에출력


![Image 39](../../assets/images/ros/intro/lesson-08/img_029_039.webp)


04
액션프로그래밍
액션클라이언트노드실행코드
28
src/ex_calculator/ex_calculator/checker/main.py
▶main 함수실행코드:
•
rclpy.init를통해ROS2 노드초기화
•
Checker 클래스를checker라는이름으로생성
•
액션목푯값을전달하는send_goal_total_sum 함수실행
▶실행인자(args.goal_total_sum) 사용
•
프로그램의실행시인자를사용해사용자가노드를실행
시킬때액션목푯값을설정가능.
•
목표값이지정되지않았을경우기본값으로50이입력됨
•
실행인자에대한자세한설명은추후강좌에서다룰예정
▶콜백함수실행및유지
•
rclpy.spin 함수를이용하여rclpy의콜백함수가지속적으로
실행되도록설정
▶종료및자원해제
•
종료시('Ctrl + c'와같은인터럽트시그널) checker 객체
소멸및rclpy.shutdown 함수로노드종료
•
추가적으로토픽이나서비스와는달리액션클라이언트는
'checker.arithmetic_action_client.destroy()' 와같이별도로소
멸시켜야함


![Image 40](../../assets/images/ros/intro/lesson-08/img_030_040.webp)


05
파라미터프로그래밍
파라미터
29
우리는이전강좌에서토픽, 서비스, 액션관련프로그래밍을익히기위하여argument, operator, calculator, 
checker 노드를작성해보았다. 이들노드중에서다음그림과같이argument 노드와calculator 노드는파
라미터를사용하고있다. argument 노드는QoS 설정과랜덤으로생성되는변수a, b의랜덤생성범위를파
라미터를이용했었고calculator 노드는QoS 설정을사용하였다. 우리는여기서argument 노드에서사용되
는파라미터에대해자세히알아볼것이다.


![Image 41](../../assets/images/ros/intro/lesson-08/img_031_041.webp)


![Image 42](../../assets/images/ros/intro/lesson-08/img_031_042.webp)


05
파라미터프로그래밍
파라미터설정
30
1.
declare_parameter 함수
2.
get_parameter 함수
3.
add_on_set_parameters_callback 함수
▶argument 노드에서파라미터를선언하고파라미터값이변경되는함수에대해
자세히알아보자
▶Argument 클래스의생성자부분에서다음과같은코드가있다. ROS2에서파라
미터를사용하려면하기와같이크게3가지의요소가필요
▶1번의declare_parameter 함수는노드에서사용할파라미터의고유이름을지
정하고초깃값설정(파라미터에대한설명이들어가는descriptor은생략함)
▶2번의get_parameter 함수는노드에서사용할파라미터의파라미터고유이름
을이용해불러옴. 이는주로launch 파일에서선언된*.yaml 형태의파라미터
파일의값을불러오는데사용됨
▶3번의add_on_set_parameters_callback 함수는서비스형태로파라미터변경
요청이있을때사용되는함수로지정된콜백함수를호출


05
파라미터프로그래밍
파라미터설정
31
src/ex_calculator/ex_calculator/checker/main.py
▶파라미터선언및초기설정
•
declare_parameter 함수로'max_random_num'과
같은파라미터선언
•
노드실행시get_parameter 함수가지정된파라
미터파일에서초깃값을불러와설정
▶파라미터변경요청처리
•
파라미터변경요청발생시
add_on_set_parameters_callback을통해지정된
콜백함수인update_parameter 함수실행
•
update_parameter 콜백함수에서는변경하려는
파라미터의이름과타입이동일한경우해당파
라미터값변경
▶argument 노드에서는파라미터값으로QoS
설정과랜덤으로생성되는변수a, b의랜덤
생성범위를파라미터를이용하여설정.
▶min_random_num 값과max_random_num
값을이용하여퍼블리시할때변수a, b의랜
덤생성범위를변경함


![Image 43](../../assets/images/ros/intro/lesson-08/img_033_043.webp)


![Image 44](../../assets/images/ros/intro/lesson-08/img_033_044.webp)


05
파라미터프로그래밍
파라미터사용방법(서비스클라이언트)
32
▶앞설명에서는CLI를이용하여파라미터를조회하고, 변경하고읽는실습을진행했다.  
그러나파라미터는CLI뿐만아니라다른노드의소스코드에서도읽고변경할수있다. 
예를들어SetParameters라는인터페이스를이용하면서비스클라이언트와유사한
방식으로서비스요청을통해파라미터를변경할수있다.
▶여기서클라이언트를선언하고서비스를요청하는방식은기존의서비스클라이언트
와완전히동일하다. 다만, 서비스요청값에파라미터의이름, 형태, 값을지정하는게
다르다. 이와관련된세부내용은set_max_random_num_parameter 함수에서확인
가능하다. 해당함수에서는Parameter 클래스를사용해name, type, integer_value
등을매개변수로설정한다. 이를통해A 노드에서B 노드의파라미터를변경할수있
게된다.


05
파라미터프로그래밍
기본파라미터설정방법(launch 설정)
33
▶참고로새롭게지정된*.yaml 파일및*.launch.py 파일을
ROS 파일시스템에맞추어설치하게하려면하기와같이
python 패키지설정파일'setup.py'에옵션을추가해야
한다.
▶launch 파일에특정파라미터파일을추가하면, 노드를실행
할때해당파일의파라미터이름과값을참조하여자동으로
초기화가능
src/ex_calculator/launch/arithmetic.launch.py

![Image 46](../../assets/images/ros/intro/lesson-08/img_035_046.webp)


![Image 47](../../assets/images/ros/intro/lesson-08/img_035_047.webp)


06
실행인자프로그래밍
실행인자
34
▶실행인자
•
프로그램실행시추가로입력되는인수로, main 함수의매개변수로사용됨
•
실행명령어와함께전달되어프로그램동작에영향을줌
▶예시: $ ros2 run ex_calculator checker –g 100
•
ros2 run: ROS2 명령어
•
ex_calculator: 패키지이름
•
checker: 실행할노드
•
-g 100: 실행인자, 여기서는GOAL_TOTAL_SUM 값을100으로설정
•
Parameter 매개변수
•
Argument 실행인자
▶참고로파라미터(parameter)는매개변수로풀이하고아규먼트(argument)
는실행인자라풀이된다. C++ 언어에서는이들의분류를더확실히하는
편인데Parameter는함수선언시사용되고Argument는함수호출시의
인수라고생각하면된다


06
실행인자프로그래밍
ROS2 에서의실행인자처리
35
▶C++
•
main 함수에서argc를통해인자개수를받고, argv로
인자를배열형태로받는형식으로인자처리
•
argc와argv를rclcpp의init 함수에인자로전달
▶Python(인수무시할때)
•
두번째예제와같이args를None으로설정후에rclpy
모듈의init 함수에바로넘김
▶Python(인수사용할때)
•
argv의첫번째인자(실행명및실행경로정보)를삭제
한후argv에저장. 
•
수정된argv를rclpy모듈의init 함수에넘김
•
이때C++과는달리argparse 모듈을이용해실행인자
를위한구문해석프로그램작성필요
※   참고로argc, argv, args는다음과같은의미로사용됨
•
argc argument count
•
argv argument vector or value
•
args arguments


![Image 48](../../assets/images/ros/intro/lesson-08/img_037_048.webp)


![Image 49](../../assets/images/ros/intro/lesson-08/img_037_049.webp)


![Image 50](../../assets/images/ros/intro/lesson-08/img_037_050.webp)


06
실행인자프로그래밍
실행인자의구문해석
36
▶실행인자구문
•
Checker 노드의main 함수에서실행인자처리코
드가구현되어있음
•
해당코드를통해실행인자를다루어볼것
•
실행인자의구문해석프로그램은python의
argparse 모듈을이용하여파서를선언후사용할
실행인자값을지정하는것이주를이룸
•
이를순서대로나열하면다음과같음
1.
파서만들기(parser = argparse.ArgumentParser)
2.
인자추가하기(parser.add_argument)
3.
인자파싱하기(args = parser.parse_args())
4.
인자사용하기(args.xxx)
src/ex_calculator/ex_calculator/checker/main.py


![Image 51](../../assets/images/ros/intro/lesson-08/img_038_051.webp)


06
실행인자프로그래밍
실행인자의구문해석
37
1.  파서만들기
•
argparse 모듈의ArgumentParser 객체를parser라는이
름으로선언
•
여기서formatter_class으로argparse 모듈의가장기본
적인형식을사용하도록설정
src/ex_calculator/ex_calculator/checker/main.py
2.  인자추가하기
3.  인자파싱하기
•
parse_args() 메서드를통해인자를파싱
4.  인자사용하기
•
인자를사용하려면args 변수를통해파싱하여대입
•
예를들어add_argument로추가한'--goal_total_sum’  인자
는'args.goal_total_sum’ 형태로사용가능
•
add_argument() 메서드를호출하고인자의내용을채워
실행인자추가가능.
•
인자이름: -g(줄인이름), --goal_total_sum(풀네임)
•
데이터타입: int형
•
기본값: 50
•
설명: 지정인자에대한설명추가(프로그램을실행시'-h'와
같이실행인자에대한도움말을실행하면볼수있는문구)


![Image 52](../../assets/images/ros/intro/lesson-08/img_039_052.webp)

07
런치프로그래밍
ROS2 Launch System
▶새로운런치파일생성:
•
'ex_calculator' 패키지에새로운launch 파일을생성
•
launch 파일의역할
•
argument 노드와calculator 노드를실행
•
두노드에서사용할파라미터파일을설정
▶launch 파일생성방법
•
원하는패키지에launch 이라는폴더가있어야함
•
해당폴더에'*.launch.py' 형식의launch 파일생성
•
여기서는'arithmetic.launch.py' 이라는파일명을사용
•
'arithmetic.launch.py' 파일은하기위치에위치해있음
└ ex_calculator/launch/arithmetic.launch.py
38
07
런치프로그래밍
launch 작성
▶launch 파일의기본구조:
•
generate_launch_description 메소드를정의하여사용
•
메소드내용으로'LaunchConfiguration' 클래스를이용하여
필요시실행관련설정선언
•
메소드의리턴값으로는'LaunchDescription' 클래스로반환
▶'arithmetic.launch.py' 파일의LaunchConfiguration 설정
•
'LaunchConfiguration' 클래스의생성자로'param_dir'
라는파라미터디렉토리를설정하는부분
•
'ex_calculator' 패키지의'param'폴더에위치한
'arithmetic_config.yaml' 파라미터설정파일을의미
•
해당파일의내용은앞서다룬'파라미터프로그래밍
(Python)’ 참고
39


![Image 62](../../assets/images/ros/intro/lesson-08/img_041_062.webp)


07
런치프로그래밍
launch 작성
▶remappings 기능(원본코드에는존재하지않음) :
•
특정이름을변경할수있는기능
•
다음예제와같이'/arithmetic_argument' 토픽
이름을'/argument' 이라는토픽이름으로변경
할수있음
•
내부코드변경없이토픽, 서비스, 액션등의
고유이름을변경할수있는유용한기능이므
로알아두기추천
40


![Image 63](../../assets/images/ros/intro/lesson-08/img_042_063.webp)


07
런치프로그래밍
launch 작성
▶launch의namespace 기능:
•
노드, 토픽, 서비스, 액션, 파라미터등의고유이름을독립적
으로그룹핑하여네트워크를구성할수있는기능
•
변경방법
•
방법1 : 각노드를실행시킬때ROS 변수중하나인
ns(namespace)를입력하여변경
•
방법2 : launch 파일로실행시킬때namespace 라는항목을변경
41
▶namespace 설정방법
•
LaunchConfiguration와DeclareLaunchArgument을통해
namespace를지정
•
예제에서는환경변수로지정한'ROS_NAMESPACE' 변수를
읽어오도록설정
•
'export ROS_NAMESPACE=robot_1' 과같은구문을터미널에서
실행하거나＇~/.bashrc에미리등록
•
Node 클래스에서namespace를지정하면실행시모든노
드이름과해당노드의토픽, 서비스, 액션, 파라미터등고유
이름이변경됨
•
활용예: namespace는복수의로봇을사용할때동일프로
그램을이용할때고유이름을사용함에있어서중복됨을
피할수있고데이터를구분지어사용할수있음


![Image 64](../../assets/images/ros/intro/lesson-08/img_043_064.webp)


07
런치프로그래밍
launch 작성
42
▶generate_launch_description 함수
의return 값이너무많을경우
LaunchDescription의add_action
함수를이용하여정리가능
▶이렇게구성하면예제와같이좀더
간결해짐


![Image 65](../../assets/images/ros/intro/lesson-08/img_044_065.webp)


07
런치프로그래밍
launch 작성
▶런치파일에서다른런치파일불러오기:
•
현재패키지의런치파일불러오기:
•
예를들어, 현재패키지가aaaaa라면, 
IncludeLaunchDescription을사용하여
xxxxx.launch.py와yyyyy.launch.py를불러올수있음
43
▶다른패키지의런치파일불러오기:
•
예를들어, bbbbb 패키지의zzzzz.launch.py 파일을불
러올때는IncludeLaunchDescription과함께
get_package_share_directory 함수를사용
•
get_package_share_directory 함수에불러올패키지명
을입력하여특정패키지의런치파일을가져옴
▶런치파일모듈화의장점
•
하나의런치파일에서동일패키지의노드실행뿐아니
라, 다른패키지의런치파일을불러와실행할수있음
•
특히, 직접작성하지않은패키지의런치파일을수정없
이불러와사용할수있어편리함
•
널리사용되는유용한기능이므로참고할것

![Image 67](../../assets/images/ros/intro/lesson-08/img_045_067.webp)


07
런치프로그래밍
패키지빌드
▶rclpy 패키지계열
•
Python 패키지설정파일(setup.py)의data_files 옵션에launch 폴더를지정
•
효과: 패키지소스코드내launch 폴더에있는*.launch.py 파일들이설치폴더에복사되어위치하게됨
44


07
런치프로그래밍
패키지빌드
▶rclpy 패키지계열
•
Python 패키지설정파일(setup.py)의data_files 옵션에launch 폴더를지정
•
효과: 패키지소스코드내launch 폴더에있는*.launch.py 파일들이설치폴더에복사되어위치하게됨
45

![Image 69](../../assets/images/ros/intro/lesson-08/img_047_069.webp)


08
46
토픽, 서비스, 액션인터페이스
패키지설계
▶argument: arithmetic_argument 토픽이름으로현재시간과변수a, b를퍼블리시
▶calculator
•
토픽이생성시점과변수a,b를arithmetic_argument 토픽을통해수신(subscribe)
•
수신한변수a,b와operator 노드로부터요청값으로받은연산자를통해계산수행(a 연산자b)
•
연산결과를arithmetic_operator 이름의서비스응답값으로operator 노드에전송
•
Checker 노드로부터액션목표값(①action goal)을수신후, 저장된변수(a, b, 연산자)를활용해
연산한값을합산
•
계산이완료된결과를arithmetic_checker라는이름의액션피드백(②action feedback)으로
checker 노드에전송
•
합산된결과값이액션목표값을넘기면최종연산합계를arithmetic_checker라는이름의액션
결과값(③action result)으로checker에전송
▶operator: arithmetic_operator 서비스이름으로calculator 노드에게연산자(+-*/)를
서비스요청값으로보내기
▶checker: 연산값의합계의한계치를arithmetic_checker 액션이름으로액션목표값으로전달


09
프로그래밍
코드리뷰
▶Visual Studio Code 를이용해ex_calculator 코드개선작업을진행합니다.
47


---

## Jupyter Notebooks


### 8차시_1_temperature_example

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/ros/jupyter_ros/8차시_1_temperature_example.ipynb)

### ROS 2 Temperature Publisher/Subscriber Example in Jupyter
가상의 온도 센서값을 1초 간격으로 퍼블리시하고, 동시에 이를 서브스크라이브하는 구조입니다.

#### 환경 설정

셀 1: ROS 2 환경 준비

먼저 터미널에서 ROS 2 환경을 source 한 다음 Jupyter를 실행해야 합니다:
```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
```

셀 2: 기본 임포트 및 초기화


```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random
import time
```

셀 3: 노드 정의


```python
class TemperatureNode(Node):
    def __init__(self):
        super().__init__('temperature_node')

        self.publisher = self.create_publisher(Float32, 'temperature', 10)
        self.subscription = self.create_subscription(Float32, 'temperature', self.listener_callback, 10)
        self.timer = self.create_timer(1.0, self.publish_temperature)
        self.temperature_value = 25.0  # 초기 온도

    def publish_temperature(self):
        self.temperature_value += random.uniform(-0.5, 0.5)
        msg = Float32()
        msg.data = self.temperature_value
        self.publisher.publish(msg)
        print(f'Published temperature: {msg.data:.2f} °C')

    def listener_callback(self, msg):
        print(f'Received temperature: {msg.data:.2f} °C')
```

셀 4: 노드 실행 및 ROS 초기화


```python
rclpy.init()
node = TemperatureNode()
```

 셀 5: 스핀 루프 (1초마다 1회 실행, 30초 동안)


```python
try:
    for _ in range(30):  # 총 30초 동안 동작
        rclpy.spin_once(node)
        time.sleep(1.0)
finally:
    node.destroy_node()
    rclpy.shutdown()
```

#### 결과
Jupyter에서 위 셀들을 순서대로 실행하면,
temperature 토픽으로 온도 데이터를 퍼블리시하고
같은 토픽을 서브스크라이브하여 출력할 수 있습니다.

Tip: Jupyter에서 log는 node.get_logger().info()로는 출력이 잘 안 보일 수 있으니 print()로 바꿔도 괜찮아요.


### 8차시_2_my_robot_system_설명

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/ros/jupyter_ros/8차시_2_my_robot_system_설명.ipynb)

### 시스템 구성 요약

#### 구성 요소	역할

```bash
Topic (/temperature)	센서 노드에서 주기적으로 온도 publish
Subscriber	온도 데이터를 받아서 30도 이상일 경우 처리 시작
Service (/cooler_motor)	30도 이상일 때 호출되는 쿨러 모터 제어용 서비스
Action (/switch_control)	goal로 스위치 on/off 제어 요청 (예: 일정 시간 동안 ON 등)

전체 구성

[SENSOR_NODE] ----(temperature topic)----> [MANAGER_NODE]
                                             |
                                             +--> call /cooler_motor (service)
                                             |
                                             +--> send_goal /switch_control (action)

```


```bash
my_robot_system/
├── sensor_node.py
├── manager_node.py
├── cooler_service.py
├── switch_action_server.py
├── action/
│   └── SwitchControl.action
```


1. Action 정의: action/SwitchControl.action


```python
# Goal
bool turn_on
---
# Result
bool success
---
# Feedback
string status
```

2. sensor_node.py (토픽 퍼블리셔)


```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random


class SensorNode(Node):
    def __init__(self):
        super().__init__("sensor_node")
        self.publisher = self.create_publisher(Float32, "temperature", 10)
        self.timer = self.create_timer(1.0, self.publish_temperature)

    def publish_temperature(self):
        temp = random.uniform(25.0, 35.0)
        self.get_logger().info(f"Publishing Temperature: {temp:.2f}")
        msg = Float32()
        msg.data = temp
        self.publisher.publish(msg)


def main():
    rclpy.init()
    sensor_node = SensorNode()
    rclpy.spin(sensor_node)
    rclpy.shutdown()
```

 3. cooler_service.py (서비스 서버)


```python
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class CoolerService(Node):
    def __init__(self):
        super().__init__("cooler_service")
        self.srv = self.create_service(Trigger, "cooler_motor", self.handle_request)

    def handle_request(self, request, response):
        self.get_logger().info("Cooler activated!")
        response.success = True
        response.message = "Cooler turned on"
        return response


def main():
    rclpy.init()
    cooler_service = CoolerService()
    rclpy.spin(cooler_service)
    rclpy.shutdown()
```

 4. switch_action_server.py (액션 서버)


```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from my_robot_interfaces.action import SwitchControl
import time


class SwitchActionServer(Node):
    def __init__(self):
        super().__init__("switch_action_server")
        self._action_server = ActionServer(
            self, SwitchControl, "switch_control", self.execute_callback
        )

    async def execute_callback(self, goal_handle):
        turn_on = goal_handle.request.turn_on
        status = ["Switch ON"] if turn_on else ["Switch OFF"]
        self.get_logger().info(f"[Action]서버 상태: {status}")

        feedback_msg = SwitchControl.Feedback()
        feedback_msg.status = status
        goal_handle.publish_feedback(feedback_msg)

        time.sleep(2)

        goal_handle.succeed()
        result = SwitchControl.Result()
        result.success = True
        return result


def main():
    rclpy.init()
    switch_action_server = SwitchActionServer()
    rclpy.spin(switch_action_server)
    rclpy.shutdown()

```

 5. manager_node.py (온도 판단 → 서비스/액션 호출)


```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from std_srvs.srv import Trigger
from rclpy.action import ActionClient
from my_robot_interfaces.action import SwitchControl


class ManagerNode(Node):
    def __init__(self):
        super().__init__("manager_node")
        self.subscriber = self.create_subscription(
            Float32, "temperature", self.temp_callback, 10
        )
        self.cooler_client = self.create_client(Trigger, "cooler_motor")
        self.switch_client = ActionClient(self, SwitchControl, "switch_control")

    def temp_callback(self, msg):
        temp = msg.data
        self.get_logger().info(f"Received temperature(현재 보드온도): {temp:.2f}")
        if temp > 30.0:
            self.call_cooler_service()
            self.send_switch_goal(True)

    def call_cooler_service(self):
        while not self.cooler_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("Waiting for cooler_motor service...")
        req = Trigger.Request()
        future = self.cooler_client.call_async(req)

        def callback(future):
            try:
                res = future.result()
                self.get_logger().info(
                    f"Cooler service called : 팬 동작: {res.success}, 스위치: {res.message}"
                )
            except Exception as e:
                self.get_logger().error(f"Service call failed: {e}")

        future.add_done_callback(callback)

    def send_switch_goal(self, turn_on):
        if not self.switch_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().warn("Switch control action server not available!")
            return

        goal_msg = SwitchControl.Goal()
        goal_msg.turn_on = ["Switch ON"]
        self.switch_client.send_goal_async(goal_msg)


def main():
    rclpy.init()
    manager_node = ManagerNode()
    rclpy.spin(manager_node)
    rclpy.shutdown()
```

실행 순서
```bash
ros2 run my_robot_system sensor_node
ros2 run my_robot_system manager_node
ros2 run my_robot_system cooler_service
ros2 run my_robot_system switch_action_server
```

디렉토리 구조 가정

```bash
my_robot_system/
├── launch/
│   └── system_launch.py   ←launch 파일
├── sensor_node.py
├── manager_node.py
├── cooler_service.py
├── switch_action_server.py
```


launch/system_launch.py


```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_robot_system',
            executable='sensor_node',
            name='sensor_node',
            output='screen'
        ),
        Node(
            package='my_robot_system',
            executable='manager_node',
            name='manager_node',
            output='screen'
        ),
        Node(
            package='my_robot_system',
            executable='cooler_service',
            name='cooler_service',
            output='screen'
        ),
        Node(
            package='my_robot_system',
            executable='switch_action_server',
            name='switch_action_server',
            output='screen'
        )
    ])
```

setup.py 설정 확인
entry_points에 각 노드 등록이 되어 있어야 해:


```python
from setuptools import setup
import os
from glob import glob

package_name = 'my_robot_system'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # 👇 launch 파일 등록
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='your_email@example.com',
    description='Sensor to Service and Action example system',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sensor_node = my_robot_system.sensor_node:main',
            'manager_node = my_robot_system.manager_node:main',
            'cooler_service = my_robot_system.cooler_service:main',
            'switch_action_server = my_robot_system.switch_action_server:main',
        ],
    },
)
```

실행 방법


```python
ros2 launch my_robot_system system.launch.py
```

추가로
만약 launch 폴더가 없다면 꼭 CMakeLists.txt 또는 setup.py에 다음 추가해:

setup.py:


```python
data_files=[
    ('share/ament_index/resource_index/packages', ['resource/my_robot_system']),
    ('share/my_robot_system', ['package.xml']),
    ('share/my_robot_system/launch', ['launch/system.launch.py']),
],
```

실행 방법


```python
colcon build --packages-select my_robot_system
source install/setup.bash
ros2 launch my_robot_system system.launch.py
```


---

## Code Examples


### `calculator_project_py/`

[View full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/calculator_project_py/){ .md-button }

#### `calculator_project_py/ex_calculator/launch/arithmetic.launch.py`

```python
#!/usr/bin/env python3
# Copyright 2021 OROCA
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

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    param_dir = LaunchConfiguration(
        'param_dir',
        default=os.path.join(
            get_package_share_directory('ex_calculator'),
            'param',
            'arithmetic_config.yaml'))

    return LaunchDescription([
        DeclareLaunchArgument(
            'param_dir',
            default_value=param_dir,
            description='Full path of parameter file'),

        Node(
            package='ex_calculator',
            executable='argument',
            name='argument',
            parameters=[param_dir],
            output='screen'),

        Node(
            package='ex_calculator',
            executable='calculator',
            name='calculator',
            parameters=[param_dir],
# ... (3 more lines)
```

#### `calculator_project_py/ex_calculator/launch/arithmetic.launch.py`

```python
#!/usr/bin/env python3
# Copyright 2021 OROCA
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

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    param_dir = LaunchConfiguration(
        'param_dir',
        default=os.path.join(
            get_package_share_directory('ex_calculator'),
            'param',
            'arithmetic_config.yaml'))

    return LaunchDescription([
        DeclareLaunchArgument(
            'param_dir',
            default_value=param_dir,
            description='Full path of parameter file'),

        Node(
            package='ex_calculator',
            executable='argument',
            name='argument',
            parameters=[param_dir],
            output='screen'),

        Node(
            package='ex_calculator',
            executable='calculator',
            name='calculator',
            parameters=[param_dir],
# ... (3 more lines)
```

#### `calculator_project_py/ex_calculator/ex_calculator/calculator/main.py`

```python
import rclpy
from rclpy.executors import MultiThreadedExecutor

from ex_calculator.calculator.calculator import Calculator


def main(args=None):
    rclpy.init(args=args)
    try:
        calculator = Calculator()
        executor = MultiThreadedExecutor(num_threads=4)
        executor.add_node(calculator)
        try:
            executor.spin()
        except KeyboardInterrupt:
            calculator.get_logger().info('Keyboard Interrupt (SIGINT)')
        finally:
            executor.shutdown()
            calculator.arithmetic_action_server.destroy()
            calculator.destroy_node()
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()

```


### `my_robot_/`

[View full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/my_robot_/){ .md-button }

#### `my_robot_/my_robot_system/my_robot_system/manager_node.py`

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from std_srvs.srv import Trigger
from rclpy.action import ActionClient
from my_robot_interfaces.action import SwitchControl


class ManagerNode(Node):
    def __init__(self):
        super().__init__("manager_node")
        self.subscriber = self.create_subscription(
            Float32, "temperature", self.temp_callback, 10
        )
        self.cooler_client = self.create_client(Trigger, "cooler_motor")
        self.switch_client = ActionClient(self, SwitchControl, "switch_control")

    def temp_callback(self, msg):
        temp = msg.data
        self.get_logger().info(f"Received temperature(현재 보드온도): {temp:.2f}")
        if temp > 30.0:
            self.call_cooler_service()
            self.send_switch_goal(True)

    def call_cooler_service(self):
        while not self.cooler_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("Waiting for cooler_motor service...")
        req = Trigger.Request()
        future = self.cooler_client.call_async(req)

        def callback(future):
            try:
                res = future.result()
                self.get_logger().info(
                    f"Cooler service called : 팬 동작: {res.success}, 스위치: {res.message}"
                )
            except Exception as e:
                self.get_logger().error(f"Service call failed: {e}")

        future.add_done_callback(callback)

    def send_switch_goal(self, turn_on):
        if not self.switch_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().warn("Switch control action server not available!")
            return

        goal_msg = SwitchControl.Goal()
        goal_msg.turn_on = ["Switch ON"]
        self.switch_client.send_goal_async(goal_msg)

# ... (11 more lines)
```

#### `my_robot_/my_robot_system/my_robot_system/sensor_node.py`

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random


class SensorNode(Node):
    def __init__(self):
        super().__init__("sensor_node")
        self.publisher = self.create_publisher(Float32, "temperature", 10)
        self.timer = self.create_timer(1.0, self.publish_temperature)

    def publish_temperature(self):
        temp = random.uniform(25.0, 35.0)
        self.get_logger().info(f"Publishing Temperature: {temp:.2f}")
        msg = Float32()
        msg.data = temp
        self.publisher.publish(msg)


def main():
    rclpy.init()
    sensor_node = SensorNode()
    rclpy.spin(sensor_node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()

```

#### `my_robot_/my_robot_system/launch/system.launch.py`

```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="my_robot_system",
                executable="sensor_node",
                name="sensor_node",
                output="screen",
            ),
            Node(
                package="my_robot_system",
                executable="manager_node",
                name="manager_node",
                output="screen",
            ),
            Node(
                package="my_robot_system",
                executable="cooler_service",
                name="cooler_service",
                output="screen",
            ),
            Node(
                package="my_robot_system",
                executable="switch_action_server",
                name="switch_action_server",
                output="screen",
            ),
        ]
    )

```
