#!/bin/sh

# Check if number of arguments is not 1 or 2 or if the first argument is not -r or -s
if ([ ! $# -eq 1 ] && [ ! $# -eq 2 ]) || ([ $1 != "-r" ] && [ $1 != "-s" ]); then
    echo "usage: sudo ./setup_docker.sh [-r/-s] [DOCKER_NAME]"
    exit
fi

if [ $1 = "-r" ]; then
    sudo cat docker_real.txt > Dockerfile
    NAME="turtlebot2_real"
elif [ $1 = "-s" ]; then
    sudo cat docker_sim.txt > Dockerfile
    NAME="turtlebot2_sim"
fi


if [ $# -eq 2 ]; then
    NAME=`echo $2 | tr '[:upper:]' '[:lower:]'`
fi

sudo docker build -t $NAME .