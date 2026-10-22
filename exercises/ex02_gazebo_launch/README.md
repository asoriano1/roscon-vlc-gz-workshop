# Ejercicio 2 — El launch y el primer spawn (12 min)

**Qué construyes:** el launch que abre Gazebo, publica el `robot_description` y mete el
robot en el mundo. Es el equivalente de los comandos sueltos, pero ordenado.

**Archivo que editas:** `mini_bot/launch/sim.launch.py`
**Solución:** `mini_bot/solutions/ex02/sim.launch.py`

> **Qué hace cada pieza:** Gazebo, `robot_state_publisher`, `create` y qué espera a qué, en
> [Anatomía de un robot simulado](../../docs/anatomia.md).

## Pasos

| TODO | Qué hay que hacer |
|---|---|
| 2a | Pásale el mundo a Gazebo: `gz_args = ['-r ', LaunchConfiguration('world')]` |
| 2b | Lanza `robot_state_publisher` con `robot_description` y `use_sim_time: True` |
| 2c | Haz el spawn con `ros_gz_sim create`, con `-topic robot_description`, `-name`, `-x`, `-y`, `-z` |

## Comprueba

```bash
ros2 launch mini_bot sim.launch.py
```

Y en otra terminal (lanza `./setup/shell.sh` en tu máquina, desde la raíz del repo):

```bash
ros2 topic list
ros2 topic echo /robot_description --once 2>/dev/null | head -3   # el 2>/dev/null calla un BrokenPipeError inofensivo
gz topic -l | head -20
```

## Lo importante de este ejercicio

Mira la lista de `gz topic -l`: el robot ya está en el mundo y Gazebo publica cosas. Mira
ahora `ros2 topic list`: de todo eso **no hay nada**, salvo lo que publica
`robot_state_publisher`. Esa separación es el tema de los dos ejercicios siguientes.

## Preguntas

1. ¿Quién publica `/tf` ahora mismo, Gazebo o `robot_state_publisher`?
2. Lanza el mismo launch dos veces sin cambiar `name`: ¿qué pasa?
3. ¿Qué diferencia hay entre `-topic robot_description` y `-file robot.urdf` en `create`?

## Errores típicos

| Síntoma | Causa |
|---|---|
| Gazebo abre un mundo vacío y el robot no aparece | `create` se lanzó antes de que `robot_state_publisher` publicara; vuelve a lanzar |
| `Invalid <robot> tag` | El xacro no expande: pruébalo a mano con `xacro ... > /tmp/mini_bot.urdf` |
| El robot cae atravesando el suelo | Falta la colisión de alguna rueda (TODO 1c) |
