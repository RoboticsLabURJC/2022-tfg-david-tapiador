import numpy as np
from time import sleep
from utils.wires.wire_img import share_image
from utils.wires.wire_str import read_string
from utils.tools.freq_monitor import monitor_frequency

import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

bridge = CvBridge()
img = None

# ros2 node class
class CamSubscriber(Node):

    def __init__(self, topic):

        super().__init__('cam_subscriber')

        self.subscription = self.create_subscription(
            Image, topic, self.callback, 10)

        self.subscription  # prevent unused variable warning


    def callback(self, msg):

        global img
        img = np.asarray(bridge.imgmsg_to_cv2(msg, "bgr8"), dtype=np.uint8)



def loop(block_name, input_wires, output_wires, parameters, flags):
    
    global img

    output_0 = share_image(output_wires[0])

    enabled = False
    try:
        enable_wire = read_string(input_wires[0])
    except IndexError:
        enabled = np.True_

    required_frequency, update = float(parameters[0]), 1
    control_data = np.array([0.0,0.03])

    if flags[0] == 1:
        monitor_frequency(block_name, control_data, required_frequency, update)

    rclpy.init()
    camera_subscriber = CamSubscriber(str(parameters[1]))

    try:

        while True:

            img =  None
            rclpy.spin_once(camera_subscriber)

            if enabled or (update := bool(enable_wire.get()[0])):

                if img is not None:
                    output_0.add(img)
                    control_data[0] += 1
                
            sleep(control_data[1])       
    
    except KeyboardInterrupt:

        camera_subscriber.destroy_node()
        rclpy.shutdown()

        enable_wire.release()
        output_0.release()
