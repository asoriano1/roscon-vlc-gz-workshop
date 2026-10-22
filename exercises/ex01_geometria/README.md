# Ejercicio 1 — La geometría del mini_bot (15 min)

**Qué construyes:** un robot de tracción diferencial hecho solo con primitivas: una caja,
dos ruedas y una rueda loca. Sin mallas, a propósito: pocos polígonos y Gazebo fluido
aunque no haya GPU.

**Qué compruebas:** que el flujo de trabajo funciona. Edita en tu máquina, relanza en el
contenedor y mira cómo cambia el robot en RViz, sin recompilar. Después, mira qué hay debajo: el
árbol de TF y los nodos que dibujan el robot.

**Archivo que editas:** `mini_bot/urdf/mini_bot.urdf.xacro`
**Solución:** `mini_bot/solutions/ex01/mini_bot.urdf.xacro`

> Los nombres de links y joints ya están escritos en el esqueleto. **No los cambies**:
> el bridge, los controladores y los launch de los ejercicios siguientes dependen de ellos.

## Antes de empezar

- Arranca el contenedor (`./setup/run.sh` desde la raíz del repo) y comprueba que
  `check_setup.sh` da el código OK. Si falla algo, sigue la
  [guía del alumno](../../docs/guia_alumno.md), "Prepara el entorno".
- Abre `mini_bot/urdf/mini_bot.urdf.xacro` del repo en tu editor, **en tu máquina**, y busca la
  sección `EJERCICIO 1: GEOMETRÍA`.

## 1. Activa la geometría, paso a paso

La geometría ya está escrita, pero comentada, en tres pasos: `PASO 1`, `PASO 2` y `PASO 3`. Para
activar un paso, **borra las líneas marcadas con `(borra esta línea)`** de ese paso. Nada más.

Primero, lanza el robot tal como está. En la terminal del contenedor (prompt `root@…`):

```bash
cd $WS && colcon build --packages-select mini_bot --symlink-install && source install/setup.bash
ros2 launch mini_bot display.launch.py
```

En RViz sale solo la caja, a medias bajo la rejilla del suelo. Ahora, un paso cada vez:

1. En tu editor, activa el **PASO 1** y guarda.
2. En el contenedor, pulsa Ctrl+C y vuelve a lanzar `ros2 launch mini_bot display.launch.py`.
3. Mira qué ha cambiado en RViz.

| Paso | Qué activa | Qué cambia en RViz |
|---|---|---|
| 1 | El origen de `base_joint` | La caja sube a la altura del eje de las ruedas y queda flotando |
| 2 | La macro de la rueda y sus dos instancias | Aparecen las ruedas, apoyadas en el suelo, y dos sliders en la ventana del `joint_state_publisher_gui` |
| 3 | La rueda loca | Aparece la esfera bajo el morro de la caja |

Al terminar, mueve los sliders: las dos ruedas deben girar.

Fíjate: no ha hecho falta otro `colcon build`. El fichero que editas en tu máquina es el
mismo que lee el contenedor, y `--symlink-install` hace que ROS 2 lo use directamente.

Comprueba también que el xacro es un URDF válido:

```bash
xacro $(ros2 pkg prefix mini_bot)/share/mini_bot/urdf/mini_bot.urdf.xacro > /tmp/mini_bot.urdf
check_urdf /tmp/mini_bot.urdf
```

`check_urdf` dibuja el árbol: `base_footprint` → `base_link` → las ruedas y la rueda loca.

## 2. Mira el árbol de TF

Con `display.launch.py` en marcha, abre otra terminal del contenedor (`./setup/shell.sh` desde la
raíz del repo) y lanza:

```bash
ros2 run rqt_tf_tree rqt_tf_tree
```

Es el mismo árbol que dibujó `check_urdf`, pero ahora en vivo: cada link es un *frame*, y cada
flecha, la transformación que lo une a su padre. Cierra la ventana al terminar.

Para ver una de esas transformaciones cambiar, sigue en la segunda terminal:

```bash
ros2 run tf2_ros tf2_echo base_link left_wheel_link
```

Si la primera línea dice `Waiting for transform … frame does not exist`, espera un segundo: es el
tiempo que tarda en recibir TF. Mueve el slider de la rueda izquierda: cambia la rotación y la
traslación se queda quieta. Sal con
Ctrl+C.

## 3. Mira qué hay en marcha

Abre `mini_bot/launch/display.launch.py` en tu editor. Lanza tres nodos:

| Ejecutable | Nombre del nodo | Qué hace |
|---|---|---|
| `robot_state_publisher` | `/robot_state_publisher` | Lee el URDF (el parámetro `robot_description`), lo publica en `/robot_description` y publica las transformaciones de TF |
| `joint_state_publisher_gui` | `/joint_state_publisher` | Lee `/robot_description` para saber qué joints se mueven, y publica en `/joint_states` el ángulo que marca cada slider |
| `rviz2` | `/rviz` | Dibuja el robot a partir de `/robot_description` y de TF |

Compruébalo en la segunda terminal:

```bash
ros2 node list
ros2 topic list
ros2 topic info /joint_states -v
rqt_graph
```

Además de los tres, `ros2 node list` muestra un `transform_listener_impl_…`: es el oyente de TF
que crea RViz. Y `/scan` y `/camera/image` salen en `ros2 topic list` porque RViz ya está
suscrito a ellos, aunque nadie los publique todavía (llegan en el ejercicio 4).

En `rqt_graph` se ve quién publica qué y quién lo escucha. Busca las respuestas:

- ¿Quién publica `/joint_states`, y quién lo lee?
- ¿Quién publica `/tf` y `/tf_static`?
- `base_joint` y `caster_joint` salen en `/tf_static`, y las ruedas, en `/tf`. ¿Por qué?

La descripción completa de cada pieza está en [Anatomía de un robot simulado](../../docs/anatomia.md).

## Preguntas

1. ¿Para qué sirve `base_footprint` si no tiene geometría?
2. ¿Por qué la rueda loca lleva rozamiento 0 y las ruedas motrices no?
3. Imagina este robot duplicado en el mismo mundo, sin tocar nada: ¿qué se rompe primero?
4. ¿Hay ya algo simulado? Gazebo no se ha lanzado: ¿qué se ve realmente en RViz?

Con estas respuestas, pasa al [ejercicio 2](../ex02_gazebo_launch/): ahí entra Gazebo.

## Sobre `${prefix}`

En el xacro, `${prefix}` va en los links y no en los joints. Los links son los frames de TF, y
`/tf` es un único topic para todos los robots: dos `base_link` se pisan. La forma del prefijo la
marca ros2_control: su `diff_drive_controller` espera namespace + barra (`robot_a/odom`,
`robot_a/base_footprint`), así que el prefijo será `robot_a/`. Los joints no lo llevan: solo los
usa el propio robot, que ya va en su namespace (`/robot_a/…`). Se usa en el ejercicio 6.

## Errores típicos

| Síntoma | Causa |
|---|---|
| RViz no cambia después de guardar | Falta relanzar `display.launch.py`: el URDF se lee al arrancar |
| La caja sigue a medias bajo el suelo | En el PASO 1 queda la línea `<origin xyz="0 0 0" …/>` |
| `xacro` da un error de XML, o desaparece todo lo que va detrás de un paso | Solo se ha borrado una de las líneas marcadas del paso |
| `rqt_tf_tree: package not found` | La imagen es anterior a este ejercicio: sal del contenedor, `docker pull ghcr.io/asoriano1/roscon-workshop:latest` y vuelve a entrar |
