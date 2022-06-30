#!/usr/bin/env python3

import numpy as np
from time import sleep
from utils.wires.wire_str import read_string, share_string
from utils.tools.freq_monitor import monitor_frequency

import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import LaserScan

bridge = CvBridge()
measure = None

# ros2 node class
class LaserSubscriber(Node):

    def __init__(self, topic):

        super().__init__('laser_subscriber')

        self.subscription = self.create_subscription(
            LaserScan, topic, self.callback, 10)

        self.subscription  # prevent unused variable warning


    def callback(self, msg):

        global measure

        measure = []
        for i in range(len(msg.ranges)):
            measure.extend((str(msg.ranges[i]),))



def loop(block_name, input_wires, output_wires, parameters, flags):
    
    global measure

    output_0 = share_string(output_wires[0])

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
    laser_subscriber = LaserSubscriber(str(parameters[1]))

    try:

        while True:

            measure = None
            rclpy.spin_once(laser_subscriber)

            if enabled or (update := bool(enable_wire.get()[0])):

                if measure is not None:
                    print("MANDAMOS")
                    to_write = np.array(measure, dtype='<U64')
                    output_0.add(to_write)
                    control_data[0] += 1
                
            sleep(control_data[1])       
    
    except KeyboardInterrupt:

        laser_subscriber.destroy_node()
        rclpy.shutdown()

        enable_wire.release()
        output_0.release()
