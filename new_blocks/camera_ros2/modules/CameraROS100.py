#!/usr/bin/env python3

import numpy as np
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from time import sleep
from utils.wires.wire_img import share_image
from utils.wires.wire_str import read_string
from utils.tools.freq_monitor import monitor_frequency


bridge = CvBridge()
img = None

# ros2 node class
class CamSubscriber(Node):

    def __init__(self):
        super().__init__('cam_subscriber')
        self.subscription = self.create_subscription(
            Image,
            '/depth_camera/image_raw',
            self.callback,
            10)
        self.subscription  # prevent unused variable warning
        print("SUB CREATED")

    def callback(self, msg):
        global img
        print("A new image is received")
        img = np.asarray(bridge.imgmsg_to_cv2(msg, "bgr8"), dtype=np.uint8)





rclpy.init()

camera_subscriber = CamSubscriber()

def loop(block_name, input_wires, output_wires, parameters, flags):

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

    print("Llega hasta aqui")
    rclpy.spin_once(camera_subscriber)
    print("Aqui ya no")

    while img is None:
        pass
    print("post - bucling")

    try:
    
        print("trying")
        while not rclpy.is_shutdown():
            rclpy.spin_once(camera_subscriber)
            print("Hola")
            if enabled or (update := bool(enable_wire.get()[0])):
            
                output_0.add(img)
                control_data[0] += 1
                
            sleep(control_data[1])       
    
    except KeyboardInterrupt:
        camera_subscriber.destroy_node()
        rclpy.shutdown()
        enable_wire.release()
        output_0.release()
