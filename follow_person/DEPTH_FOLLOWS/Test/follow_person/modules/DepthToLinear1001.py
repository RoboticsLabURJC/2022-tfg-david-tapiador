import cv2

#*** ROSCAM Depth ***#

import numpy as np
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

bridge = CvBridge()
frame = None

# ros2 node class
class CamSubscriber(Node):

    def __init__(self, topic):

        super().__init__('cam_subscriber')
        self.subscription = self.create_subscription(
            Image, topic, self.callback, 10)

        self.subscription  # prevent unused variable warning


    def callback(self, msg):

        global frame
        frame = msg.data
        print("LEN frame ->" + str(len(frame)))



def main(inputs, outputs, parameters, synchronise):
    global frame

    auto_enable = False
    try:
        enable = inputs.read_number('Enable')
    except Exception:
        auto_enable = True

    rclpy.init()
    camera_subscriber = CamSubscriber(parameters.read_string("ROSTopic"))
    print("PREWHILE")
    try:
        while auto_enable or inputs.read_number('Enable'):
            print("WHILE INIT")
            frame =  None
            rclpy.spin_once(camera_subscriber)
            print("SPINNED")
            if frame is not None:
                bbox = inputs.read_array("BoundingBox")
                if bbox is None:
                    continue
                try:
                    x = int(bbox[0]+bbox[2]/2)
                    y = int(bbox[1]+bbox[3]/2)
                except Exception:
                    continue

                dist = frame[x][y]
                
                print("DISTANCIA -> " + str(dist))
                outputs.share_number("Linear", dist)

            synchronise()
    except Exception as e:
        print('Error:', e)
        pass
    finally:
        print("Exiting")
        synchronise()     
        camera_subscriber.destroy_node()
        rclpy.shutdown()
