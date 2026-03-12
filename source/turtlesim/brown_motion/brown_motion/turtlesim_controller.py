#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from rclpy.parameter import Parameter
from rcl_interfaces.srv import SetParameters
from std_srvs.srv import Empty
from rcl_interfaces.msg import Log
import random
import math
import time

class TurtlesimController(Node):
    def __init__(self):
        super().__init__('turtlesim_controller')
        # 거북이 속도 제어를 위한 publisher
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        # 거북이의 위치 정보를 받기 위한 subscriber (일반 직진 제어용)
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        # /rosout 토픽을 구독하여 로그 메시지 감지
        self.rosout_sub = self.create_subscription(Log, '/rosout', self.rosout_callback, 10)
        # 주기적으로 속도 명령을 발행하는 타이머 (0.1초 주기)
        self.timer = self.create_timer(0.1, self.timer_callback)

        # 상태: "moving" (직진) 또는 "turning" (회전 중)
        self.state = "moving"
        self.speed = 1.0
        self.angular_speed = 1.0  # rad/s, 회전할 때 사용할 고정 각속도
        self.turning_end_time = 0.0
        
        # 초기 Twist 메시지: 직진
        self.current_twist = Twist()
        self.current_twist.linear.x = self.speed
        self.current_twist.angular.z = 0.0

        # turtlesim 배경색 변경을 위한 파라미터 클라이언트 생성
        self.param_client = self.create_client(SetParameters, '/turtlesim/set_parameters')
        while not self.param_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for turtlesim parameter service...')
        # 배경 재설정을 위한 /clear 서비스 클라이언트 생성
        self.clear_client = self.create_client(Empty, '/clear')
        while not self.clear_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /clear service...')

    def update_background_color(self):
        """충돌 이벤트 시 배경색을 랜덤하게 변경"""
        r_val = random.randint(0, 255)
        g_val = random.randint(0, 255)
        b_val = random.randint(0, 255)
        self.get_logger().info(f'Updating background color to r:{r_val} g:{g_val} b:{b_val}')
        req = SetParameters.Request()
        req.parameters = [
            Parameter('background_r', Parameter.Type.INTEGER, r_val).to_parameter_msg(),
            Parameter('background_g', Parameter.Type.INTEGER, g_val).to_parameter_msg(),
            Parameter('background_b', Parameter.Type.INTEGER, b_val).to_parameter_msg()
        ]
        self.param_client.call_async(req)
        clear_req = Empty.Request()
        self.clear_client.call_async(clear_req)

    def rosout_callback(self, msg):
        """
        /rosout 토픽에서 turtlesim의 충돌 로그를 감지하면,
        현재 moving 상태라면 회전 이벤트를 발생시킵니다.
        """
        # 로그가 turtlesim 노드에서 온 것이고, 메시지에 충돌 문구가 포함된 경우
        if msg.name == "turtlesim" and "Oh no! I hit the wall!" in msg.msg:
            self.get_logger().info("Collision detected from /rosout log")
            if self.state == "moving":
                # moving 상태에서 충돌 이벤트 발생 시, 바로 turning 상태로 전환
                self.state = "turning"
                # 직진을 멈춤
                self.current_twist.linear.x = 0.0
                
                # 최소 90도(1.57 rad) 이상 최대 270도(4.71 rad) 이하의 회전 각도 선택
                turning_angle = random.uniform(math.radians(90), math.radians(270))
                # 일정한 angular_speed (rad/s)를 사용하므로, 회전 시간은 각도 / angular_speed
                turning_duration = turning_angle / self.angular_speed
                self.turning_end_time = time.time() + turning_duration
                
                # 회전 시작: 여기서는 양의 angular_speed를 사용하여 반시계방향으로 회전
                self.current_twist.angular.z = self.angular_speed
                self.cmd_pub.publish(self.current_twist)
                self.get_logger().info(
                    f"Turning for {turning_duration:.2f} seconds with a turning angle of {math.degrees(turning_angle):.2f} degrees."
                )
                
                # 배경색도 변경 (필요 시)
                self.update_background_color()

    def pose_callback(self, msg):
        """
        pose 콜백은 주로 moving 상태에서의 직진 유지에 사용됩니다.
        현재 turning 상태인 경우는 별도로 회전 타이머에서 제어합니다.
        """
        if self.state == "moving":
            self.current_twist.linear.x = self.speed
            self.current_twist.angular.z = 0.0
            self.cmd_pub.publish(self.current_twist)

    def timer_callback(self):
        """
        타이머 콜백은 turning 상태의 종료를 체크하여 
        일정 시간 후 다시 직진(moving) 상태로 전환합니다.
        """
        if self.state == "turning":
            if time.time() >= self.turning_end_time:
                self.state = "moving"
                self.current_twist.linear.x = self.speed
                self.current_twist.angular.z = 0.0
                self.cmd_pub.publish(self.current_twist)
                self.get_logger().info("Resuming forward movement.")
            else:
                # turning 상태일 때 주기적으로 회전 명령을 재발행 (안정적 제어를 위해)
                self.cmd_pub.publish(self.current_twist)
        else:
            # moving 상태에서는 pose_callback에서 계속 직진 명령을 발행 중
            pass

def main(args=None):
    rclpy.init(args=args)
    controller = TurtlesimController()
    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
