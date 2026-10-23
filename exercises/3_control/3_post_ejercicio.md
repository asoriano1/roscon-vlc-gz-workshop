# Post-ejercicio 3 — Todo con la suite (15 min)

Primero, la demo del ponente. Después, haz con los tres plugins de la suite todo lo que hace
`mast.launch.py`: meter el `mast_bot` en el mundo, llevar sus sensores a ROS 2 y activar sus tres
controladores. Sin escribir una línea.

El **ROS 2 Control Manager** es el tercer plugin. Encuentra los `controller_manager` que hay en el
mundo y enseña sus controladores: los carga, los configura y los activa con botones, el mismo
ciclo de vida que hiciste con `ros2 control` en el preámbulo 3.

**Punto de partida:** el ejercicio 3 terminado (o su solución copiada): el `mast_bot` con el
control del mástil.

## 1. El robot: Model Importer

Cierra el `mast.launch.py` (Ctrl+C) y lanza Gazebo con la suite:

```bash
cd $WS/robots && ros2 launch gz_model_importer gazebo_importer.launch.py \
  world:=$(ros2 pkg prefix mini_bot)/share/mini_bot/worlds/workshop.sdf
```

Importa `mast_bot.urdf.xacro` como en el post-ejercicio 1, con *Namespace* y *Frame prefix*
**vacíos** y **robot_state_publisher** marcado. Pulsa **Import** y después ▶.

## 2. Los sensores: Bridge Manager

Como en el post-ejercicio 2: **Refresh**, marca el LiDAR y la cámara del mástil, lee el
**Bridge command** y pulsa **Run**. Abre RViz con la configuración del `mast_bot`:

```bash
ros2 run rviz2 rviz2 -d $(ros2 pkg prefix mini_bot)/share/mini_bot/rviz/mast_bot.rviz \
  --ros-args -p use_sim_time:=true
```

## 3. Los controladores: Control Manager

1. Abre el panel **ROS 2 Control Manager** y pulsa **Refresh**. Tiene que salir un
   `controller_manager`: el que arrancó el plugin `gz_ros2_control` al crear el robot.
2. Activa el modo **Debug** y revisa los componentes hardware y sus interfaces: las dos ruedas por
   velocidad y `mast_joint` por posición.
3. Los tres controladores de `mast_controllers.yaml` salen declarados, pero sin cargar. Para
   `joint_state_broadcaster`, `diff_drive_controller` y `mast_controller`: carga, configura y
   activa. Observa cómo cambia el estado: `unconfigured` → `inactive` → `active`.

## Comprueba

Lo mismo que en el ejercicio 3:

```bash
ros2 control list_controllers
ros2 topic pub --once /mast_controller/commands std_msgs/msg/Float64MultiArray "{data: [1.0]}"
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -p stamped:=true -r cmd_vel:=/diff_drive_controller/cmd_vel
```

El mástil gira, la imagen cambia en RViz y el robot conduce. Desactiva `mast_controller` desde
el panel y vuelve a mandar el `pub`: no se mueve.

⏱️ Apunta el tiempo y compáralo con el del ejercicio 3.

## La comparación

En el ejercicio 3 tocaste tres ficheros y relanzaste todo. Aquí, el robot, el puente y los
controladores han sido tres paneles, y activar o desactivar un controlador en caliente es un
clic.

Son dos usos distintos. La suite, para la fase en la que todavía se está decidiendo: qué robot,
dónde, qué sensores, qué controladores. El launch, para cuando ya está decidido: es
reproducible, va en el repositorio, corre sin GUI.

## Preguntas

1. ¿De dónde salen los controladores que aparecen declarados pero no cargados?
2. En un despliegue real sin GUI, ¿qué parte de lo que has hecho acaba en un launch?
3. Importa un segundo `mast_bot` con namespace `robot_b` y prefijo `robot_b/`. ¿Cuántos
   `controller_manager` ve el panel?

## Errores típicos

| Síntoma | Causa |
|---|---|
| El panel no lista ningún `controller_manager` | La simulación está en pausa después de importar: ▶ y *Refresh* |
| `mast_controller` no sale en el panel | El `mast_controllers.yaml` no tiene el controlador: falta el ejercicio 3 |
| El controlador está `active` pero el teleop no mueve el robot | Falta `-p stamped:=true`, o la ventana del teleop no tiene el foco |
| En RViz la cabeza del mástil no tiene TF | `joint_state_broadcaster` no está activo |
