#!/usr/bin/env python3

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
        print("THE TOPIC IS -> " + topic)
        self.subscription = self.create_subscription(
            Image, topic, self.callback, 10)

        self.subscription  # prevent unused variable warning


    def callback(self, msg):

        global frame
        frame = np.asarray(bridge.imgmsg_to_cv2(msg, "bgr8"), dtype=np.uint8)
        print("SENDING IMG")




def main(inputs, outputs, parameters, synchronise):
    global frame

    auto_enable = False
    try:
        enable = inputs.read_number('Enable')
    except Exception:
        auto_enable = True

    rclpy.init()
    camera_subscriber = CamSubscriber(parameters.read_string("ROS Topic"))

    try:
        while auto_enable or inputs.read_number('Enable'):
            frame =  None
            rclpy.spin_once(camera_subscriber)

            if frame is not None:
                outputs.share_image("Img", frame)

            outputs.share_image("Img", frame)
            synchronise()
    except Exception as e:
        print('Error:', e)
        pass
    finally:
        print("Exiting")
        synchronise()     
        camera_subscriber.destroy_node()
        rclpy.shutdown()
