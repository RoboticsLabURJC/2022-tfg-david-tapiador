#!/usr/bin/env python3

import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from struct import unpack

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
        print("LEN -> ", end="")
        print(len(msg.data))
        measure = msg.data
        # for i in range(len(msg.data)):
        #     measure.extend((str(msg.data[i]),))

def main():
    global measure
    rclpy.init()
    # depth_subscriber = DepthSubscriber(parameters.read_string("ROSTopic"))
    depth_subscriber = DepthSubscriber("/depth_camera/points")
    try:
        measure = None
        rclpy.spin_once(depth_subscriber)
        width = 640
        heigth = 480
        x = int(width/2)
        y = 0
        if measure is not None:
            point = (width*y+x)*32
            [x,y,z] = unpack('3f', measure[point:point+3*4])
            print("X -> " + str(x), end="\t")
            print("Y -> " + str(y), end="\t")
            print("Z -> " + str(z))
                # print("SEND")
                # outputs.share_array("Depth",measure)   
 
    except Exception as e:
        print('Error:', e)
        pass
    finally:
        print("Exiting") 
        depth_subscriber.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()