# ROS2 입문 8차시 - ROS2 복습 (2)


## ROS2 복습_2
토픽, 서비스, 액션 인터페이스
패키지 설계

## 패키지구성

- Node 클래스의create_publisher 함수를 사용하여 퍼블리셔 선언
- 토픽 타입: ArithmeticArgument
- 토픽 이름: 'arithmetic_argument
- 'QoS 설정: 이전에 설정한QOS_RKL10V 사용

## ararithmetic_argument_publisher 선언
## create_timer 함수를이용하여1초마다publish_random_arithmetic_arguments 함수실행설정
## create_publisher에서의설정들은퍼블리시를위한기본설정
## 실제토픽발행이이루어지는부분은publish_random_arithmetic_arguments 함수


- 타이머 콜백 함수로1초마다 실행
- msg 변수를ArithmeticArgument() 클래스로 생성(지난‘토픽, 서 비스, 액션 인터페이스’ 강좌에서 작성한msg 인터페이스 활용)
- 토픽 생성 시간을get_clock().now().to_msg()로 가져와 msg.stamp에기록
- 랜덤 함수로0~9 사이의 숫자를float로 변환하여 msg.argument_a와msg.argument_b에저장

## publish_random_arithmetic_arguments 함수
- 실제로 토픽 발행이 이루어지는 함수로 우리가 발행 시간 및 변수a, b를 저장한msg 메시지를 퍼 블 리시한다는 의미

## arithmetic_argument_publisher.publish(msg) 함수
- get_logger().info() 를사용하여디버깅목적으로변수a, b 값을 터미널에 표시

## 로그출력
- 토픽 퍼블리셔 노 드와 마찬가지로Node 클래스 상속
- 생성자에서'calculator'라는 이름으로 노드 초기화
- 토픽서브스크라이버, 서비스 서버, 액션 서버를 포함하여 코드가 길기 때문에 전체 코드는 생략
- 여기서는토픽서브스크라이버관련코드만설명
- Calculator 클래스 설정
- QoS 설정
- QoSProfile 클래스를이용하여토픽서브스크라이버의 QoS 설정 적용
- QoS 설정값: RELIABLE, KEEP_LAST, DEPTH 10, VOLATILE (토픽 퍼블리셔와 동일 설정)
- QoS에 대한 자세한 내용은'DDS의QoS(Quality of Service)' 강좌 참고
- 제일 중요한 설정으로Node 클래스의create_subscription 함수를이용하여서브스크라이버로선언
- get_arithmetic_argument라는 콜백 함수를 지정하여 퍼 블 리셔로부터 메시지를 서브스크라이브 할 때마다 실행되는 함수를 지정
- ReentrantCallbackGroup으로callback_group을 지정하여 콜백 함수를 병렬로 실행할 수 있게해 주며 뒤에서 설정
- 이후 설명할MultiThreadedExecutor와 함께 사용됨
- arithmetic_argument_subscriber 설정
- callback_group
- MutuallyExclusiveCallbackGroup이 기본 설정으로 사용됨
- MutuallyExclusiveCallbackGroup: 한 번에 하나의 콜백 함 수만 실행하도록 제한
- ReentrantCallbackGroup: 제한 없이 콜백 함수를 병렬로 실행 가능 토픽 프로그래밍 토픽서브스크라이버코드 토픽 프로그래밍 토픽서브스크라이버코드
- 콜백 함수인 이 함수는'arithmetic_argument'이라는 토픽 이름에ArithmeticArgument 타입의 메시지를 서브스크라이브하게 되면 실행됨
- 서브스크라이브한msg의argument_a와argument_b를 멤버 변수에 저장하고, get_logger().info() 함수를 이용하여 토픽으로 받은 시간, 변수a, b 값을 화면에 표시
- get_arithmetic_argument

## entry_points 설정
- setup.py의entry_points는 실행 가능한 콘솔 스크립트 이름과 호출 함수를 지정
- 'ros2 run' 명령어로 각 노드를 실행할 수 있도록4개의 노드entry_points 추가

## 노드파일경로
- argument 노드: ex_calculator 패키지의arithmetic 폴더의argument.py main문에 실행 코드 포함
- operator 노드: ex_calculator 패키지의arithmetic 폴더의operator.py main문에 실행 코드 포함
- calculator 노드: ex_calculator 패키지의calculator 폴더의main.py main문에 실행 코드 포함
- checker 노드: ex_calculator 패키지의checker 폴더의main.py main문에 실행 코드 포함 토픽 프로그래밍 노드 실행 코드

