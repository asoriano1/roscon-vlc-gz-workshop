# Ejercicio 4 — El puente, a mano (15 min)

**Qué se construye:** el YAML de `ros_gz_bridge` y su nodo dentro del launch. Al final de este
ejercicio, el LiDAR y la cámara se ven en RViz.

**Archivos que se editan:** `mini_bot/config/bridge.yaml` y `mini_bot/launch/sim.launch.py`
**Soluciones:** `mini_bot/solutions/ex04/`

> **Qué hace cada pieza:** por qué hacen falta el puente y `/clock`, en
> [Anatomía de un robot simulado](../../docs/anatomia.md).

## Pasos

1. Consultar los nombres reales de los topics de Gazebo:

   ```bash
   gz topic -l | grep -E "scan|image"
   ```

2. Completar `config/bridge.yaml` con tres entradas: LiDAR, cámara y, opcionalmente,
   `camera_info`. Cada una necesita los dos nombres, los dos tipos y la dirección.

   | ROS 2 | Gazebo |
   |---|---|
   | `sensor_msgs/msg/LaserScan` | `gz.msgs.LaserScan` |
   | `sensor_msgs/msg/Image` | `gz.msgs.Image` |
   | `sensor_msgs/msg/CameraInfo` | `gz.msgs.CameraInfo` |

   > Este YAML usa nombres absolutos (`/scan`, `/camera/image`): solo vale para el robot
   > **sin namespace**. Con `namespace:=robot_a` Gazebo publica en `/robot_a/scan` y haría falta
   > otro YAML por robot. Ese es el límite que resuelve el Bridge Manager en el ejercicio 7.

3. Añadir al launch el nodo `parameter_bridge` con `config_file` apuntando a ese YAML,
   y un nodo de RViz con `rviz/mini_bot.rviz`.

## Comprobación

```bash
ros2 launch mini_bot sim.launch.py
```

En otra terminal (`./setup/shell.sh` en la máquina propia, desde la raíz del repo):

```bash
ros2 topic hz /scan
```

> `ros2 topic hz` mide en tiempo **real**, y Gazebo publica en tiempo **simulado**: lo que se ve es
> la frecuencia nominal multiplicada por el RTF (el % que marca Gazebo abajo a la derecha). Con
> RTF 0.7, el LiDAR de 5 Hz llega a ~3.5 Hz y la cámara de 10 Hz a ~7 Hz. **No es un error.**

En RViz: `Fixed Frame` = `base_footprint`, LaserScan en `/scan`, Image en `/camera/image`.

## Preguntas

1. ¿Qué pasa si el tipo de mensaje está mal? ¿Falla al arrancar o calla?
2. ¿Por qué `/clock` va puenteado y por qué importa `use_sim_time`?
3. Si mañana se añade otro sensor al URDF, ¿cuántos archivos hay que tocar?

La respuesta a la tercera es el motivo de que exista el Bridge Manager. Vuelve a salir en el ejercicio 7.

## Errores típicos

| Síntoma | Causa |
|---|---|
| `ros2 topic list` muestra `/scan` pero `hz` no da nada | El nombre del topic de Gazebo no coincide exactamente |
| RViz dice "No transform from [lidar_link]" | Falta `<gz_frame_id>` en el sensor, o el Fixed Frame está mal |
| `hz /scan` da 3–4 Hz en vez de 5 | Es el RTF: frecuencia real = nominal × RTF. No es un error |
| La imagen se ve a tirones | Es normal a 10 Hz con render por software |
