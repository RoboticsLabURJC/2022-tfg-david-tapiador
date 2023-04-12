#!/usr/bin/env python3

import pandas as pd
import numpy as np
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from nav_msgs.msg import Odometry
from scipy.spatial.transform import Rotation

bridge = CvBridge()
odom = [0,0,0]

# ros2 node class
class OdometerSubscriber(Node):

    def __init__(self, topic):

        super().__init__('odometer_subscriber')

        self.subscription = self.create_subscription(
            Odometry, topic, self.callback, 10)

        self.subscription  # prevent unused variable warning


    def callback(self, msg):

        global odom
        odom[0] = msg.pose.pose.position.x
        odom[1] = msg.pose.pose.position.y

        rot = Rotation.from_quat([msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w])
        odom[2] = rot.as_euler('xyz', degrees=True)[2]

def main(inputs, outputs, parameters, synchronise):
    
    global odom

    auto_enable = False
    try:
        enable = inputs.read_number('Enable')
    except Exception:
        auto_enable = True

    rclpy.init()
    odom_subscriber = OdometerSubscriber(parameters.read_string("ROSTopic"))

    try:
        while auto_enable or inputs.read_number('Enable'):
            
            rclpy.spin_once(odom_subscriber)
            print("ODOM -> " + str(odom))
            outputs.share_array("Odom",odom)

            synchronise()  
    except Exception as e:
        print('Error:', e)
        pass
    finally:
        print("Exiting")
        synchronise()     
        odom_subscriber.destroy_node()
        rclpy.shutdown()
