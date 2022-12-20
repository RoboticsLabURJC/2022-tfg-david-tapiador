#!/usr/bin/env python3

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from sensor_msgs.msg import PointCloud2
from struct import unpack

measure = None

# ros2 node class
class DepthSubscriber(Node):

    def __init__(self, topic):

        super().__init__('depth_subscriber')

        ###******ROBOT REAL******###
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT,
            history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST,
            depth=1
        )
        self.subscription = self.create_subscription(
            PointCloud2, topic, self.callback, qos_profile=qos_profile)
        ###**********************###


        ###******ROBOT SIM*******###
        self.subscription = self.create_subscription(
            PointCloud2, topic, self.callback, 10)
        ###**********************###

        self.subscription  # prevent unused variable warning


    def callback(self, msg):

        global measure
        print("LEN -> ", end="")
        print(len(msg.data))
        measure = msg.data

def main(inputs, outputs, parameters, synchronise):
    global measure
    rclpy.init()
    depth_subscriber = DepthSubscriber(parameters.read_string("ROSTopic"))
    try:
        measure = None
        width = 640
        heigth = 480
        while(1):
            bbox = inputs.read_array("Bbox")
            if bbox is None:
                continue
            try:
                x = int(bbox[0]+bbox[2]/2)
                y = int(bbox[1]+bbox[3]/2)
            except:
                continue

            rclpy.spin_once(depth_subscriber)
            point = (width*y+x)*32+8
            depth = unpack('f', measure[point:point+4])
            print("DEPTH -> " + str(depth))
            outputs.share_array("Depth",depth)   
            synchronise()  
 
    except Exception as e:
        print('Error:', e)
        pass
    finally:
        print("Exiting") 
        depth_subscriber.destroy_node()
        rclpy.shutdown()
