#!/usr/bin/env python3

import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2

measure = None

# ros2 node class
class DepthSubscriber(Node):

    def __init__(self, topic):

        super().__init__('depth_subscriber')

        self.subscription = self.create_subscription(
            PointCloud2, topic, self.callback, 10)

        self.subscription  # prevent unused variable warning


    def callback(self, msg):

        global measure
        
        measure = msg.data



def main(inputs, outputs, parameters, synchronise):
    
    global measure

    auto_enable = False
    try:
        enable = inputs.read_number('Enable')
    except Exception:
        auto_enable = True

    rclpy.init()
    depth_subscriber = DepthSubscriber(parameters.read_string("ROSTopic"))

    try:
        while auto_enable or inputs.read_number('Enable'):
            measure = None
            rclpy.spin_once(depth_subscriber)

            if measure is not None:
                outputs.share_array("Out",measure)   

            synchronise()  
    except Exception as e:
        print('Error:', e)
        pass
    finally:
        print("Exiting")
        synchronise()     
        depth_subscriber.destroy_node()
        rclpy.shutdown()
