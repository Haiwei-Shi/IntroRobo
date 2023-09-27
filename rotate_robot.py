###########
#Haiwei Shi
#Paul Blum
###########


import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Twist

class Rotate_Robot(Node):
    
    def __init__(self):
        super().__init__("Rotate_Robot")
        
        # Create a subscriber which receive coordinate message 
        # from 'find_object' node in the 'position_topic'
        self._point_subscribe = self.create_subscription(
            Point,
            'position_topic',
            self._rotator_callback,
            5
        )
        
        # Create a publisher which publish the turning speed
        # to turtlebots in the '/cmd_vel' topic
        self._vel_publish = self.create_publisher(
            Twist, 
            '/cmd_vel', 
            5
        )
        
    def _rotator_callback(self, msg):
        
        # Calculate the turning speed
        # Normalize the coordinate by the length limit 
        # So that the magnitude of turning speed can be constrained
        # Minus center to get direction of turing
        # Multiply a Kp to turn into a Proportional Controller
        vel = ((msg.x/320)-0.5) * 4
        
        twist = Twist()
        twist.angular.z = vel
        self.get_logger().info('Normalized position is ' + str((msg.x/320)-0.5))
        self.get_logger().info('Turning in speed of ' + str(vel) + ' rad/s')
        self._vel_publish.publish(twist)
        
        
        
        
def main(args=None):
    
    rclpy.init(args=args)
    rotate_robot = Rotate_Robot()
    
    rclpy.spin(rotate_robot)
    rotate_robot.destroy_node()
    rclpy.shutdown()
    
    
    
if __name__ == '__main__':
    main()