## argument 노드
- main 함수로rclpy.init를 이용하여 초기화
- Argument 클래스를argument라는 이름으로 생성
- rclpy.spin 함수를 이용하여 생성한 노드를spin 시켜 지정된 콜백 함수 실행
- 종료(ctrl + c)와 같은 인터럽트 시그널 예외상 황에서는argument를 소멸시키고 rclpy.shutdown 함수로 노드를 종료 토픽 프로그래밍 노드 실행 코드 토픽 프로그래밍 노드 실행 코드

## calculator 노드초기화
- rclpy.init를 이용하여ROS2 초기화
- Calculator 클래스를calculator라는 이름으로 생성
- MultiThreadedExecutor를 사용하여4개스 레드로 구성된executor 생성

## MultiThreadedExecutor 설정
- 스레드 풀(thread pool)을 사용하여 콜백을 병렬로 실행
- num_threads로스 레드 수를 지정 가능
- 콜백을 병렬로 처리 가능하여ReentrantCallbackGroup과 함께 사용 시 병렬 실행 지원

## 콜백함수의병렬처리설정
- create_subscription(), create_service(), ActionServer(), create_timer() 등의 함수로 설정된 콜백 함수들의 병렬 처리 가능

## executor와노드실행
- calculator 노드를MultiThreadedExecutor에추가
- executor.spin()으로노드를 실행하여 지정된 콜백 함수 실행 가능’

## 종료처리
- 인터럽트시그널(Ctrl + C) 발생시, executor, calculator의 액션 서버(별도 소멸 필요), calculator 노드를 소멸
- rclpy.shutdown으로노드를 종료


서비스 클라이언트/서버


![Image 19](../../assets/images/ros/intro/lesson-08/img_012_019.webp)

src/ex_calculator/ex_calculator/calculator/calculator.py

## calculator 노드초기화
- 변수(a, b)와operator 노드로부터 요청 값으로 받은 연산자를 이용해 계산 수행
- 연산 결과를operator 노드에 서비스 응답 값으로 전송

## 서비스서버설정코드
- 서비스 서버 선언: arithmetic_service_server를Node 클래스의create_service 함수로 선언
- 서비스 타입: ArithmeticOperator
- 서비스 이름: 'arithmetic_operator’
- 콜백 함수: get_arithmetic_operator (서비스 요청 시 실행)
- callback_group 설정: 멀티 스레드 병렬 콜백 함수 실행 지원
- 콜백을 병렬로 처리 가능하여ReentrantCallbackGroup과 함께 사용 시 병렬 실행 지원

## 콜백함수역할
- 콜백 함수인get_arithmetic_operator이 실제 서비스 요청에 해당되는 특정 수행 코드가 수행되는 부분


src/ex_calculator/ex_calculator/calculator/calculator.py

## get_arithmetic_operator 함수
- 매개변수:
- request와response는ArithmeticOperator() 클래스로 생성된 인터 페이스
- request: 서비스 요청 데이터
- response: 서비스 응답 데이터

## 함수의역할
- 서비스 요청 시 실행되는 콜백 함수
- request에서 받은 연산자와, 토픽서브스크라이버가전달받아 저장한 변수(a, b)를 사용해 연산 수행
- 연산 결과를 서비스 응답 값(response)으로 반환

## 연산과정
- request.arithmetic_operator를calculate_given_formula 함수에 전달하여 연산 수행 연산 결과를response.arithmetic_result에 저장
- 관련 수식을**get_logger().info()**를 통해 문자열로 출력하여 화면에 표시


src/ex_calculator/ex_calculator/arithmetic/operator.py

## Operator 클래스초기화
- rclpy.node 모듈의Node 클래스 상속
- 생성자에서 노 드 이름을'operator'로 초기화

## arithmetic_service_client 설정
- Node 클래스의create_client 함수를 이용하여 서비스 클라이언트로 선언
- 서비스의 타입: ArithmeticOperator(서비스 서버와 동일)로 선언하였고
- 서비스 이름: ‘arithmetic_operator’로 선언하였다

