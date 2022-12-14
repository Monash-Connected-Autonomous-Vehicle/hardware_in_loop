#!/usr/bin/env python3
'''
Republishes twist messages found in Odometry topic in CARLA to
same topic as SD_interface
'''
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry

class TwistPub(Node):

    def __init__(self):
        super().__init__('carla_odom_to_twist')
        self.twist_pub = self.create_publisher(TwistStamped, '/twist_cmd', 10)
        self.odom_sub = self.create_subscription(Odometry,
            '/carla/ego_vehicle/odometry', self.odom_callback, 1)

        self.speed_scale_factor = 1/200
        self.steer_scale_factor = 1/10


    def odom_callback(self, odom_msg: Odometry):
        twist_msg = TwistStamped()
        twist_msg.header = odom_msg.header
        twist_msg.twist.linear.x = odom_msg.twist.twist.linear.x * self.speed_scale_factor
        twist_msg.twist.angular.z = odom_msg.twist.twist.angular.z * self.steer_scale_factor
        self.get_logger().info(f'speed: {twist_msg.twist.linear.x}, steer: {twist_msg.twist.angular.z}')
        self.twist_pub.publish(twist_msg)


def main(args=None):
    rclpy.init(args=args)

    twist_pub = TwistPub()
    rclpy.spin(twist_pub)
    twist_pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
