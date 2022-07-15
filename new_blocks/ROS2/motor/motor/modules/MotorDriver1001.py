#!/usr/bin/env python3

import numpy as np
from time import sleep
from utils.wires.wire_str import read_string
from utils.tools.freq_monitor import monitor_frequency

import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist

bridge = CvBridge()
velocities = 0

# ros2 node class
class VelPublisher(Node):

    def __init__(self, topic):
        super().__init__('vel_publisher')
        self.error = 0
        self.publisher_ = self.create_publisher(Twist, topic, 1)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        global velocities
        msg = Twist()
        
        try:
            msg.linear.x = float(velocities[0])
            msg.linear.y = float(velocities[1])
            msg.linear.z = float(velocities[2])
            msg.angular.x = float(velocities[3])
            msg.angular.y = float(velocities[4])
            msg.angular.z = float(velocities[5])
        except IndexError:
            print("bad length for input array")
            self.error = 1
            return
        self.publisher_.publish(msg)



def loop(block_name, input_wires, output_wires, parameters, flags):
    
    global velocities

    input_0 = read_string(input_wires[0])

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
    vel_publisher = VelPublisher(str(parameters[1]))

    try:

        while True:

            if enabled or (update := bool(enable_wire.get()[0])):

                velocities = input_0.get()
                rclpy.spin_once(vel_publisher)
                
            sleep(control_data[1])       
    
    except KeyboardInterrupt:

        vel_publisher.destroy_node()
        rclpy.shutdown()

        enable_wire.release()
        input_0.release()
