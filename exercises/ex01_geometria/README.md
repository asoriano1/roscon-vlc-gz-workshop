# Ejercicio 1 — La geometría del mini_bot (15 min)

**Qué construyes:** un robot de tracción diferencial hecho solo con primitivas: una caja,
dos ruedas y una rueda loca. Sin mallas, a propósito: pocos polígonos y Gazebo fluido
aunque no haya GPU.

**Archivo que editas:** `mini_bot/urdf/mini_bot.urdf.xacro`
**Solución:** `mini_bot/solutions/ex01/mini_bot.urdf.xacro`

> Los nombres de links y joints ya están escritos en el esqueleto. **No los cambies**:
> el bridge, los controladores y los launch de los ejercicios siguientes dependen de ellos.

> **`${prefix}` va en los links, no en los joints.** Los frames llevan el prefijo porque son
> los links: `/tf` es un único topic para todos los robots, y dos `base_link` se pisan. La forma
> del prefijo la marca ros2_control: su `diff_drive_controller` espera namespace + barra
> (`robot_a/odom`, `robot_a/base_footprint`), así que el prefijo será `robot_a/`. Los joints no
> lo llevan: solo los usa el propio robot, que ya va en su namespace (`/robot_a/…`).

## Antes de empezar

- Arranca el contenedor (`./setup/run.sh` desde la raíz del repo) y comprueba que
  `check_setup.sh` da el código OK. Si falla algo, sigue la
  [guía del alumno](../../docs/guia_alumno.md), "Prepara el entorno".
- Abre `mini_bot/urdf/mini_bot.urdf.xacro` del repo en tu editor, **en tu máquina**.

## Pasos

Rellena los TODO en este orden. Cada uno es una o dos líneas.

| TODO | Qué hay que hacer |
|---|---|
| 1a | Eleva `base_link` sobre `base_footprint` hasta el eje de las ruedas |
| 1b | Dibuja el visual de la rueda: cilindro `wheel_r` × `wheel_l`, girado `rpy="${pi/2} 0 0"` |
| 1c | Copia el visual como colisión de la rueda |
| 1d | Coloca la rueda a media separación en Y, usando `reflect` |
| 1e | Pon el eje de giro del joint |
| 1f | Instancia las dos ruedas con la macro |
| 1g | Añade la rueda loca: esfera, joint fijo y rozamiento 0 en Gazebo |

## Comprueba

En la terminal del contenedor (prompt `root@…`):

```bash
cd $WS && colcon build --packages-select mini_bot --symlink-install && source install/setup.bash

# ¿el xacro expande sin errores?
xacro $(ros2 pkg prefix mini_bot)/share/mini_bot/urdf/mini_bot.urdf.xacro > /tmp/mini_bot.urdf
check_urdf /tmp/mini_bot.urdf

# a verlo
ros2 launch mini_bot display.launch.py
```

En RViz debe verse el robot completo. Mueve los sliders del `joint_state_publisher_gui`: las dos
ruedas deben girar.

## Preguntas

1. ¿Para qué sirve `base_footprint` si no tiene geometría?
2. ¿Por qué la rueda loca lleva rozamiento 0 y las ruedas motrices no?
3. Imagina este robot duplicado en el mismo mundo, sin tocar nada: ¿qué se rompe primero?

## Errores típicos

| Síntoma | Causa |
|---|---|
| `check_urdf` se queja de un link sin padre | Falta un joint, o el nombre del `child` no coincide |
| Las ruedas salen tumbadas | Falta el `rpy="${pi/2} 0 0"` en el cilindro |
| El robot se hunde en RViz | El TODO 1a sigue en `xyz="0 0 0"` |
