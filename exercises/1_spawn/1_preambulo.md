# Preámbulo 1 — Un robot en Gazebo (15 min)

**Qué haces:** activa, paso a paso, la geometría del `mini_bot` y el launch que lo mete en Gazebo.
Todo está escrito y comentado: lee los comentarios, descomenta y mira qué cambia.

**Qué compruebas:** que el flujo funciona (editas en tu máquina, relanzas en el contenedor y el
cambio se ve sin recompilar) y qué sabe ROS 2 de un robot que ya está en Gazebo.

**Archivos que editas:** `mini_bot/urdf/mini_bot.urdf.xacro` (PASOS 1 a 3) y
`mini_bot/launch/sim.launch.py` (PASOS 4 a 6)
**Solución:** `mini_bot/solutions/preambulo_1/`

> Qué hace cada pieza (xacro, `robot_state_publisher`, `create`…), en detalle:
> [Anatomía de un robot simulado](../../docs/anatomia.md).

## Antes de empezar

Con el contenedor arrancado (`./setup/run.sh`) y `check_setup.sh` en OK, compila una vez. En la
terminal del contenedor (prompt `root@…:/workshop_ws#`):

```bash
colcon build --packages-select mini_bot --symlink-install && source install/setup.bash
```

Abre `mini_bot/urdf/mini_bot.urdf.xacro` del repo en tu editor, **en tu máquina**.

> Los nombres de links y joints ya están escritos. **No los cambies**: el bridge, los
> controladores y los launch de los ejercicios siguientes dependen de ellos.

## 1. La geometría, en RViz (PASOS 1 a 3)

Busca la sección `PREÁMBULO 1: GEOMETRÍA`. Para activar un paso, **borra las líneas marcadas con
`(borra esta línea)`** de ese paso. Nada más.

Lanza el robot tal como está:

```bash
ros2 launch mini_bot display.launch.py
```

En RViz sale solo la caja, a medias bajo la rejilla. La franja roja de encima marca el frontal: es
un segundo `<visual>` del mismo link, sin colisión. Ahora, un paso cada vez: actívalo, guarda,
Ctrl+C en el contenedor, vuelve a lanzar y mira qué cambia.

| Paso | Qué activa | Qué cambia en RViz |
|---|---|---|
| 1 | El origen de `base_joint` | La caja sube a la altura del eje de las ruedas y queda flotando |
| 2 | La macro de la rueda y sus dos instancias | Aparecen las ruedas, apoyadas en el suelo, y dos sliders |
| 3 | La rueda loca | Aparece la esfera bajo el morro de la caja |

Mueve los sliders: las ruedas giran. No ha hecho falta `colcon build` entre paso y paso: el
fichero que editas es el mismo que lee el contenedor.

Mira el árbol que acabas de construir, en otra terminal del contenedor (`./setup/shell.sh` desde
la raíz del repo):

```bash
ros2 run rqt_tf_tree rqt_tf_tree
```

`base_footprint` → `base_link` → las dos ruedas y la rueda loca. Cada link es un *frame* de TF.
Cierra la ventana y el `display.launch.py`.

## 2. El launch, en Gazebo (PASOS 4 a 6)

Abre `mini_bot/launch/sim.launch.py` y **léelo de arriba abajo**: cada pieza lleva un comentario
que explica qué hace. Solo se lanza lo que está descomentado en la lista del final. Para activar
un paso, **descomenta su línea** (quita el `# ` del principio).

Un paso cada vez: descomenta, guarda, y lanza (o Ctrl+C y vuelve a lanzar):

```bash
ros2 launch mini_bot sim.launch.py
```

| Paso | Qué activa | En Gazebo | En `ros2 topic list` |
|---|---|---|---|
| 4 | `gazebo` | Se abre el mundo del taller, sin robot | Nada nuevo |
| 5 | `robot_state_publisher` | Nada nuevo | `/robot_description`, `/tf`, `/tf_static`, `/clock` y `/joint_states` |
| 6 | `spawn_delayed` | A los 3 s aparece el robot y se apoya en el suelo | Nada nuevo |

En el PASO 6, `create` escribe `Entity creation successful` y termina (`process has finished
cleanly`): hace su trabajo y se va. Lee en el launch el comentario del `TimerAction`.

## 3. ¿Qué sabe ROS 2 del robot?

Con el robot en Gazebo, en la segunda terminal:

```bash
ros2 node list                                       # uno solo: /robot_state_publisher
ros2 topic info /clock -v                            # 0 publicadores
ros2 topic info /joint_states -v                     # 0 publicadores
ros2 run tf2_ros tf2_echo base_link left_wheel_link  # "frame does not exist" (Ctrl+C)
gz topic -l                                          # Gazebo sí tiene /clock y sus topics
```

- `create` ya terminó y Gazebo no es un nodo de ROS 2: solo queda `robot_state_publisher`.
- `/clock` y `/joint_states` salen en la lista porque `robot_state_publisher` está suscrito a
  ellos, esperando datos que nadie publica.
- Por eso las ruedas no tienen TF: su posición depende de `/joint_states`.
- Gazebo tiene sus propios topics, y ROS 2 no ve ninguno. Son dos mundos separados: es el tema de
  la sección 2.

## Preguntas

1. ¿Para qué sirve `base_footprint` si no tiene geometría?
2. En RViz, antes de lanzar Gazebo, ¿había algo simulado? ¿Qué se veía realmente?
3. ¿Quién publica `/tf` ahora mismo, Gazebo o `robot_state_publisher`?
4. Quita el `TimerAction` y lanza `spawn` directamente: ¿cambia algo?

## Errores típicos

| Síntoma | Causa |
|---|---|
| RViz o Gazebo no cambian después de guardar | Falta relanzar: el URDF se lee al arrancar |
| La caja sigue a medias bajo el suelo | En el PASO 1 queda la línea `<origin xyz="0 0 0" …/>` |
| `xacro` da un error de XML, o desaparece todo lo que va detrás de un paso | Solo se ha borrado una de las líneas marcadas del paso |
| El launch termina al momento y no abre nada | No hay ninguna línea descomentada en la lista del final |
| Gazebo abre el mundo y el robot no aparece | Falta el PASO 6, o aún no han pasado los 3 s |
| `rqt_tf_tree: package not found` | La imagen es antigua: sal del contenedor, `docker pull ghcr.io/asoriano1/roscon-workshop:latest` y vuelve a entrar |
