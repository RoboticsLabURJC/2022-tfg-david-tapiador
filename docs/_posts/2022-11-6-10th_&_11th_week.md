---
title: "10th and 11th weeks: Back into Gazebo11, tests with real Turtlebot2 and follow_person updates."
last_modified_at: 2022-11-06T20:30:00
categories:
  - Blog
tags:
  - ROS Humble
  - Visual Circuit
youtubeId_camer_real: MNaFWD9-ats
youtubeId_laser_real: -MweaxUVsCg
youtubeId_motor_real: 2uc8A_Bhx-Y
youtubeId_follow_person_no_move: Uir_iqMOplc
---

On these two weeks I went back to gazebo11, as it has better support for ros2 than ignition. 

Also I've had some problems when coming back to gazebo11. When spawning the robot model, the simulator freezed for some time, and later spawned the model without the base. This happened because the URDF model didn't find the meshes that corresponded to the wheels and the base of the robot.
I solved this error by manually changing the path to the meshes (previously was set as a relative path) to the absolute path on the [urdf file](https://github.com/RoboticsLabURJC/2022-tfg-david-tapiador/blob/main/turtlebot_sim/turtlebot2/urdf/turtlebot2.urdf#L28).

Also I tested the ROS2 blocks with the real turtlebot2, for what I needed to install several things. One of them was the [kobuki launcher](https://github.com/IntelligentRoboticsLabs/Robots/tree/humble) as well as the [third parties dependencies](https://github.com/IntelligentRoboticsLabs/Robots/blob/humble/kobuki/Readme.md#kobuki--rplidar-a2-setup), that I needed to launch the kobuki driver using ROS2 humble. Also for the camera, the one that the robot had was an asus xtion model, so I needed the [plugins](https://github.com/mgonzs13/ros2_asus_xtion) to use it with ROS2.

With everything installed, it was time to start testing the blocks!

With the camera, I used a camera block with a screen block to see what the camera shows. We can also see the rviz2 execution, where the image and the point cloud are shown:

{% include youtubePlayer.html id=page.youtubeId_camer_real %}


For the laser block, I show the rviz2 laser data and in the terminal all the data (number array) received by the ROS2 laser block:

{% include youtubePlayer.html id=page.youtubeId_laser_real %}


For the motor block, I used a 0.5 rotation velocity and the robot movement can be seen in the camera image shown by rviz2:

{% include youtubePlayer.html id=page.youtubeId_motor_real %}


I also tested the follow person project with the real robot. In this video we can see that the robot rotates to follow the bounding box of a person. Also we can see that with the real robot we don't have the problem of the fading bounding box, it is there everytime I stay on sight. Also we can see the PD controller making the robot rotate faster when the bounding box is farther from the middle, and slower when it gets closer.

{% include youtubePlayer.html id=page.youtubeId_follow_person_no_move %}


I didn't make the robot move linearly, but for the next week I will add a new block to receive the point cloud and be able to see the distance to the middle point of the bounding box (or the mean of the center points). With this I will be able to follow a person completely and maintain a constant distance by aplying a PID to the distance and moving faster when the person is farther!







