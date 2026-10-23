# Preámbulo 2 — Sensores y puente (12 min)

**Qué haces:** activa un LiDAR y una cámara en el `mini_bot`, comprueba que Gazebo los simula y
que ROS 2 no los ve, y después activa el puente que los lleva a ROS 2.

**Punto de partida:** el preámbulo 1 terminado (o su solución copiada). A partir de aquí, un
solo robot y sin namespace.

**Archivos que editas:** `mini_bot/urdf/mini_bot.urdf.xacro` (PASOS 7 y 8),
`mini_bot/config/bridge.yaml` (PASO 9) y `mini_bot/launch/sim.launch.py` (PASO 10)
**Solución:** `mini_bot/solutions/preambulo_2/`

## 1. Los sensores (PASOS 7 y 8)

Busca en el xacro la sección `PREÁMBULO 2: SENSORES` y lee su comentario. Activa los PASOS 7
(LiDAR) y 8 (cámara), igual que en el preámbulo 1: borra las líneas marcadas con
`(borra esta línea)`. Después, lanza:

```bash
ros2 launch mini_bot sim.launch.py
```

En otra terminal (`./setup/shell.sh` desde la raíz del repo):

```bash
gz topic -l | grep -E "scan|image"          # Gazebo publica /scan y /camera/image
gz topic -e -t /scan -n 1 | head -20        # y el LiDAR mide
ros2 topic list | grep -E "scan|image"      # ROS 2 no ve nada
```

Los sensores funcionan, pero solo en Gazebo. Gazebo y ROS 2 son dos sistemas de mensajería
distintos, y nadie ha pedido todavía que se hablen.

> Las resoluciones y frecuencias bajas son a propósito: un LiDAR de 1080 muestras a 30 Hz
> multiplicado por veinte portátiles sin GPU convierte el taller en un pase de diapositivas.

## 2. El puente (PASOS 9 y 10)

1. Abre `mini_bot/config/bridge.yaml` y lee el comentario. Cada entrada copia un topic: los dos
   nombres, los dos tipos y la dirección. El reloj ya está. **PASO 9:** descomenta las tres
   entradas (LiDAR, cámara y `camera_info`).
2. En `sim.launch.py`, lee el bloque del PASO 10 y descomenta sus dos líneas en la lista del
   final: `bridge` y `rviz`.
3. Ctrl+C y vuelve a lanzar `ros2 launch mini_bot sim.launch.py`. Ahora se abre también RViz.

## Comprueba

```bash
ros2 topic list | grep -E "scan|image|clock"
ros2 topic hz /scan                          # Ctrl+C para salir
ros2 topic echo /scan --once | grep frame_id
```

En RViz deben verse el robot, el LaserScan y la imagen de la cámara.

> `ros2 topic hz` mide en tiempo **real**, y Gazebo publica en tiempo **simulado**: lo que sale es
> la frecuencia nominal multiplicada por el RTF (el % que marca Gazebo abajo a la derecha). Con
> RTF 0.5, el LiDAR de 5 Hz llega a ~2.5 Hz. **No es un error.**

## Preguntas

1. ¿Por qué `/clock` va puenteado y por qué importa `use_sim_time`?
2. Pon a propósito un tipo de mensaje equivocado en el `bridge.yaml`: ¿falla al arrancar o se
   calla?
3. Si mañana el robot lleva un sensor más, ¿cuántos ficheros hay que tocar?

## Errores típicos

| Síntoma | Causa |
|---|---|
| El sensor no aparece en `gz topic -l` | Solo se ha borrado una de las líneas marcadas del paso, o falta relanzar |
| `ros2 topic list` muestra `/scan` pero `hz` no da nada | El nombre del topic de Gazebo en el YAML no coincide exactamente |
| No se abre RViz y ROS 2 sigue sin ver los sensores | Falta el PASO 10: `bridge` y `rviz` en la lista del launch |
| RViz dice "No transform from [lidar_link]" | El *Fixed Frame* no es `base_footprint` |
| `hz /scan` da 2–4 Hz en vez de 5 | Es el RTF: frecuencia real = nominal × RTF |
