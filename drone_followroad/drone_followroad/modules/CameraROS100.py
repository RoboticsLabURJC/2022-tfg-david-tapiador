#!/usr/bin/env python3

import numpy as np
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from time import sleep
from utils.wires.wire_img import share_image
from utils.wires.wire_str import read_string
from utils.tools.freq_monitor import monitor_frequency

bridge = CvBridge()
img = None

def callback(msg):
    
    global img
    img = np.asarray(bridge.imgmsg_to_cv2(msg, "bgr8"), dtype=np.uint8)

def loop(block_name, input_wires, output_wires, parameters, flags):

    output_0 = share_image(output_wires[0])

    enabled = False
    try:
        enable_wire = read_string(input_wires[0])
    except IndexError:
        enabled = True

    required_frequency, update = float(parameters[0]), 1
    control_data = np.array([0.0,0.03])

    if flags[0] == 1:
        monitor_frequency(block_name, control_data, required_frequency, update)

    rospy.init_node("camera_ros", anonymous=True)
    
    camera_subscriber = rospy.Subscriber(parameters[1], Image, callback)
    
    while img is None:
        pass

    try:
    
        while not rospy.is_shutdown():
    
            if enabled or (update := bool(enable_wire.get()[0])):
            
                output_0.add(img)
                control_data[0] += 1
                
            sleep(control_data[1])       
    
    except KeyboardInterrupt:
    
        enable_wire.release()
        output_0.release()
