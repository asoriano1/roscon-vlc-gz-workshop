# Post-ejercicio 2 — Los sensores de dos `mini_bot`, con el Bridge Manager (13 min)

Primero te lo enseño en directo, en el proyector. Después, haz el ejercicio 2 otra vez sin tocar
el `bridge.yaml`, y con dos robots: `robot_a` y `robot_b`, cada uno con su namespace.

El **Bridge Manager** es un plugin de la GUI de Gazebo. Pregunta a Gazebo qué topics publica cada
modelo, propone el tipo de ROS 2 equivalente y lanza el mismo `ros_gz_bridge` que lanzas tú desde
`sim.launch.py`. Antes de lanzarlo, enseña el comando.

## 1. Gazebo con la suite y dos `mini_bot`

Cierra el `sim.launch.py` (Ctrl+C) y lanza Gazebo con la suite:

```bash
cd $WS/robots && ros2 launch mini_bot suite.launch.py
```

Importa tu `mini_bot.urdf.xacro` dos veces, como en el post-ejercicio 1, con
**robot_state_publisher** marcado y estos campos:

| *Namespace* | *Frame prefix* | *Pose* x |
|---|---|---|
| `robot_a` | `robot_a/` | `0` |
| `robot_b` | `robot_b/` | `-0.9` |

`robot_b` queda detrás de `robot_a`, mirando hacia el mismo lado: el ultrasonido de `robot_a` lo
tiene delante. Después de cada **Import**, pulsa ▶.

## 2. El Bridge Manager

1. Despliega el panel **ROS 2 Bridge Manager** (abajo a la derecha, con un clic en su título) y
   pulsa **Refresh**. Si un robot recién importado sale sin sensores, espera unos segundos y pulsa
   **Refresh** otra vez.
2. Los topics aparecen agrupados por modelo: `robot_a` y `robot_b`. En cada uno, marca el LiDAR,
   las dos cámaras y el ultrasonido.
3. Despliega **Bridge command** y **léelo antes de lanzarlo**.
4. Pulsa **Run**.
5. Abre RViz en otra terminal, con los sensores de `robot_a` ya cargados:

   ```bash
   ros2 run rviz2 rviz2 -d $(ros2 pkg prefix mini_bot)/share/mini_bot/rviz/post2_minibot.rviz \
     --ros-args -p use_sim_time:=true
   ```

Abre a la vez tu `config/bridge.yaml` y el **Bridge command** del panel. Son la misma
información: una la escribiste mirando `gz topic -l`, la otra ha salido de recorrer el mundo.

## Comprueba

```bash
ros2 topic list | grep robot_
ros2 topic echo /robot_a/scan --once --field header.frame_id
ros2 topic echo /robot_a/ultrasound --once --field ranges
```

Los topics salen con el namespace de cada robot, y el `frame_id` con su prefijo,
`robot_a/lidar_link`: por eso RViz encuentra cada sensor en el árbol de TF de su robot. El
ultrasonido de `robot_a` mide la distancia hasta `robot_b`.

## La comparación

Para un `mini_bot` sin namespace escribiste seis entradas de YAML. Para dos con namespace harían
falta el doble, con todos los nombres cambiados: el `bridge.yaml` usa nombres absolutos, así que
no sirve el mismo para los dos robots. El panel ha encontrado los ocho topics con su namespace sin
que escribas ninguno.

El YAML sigue siendo lo que se versiona y se lanza sin GUI. El Bridge Manager sirve para descubrir
qué hay y probarlo; el comando que enseña es el punto de partida del YAML.

## Preguntas

1. ¿Qué topics de Gazebo no aparecen como puenteables, y por qué?
2. Con el puente en marcha, marca un sensor más. ¿Qué dice el estado del panel? Mira
   `ros2 node list` antes y después de pulsar el botón que te propone.
3. ¿Qué cambiarías en RViz para ver los sensores de `robot_b`?

## Extra: los sensores de un RB-Summit

Opcional, si te sobra tiempo. Un robot real de Robotnik: un LiDAR 3D, una cámara RGB-D, una IMU y
un GPS.

1. Importa `rbsummit.urdf.xacro` con *Namespace* `summit_a`, *Frame prefix* `summit_a/`,
   **robot_state_publisher** marcado y *Pose* y `2.5`, lejos de los `mini_bot`. **Import** y ▶.
2. Espera unos segundos: el Summit tarda más que el `mini_bot` en crear sus sensores. En el Bridge
   Manager, **Refresh**. Sale un grupo nuevo, `summit_a`, con nueve topics. Mira los tipos que
   propone: la nube de puntos del LiDAR 3D es `PointCloudPacked` en Gazebo y `PointCloud2` en
   ROS 2.
3. Marca la nube de puntos del LiDAR (`/summit_a/top_lidar/scan/points`) y la imagen de la cámara
   de color (`/summit_a/front_camera_color/color/image_raw`). El estado del panel pasa a
   **Restart required**: el puente que corre todavía es el de antes. Pulsa **Restart**.
4. Abre otro RViz, el del Summit:

   ```bash
   ros2 run rviz2 rviz2 -d $(ros2 pkg prefix mini_bot)/share/mini_bot/rviz/post2_rbsummit.rviz \
     --ros-args -p use_sim_time:=true
   ```

   Salen el robot, la nube de puntos del LiDAR coloreada por altura y la imagen de la cámara.

Nueve topics de sensores, con tres tipos de mensaje que no salían en tu tabla (`PointCloudPacked`,
`IMU` y `NavSat`). Echa la cuenta: cuánto costaría escribir a mano el YAML de tres robots así.

## Errores típicos

| Síntoma | Causa |
|---|---|
| El panel no lista nada | Falta pulsar *Refresh*, o la simulación está en pausa (después de importar): ▶ y *Refresh* |
| Un robot sale en el panel sin sensores | Acaba de importarse y todavía no los ha creado: espera unos segundos y *Refresh* |
| Los topics salen en ROS 2 sin `/robot_a` delante | Se importó con el *Namespace* vacío: cierra Gazebo y vuelve a importar |
| RViz no pinta nada y avisa de un frame que no existe | El *Frame prefix* no es `robot_a/`, con barra: el *Fixed Frame* de `post2_minibot.rviz` es `robot_a/base_footprint` |
| Un sensor marcado después no llega a ROS 2 | El estado dice *Restart required*: pulsa **Restart** |
| El ultrasonido da `.inf` | `robot_b` no está detrás de `robot_a`: su *Pose* x tiene que ser `-0.9` |
| Al importar el Summit se para toda la simulación | Falta marcar **robot_state_publisher**: su plugin de control espera el `robot_description` y frena Gazebo. Cierra Gazebo y vuelve a empezar |
| El Summit no tiene sensores en el panel | Espera unos segundos y *Refresh*; si siguen sin salir, el xacro no es `rbsummit.urdf.xacro` de `$WS/robots` |
| La simulación va lenta con el Summit | Sus sensores se renderizan cuando alguien se suscribe: puentea solo los dos de la lista |