## wait_for_service 함수
- 서비스 요청 가능 여부를 위해0.1초간격으로 서비스 서버가 실행되어 있는지 확인


src/ex_calculator/ex_calculator/arithmetic/operator.py

## 서비스클라이언트의목적: 서비스서버에게연산에필요한연산자를전달
## 서비스요청설정: 서비스인터페이스ArithmeticOperator.Request() 클래스로
service_request를 선언 후random.randint() 함수를 이용하여 특정 연산자를
self.request의arithmetic_operator 변수에 저장

## send_request 함수: 실질적인서비스클라이언트의실행코드로서비스요청값을서버에
보내고 응답 값을 수신

## call_async(self.request) 함수로서비스요청수행
## 서비스상태및응답값을담은futures를반환


서비스 클라이언트 노드 실행 코드
src/ex_calculator/ex_calculator/arithmetic/operator.py
- rclpy.init를 이용하여 초기화
- Operator 클래스를operator라는 이름으로 생성한 후future = operator.send_request()로 서비스 요청을 전송 후 응답 값 수신
- rclpy.spin_once 함수로 노드를 주기적으로spin시켜 지정된 콜백 함수가 실행
- 각spin마다노드의 콜백 함수가 실행
- 서비스 응답 값을 수신 시future의done 함수를 이용해 요청 값을 제대로 받았는지 확인
- 결과 값을service_response = future.result()로저장
- get_logger().info() 함수를 이용하여 화면에 서비스 응답 값에 해당되는 연산 결과 값을 표시
- ‘ctrl + c'와 같은 인터럽트 시그널 예외 상황에서 operator를 소멸시키고rclpy.shutdown 함수로 노 드 를 종료


서비스 클라이언트 노드 실행 코드
src/ex_calculator/ex_calculator/arithmetic/operator.py
- 서비스 클라이언트는 한 번 실행 후 종료되는 방식으로, 토픽과 같은 지속적인 수행은 없음
- 다만, 예제에서는 원하는 시점에 서비스 요청을 다시 보낼 수 있도록user_trigger 변수와 input(＇xxxxx＇)을 사용해 반복 실행 가능하게 구성
- 최초1회에 한해서 사용자 입력 없이 바로 임 의의 연산 자를 서비스 요청 값으로 송신
- 그 이후 노드가 종료되기 전까지, 사용자의 입 력을 받을 때마다 임의의 연산 자를 랜덤으로 선택해 서비스 요청 값으로 송신
- 즉. 최초 요청 후 서비스 재요청이 필요할 경우, 터미널 창에서 엔터 키를 눌러operator 실행
- 연산자 선택은 사 칙 연산자(+, -, * , /) 중 하나가 랜덤으로 선택되어 송신됨


액션 클라이언트/서버
다음 그림과 같은 액션 목표(action goal)를 지정하는 액션 클라이언트와 액션 목표를 받아 특
정 태스크를 수행하면서 중간 결과 값에 해당되는 액션 피드백(action feedback)과 최종 결과 값
에 해당되는 액션 결과(action result)를 전송하는 액션 서버를 작성해 볼 것이다.


![Image 28](../../assets/images/ros/intro/lesson-08/img_019_028.webp)


src/ex_calculator/ex_calculator/calculator/calculator.py

## arithmetic_action_server : rclpy.action
모듈의ActionServer 클래스를 이용하여
액션 서버로 선언
- 액션 타입: ArithmeticChecker
- 액션 이름: 'arithmetic_checker’
- 콜백 함수: execute_checker(액션 클라이언트로부터 액션 목표를 받으면 실행됨)
- 멀티 스레드 병렬 콜백 함수 실행을 위한 callback_group 설정 적용

## 이러한설정들은액션서버를위한기본
설정이고 실제 액션 목표를 받은 후에
실행되는 콜백 함수는execute_checker
함수임을 알아 두자


src/ex_calculator/ex_calculator/calculator/calculator.py

## goal_handle 매개변수
- rclpy.action 모듈의ServerGoalHandle 클래스로 생성된 액션 상태 처리용으로execute, succeed, abort, canceled 등 액션 상태에 따른 관련 함수 호출 가능
- publish_feedback을 통해 피드백 퍼 블 리 시 가능 Get_logger().info() 함수를 이용해 터미널 창에 액션 서버 시작 표시 ArithmeticChecker.Feedback()을 통해 액션 피 드 백을 보낼feedback_msg 변수 선언 실제 피드백에 해당되는 feedback_msg.formula와 연산 합계 값을 담을 total_sum 변수 초기화 goal_handle를 이용하여 goal_handle.request.goal_sum에서 액션 목표 값을 불러옴

