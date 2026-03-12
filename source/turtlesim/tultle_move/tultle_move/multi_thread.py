import rclpy as rp
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from tultle_move.publisher_t import TurtlesimPublisher
from tultle_move.subscriber_t import TurtlesimSubscriber

def main(args=None):
    rp.init()
    
    sub = TurtlesimSubscriber()
    pub = TurtlesimPublisher()
    
    executor = MultiThreadedExecutor()
    
    executor.add_node(sub)
    executor.add_node(pub)
    
    try:
        executor.spin()
        
    finally:
        executor.shutdown()
        pub.destroy_node()
        rp.shutdown()
        
if __name__=='__main__':
    main()