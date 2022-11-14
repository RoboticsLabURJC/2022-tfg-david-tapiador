# Turtlebot2 setup and dependencies

## Installation
Install one package and add the user to the dialout group (not needed if already in it)
```shell
sudo apt install ros-humble-depth-image-proc
sudo usermod -aG dialout tapi1300
```
Clone the Robots repository
```shell
cd ~/ros2_ws/src
git clone -b humble https://github.com/IntelligentRoboticsLabs/Robots.git
```
Install the third party repositories needed for the kobuki
```shell
vcs import . < Robots/kobuki/third_parties.repos
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
```
Install the third party repositories needed for the kobuki
```shell
cd ~/ros2_ws/src/ThirdParty/kobuki_ftdi
sudo mv 60-kobuki.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
```
Install the camera plugins for the xtion real camera.
```shell
cd ~/ros2_ws/src
git clone https://github.com/mgonzs13/ros2_asus_xtion
cd ~/ros2_ws/src/ros2_asus_xtion
rm -rf openni2_camera
git clone -b ros2 git@github.com:mikeferguson/openni2_camera.git
```
Compile everything
```shell
colcon build --symlink-install
```

## Usage with real Turtlebot2
Launch the kobuki driver and the camera driver
```shell
ros2 launch ir_kobuki kobuki_rplidar.launch.py
ros2 launch asus_xtion asus_xtion.launch.py
```
To see the camera in rviz2:
```shell
ros2 launch asus_xtion_visualization rviz2.launch.py
```