## ## ## ## ![Image 30](../../assets/images/ros/intro/lesson-08/img_021_030.webp)


src/ex_calculator/ex_calculator/calculator/calculator.py

## •
total_sum: argument_result(매번 계산되는
연산 결과 값)를 누적한 합계
액션 목표 값(goal_sum)과total_sum이
액션 목표 값(goal_sum)을 넘을 때까지
연산식(argument_formula)을 액션 피드
백(feedback_msg.formula)에저장

## 피드백값은디버깅을위해
get_logger().info()을 통해 터미널 창에 출
력후goal_handle.publish_feedback() 함
수를 통해 액션 클라이언트로 전송

src/ex_calculator/ex_calculator/calculator/calculator.py

## 액션목표를달성했다는상태전환함수인
goal_handle.succeed()를 실행시켜 액션
클라이언트에게 현재의 액션 상태를 알림

## 액션결과값인all_formula에계산식전체
를 저장하고total_sum에 연산 합계를 저
장하여 액션 결과 값인result은리턴

액션 서버 실행 코드
src/ex_calculator/ex_calculator/calculator/main.py

## 액션서버인calculator 노드는토픽서브
스크라이버, 서비스 서버, 액션 서버를 역
할을 하는 복합 기능의 노드

## 해당코드에대한설명은토픽프로그래밍
(Python) 강좌 참조

src/ex_calculator/ex_calculator/checker/checker.py

## Checker 클래스
- rclpy.node 모듈의Node 클래스를 상속
- 생성자에서 노 드 이름을‘checker'로 초기화

## 액션클라이언트에서수행하는액션목표
는 토픽과 달리, 필요시에만 비정기적으로
실행됨

## 여기서는예시를위해액션목표를main
함수에서 한 번만 실행

## rclpy.action모듈의ActionClient 클래스
이용하여 액션 클라이언트 선언
- 액션 타입: ArithmeticChecker
- 액션 이름: 'arithmetic_checker’

src/ex_calculator/ex_calculator/checker/checker.py

## send_goal_total_sum 함수
- 액션 목표를 액션 서버에게 전송하고, 액션 피드백 및 결과 값을 받기 위한 콜백 함수 지정

## 액션클라이언트가액션서버에연결
시도를 함

## 연결에문제가있을때에while문을
반복하게 되고 문제 없이 연결되었을
때에는 다음 구문으로 넘어감
src/ex_calculator/ex_calculator/checker/checker.py

## 액션메시지설정
- ArithmeticChecker.Goal() 클래스로 액션 메시지(goal_msg) 선언
- goal_msg.goal_sum으로 액션 목 푯 값 설정

## 비동기액션전송및피드백설정
- ActionClient 클래스의send_goal_async 함수를 이용해 설정해 둔 액션 메시지를 매개 변 수로 전달
- 액션 피드백을 수신을 위한 콜백 함수로 get_arithmetic_action_feedback 지정

## 액션결과수신설정
- send_goal_async으로 선언된 비동기 작업 (future task)인send_goal_future의 add_done_callback 함수를 통해 액션 결과 값을 받을 때 사용할 콜백 함수로 get_arithmetic_action_goal를선언

1. 액션 클라이언트 선언: arithmetic_action_client
2. 액션 목 푯 값 전달 함수 선언: send_goal_future
3. 액션 피드백 값 콜백 함수 선언: get_arithmetic_action_feedback
4. 액션 상태 값 콜백 함수 선언: get_arithmetic_action_goal
5. 액션 결과 값 콜백 함수 선언: get_arithmetic_action_result


src/ex_calculator/ex_calculator/checker/checker.py

## 액션피드백값콜백함수
- 액션 피드백을 액션 서버로부터 전달 받으면get_arithmetic_action_feedback 콜백 함수 실행
- 피드백인feedback_msg.feedback.formula 값을 받아get_logger().info()으로 터미널 창에 출력

