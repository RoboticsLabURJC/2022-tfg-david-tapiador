#!/usr/bin/env python3

import rospy
import numpy as np
from time import sleep
from geometry_msgs.msg import Twist
from utils.wires.wire_str import read_string
from utils.tools.freq_monitor import monitor_frequency

linear_velocity, angular_velocity = 0.0, 0.0

def callback(mem):
    
    global linear_velocity, angular_velocity
    
    msg = mem.get()
    if msg is not None:
        linear_velocity = float(msg[0])
        angular_velocity = float(msg[1])

def loop(block_name, input_wires, output_wires, parameters, flags):

    input_0 = read_string(input_wires[1])

    rospy.init_node("motordriverVC", anonymous=True)
    output_0 = rospy.Publisher(parameters[1], Twist, queue_size=10)

    enabled = False
    try:
        enable_wire = read_string(input_wires[0])
    except IndexError:
        enabled = True

    required_frequency, update = float(parameters[0]), 1
    control_data = np.array([0.0,0.03])

    if flags[0] == 1:
        monitor_frequency(block_name, control_data, required_frequency, update)

    data = Twist()

    try:
    
        while not rospy.is_shutdown():
        
            if enabled or (update := bool(enable_wire.get()[0])):
        
                callback(input_0)
                data.linear.x = linear_velocity
                data.angular.z = angular_velocity
                output_0.publish(data)
                control_data[0] += 1
                
            sleep(control_data[1])

    except KeyboardInterrupt:
    
        input_0.release()
        enable_wire.release()
