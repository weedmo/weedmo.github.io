import random

from ros_study_msgs.srv import ArithmeticOperator
import rclpy as rp
from rclpy.node import Node

class Operator(Node):
    
    def __init__(self):
        super().__init__('operator')
        
        # connection
        self.arithmetic_client = self.create_client(
            ArithmeticOperator,
            'arithmetic_operator')
        while not self.arithmetic_client.wait_for_service(timeout_sec=0.1):
            self.get_logger().warning('The arithmetic_operator service not available.')
    
    # Request        
    def send_request(self):
        service_request = ArithmeticOperator.Request()
        service_request.arithmetic_operator = random.randint(1,4)
        future = self.arithmetic_client.call_async(service_request)
        return future
    
def main(args=None):
    rp.init(args=args)
    operator = Operator()
    future = operator.send_request()
    user_trigger = True
    try:
        while rp.ok():
            if user_trigger is True:
                rp.spin_once(operator)
                if future.done():
                    try:
                        service_response = future.result()
                    except Exception as e:  # noqa: B902
                        operator.get_logger().warn('Service call failed: {}'.format(str(e)))
                    else:
                        operator.get_logger().info(
                            'Result: {}'.format(service_response.arithmetic_result))
                        user_trigger = False
            else:
                input('Press Enter for next service call.') # stop
                future = operator.send_request()
                user_trigger = True

    except KeyboardInterrupt:
        operator.get_logger().info('Keyboard Interrupt (SIGINT)')

    operator.destroy_node()
    rp.shutdown()


if __name__ == '__main__':
    main()