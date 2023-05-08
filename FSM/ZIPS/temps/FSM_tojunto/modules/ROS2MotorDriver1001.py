#!/usr/bin/env python3

import numpy as np

import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist

bridge = CvBridge()
velocities = 0

# ros2 node class
class VelPublisher(Node):

    def __init__(self, topic):
        super().__init__('vel_publisher')
        self.publisher_ = self.create_publisher(Twist, topic, 1)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        global velocities
        msg = Twist()
        
        try:
            msg.linear.x = float(velocities[0])
            msg.linear.y = float(velocities[1])
            msg.linear.z = float(velocities[2])
            msg.angular.x = float(velocities[3])
            msg.angular.y = float(velocities[4])
            msg.angular.z = float(velocities[5])
        except IndexError:
            print("bad length for input array")
            return
        self.publisher_.publish(msg)



def main(inputs, outputs, parameters, synchronise):
    
    global velocities

    rclpy.init()
    vel_publisher = VelPublisher(parameters.read_string('ROSTopic'))

    try:
        while 1:
            enable = inputs.read_number('Enable')
            if enable == 1:

                velocities = inputs.read_array('Vels')
                try:
                    if velocities[0] != None:
                        rclpy.spin_once(vel_publisher) 
                    synchronise() 
                except Exception:
                    continue
            else:
                velocities = [0,0,0,0,0,0]
                rclpy.spin_once(vel_publisher) 
                synchronise()
    except KeyboardInterrupt:

        vel_publisher.destroy_node()
        rclpy.shutdown()
