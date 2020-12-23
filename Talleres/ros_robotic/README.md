# Robótica y Control Servovisual - Taller 1
Código de ROS para la solución de la parte práctica del Taller 1 para la asignatura Robótica y Control Servovisual.

<br />
<br />

**Autores:**
- Jesús Caballero
- Sebastián Cortés
- Jhohan Higuera
- ALejandro Montés
 
**Profesor:** Flavio Prieto

**Tutor:** Jose Fajardo

<br />
<br />

**Comandos:**

_Lanzar modelo en Gazebo y Rviz:_

    roslaunch ros_robotic ddrobot_load.launch
  
_Ejecutar nodo para la lectura del teclado y control del robot:_
  
    rosrun ros_robotic lecture

_Leer el topico que contiene la velocidad lineal y angular del robot (solo publica al momento de realizar una orden al robot):_

    rostopic echo -n 10 /vel_ddrobot
