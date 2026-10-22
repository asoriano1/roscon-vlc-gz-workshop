# Ejercicio 2 — El launch y el primer spawn (12 min)

**Qué construyes:** el launch que abre Gazebo, publica el `robot_description` y mete el
robot en el mundo. Es el equivalente de los comandos sueltos, pero ordenado.

**Qué compruebas:** qué hace cada pieza del launch y, sobre todo, qué hay en ROS 2 cuando el robot
ya está en Gazebo. Spoiler: casi nada.

**Archivo que editas:** `mini_bot/launch/sim.launch.py`
**Solución:** `mini_bot/solutions/ex02/sim.launch.py`

> **Qué hace cada pieza:** Gazebo, `robot_state_publisher`, `create` y qué espera a qué, en
> [Anatomía de un robot simulado](../../docs/anatomia.md).

## Antes de empezar

- El xacro tiene que tener los tres pasos del ejercicio 1 activados. Si no, copia la solución
  (en tu máquina, desde la raíz del repo): `cp mini_bot/solutions/ex01/mini_bot.urdf.xacro mini_bot/urdf/`
- Cierra el `display.launch.py` del ejercicio 1 (Ctrl+C).
- Abre `mini_bot/launch/sim.launch.py` en tu editor y **léelo de arriba abajo**. Cada pieza lleva
  un comentario que explica qué hace: la descripción del robot, Gazebo (PASO 1),
  `robot_state_publisher` (PASO 2) y el spawn con `create` (PASO 3).

## 1. Activa las piezas, una a una

Las tres piezas ya están escritas, pero no se lanzan: solo se ejecuta lo que está en la lista del
final del fichero, y ahí están comentadas. Para activar un paso, **descomenta su línea** (quita el
`# ` del principio) y guarda.

Un paso cada vez:

1. En tu editor, descomenta la línea del paso y guarda.
2. En el contenedor, lanza (o, si ya estaba en marcha, Ctrl+C y vuelve a lanzar):

   ```bash
   ros2 launch mini_bot sim.launch.py
   ```

3. Mira qué ha cambiado en Gazebo y, en otra terminal (`./setup/shell.sh` desde la raíz del repo),
   en `ros2 topic list`.

| Paso | Qué activa | En Gazebo | En `ros2 topic list` |
|---|---|---|---|
| 1 | `gazebo` | Se abre el mundo del taller, sin robot | Nada nuevo: solo `/parameter_events` y `/rosout` |
| 2 | `robot_state_publisher` | Nada nuevo | `/robot_description`, `/tf`, `/tf_static`, `/clock` y `/joint_states` |
| 3 | `spawn_delayed` | A los 3 s aparece el robot, cae unos centímetros y se apoya en el suelo | Nada nuevo |

En el PASO 3, la salida del launch muestra `Entity creation successful` y, después,
`[create-3]: process has finished cleanly`. `create` hace su trabajo y termina: no es un error.

El PASO 3 lanza `create` con un `TimerAction` de 3 s. Lee el comentario que lo acompaña en el
launch: explica por qué está ahí.

## 2. Investiga qué hay en ROS 2

El robot ya está en Gazebo. Con el launch en marcha, mira qué sabe ROS 2 de él. En la segunda
terminal, uno a uno:

**¿Qué nodos hay?**

```bash
ros2 node list
```

Sale uno solo: `/robot_state_publisher`. `create` ya terminó, y Gazebo no es un nodo de ROS 2.

**¿Quién publica cada topic?**

```bash
ros2 topic info /tf_static -v
ros2 topic info /clock -v
ros2 topic info /joint_states -v
```

`/tf_static` tiene un publicador, `robot_state_publisher`. `/clock` y `/joint_states` tienen
**0 publicadores**: salen en la lista solo porque `robot_state_publisher` está suscrito a ellos,
esperando datos que no llegan.

**¿Qué TF hay?**

```bash
ros2 run tf2_ros tf2_echo base_footprint base_link
```

Sale la traslación `[0.000, 0.000, 0.090]`: la de `base_joint`, que es fijo. Sal con Ctrl+C y
prueba con una rueda:

```bash
ros2 run tf2_ros tf2_echo base_link left_wheel_link
```

Se queda en `frame does not exist`. Los joints de las ruedas se mueven, y su TF depende de
`/joint_states`, que nadie publica. Sal con Ctrl+C.

**¿Y en Gazebo?**

```bash
gz topic -l
gz model --list
```

Gazebo tiene sus propios topics, `/clock` incluido, y el modelo `mini_bot` en la lista. Compara
con `ros2 topic list`: ninguno de esos topics existe en ROS 2. Los topics de Gazebo y los de ROS 2
son mundos separados, y ese es el tema de los dos ejercicios siguientes.

## Preguntas

1. ¿Quién publica `/tf` ahora mismo, Gazebo o `robot_state_publisher`? ¿Por qué no hay TF de las
   ruedas?
2. Gazebo tiene un `/clock` y ROS 2 tiene otro sin publicador. ¿Qué les falta para ser el mismo?
3. Quita el `TimerAction` y lanza `spawn` directamente: ¿cambia algo? Vuelve a leer el comentario
   del launch.
4. ¿Qué diferencia hay entre `-topic robot_description` y `-file robot.urdf` en `create`?

## Errores típicos

| Síntoma | Causa |
|---|---|
| El launch termina al momento y no abre nada | No hay ninguna línea descomentada en la lista del final |
| Gazebo abre el mundo y el robot no aparece | Falta el PASO 3, o aún no han pasado los 3 s |
| `Invalid <robot> tag` | El xacro no expande: pruébalo a mano con `xacro ... > /tmp/mini_bot.urdf` |
| El robot sale sin ruedas o a medias bajo el suelo | El ejercicio 1 está incompleto: copia su solución |