## 액션상태값콜백함수
- 비동기 작업(future task)으로 생성된 send_goal_future에대해add_done_callback 함수를 사용해 콜백 함수 설정
- 이 콜백 함수는 액션 서버가 액션 목 푯 값을 수신했을 때Goal State Machine의 상태가 accepted인지 확인하여 처리
- 액션 목 푯 값을 문제없이 전달된 경우, 액션 결과를 받을 콜백 함수를 get_arithmetic_action_result로설정


src/ex_calculator/ex_calculator/checker/checker.py

## 앞서지정한"액션결과값콜백함수"
는 비동기future task로 현재의 상태값
(status)과 결과 값(result)을수신

## 상태값이STATUS_SUCCEEDED 일때
액션 서버로부터 전달받은 액션 결과 값
인 계산 식(action_result.all_formula)과
연산 합계(action_result.total_sum)를
터미널 창에 출력


액션 클라이언트 노드 실행 코드
src/ex_calculator/ex_calculator/checker/main.py

## main 함수실행코드:
- rclpy.init를통해ROS2 노드 초기화
- Checker 클래스를checker라는 이름으로 생성
- 액션 목 푯 값을 전달하는send_goal_total_sum 함수 실행

## 실행인자(args.goal_total_sum) 사용
- 프로그램의 실행 시 인자를 사용해 사용자가 노드를 실행시킬 때 액션 목 푯 값을 설정 가능.
- 목표 값이 지정되지 않았을 경우 기본 값으로50이 입력됨
- 실행 인자에 대한 자세한 설명은 추후 강좌에서 다룰 예정

## 콜백함수실행및유지
- rclpy.spin 함수를 이용하여rclpy의 콜백 함수가 지속적으로 실행되도록 설정

## 종료및자원해제
- 종료시('Ctrl + c'와 같은 인터럽트 시그널) checker 객체 소멸 및rclpy.shutdown 함수로 노 드 종료
- 추가적으로 토픽이나 서비스와는 달리 액션 클라이언트는 'checker.arithmetic_action_client.destroy()' 와 같이 별도로 소 멸시켜야함


파라미터 프로그래밍
파라미터
우리는 이전 강좌에서 토픽, 서비스, 액션 관련 프로그래밍을 익히기 위하여argument, operator, calculator,
checker 노드를 작성해 보았다. 이들 노드 중에서 다음 그림과 같이argument 노드와calculator 노드는 파
라미터를 사용하고 있다. argument 노드는QoS 설정과 랜덤으로 생성되는 변수a, b의 랜덤 생성 범위를 파
라미 터를 이용했었고calculator 노드는QoS 설정을 사용하였다. 우리는 여기서argument 노드에서 사용되
는 파라미터에 대해 자세히 알아볼 것이다.


![Image 42](../../assets/images/ros/intro/lesson-08/img_031_042.webp)


파라미터 프로그래밍
파라미터 설정
1.
declare_parameter 함수
2.
get_parameter 함수
3.
add_on_set_parameters_callback 함수

## argument 노드에서파라미터를선언하고파라미터값이변경되는함수에대해
자세히 알아보자

## Argument 클래스의생성자부분에서다음과같은코드가있다. ROS2에서파라
미터를 사용하려면 하기와 같이 크게3가지의 요소가 필요

## 1번의declare_parameter 함수는노드에서사용할파라미터의고유이름을지
정 하고 초 깃 값 설정(파라미터에 대한 설명이 들어가는descriptor은 생략함)

## 2번의get_parameter 함수는노드에서사용할파라미터의파라미터고유이름
을 이용해 불러옴. 이는 주로launch 파일에서 선언된*.yaml 형태의 파라미터
파일의 값을 불러오는 데 사용됨

## 3번의add_on_set_parameters_callback 함수는서비스형태로파라미터변경
요청이 있을 때 사용되는 함수로 지정된 콜백 함수를 호출


파라미터 프로그래밍
파라미터 설정
src/ex_calculator/ex_calculator/checker/main.py

## 파라미터선언및초기설정
- declare_parameter 함수로'max_random_num'과 같은 파라미터 선언
- 노드 실행 시get_parameter 함수가 지정된 파라 미터 파일에서 초 깃 값을 불러와 설정

## 파라미터변경요청처리
- 파라미터 변경 요청 발생 시 add_on_set_parameters_callback을 통해 지정된 콜백 함수인update_parameter 함수 실행
- update_parameter 콜백 함수에서는 변경하려는 파라미터의 이름과 타입이 동일한 경우 해당 파 라 미터 값 변경

