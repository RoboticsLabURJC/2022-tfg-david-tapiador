# Docker con Turtlebot2 simulado

Se necesita que esté en una misma carpeta los Dockerfile y la carpeta turtlebot2, brain_turtle, robotics_academy
- El docker tiene como base Ubuntu 22.04 e incluye ros2 humble y Gazebo 11

## Modo de uso
Para crear la imagen (base nvidia con ubuntu 22.04)
~~~
./build.sh
~~~

Para crear el contenedor 
~~~
./run.sh
~~~

Para entrar en la máquina con bash:
~~~
sudo docker exec -it [ID] /bin/bash
~~~

### Dentro del contenedor 

Para lanzar xserver, vnc y novnc
~~~
/xserver.sh [display]
/vnc_novnc.sh [display] [in_port] [out_port]
~~~
* Ejemplo (importante primero lanzar xserver)
~~~
/xserver.sh :0
/vnc_novnc.sh :0 5900 6080
~~~
* Los puertos utilizados en [esta plantilla html](https://github.com/RoboticsLabURJC/2022-tfg-lucia-chen/tree/main/frontend) son: 6080 para gzclient, 1108 para consola, 6081 para rviz2 y 6082 para la ventana GUI.

Para lanzar el robot en un mundo vacío, abrir gzclient y rviz2 (estando en /home/turtlebot2_ws)
~~~
./empty_world_robot
~~~

Para teleoperar el robot:
~~~
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/cmd_vel -p use_sim_time:=true
~~~
