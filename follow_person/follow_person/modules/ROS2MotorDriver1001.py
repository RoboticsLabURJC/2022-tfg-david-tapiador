#!/usr/bin/env python3

import numpy as np
from time import sleep

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
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        global velocities
        msg = Twist()
        
        try:
            #print("LAS VELOSIDADE -> ", end="")
            #print(velocities)
            # msg.linear.x = float(velocities[0])
            # msg.linear.y = float(velocities[1])
            # msg.linear.z = float(velocities[2])
            # msg.angular.x = float(velocities[3])
            # msg.angular.y = float(velocities[4])
            # msg.angular.z = float(velocities[5])
            msg.linear.x = 0
            msg.linear.y = 0
            msg.linear.z = 0
            msg.angular.x = 0
            msg.angular.y = 0
            msg.angular.z = 0
        except IndexError:
            print("bad length for input array")
            return
        self.publisher_.publish(msg)



def main(inputs, outputs, parameters, synchronise):
    
    global velocities

    auto_enable = False
    try:
        enable = inputs.read_number('Enable')
    except Exception:
        auto_enable = True

    rclpy.init()
    vel_publisher = VelPublisher(parameters.read_string('ROS Topic'))

    try:

        while auto_enable:
            try:
                decision = inputs.read_number("Decision")
                if(decision == 0):
                    velocities = inputs.read_array('Vels1')
                else:
                    velocities = inputs.read_array('Vels2')
            except Exception:
                continue
            try:
                if(velocities.any()):
                    rclpy.spin_once(vel_publisher) 
                    sleep(0.01)
                synchronise()   
            except Exception:
                continue
    
    except KeyboardInterrupt:

        vel_publisher.destroy_node()
        rclpy.shutdown()