## argument 노드에서는파라미터값으로QoS
설정과 랜덤으로 생성되는 변수a, b의랜덤
생성 범위를 파라미터를 이용하여 설정.

## min_random_num 값과max_random_num
값을 이용하여 퍼 블 리 시할 때 변수a, b의랜
덤 생성 범위를 변경함


파라미터 프로그래밍
파라미터 사용 방법(서비스 클라이언트)

## 앞설명에서는CLI를이용하여파라미터를조회하고, 변경하고읽는실습을진행했다.
그러나 파라미터는CLI뿐만 아니라 다른 노드의 소스 코드에서도 읽고 변경할 수 있다.
예를 들어SetParameters라는 인터페이스를 이용하면 서비스 클라이언트와 유사한
방식으로 서비스 요청을 통해 파라미터를 변경할 수 있다.

## 여기서클라이언트를선언하고서비스를요청하는방식은기존의서비스클라이언트
와 완전히 동일하다. 다만, 서비스 요청 값에 파라미터의 이름, 형태, 값을 지정하는 게
다르다. 이와 관련된 세부 내용은set_max_random_num_parameter 함수에서 확인
가능하다. 해당 함수에서는Parameter 클래스를 사용해name, type, integer_value
등을 매개 변수로 설정한다. 이를 통해A 노드에서B 노드의 파라미터를 변경할 수 있
게된다.


파라미터 프로그래밍
기본 파라미터 설정 방법(launch 설정)

## 참고로새롭게지정된*.yaml 파일및*.launch.py 파일을
ROS 파일 시스템에 맞추어 설치하게하려면 하기와 같이
python 패키지 설정 파일'setup.py'에 옵션을 추가해야
한다.

## launch 파일에특정파라미터파일을추가하면, 노드를실행
할 때 해당 파일의 파라미터 이름과 값을 참조하여 자동으로
초기화 가능
src/ex_calculator/launch/arithmetic.launch.py


실행 인자 프로그래밍

## 실행인자
- 프로그램 실행 시 추가로 입력되는 인 수로, main 함수의 매개변수로 사용됨
- 실행 명령어와 함께 전달되어 프로그램 동작에 영향을 줌

## 예시: $ ros2 run ex_calculator checker –g 100
- ros2 run: ROS2 명령어
- ex_calculator: 패키지 이름
- checker: 실행할 노드
- -g 100: 실행 인자, 여기서는GOAL_TOTAL_SUM 값을100으로 설정
- Parameter 매개변수
- Argument 실행 인자

## 참고로파라미터(parameter)는매개변수로풀이하고아규먼트(argument)
는 실행 인자라 풀이된다. C++ 언어에서는 이들의 분류를 더 확실히 하는
편인데Parameter는 함수 선언 시 사용되고Argument는 함수 호출 시의
인수라고 생각하면 된다


실행 인자 프로그래밍
ROS2 에서의 실행 인자 처리

## C++
- main 함수에서argc를 통해 인자 개수를 받고, argv로 인자를 배열 형태로 받는 형식으로 인자 처리
- argc와argv를rclcpp의init 함수에 인자로 전달

## Python(인수무시할때)
- 두 번째 예제와 같이args를None으로 설정 후에rclpy 모듈의init 함수에 바로 넘김

## Python(인수사용할때)
- argv의 첫 번째 인자(실행 명 및 실행 경로 정보)를 삭제한 후argv에저장.
- 수정된argv를rclpy모듈의init 함수에 넘김
- 이때C++과는 달리argparse 모듈을 이용해 실행 인자를 위한 구문 해석 프로그램 작성 필요 ※ 참고로argc, argv, args는 다음과 같은 의미로 사용됨
- argc argument count
- argv argument vector or value
- args arguments


실행 인자 프로그래밍
실행 인자의 구문 해석

## 실행인자구문
- Checker 노드의main 함수에서 실행 인자 처리 코 드가 구현되어 있음
- 해당 코드를 통해 실행 인자를 다루어 볼 것
- 실행 인자의 구문 해석 프로그램은python의 argparse 모듈을 이용하여 파서를 선언 후 사용할 실행 인자 값을 지정하는 것이 주를 이룸
- 이를 순서대로 나열하면 다음과 같음 1. 파서 만들기(parser = argparse.ArgumentParser) 2. 인자 추가하기(parser.add_argument) 3. 인자 파 싱하기(args = parser.parse_args()) 4. 인자 사용하기(args.xxx) src/ex_calculator/ex_calculator/checker/main.py


