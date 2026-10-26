# Ejercicio 1 — Tres robots en el almacén (15 min)

**El problema:** un almacén con estanterías, pasillos de 1 m y tres estaciones de carga
(amarilla, azul y verde). Lanza tres `mini_bot` con un solo launch y deja cada uno en su
estación: entero sobre la placa y mirando a su cargador.

**Punto de partida:** el preámbulo 1 terminado (o su solución copiada).

**Archivo que editas:** `mini_bot/launch/almacen.launch.py`
**Solución:** `mini_bot/solutions/ejercicio_1/almacen.launch.py`

## Antes de empezar

Abre `mini_bot/launch/almacen.launch.py` en tu editor. Trae el almacén y un robot completo,
`robot_a`, en la pose `(0, 0, 0)`. Lee el comentario del bloque de `robot_a`: explica las tres
cosas que tienen que cambiar de un robot a otro.

## Parte 1 — Tres robots, un launch

1. Copia el bloque de `robot_a` dos veces, para `robot_b` y `robot_c`. Cambia todo lo que diga
   `robot_a`, y añade los nodos nuevos a las dos listas del final: la del `TimerAction` y la de
   `LaunchDescription`. No toques las poses.
2. Lanza:

   ```bash
   ros2 launch mini_bot almacen.launch.py
   ```

3. Cuenta los robots en Gazebo. Después, en otra terminal (`./setup/shell.sh`):

   ```bash
   gz model --list
   ```

Gazebo dice que hay tres, y en pantalla se ve uno: están los tres en el mismo sitio, uno dentro
de otro. Cada robot necesita su propia pose.

## Parte 2 — Cada uno en su estación

El plano del almacén da la pose de cada estación. Escríbela en el `create` de cada robot
(`-x`, `-y` y `-Y`), guarda, Ctrl+C y vuelve a lanzar.

| Robot | Estación | x | y | Orientación |
|---|---|---|---|---|
| `robot_a` | amarilla | 3.45 | -1.10 | 0° |
| `robot_b` | azul | -1.00 | -2.15 | -90° |
| `robot_c` | verde | -1.60 | 1.50 | 135° |

La orientación del plano va en grados, y `-Y` la quiere en **radianes**: conviértela
(180° son π, 3.1416). Positivo es giro a la izquierda, visto desde arriba.

Comprueba en Gazebo que los tres quedan **sobre su placa y mirando al cargador**. El frontal del
robot es el de la franja roja. Si uno mira hacia otro lado, revisa su `-Y`.

## Comprueba

```bash
gz model --list                         # robot_a, robot_b y robot_c
ros2 node list                          # tres robot_state_publisher, cada uno en su namespace
ros2 topic list | grep robot_description  # tres /robot_x/robot_description
```

Cuando los tres estén en su estación, **pon el post-it verde**.

## Por qué la barra en el prefijo

El prefijo es `robot_a/`, con barra, y no `robot_a_`. `diff_drive_controller`, el controlador de
la sección 3, publica la odometría como `robot_a/odom → robot_a/base_footprint`: cuando corre en
un namespace, prefija sus frames con el namespace y una barra. Para que ese TF enlace con el URDF,
los links tienen que llamarse igual: `robot_a/base_footprint`, `robot_a/base_link`… Con
`robot_a_` habría dos árboles sueltos.

## Preguntas

1. Quita el namespace de `robot_b` y de `robot_c` (deja el `-name`). En Gazebo aparecen los tres.
   ¿Qué se ha roto en ROS 2? Pista: `ros2 node list` y `ros2 topic info /robot_description`.
2. Cada robot más son veinte líneas copiadas en las que hay que cambiar el nombre en cinco sitios.
   ¿Cómo lo harías con diez robots?

## Errores típicos

| Síntoma | Causa |
|---|---|
| `file 'almacen.launch.py' was not found` | La imagen es anterior a ese fichero: `colcon build --packages-select mini_bot --symlink-install && source install/setup.bash` |
| Sale solo `robot_a` | Los nodos nuevos no están en las listas del final del launch |
| Falta un robot, y `create` dice `Entity creation successful` | Dos `-name` iguales: Gazebo descarta el segundo sin avisar. Revisa el `-name` de cada bloque copiado |
| El robot cae girado, pero no como se esperaba | `-Y` va en radianes, no en grados |
| El robot queda mirando al revés | El signo de `-Y`: positivo gira a la izquierda |
| Un robot sale despedido al aparecer | Ha nacido dentro de un cargador o de una estantería: ajusta la pose |
