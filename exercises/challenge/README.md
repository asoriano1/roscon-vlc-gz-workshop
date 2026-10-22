# Reto final por parejas (15 min)

Cada pareja elige **uno**. A falta de 5 minutos para el cierre, dos parejas enseñan su pantalla.

## A — Ampliar el mini_bot

Añadir un sensor más al `mini_bot`: un segundo LiDAR mirando atrás, una IMU o una cámara de
profundidad. Reimportarlo con el Model Importer y comprobar que el sensor nuevo aparece solo en
el Bridge Manager.

Criterio de éxito: el sensor publica en ROS 2 sin escribir una línea de YAML.

## B — Flota de mini_bots

Cuatro `mini_bot` en el mismo mundo, cada uno con su namespace y su prefijo de frames
(`robot_a/` … `robot_d/`), todos con LiDAR puenteado y controlador activo.

La dificultad de verdad: **verlos los cuatro a la vez en RViz.** Cada robot tiene su propio árbol
de TF colgando de su `robot_x/odom`, y ninguno sabe dónde está el otro. Hace falta un frame
común: un `static_transform_publisher` por robot, desde `world` hasta su `odom`, con la pose en
la que se importó:

```bash
ros2 run tf2_ros static_transform_publisher --x 0 --y 1.5 \
  --frame-id world --child-frame-id robot_b/odom --ros-args -p use_sim_time:=true
```

Es exactamente lo que se hace en multi-robot de verdad: un mapa común y la odometría de cada robot
colgando de él.

Criterio de éxito: `ros2 topic list | grep -c scan` devuelve 4, los cuatro se mueven, y en RViz
con *Fixed Frame* `world` se ven los cuatro robots y sus cuatro LaserScan a la vez.

## C — Un robot propio

Importar el URDF o xacro de un robot propio.

- Si falla: leer el informe de preflight y contar qué ha detectado.
- Si funciona: puentear sus sensores y enseñarlo.

Es el reto más útil para la suite: los fallos que salgan aquí son issues reales. Conviene
apuntarlos para abrirlos en GitHub al terminar.

## Si sobra tiempo

Cronometrar cuánto se tarda ahora en montar lo de los ejercicios 1 a 5 desde cero, y compararlo
con la primera marca.
