#!/bin/python3


import time
import rospy
from os import system
from mavros_msgs.srv import SetMode

set_mode = rospy.ServiceProxy('mavros/set_mode', SetMode)

command = "rosservice call /mavros/set_mode \"base_mode: 0 custom_mode: 'OFFBOARD'\""


while (True):
	set_mode(0,"OFFBOARD")
	time.sleep(4)