실행 인자 프로그래밍
실행 인자의 구문 해석

1. 파서 만들기
- argparse 모듈의ArgumentParser 객체를parser라는 이 름으로 선언
- 여기서formatter_class으로argparse 모듈의 가장 기본적인 형식을 사용하도록 설정 src/ex_calculator/ex_calculator/checker/main.py

2. 인자 추가하기
3. 인자 파 싱하기
- parse_args() 메서드를 통해 인 자를 파싱

4. 인자 사용하기
- 인자를 사용하려면args 변수를 통해 파 싱하여 대입
- 예를 들어add_argument로 추가한'--goal_total_sum’ 인자 는'args.goal_total_sum’ 형태로 사용 가능
- add_argument() 메서드를 호출하고 인자의 내용을 채워 실행 인자 추가 가능.
- 인자 이름: -g(줄인 이름), --goal_total_sum(풀네임)
- 데이터 타입: int형
- 기본값: 50
- 설명: 지정 인자에 대한 설명 추가(프로그램을 실행 시'-h'와 같이 실행 인자에 대한 도움말을 실행하면 볼 수 있는 문구)


런치 프로그래밍
ROS2 Launch System

## 새로운런치파일생성:
- 'ex_calculator' 패키지에 새로운launch 파일을 생성
- launch 파일의 역할
- argument 노드와calculator 노드를 실행
- 두노드에서 사용할 파라미터 파일을 설정

## launch 파일생성방법
- 원하는 패키지에launch 이라는 폴더가 있어야함
- 해당 폴더에'*.launch.py' 형식의launch 파일 생성
- 여기서는'arithmetic.launch.py' 이라는 파일 명을 사용
- 'arithmetic.launch.py' 파일은 하기 위치에 위치해 있음 └ ex_calculator/launch/arithmetic.launch.py 런치 프로그래밍 launch 작성

## launch 파일의기본구조:
- generate_launch_description 메소드를 정의하여 사용
- 메소드 내용으로'LaunchConfiguration' 클래스를 이용하여 필요시 실행 관련 설정 선언
- 메소드의 리턴 값으로는'LaunchDescription' 클래스로 반환

## 'arithmetic.launch.py' 파일의LaunchConfiguration 설정
- 'LaunchConfiguration' 클래스의 생성자로'param_dir' 라는 파라미터 디렉토리를 설정하는 부분
- 'ex_calculator' 패키지의'param'폴더에 위치한 'arithmetic_config.yaml' 파라미터 설정 파일을 의미
- 해당 파일의 내용은 앞서 다룬'파라미터 프로그래밍 (Python)’ 참고


런치 프로그래밍
launch 작성

## remappings 기능(원본코드에는존재하지않음) :
- 특정 이름을 변경할 수 있는 기능
- 다음 예제와 같이'/arithmetic_argument' 토픽 이름을'/argument' 이라는 토픽 이름으로 변경할 수 있음
- 내부 코드 변경 없이 토픽, 서비스, 액션 등의 고유 이름을 변경할 수 있는 유용한 기능이므로 알아 두기 추천


런치 프로그래밍
launch 작성

## launch의namespace 기능:
- 노드, 토픽, 서비스, 액션, 파라미터 등의 고유 이름을 독립적으로 그룹 핑하여 네트워크를 구성할 수 있는 기능
- 변경 방법
- 방법1 : 각 노드를 실행시킬 때ROS 변수 중 하나인 ns(namespace)를 입력하여 변경
- 방법2 : launch 파일로 실행시킬 때namespace 라는 항목을 변경

## namespace 설정방법
- LaunchConfiguration와DeclareLaunchArgument을통해 namespace를지정
- 예제에서는 환경 변수로 지정한'ROS_NAMESPACE' 변수를 읽어 오도록 설정
- 'export ROS_NAMESPACE=robot_1' 과 같은 구문을 터미널에서 실행하거나＇~/.bashrc에 미리 등록
- Node 클래스에서namespace를 지정하면 실행 시 모든 노 드 이름과 해당 노드의 토픽, 서비스, 액션, 파라미터 등 고유 이름이 변경됨
- 활용예: namespace는 복수의 로봇을 사용할 때 동일 프로 그램을 이용할 때 고유 이름을 사용함에 있어서 중복됨을 피할 수 있고 데이터를 구분 지어 사용할 수 있음


