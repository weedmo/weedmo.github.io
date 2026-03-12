import random

from ros_study_msgs.msg import ArithmeticArgument
from rcl_interfaces.msg import SetParametersResult

import rclpy as rp
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSHistoryPolicy
from rclpy.qos import QoSProfile
from rclpy.qos import QoSReliabilityPolicy

class ArgumentNode(Node):
    
    def __init__(self):
        super().__init__('argument_node')
        
        # param 
        self.declare_parameter('qos_depth', 10)
        self.declare_parameter('min_random_num',0)
        self.declare_parameter('max_random_num',9)
        
        qos_depth = self.get_parameter('qos_depth').value
        self.min_val = self.get_parameter('min_random_num').value
        self.max_val = self.get_parameter('max_random_num').value
        self.add_on_set_parameters_callback(self.update_parameter)
        
        # QOS
        QOS_RKL10V = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=qos_depth,
            durability=QoSDurabilityPolicy.VOLATILE)
        
        # publish, timer
        self.publisher = self.create_publisher(
            ArithmeticArgument,
            'arithmetic_argument', QOS_RKL10V)
        
        self.timer = self.create_timer(1.0, self.timer_callback)
    
    def update_parameter(self, params):
        for param in params:
            if param.name=='min_random_num' and param.type_==Parameter.Type.INTEGER:
                self.min_val = param.value
            elif param.name=='max_random_num' and param.type_==Parameter.Type.INTEGER:
                self.max_val = param.value
            
    def timer_callback(self):
        msg = ArithmeticArgument()
        msg.stamp = self.get_clock().now().to_msg()
        msg.argument_a = random.uniform(self.min_val, self.max_val)
        msg.argument_b = random.uniform(self.min_val, self.max_val)
        
        self.publisher.publish(msg)
        
        self.get_logger().info(f'Published argument a: {msg.argument_a:.2f}')
        self.get_logger().info(f'Published argument b: {msg.argument_b:.2f}')

def main(args=None):
    rp.init(args=args)
    try:
        argument = ArgumentNode()
        try:
            rp.spin(argument)
        except KeyboardInterrupt:
            argument.get_logger().info('Keyboard Interrupt (SIGINT)')
        finally:
            argument.destroy_node()
    finally:       
        rp.shutdown()
    
if __name__=='__main__':
    main()