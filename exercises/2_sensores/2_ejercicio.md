# Ejercicio 2 — Dos sensores más (20 min)

**El problema:** el `mini_bot` necesita ver hacia atrás y medir distancias cortas detrás. Añádele
una **cámara trasera** y un **ultrasonido** trasero, llévalos a ROS 2 y míralos en RViz.

El código de los sensores te lo damos: cópialo y pégalo. **El trabajo está en el puente**:
averigua qué publica Gazebo y escribe tú las entradas del `bridge.yaml`.

**Punto de partida:** el preámbulo 2 terminado (o su solución copiada).

**Archivos que editas:** `mini_bot/urdf/mini_bot.urdf.xacro` y `mini_bot/config/bridge.yaml`
**Solución:** `mini_bot/solutions/ejercicio_2/`

## 1. Pega los sensores

En el xacro, busca la sección `EJERCICIO 2: SENSORES NUEVOS` y pega este bloque debajo del
comentario `Pega aquí los sensores del ejercicio 2`:

```xml
  <!-- Cámara trasera: 160 × 120 a 5 Hz, mirando hacia atrás (giro de 180° en el joint). -->
  <link name="${prefix}rear_camera_link">
    <visual>
      <geometry><box size="0.02 0.06 0.03"/></geometry>
      <material name="accent_red"/>
    </visual>
    <xacro:box_inertia m="0.05" x="0.02" y="0.06" z="0.03"/>
  </link>

  <joint name="rear_camera_joint" type="fixed">
    <parent link="${prefix}base_link"/>
    <child  link="${prefix}rear_camera_link"/>
    <origin xyz="${-base_x/2 + 0.01} 0 ${base_z/2 - 0.01}" rpy="0 0 ${pi}"/>
  </joint>

  <gazebo reference="${prefix}rear_camera_link">
    <sensor name="rear_camera" type="camera">
      <topic>${tns}/rear_camera/image</topic>
      <gz_frame_id>${prefix}rear_camera_link</gz_frame_id>
      <update_rate>5</update_rate>
      <always_on>true</always_on>
      <camera>
        <horizontal_fov>1.047</horizontal_fov>
        <image>
          <width>160</width>
          <height>120</height>
          <format>R8G8B8</format>
        </image>
        <clip>
          <near>0.05</near>
          <far>10.0</far>
        </clip>
      </camera>
    </sensor>
  </gazebo>

  <!-- "Ultrasonido": Gazebo no tiene sensor de ultrasonidos, así que se imita con un lidar de
       5 rayos en un cono de 15° y 3 m de alcance, a 10 Hz. Va detrás, mirando hacia atrás (giro
       de 180° en el joint): delante ya mira el LiDAR, y así sus medidas no se mezclan. -->
  <link name="${prefix}ultrasound_link">
    <visual>
      <origin xyz="0 0 0" rpy="0 ${pi/2} 0"/>
      <geometry><cylinder radius="0.012" length="0.01"/></geometry>
      <material name="dark"/>
    </visual>
    <xacro:cylinder_inertia m="0.01" r="0.012" l="0.01"/>
  </link>

  <joint name="ultrasound_joint" type="fixed">
    <parent link="${prefix}base_link"/>
    <child  link="${prefix}ultrasound_link"/>
    <origin xyz="${-base_x/2 - 0.005} 0 0" rpy="0 0 ${pi}"/>
  </joint>

  <gazebo reference="${prefix}ultrasound_link">
    <sensor name="ultrasound" type="gpu_lidar">
      <topic>${tns}/ultrasound</topic>
      <gz_frame_id>${prefix}ultrasound_link</gz_frame_id>
      <update_rate>10</update_rate>
      <always_on>true</always_on>
      <lidar>
        <scan>
          <horizontal>
            <samples>5</samples>
            <resolution>1</resolution>
            <min_angle>-0.13</min_angle>
            <max_angle>0.13</max_angle>
          </horizontal>
        </scan>
        <range>
          <min>0.02</min>
          <max>3.0</max>
          <resolution>0.01</resolution>
        </range>
      </lidar>
    </sensor>
  </gazebo>
```

