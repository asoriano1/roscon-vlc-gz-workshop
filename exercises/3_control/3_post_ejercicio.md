# Post-ejercicio 3 — El `mast_bot`, todo con la suite (15 min)

Primero te lo enseño en directo, en el proyector. Después, haz con los tres plugins de la suite lo
que hace tu `mast.launch.py`: meter el `mast_bot` en el mundo, llevar sus sensores a ROS 2,
activar sus tres controladores y moverlo. Sin escribir una línea, y esta vez con namespace.

El **ROS 2 Control Manager** es el tercer plugin. Encuentra los `controller_manager` que hay en el
mundo y enseña sus controladores: los carga, los configura y los activa con botones, el mismo
ciclo de vida que hiciste con `ros2 control` en el preámbulo 3.

## 1. El robot: Model Importer

Cierra el `mast.launch.py` (Ctrl+C) y lanza Gazebo con la suite:

```bash
cd $WS/robots && ros2 launch mini_bot suite.launch.py
```

Importa tu `mast_bot.urdf.xacro`, el del ejercicio 3 terminado, con *Namespace* `robot_a`,
*Frame prefix* `robot_a/` y **robot_state_publisher** marcado. Pulsa **Import** y después ▶.

## 2. Los sensores: Bridge Manager

Como en el post-ejercicio 2: despliega el panel, **Refresh**, marca el LiDAR (`/robot_a/scan`) y la
cámara del mástil (`/robot_a/mast_camera/image`), lee el **Bridge command** y pulsa **Run**.

## 3. Los controladores: Control Manager

1. Despliega el panel **ROS 2 Control Manager** y pulsa **Refresh**. Tiene que salir
   `/robot_a/controller_manager`: el que arrancó el plugin `gz_ros2_control` del `mast_bot` al
   crear el robot.
2. Activa el modo **Debug** y revisa los componentes hardware y sus interfaces: las dos ruedas por
   velocidad, y `mast_joint` por posición.
3. Los tres controladores salen declarados, pero sin cargar. Para `joint_state_broadcaster`,
   `diff_drive_controller` y `mast_controller`: carga, configura y activa. Observa cómo cambia el
   estado: `unconfigured` → `inactive` → `active`.

## 4. Muévelo

En otra terminal, RViz con la configuración de `robot_a`:

```bash
ros2 run rviz2 rviz2 -d $(ros2 pkg prefix mini_bot)/share/mini_bot/rviz/post3_mastbot.rviz \
  --ros-args -p use_sim_time:=true
```

En otra, el teleop con el ratón del ejercicio 3, ahora en el namespace del robot:

```bash
ros2 launch mini_bot teleop_raton.launch.py namespace:=robot_a frame:=robot_a/base_footprint
```

Y en otra, el slider del mástil, también en el namespace:

```bash
ros2 run mini_bot mast_slider.py --ros-args -r __ns:=/robot_a
```

Arrastra la flecha roja para avanzar, gira el anillo azul y mueve el slider: la imagen de la cámara
gira con el mástil.

## Comprueba

```bash
ros2 control list_controllers -c /robot_a/controller_manager   # los tres, active
ros2 control list_hardware_interfaces -c /robot_a/controller_manager
ros2 topic echo /robot_a/diff_drive_controller/odom --once --field pose.pose.position
```

Desactiva `mast_controller` desde el panel y mueve el slider: el mástil no se mueve. Actívalo otra
vez.

⏱️ Apunta el tiempo y compáralo con el del ejercicio 3.

## La comparación

En el ejercicio 3 tocaste tres ficheros para un joint nuevo y relanzaste todo. Aquí, el mismo
robot con namespace ha sido tres paneles, y activar o desactivar un controlador en caliente es un
clic.

Lo que la suite no hace es inventarse los controladores: los tres salen de tu
`mast_controllers.yaml`, y el panel gestiona los que ese YAML declara. Son dos usos distintos. La
suite, para la fase en la que todavía se está decidiendo: qué robot, dónde, qué sensores, qué
controladores. El launch, para cuando ya está decidido: es reproducible, va en el repositorio,
corre sin GUI.

## Preguntas

1. ¿De dónde salen los controladores que aparecen declarados pero no cargados?
2. ¿Por qué el teleop y el slider necesitan aquí el namespace, y en el ejercicio 3 no?
3. En un despliegue real sin GUI, ¿qué parte de lo que has hecho acaba en un launch?

## Extra: un RB-Summit conduciendo

Opcional, si te sobra tiempo. El mismo flujo con un robot real de Robotnik.

1. Importa `rbsummit.urdf.xacro` con *Namespace* `summit_a`, el *Frame prefix* **vacío**,
   **robot_state_publisher** marcado y *Pose* y `2.5`, lejos del `mast_bot`. **Import** y ▶.

   Esta vez el prefijo va vacío a propósito. Los xacros de Robotnik ponen el prefijo también en los
   joints, y el YAML de controladores del Summit nombra las ruedas sin él: con prefijo, el
   controlador de las ruedas no encuentra sus joints. Sus frames sin prefijo no chocan con los de
   `robot_a`, que sí lo llevan.
2. Espera unos segundos a que el Summit cree sus sensores. En el Bridge Manager, **Refresh**, marca
   la nube de puntos del LiDAR (`/summit_a/top_lidar/scan/points`) y la cámara de color
   (`/summit_a/front_camera_color/color/image_raw`), y pulsa **Restart**: el puente que corre
   todavía es el de antes.
3. En el Control Manager, **Refresh**: sale `/summit_a/controller_manager`. Carga, configura y
   activa sus dos controladores, `joint_state_broadcaster` y `diff_drive_controller`.
4. RViz del Summit y su teleop con el ratón:

   ```bash
   ros2 run rviz2 rviz2 -d $(ros2 pkg prefix mini_bot)/share/mini_bot/rviz/post3_rbsummit.rviz \
     --ros-args -p use_sim_time:=true
   ros2 launch mini_bot teleop_raton.launch.py namespace:=summit_a   # en otra terminal
   ```

## Errores típicos

| Síntoma | Causa |
|---|---|
| El panel no lista ningún `controller_manager` | La simulación está en pausa después de importar: ▶ y *Refresh* |
| No salen controladores declarados, o falta `mast_controller` | El ejercicio 3 está sin terminar: copia su solución (`mini_bot/solutions/ejercicio_3/`), cierra Gazebo y vuelve a importar |
| El robot no se mueve con las flechas | `diff_drive_controller` no está `active`, o el teleop se lanzó sin `namespace:=robot_a frame:=robot_a/base_footprint` |
| El mástil no se mueve con el slider | `mast_controller` no está `active`, o el slider se lanzó sin `-r __ns:=/robot_a` |
| RViz no pinta el robot y avisa de un frame que no existe | El *Frame prefix* no es `robot_a/`, o `diff_drive_controller` no está `active`: el *Fixed Frame* es `robot_a/odom`, y lo publica el controlador |
| RViz no pinta el scan ni la imagen | Falta pulsar **Run** en el Bridge Manager, o no están marcados esos dos topics |
| El Summit: `diff_drive_controller` no pasa a `active` | El *Frame prefix* no está vacío: los joints de las ruedas llevan el prefijo y el YAML no. Cierra Gazebo y vuelve a importar |
| Al importar el Summit se para toda la simulación | Falta marcar **robot_state_publisher**: su plugin de control espera el `robot_description` y frena Gazebo |
| La simulación va lenta con el Summit | Sus sensores se renderizan cuando alguien se suscribe: puentea solo los dos de la lista |
