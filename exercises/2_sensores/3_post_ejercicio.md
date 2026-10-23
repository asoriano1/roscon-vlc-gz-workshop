# Post-ejercicio 2 — Lo mismo, con el Bridge Manager (15 min)

Primero, la demo del ponente. Después, repite el ejercicio 2 con el **Bridge Manager**: los cuatro
sensores del `mini_bot` en ROS 2 sin tocar el `bridge.yaml`.

El Bridge Manager es un plugin de la GUI de Gazebo. Pregunta a Gazebo qué topics publica cada
modelo, propone el tipo de ROS 2 equivalente y lanza el mismo `ros_gz_bridge` que lanzas tú desde
`sim.launch.py`. Antes de lanzarlo, enseña el comando.

## Lanza Gazebo con la suite e importa el robot

Cierra el `sim.launch.py` (Ctrl+C) y lanza Gazebo con los plugins de la suite:

```bash
cd $WS/robots && ros2 launch gz_model_importer gazebo_importer.launch.py \
  world:=$(ros2 pkg prefix mini_bot)/share/mini_bot/worlds/workshop.sdf
```

Importa tu `mini_bot.urdf.xacro`, como en el post-ejercicio 1, pero esta vez **con *Namespace* y
*Frame prefix* vacíos**: un solo robot, como en `sim.launch.py`. Deja marcado
**robot_state_publisher**, pulsa **Import** y después ▶.

Este launch ya puentea `/clock` por su cuenta.

## Pasos

1. Abre el panel **ROS 2 Bridge Manager** y pulsa **Refresh**.
2. Los topics aparecen agrupados por modelo. Marca el LiDAR, las dos cámaras y el ultrasonido.
3. Despliega **Bridge command** y **léelo antes de lanzarlo**.
4. Pulsa **Run**.
5. Abre RViz en otra terminal, con la configuración del taller:

   ```bash
   ros2 run rviz2 rviz2 -d $(ros2 pkg prefix mini_bot)/share/mini_bot/rviz/mini_bot.rviz \
     --ros-args -p use_sim_time:=true
   ```

   Añade la cámara trasera y el ultrasonido como en el ejercicio 2.

⏱️ Apunta el tiempo y compáralo con el del ejercicio 2.

## Comprueba

Los mismos comandos que en el ejercicio 2:

```bash
ros2 topic list
ros2 topic hz /rear_camera/image
ros2 topic echo /ultrasound --once | grep -A5 ranges
```

## La comparación

Abre a la vez tu `config/bridge.yaml` y el comando que ha generado el panel. Son la misma
información. La diferencia es que uno lo escribiste a mano mirando `gz topic -l`, y el otro ha
salido de recorrer el mundo.

Ahora echa la cuenta: cuánto costaría escribir a mano el YAML de tres robots con cuatro sensores
cada uno, con sus namespaces.

## Preguntas

1. ¿Qué topics de Gazebo no aparecen como puenteables, y por qué?
2. Al marcar un sensor más, ¿reinicia el puente o lanza otro proceso? Míralo con
   `ros2 node list` antes y después.
3. Importa un segundo robot con namespace `robot_b`. ¿Sus topics salen en ROS 2 con el namespace?
   Compruébalo con `ros2 topic list`.

> Si en la tercera los topics salen sin el namespace del robot, dilo en voz alta: es información
> útil para la suite.

## Errores típicos

| Síntoma | Causa |
|---|---|
| El panel no lista nada | Falta pulsar *Refresh*, o la simulación está en pausa (después de importar): ▶ y *Refresh* |
| No aparece un sensor | El sensor no publica todavía: comprueba que la simulación corre y mira `gz topic -l` |
| Los topics salen en ROS 2 pero RViz no pinta nada | El *Fixed Frame* tiene que ser `base_footprint` |
