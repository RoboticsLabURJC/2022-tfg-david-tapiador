#!/bin/bash

sudo docker build -f Dockerfile.base -t humble_base .
sudo docker build --no-cache=true -f Dockerfile.turtlebot -t turtlebot2 .
