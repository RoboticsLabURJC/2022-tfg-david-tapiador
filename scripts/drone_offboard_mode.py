#!/bin/python3


import time
import rospy
from os import system
from mavros_msgs.srv import SetMode

#set_mode = rospy.ServiceProxy('set_mode', mavros_msgs.srv.SetMode)
set_mode = rospy.ServiceProxy('mavros/set_mode', SetMode)

command = "rosservice call /mavros/set_mode \"base_mode: 0 custom_mode: 'OFFBOARD'\""


while (True):
	print(int(time.time()))
	#system(command)
	set_mode(0,"OFFBOARD")
	time.sleep(4)
