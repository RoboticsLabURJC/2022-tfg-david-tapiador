FROM ubuntu:22.04


ARG WORKSPACE=/ros2_ws
ARG DEBIAN_FRONTEND=noninteractive


# Install CLI tools
RUN apt-get update && apt-get install -y \
  curl \
  lsb-release \
  python3 \
  git \
  gnupg \
  build-essential \
  apt-utils

# Install ROS
ENV ROS_DISTRO humble
ENV AMENT_PREFIX_PATH=/opt/ros/humble
ENV COLCON_PREFIX_PATH=/opt/ros/humble
ENV PYTHONPATH=/opt/ros/humble/lib/python3.10/site-packages
ENV ROS_PYTHON_VERSION=3
ENV ROS_VERSION=2


RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key  -o /usr/share/keyrings/ros-archive-keyring.gpg \
  && sh -c 'echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null' \
  && apt-get update \
  && apt-get upgrade \
  && apt-get -y install ros-$ROS_DISTRO-ros-base





# Install ROS packages
RUN apt-get install -y \
  python3-colcon-common-extensions \
  ros-$ROS_DISTRO-gazebo-* \
  python3-rosdep

# Rosdep config
RUN rosdep init \
  && rosdep update \
  && rosdep fix-permissions


# Creating workspace
SHELL ["/bin/bash", "-c"] 
RUN source /opt/ros/$ROS_DISTRO/setup.bash

RUN mkdir -p ${WORKSPACE}/src
WORKDIR ${WORKSPACE}/src
RUN git clone https://github.com/RoboticsLabURJC/2022-tfg-david-tapiador.git

RUN rosdep update \
  && rosdep install --from-paths . --ignore-src -r -y

WORKDIR ${WORKSPACE}
RUN colcon build --symlink-install


SHELL ["/bin/bash", "-c"]
RUN . /${WORKSPACE}/install/setup.sh
