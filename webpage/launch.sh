#!/bin/bash

docker_ID=`sudo docker ps | grep -v CONTAINER | cut -d ' ' -f1`
echo $docker_ID

# Display 0
sudo docker exec $docker_ID /usr/bin/Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile ./xdummy.log -config /xorg.conf :0 &
sleep 1
sudo docker exec $docker_ID x11vnc -display :0 -nopw -forever -xkb -rfbport 5900 &
sleep 1
sudo docker exec $docker_ID /noVNC/utils/novnc_proxy --listen 6080 --vnc localhost:5900 &
sleep 2

# Display 1
sudo docker exec $docker_ID /usr/bin/Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile ./xdummy.log -config /xorg.conf :1 &
sleep 1
sudo docker exec $docker_ID x11vnc -display :1 -nopw -forever -xkb -rfbport 5901 &
sleep 1
sudo docker exec $docker_ID /noVNC/utils/novnc_proxy --listen 6081 --vnc localhost:5901 & 
sleep 2

# Display 2
sudo docker exec $docker_ID /usr/bin/Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile ./xdummy.log -config /xorg.conf :2 &
sleep 1
sudo docker exec $docker_ID x11vnc -display :2 -nopw -forever -xkb -rfbport 5902 &
sleep 1
sudo docker exec $docker_ID /noVNC/utils/novnc_proxy --listen 6082 --vnc localhost:5902 & 
sleep 2

# Display 3
sudo docker exec $docker_ID /usr/bin/Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile ./xdummy.log -config /xorg.conf :3 &
sleep 1
sudo docker exec $docker_ID x11vnc -display :3 -nopw -forever -xkb -rfbport 5903 &
sleep 1
sudo docker exec $docker_ID /noVNC/utils/novnc_proxy --listen 6083 --vnc localhost:5903 & 
sleep 3

reset

sudo docker exec -it $docker_ID /bin/bash

