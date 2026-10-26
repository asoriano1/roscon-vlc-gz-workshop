# Post-ejercicio 2 — Los sensores de un RB-Summit, con el Bridge Manager (15 min)

Primero, la demo del ponente. Después, dos robots:

1. Tu `mini_bot`: el ejercicio 2 otra vez, sin tocar el `bridge.yaml`, para comparar.
2. Un **RB-Summit** de Robotnik: un LiDAR 3D, una cámara RGB-D, una IMU y un GPS. Su puente no lo
   has escrito, ni hace falta.

El **Bridge Manager** es un plugin de la GUI de Gazebo. Pregunta a Gazebo qué topics publica cada
modelo, propone el tipo de ROS 2 equivalente y lanza el mismo `ros_gz_bridge` que lanzas tú desde
`sim.launch.py`. Antes de lanzarlo, enseña el comando.

## 1. Lanza Gazebo con la suite e importa el `mini_bot`

Cierra el `sim.launch.py` (Ctrl+C) y lanza Gazebo con los plugins de la suite:

```bash
cd $WS/robots && ros2 launch gz_model_importer gazebo_importer.launch.py \
  world:=$(ros2 pkg prefix mini_bot)/share/mini_bot/worlds/workshop.sdf
```

Importa tu `mini_bot.urdf.xacro`, como en el post-ejercicio 1, pero esta vez **con *Namespace* y
*Frame prefix* vacíos**: el mismo robot que en `sim.launch.py`. Deja marcado
**robot_state_publisher**, pulsa **Import** y después ▶.

Este launch ya puentea `/clock` por su cuenta.

## 2. El `mini_bot`, con el Bridge Manager

1. Abre el panel **ROS 2 Bridge Manager** y pulsa **Refresh**.
2. Los topics aparecen agrupados por modelo. Marca el LiDAR, las dos cámaras y el ultrasonido.
3. Despliega **Bridge command** y **léelo antes de lanzarlo**.
4. Pulsa **Run**.
5. Abre RViz en otra terminal, con la configuración del ejercicio 2:

   ```bash
   ros2 run rviz2 rviz2 -d $(ros2 pkg prefix mini_bot)/share/mini_bot/rviz/ejercicio_2.rviz \
     --ros-args -p use_sim_time:=true
   ```

Abre a la vez tu `config/bridge.yaml` y el **Bridge command** del panel. Son la misma
información: una la escribiste mirando `gz topic -l`, la otra ha salido de recorrer el mundo.

## 3. El RB-Summit

1. Importa `rbsummit.urdf.xacro` con *Namespace* `summit_a` y *Frame prefix* `summit_a/`, como en
   el post-ejercicio 1, lejos del `mini_bot`. **Import** y ▶.
2. En el Bridge Manager, **Refresh**. Sale un grupo nuevo, `summit_a`, con sus sensores. Mira los
   tipos que propone: la nube de puntos del LiDAR 3D es `PointCloudPacked` en Gazebo y
   `PointCloud2` en ROS 2.
3. Marca la nube de puntos del LiDAR (`/summit_a/top_lidar/scan/points`) y la imagen de la cámara
   de color (`/summit_a/front_camera_color/color/image_raw`). Lee el *Bridge command* y pulsa
   **Run**.
4. Cierra el RViz del `mini_bot` y abre el del Summit:

   ```bash
   ros2 run rviz2 rviz2 -d $(ros2 pkg prefix mini_bot)/share/mini_bot/rviz/post2_rbsummit.rviz \
     --ros-args -p use_sim_time:=true
   ```

   Salen el robot, la nube de puntos del LiDAR coloreada por altura y la imagen de la cámara.

## Comprueba

```bash
ros2 topic list | grep summit_a
ros2 topic hz /summit_a/top_lidar/scan/points
ros2 topic echo /summit_a/top_lidar/scan/points --once --field header.frame_id
```

El `frame_id` lleva el prefijo, `summit_a/top_3d_laser_link`: por eso RViz encuentra el sensor en
el árbol de TF del Summit.

## La comparación

Para el `mini_bot` escribiste seis entradas de YAML. El Summit tiene nueve topics de sensores, con
tres tipos de mensaje que no salían en tu tabla (`PointCloudPacked`, `IMU` y `NavSat`), y todos con
su namespace. Echa la cuenta: cuánto
costaría escribir a mano el YAML de tres robots así.

El YAML sigue siendo lo que se versiona y se lanza sin GUI. El Bridge Manager sirve para descubrir
qué hay y probarlo; el comando que enseña es el punto de partida del YAML.

## Preguntas

1. ¿Qué topics de Gazebo no aparecen como puenteables, y por qué?
2. Al marcar un sensor más, ¿reinicia el puente o lanza otro proceso? Míralo con
   `ros2 node list` antes y después.
3. Si hubieras importado el Summit con el *Frame prefix* vacío, ¿qué `frame_id` llevaría la nube
   de puntos? ¿Con qué frames del `mini_bot` chocaría en TF?

## Errores típicos

| Síntoma | Causa |
|---|---|
| El panel no lista nada | Falta pulsar *Refresh*, o la simulación está en pausa (después de importar): ▶ y *Refresh* |
| No aparece un sensor | El sensor no publica todavía: comprueba que la simulación corre y mira `gz topic -l` |
| Los topics del `mini_bot` salen en ROS 2 pero RViz no pinta nada | El *Fixed Frame* tiene que ser `base_footprint` |
| RViz del Summit no pinta nada y avisa de un frame que no existe | El *Frame prefix* no es `summit_a/`: el *Fixed Frame* de `post2_rbsummit.rviz` es `summit_a/base_footprint` |
| El Summit no tiene sensores en el panel | Se importó un xacro distinto: tiene que ser `rbsummit.urdf.xacro` de `$WS/robots` |
| La simulación va lenta con el Summit | Sus sensores se renderizan cuando alguien se suscribe: puentea solo los dos de la lista |