런치 프로그래밍
launch 작성

## generate_launch_description 함수
의return 값이 너무 많을 경우
LaunchDescription의add_action
함수를 이용하여 정리 가능

## 이렇게구성하면예제와같이좀더
간결해짐


런치 프로그래밍
launch 작성

## 런치파일에서다른런치파일불러오기:
- 현재 패키지의 런치 파일 불러오기:
- 예를 들어, 현재 패키지가aaaaa라면, IncludeLaunchDescription을 사용하여 xxxxx.launch.py와yyyyy.launch.py를 불러올 수 있음

## 다른패키지의런치파일불러오기:
- 예를 들어, bbbbb 패키지의zzzzz.launch.py 파일을 불러 올 때는IncludeLaunchDescription과함께 get_package_share_directory 함수를 사용
- get_package_share_directory 함수에 불러올 패키지 명을 입력하여 특정 패키지의 런치 파일을 가져옴

## 런치파일모듈화의장점
- 하나의 런치 파일에서 동일 패키지의 노드 실행뿐 아니라, 다른 패키지의 런치 파일을 불러와 실행할 수 있음
- 특히, 직접 작성하지 않은 패키지의 런치 파일을 수정 없이 불러와 사용할 수 있어 편리함
- 널리 사용되는 유용한 기능이므로 참고할 것


런치 프로그래밍
패키지 빌드

## rclpy 패키지계열
- Python 패키지 설정 파일(setup.py)의data_files 옵션에launch 폴더를 지정
- 효과: 패키지 소스 코드 내launch 폴더에 있는*.launch.py 파일들이 설치 폴더에 복사되어 위치하게 됨 런치 프로그래밍 패키지 빌드

## rclpy 패키지계열
- Python 패키지 설정 파일(setup.py)의data_files 옵션에launch 폴더를 지정
- 효과: 패키지 소스 코드 내launch 폴더에 있는*.launch.py 파일들이 설치 폴더에 복사되어 위치하게 됨


토픽, 서비스, 액션 인터페이스
패키지 설계

## argument: arithmetic_argument 토픽이름으로현재시간과변수a, b를퍼블리시
## calculator
- 토픽이 생성 시점과 변수a,b를arithmetic_argument 토픽을 통해 수신(subscribe)
- 수신한 변수a,b와operator 노드로부터 요청 값으로 받은 연산자를 통해 계산 수행(a 연산자b)
- 연산 결과를arithmetic_operator 이름의 서비스 응답 값으로operator 노드에 전송
- Checker 노드로부터 액션 목표 값(①action goal)을 수신 후, 저장된 변수(a, b, 연산자)를 활용해 연산한 값을 합산
- 계산이 완료된 결과를arithmetic_checker라는 이름의 액션 피드백(②action feedback)으로 checker 노드에 전송
- 합산된 결과 값이 액션 목표 값을 넘기면 최종 연산 합계를arithmetic_checker라는 이름의 액션 결과 값(③action result)으로checker에전송

## operator: arithmetic_operator 서비스이름으로calculator 노드에게연산자(+-*/)를
서비스 요청 값으로 보내기

## checker: 연산값의합계의한계치를arithmetic_checker 액션이름으로액션목표값으로전달


프로그래밍
코드 리뷰

## Visual Studio Code 를이용해ex_calculator 코드개선작업을진행합니다.
---

## Jupyter Notebooks


### 8차시_1_temperature_example

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/ros/jupyter_ros/8차시_1_temperature_example.ipynb)

### ROS 2 Temperature Publisher/Subscriber Example in Jupyter
가상의 온도 센서 값을 1초 간격으로 퍼블리시하고, 동시에 이를 서브스크라이브하는 구조입니다.

#### 환경 설정

셀 1: ROS 2 환경 준비

먼저 터미널에서 ROS 2 환경을 source 한 다음 Jupyter를 실행해야합니다:
```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
```

셀 2: 기본 임 포트 및 초기화


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
entry_points에 각 노드 등록이 되어 있어야해:


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
