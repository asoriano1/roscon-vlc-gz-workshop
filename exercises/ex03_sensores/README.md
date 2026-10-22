# Ejercicio 3 — Sensores en el URDF (12 min)

**Qué se construye:** un LiDAR y una cámara, los dos de baja resolución para que la
simulación siga siendo fluida.

**Archivo que se edita:** `mini_bot/urdf/mini_bot.urdf.xacro`, sección del ejercicio 3
**Solución:** `mini_bot/solutions/ex03/mini_bot.urdf.xacro`

## Pasos

1. **`lidar_link`** y su joint fijo sobre la base: cilindro de radio 0.035 y largo 0.04.
2. **`camera_link`** y su joint fijo en el morro: caja de 0.02 × 0.06 × 0.03.
3. La etiqueta `<gazebo reference="${prefix}lidar_link">` con un `<sensor type="gpu_lidar">`:

   - `<topic>${tns}/scan</topic>`
   - `<update_rate>5</update_rate>` y **180 muestras** entre −π/2 y π/2
   - rango de 0.12 a 8 m
   - `<gz_frame_id>${prefix}lidar_link</gz_frame_id>`

4. Lo mismo para la cámara, con `type="camera"`, 320 × 240 y 10 Hz, en `${tns}/camera/image`.

> Los números bajos son deliberados. Un LiDAR de 1080 muestras a 30 Hz multiplicado por
> cuatro robots es lo que convierte este taller en un pase de diapositivas.

## Comprobación

```bash
cd $WS && colcon build --packages-select mini_bot --symlink-install && source install/setup.bash
ros2 launch mini_bot sim.launch.py
```

En otra terminal (`./setup/shell.sh` en la máquina propia, desde la raíz del repo):

```bash
gz topic -l | grep -E "scan|image"
gz topic -e -t /scan -n 1 | head -20
ros2 topic list | grep -E "scan|image"      # ← sigue vacío
```

## La pregunta del ejercicio

Los sensores publican, como muestra `gz topic`. Pero `ros2 topic list` no muestra nada.
**¿Por qué?** Para pensarlo antes del ejercicio 4: Gazebo y ROS 2 son dos sistemas de
mensajería distintos, y nadie ha pedido todavía que se hablen.

## Errores típicos

| Síntoma | Causa |
|---|---|
| El sensor no aparece en `gz topic -l` | Falta el sistema `Sensors` en el mundo, o el `<gazebo reference>` apunta a un link que no existe |
| El LiDAR se ve pero el TF del scan está mal | Falta `<gz_frame_id>` |
| La simulación se arrastra | Se ha subido la resolución o la frecuencia; volver a 180 muestras y 5 Hz |
