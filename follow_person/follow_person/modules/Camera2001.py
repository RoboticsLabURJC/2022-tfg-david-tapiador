import cv2

#*** CAM ***#
# def main(inputs, outputs, parameters, synchronise):
#     cap = cv2.VideoCapture(0)
#     auto_enable = False
#     try:
#         enable = inputs.read_number('Enable')
#     except Exception:
#         auto_enable = True
#     try:
#         while cap.isOpened() and (auto_enable or inputs.read_number('Enable')):
#             ret, frame = cap.read()
#             if not ret:
#                 continue
#             outputs.share_image("Img", frame)
#             outputs.share_number("Width", frame.shape[1])
#             synchronise()
#     except Exception as e:
#         print('Error:', e)
#         pass
#     finally:
#         print("Exiting")
#         cap.release()




#*** ROSCAM ***#

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
        frame = np.asarray(bridge.imgmsg_to_cv2(msg, "bgr8"), dtype=np.uint8)



def main(inputs, outputs, parameters, synchronise):
    global frame

    auto_enable = False
    try:
        enable = inputs.read_number('Enable')
    except Exception:
        auto_enable = True

    rclpy.init()
    camera_subscriber = CamSubscriber(parameters.read_string("ROSTopic"))

    try:
        while auto_enable or inputs.read_number('Enable'):
            frame =  None
            rclpy.spin_once(camera_subscriber)

            if frame is not None:
                outputs.share_image("Img", frame)
                outputs.share_number("Width", frame.shape[1])

            synchronise()
    except Exception as e:
        print('Error:', e)
        pass
    finally:
        print("Exiting")
        synchronise()     
        camera_subscriber.destroy_node()
        rclpy.shutdown()
