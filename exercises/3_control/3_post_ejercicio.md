# Post-ejercicio 3 — Un RB-Summit conduciendo, todo con la suite (15 min)

Primero, la demo del ponente. Después, haz con los tres plugins de la suite lo que hace un launch
completo, con un robot que no has escrito tú: meter un **RB-Summit** en el mundo, llevar sus
sensores a ROS 2, activar sus controladores y conducirlo. Sin escribir una línea.

El **ROS 2 Control Manager** es el tercer plugin. Encuentra los `controller_manager` que hay en el
mundo y enseña sus controladores: los carga, los configura y los activa con botones, el mismo
ciclo de vida que hiciste con `ros2 control` en el preámbulo 3.

## 1. El robot: Model Importer

Cierra el `mast.launch.py` (Ctrl+C) y lanza Gazebo con la suite:

```bash
cd $WS/robots && ros2 launch gz_model_importer gazebo_importer.launch.py \
  world:=$(ros2 pkg prefix mini_bot)/share/mini_bot/worlds/workshop.sdf
```

Importa `rbsummit.urdf.xacro` con *Namespace* `summit_a` y el *Frame prefix* **vacío**, con
**robot_state_publisher** marcado. Pulsa **Import** y después ▶.

Esta vez el prefijo va vacío a propósito. Los xacros de Robotnik ponen el prefijo también en los
joints, y el YAML de controladores del Summit nombra las ruedas sin él: con prefijo, el
controlador de las ruedas no encuentra sus joints. Como el Summit es el único robot del mundo, sus
frames no chocan con los de nadie.

## 2. Los sensores: Bridge Manager

Como en el post-ejercicio 2: **Refresh**, marca la nube de puntos del LiDAR
(`/summit_a/top_lidar/scan/points`) y la cámara de color
(`/summit_a/front_camera_color/color/image_raw`), lee el **Bridge command** y pulsa **Run**.

## 3. Los controladores: Control Manager

1. Abre el panel **ROS 2 Control Manager** y pulsa **Refresh**. Tiene que salir
   `/summit_a/controller_manager`: el que arrancó el plugin `gz_ros2_control` del Summit al crear
   el robot.
2. Activa el modo **Debug** y revisa los componentes hardware y sus interfaces: las cuatro ruedas,
   por velocidad.
3. Los dos controladores salen declarados, pero sin cargar. Para `joint_state_broadcaster` y
   `diff_drive_controller`: carga, configura y activa. Observa cómo cambia el estado:
   `unconfigured` → `inactive` → `active`.

## 4. Condúcelo

En otra terminal, RViz con la configuración del Summit:

```bash
ros2 run rviz2 rviz2 -d $(ros2 pkg prefix mini_bot)/share/mini_bot/rviz/post3_rbsummit.rviz \
  --ros-args -p use_sim_time:=true
```

Y en otra, el teleop con el ratón, el mismo del ejercicio 3, ahora en el namespace del Summit:

```bash
ros2 launch mini_bot teleop_raton.launch.py namespace:=summit_a
```

En RViz salen las flechas alrededor del Summit: arrastra la roja para avanzar y gira el anillo
azul. Si prefieres el teclado:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -p stamped:=true -r cmd_vel:=/summit_a/diff_drive_controller/cmd_vel
```

## Comprueba

```bash
ros2 control list_controllers -c /summit_a/controller_manager   # los dos, active
ros2 control list_hardware_interfaces -c /summit_a/controller_manager
ros2 topic echo /summit_a/diff_drive_controller/odom --once --field pose.pose.position
```

El Summit se mueve en Gazebo, y en RViz la nube de puntos y la imagen cambian. Desactiva
`diff_drive_controller` desde el panel e intenta conducir: no se mueve. Actívalo otra vez.

⏱️ Apunta el tiempo y compáralo con el del ejercicio 3.

## La comparación

En el ejercicio 3 tocaste tres ficheros para un joint de un robot que conocías, y relanzaste
todo. Aquí, un robot que no has escrito ha sido tres paneles, y activar o desactivar un
controlador en caliente es un clic.

Lo que la suite no hace es inventarse los controladores: el Summit trae su YAML, y el panel
gestiona los que ese YAML declara. Son dos usos distintos. La suite, para la fase en la que todavía
se está decidiendo: qué robot, dónde, qué sensores, qué controladores. El launch, para cuando ya
está decidido: es reproducible, va en el repositorio, corre sin GUI.

## Preguntas

1. ¿De dónde salen los controladores que aparecen declarados pero no cargados?
2. ¿Por qué aquí el *Frame prefix* va vacío, y en el post-ejercicio 2 era `summit_a/`?
3. En un despliegue real sin GUI, ¿qué parte de lo que has hecho acaba en un launch?

## Errores típicos

| Síntoma | Causa |
|---|---|
| El panel no lista ningún `controller_manager` | La simulación está en pausa después de importar: ▶ y *Refresh* |
| `diff_drive_controller` no pasa a `active` | El *Frame prefix* no está vacío: los joints de las ruedas llevan el prefijo y el YAML no. Cierra Gazebo y vuelve a importar |
| El robot no se mueve con el teleop | `diff_drive_controller` no está `active`; con el teclado, falta `-p stamped:=true` o el remap con `/summit_a` |
| En RViz no salen las flechas | Falta el `teleop_raton.launch.py`, o se lanzó sin `namespace:=summit_a` |
| `teleop_raton.launch.py` no se encuentra | La imagen es anterior a él: `colcon build --packages-select mini_bot --symlink-install && source install/setup.bash` |
| RViz no pinta la nube ni la imagen | Falta pulsar **Run** en el Bridge Manager, o no están marcados esos dos topics |
| La simulación va lenta | Los sensores del Summit se renderizan cuando alguien se suscribe: puentea solo los dos de la lista |
