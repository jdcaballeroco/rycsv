# Modelos de robots para prueba de pub/sub

En este paquete se encuentran los modelos de los robots para realizar los ejercicios de publicadores y subscriptores de ROS de la clase de RyCSV.

## Robot 1

El robot 1 tiene tres ruedas tipo suecas con los rodillos a 90 grados:

<img src="https://render.githubusercontent.com/render/math?math=\gamma=0">

Las ruedas estan en las esquinas de un triangulo rectangulo de lado <img src="https://render.githubusercontent.com/render/math?math=l=0.5">

La configuración de las ruedas y del sistema de referencia del robot es como se muestra en la imagen inferior:

<img src="./imgs/Esquema_robot_1.png" heigh=200 alt="Esquema_robot_1">

Con esta configuración se obtienen los siguientes parametros:

<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top}
</style>
<table class="tg">
<thead>
  <tr>
    <th class="tg-0pky"><img src="https://render.githubusercontent.com/render/math?math=Rueda"></th>
    <th class="tg-0pky"><img src="https://render.githubusercontent.com/render/math?math=l"></th>
    <th class="tg-0pky"><img src="https://render.githubusercontent.com/render/math?math=\alpha"></th>
    <th class="tg-0pky"><img src="https://render.githubusercontent.com/render/math?math=\beta"></th>
    <th class="tg-0pky"><img src="https://render.githubusercontent.com/render/math?math=\gamma"></th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-0pky"><img src="https://render.githubusercontent.com/render/math?math=front"></td>
    <td class="tg-0pky"><img src="https://render.githubusercontent.com/render/math?math=0.433"></td>
    <td class="tg-0pky"><img src="https://render.githubusercontent.com/render/math?math=0.0"></td>
    <td class="tg-0pky"><img src="https://render.githubusercontent.com/render/math?math=0.0"></td>
    <td class="tg-0pky"><span style="font-weight:400;font-style:normal"><img src="https://render.githubusercontent.com/render/math?math=0.0"></span></td>
  </tr>
  <tr>
    <td class="tg-0pky"><img src="https://render.githubusercontent.com/render/math?math=left"></td>
    <td class="tg-0pky"><img src="https://render.githubusercontent.com/render/math?math=0.25"></td>
    <td class="tg-0pky"><img src="https://render.githubusercontent.com/render/math?math=\frac{\pi}{2}"></td>
    <td class="tg-0pky"><span style="font-weight:400;font-style:normal"><img src="https://render.githubusercontent.com/render/math?math=0.0"></span></td>
    <td class="tg-0pky"><span style="font-weight:400;font-style:normal"><img src="https://render.githubusercontent.com/render/math?math=0.0"></span></td>
  </tr>
  <tr>
    <td class="tg-0pky"><img src="https://render.githubusercontent.com/render/math?math=right"></td>
    <td class="tg-0pky"><img src="https://render.githubusercontent.com/render/math?math=0.25"></td>
    <td class="tg-0pky"><img src="https://render.githubusercontent.com/render/math?math=-\frac{\pi}{2}"></td>
    <td class="tg-0pky"><img src="https://render.githubusercontent.com/render/math?math=\pi"></td>
    <td class="tg-0pky"><span style="font-weight:400;font-style:normal"><img src="https://render.githubusercontent.com/render/math?math=0.0"></span></td>
  </tr>
</tbody>
</table>

<br/>

<img src="./imgs/Esquema_robot_1_sol.png" heigh=200 alt="Modelo_robot_1">

## Robot 2

El robot 2 tiene cuatro ruedas tipo suecas con los rodillos a 90 grados:

<img src="https://render.githubusercontent.com/render/math?math=\gamma=0">

Las ruedas estan en las esquinas de un cuadrado de lado <img src="https://render.githubusercontent.com/render/math?math=l=0.5"> el cual esta rotado 45 grados.

La configuración de las ruedas y del sistema de referencia del robot es como se muestra en la imagen inferior:

<img src="./imgs/Esquema_robot_2.png" heigh=200 alt="Esquema_robot_2">