Lee los comentarios del bloque: Gazebo no tiene sensor de ultrasonidos, así que se imita con un
lidar de cinco rayos.

## 2. Llévalos a ROS 2

Lanza el robot con la configuración de RViz del ejercicio y averigua qué publican los sensores
nuevos en Gazebo:

```bash
ros2 launch mini_bot sim.launch.py rviz_config:=ejercicio_2.rviz
```

En otra terminal:

```bash
gz topic -l
gz topic -i -t <topic>        # el tipo de mensaje de un topic de Gazebo
```

Cada sensor nuevo publica más de un topic: la cámara, también su `camera_info`, y el
ultrasonido, también `/ultrasound/points`, la misma medida como nube de puntos. Basta con la
imagen y el scan.

Con eso, **añade al final de `config/bridge.yaml` una entrada por cada sensor nuevo**, siguiendo
el formato de las que ya hay. Para el tipo de ROS 2, esta tabla:

| Gazebo | ROS 2 |
|---|---|
| `gz.msgs.Image` | `sensor_msgs/msg/Image` |
| `gz.msgs.LaserScan` | `sensor_msgs/msg/LaserScan` |
| `gz.msgs.CameraInfo` | `sensor_msgs/msg/CameraInfo` |

Guarda, Ctrl+C y vuelve a lanzar, con el mismo `rviz_config:=ejercicio_2.rviz`.

## 3. Míralos en RViz

`ejercicio_2.rviz` es la configuración de siempre con dos displays más: **RearCamera**, la imagen
de `/rear_camera/image`, y **Ultrasound**, el scan de `/ultrasound` en puntos amarillos. Mientras
no llegue nada por su topic, se quedan vacíos o con un aviso en el panel *Displays*. Cuando tu
puente funcione, se llenan solos.

## Comprueba

```bash
ros2 topic list                           # aparecen los dos topics nuevos
ros2 topic hz <topic de la cámara trasera>   # ~5 Hz × RTF
ros2 topic echo <topic del ultrasonido> --once | grep -A5 ranges
```

Sin nada detrás, el ultrasonido da `.inf` en los cinco rayos: no hay eco. Para verlo medir,
lanza el robot de espaldas a una caja y vuelve a mirar:

```bash
ros2 launch mini_bot sim.launch.py rviz_config:=ejercicio_2.rviz x:=3.0 y:=1.0   # ~0.55 m
```

Cuando veas en RViz la imagen trasera y los puntos del ultrasonido sobre la caja, **pon el
post-it verde**.

## Preguntas

1. ¿Cuántos ficheros has tocado para añadir dos sensores? ¿Y si fueran tres robots, cada uno con
   su namespace?
2. ¿Por qué el ultrasonido va detrás y no delante? Pista: el comentario del bloque, y en RViz
   dónde caerían sus puntos.
3. ¿Qué pasa si te equivocas de dirección (`ROS_TO_GZ`) en una entrada?

## Errores típicos

| Síntoma | Causa |
|---|---|
| `xacro` da un error al lanzar | El bloque se ha pegado fuera de `<robot>`, o a medias |
| El topic sale en `ros2 topic list` pero no llega nada | El `gz_topic_name` no coincide exactamente con `gz topic -l` |
| El topic nuevo no sale en ROS 2 | Falta relanzar, o la entrada del YAML está mal sangrada |
| RViz no tiene los displays RearCamera y Ultrasound | Falta `rviz_config:=ejercicio_2.rviz` al lanzar |
| RViz se abre vacío, sin el robot ni los displays | La imagen es anterior a ese fichero: `colcon build --packages-select mini_bot --symlink-install && source install/setup.bash` |
| RViz no pinta el ultrasonido | El topic del puente no es `/ultrasound`; o los rayos dan `.inf` porque no hay nada detrás |
| RearCamera sale vacío | El topic del puente no es `/rear_camera/image` |
