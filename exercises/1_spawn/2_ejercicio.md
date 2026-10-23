# Ejercicio 1 — Tres robots en el almacén (20 min)

**El problema:** un almacén con estanterías, pasillos de 1 m y tres estaciones de carga
(amarilla, azul y verde). Lanza tres `mini_bot` con un solo launch y deja cada uno en su
estación: entero sobre la placa y mirando a su cargador.

**Punto de partida:** el preámbulo 1 terminado (o su solución copiada).

**Archivo que editas:** `mini_bot/launch/almacen.launch.py`
**Solución:** `mini_bot/solutions/ejercicio_1/almacen.launch.py`

> **No abras `workshop_almacen.sdf`.** Las poses de las estaciones están ahí escritas, y la
> segunda parte del ejercicio consiste justo en no saberlas.

## Antes de empezar

`almacen.launch.py` y el mundo del almacén son ficheros nuevos para ROS 2: compila una vez para
que se instalen. En el contenedor:

```bash
colcon build --packages-select mini_bot --symlink-install && source install/setup.bash
```

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

Pon cada robot en su estación: cambia `-x`, `-y` y `-Y` en su `create`, guarda, Ctrl+C y vuelve a
lanzar. Repite hasta que los tres queden **sobre su placa y mirando al cargador**. El frontal del
robot es el lado de la rueda loca.

| Robot | Estación |
|---|---|
| `robot_a` | amarilla |
| `robot_b` | azul |
| `robot_c` | verde |

⏱️ Apunta el tiempo y el número de intentos.

Pistas:

- La rejilla del suelo de Gazebo es de 1 m. Mirando hacia el panel de Robotnik, delante es +Y y
  a la derecha, +X.
- `-Y` va en radianes: 90° son 1.571 y 180° son 3.142. Positivo, giro a la izquierda.
- Si el robot nace encima de un cargador o de una estantería, sale despedido: los cargadores y las
  estanterías tienen colisión. Las placas del suelo, no.

## Comprueba

```bash
gz model --list                         # robot_a, robot_b y robot_c
ros2 node list                          # tres robot_state_publisher, cada uno en su namespace
ros2 topic list | grep robot_description  # tres /robot_x/robot_description
```

Cuando los tres estén en su estación, **pon el post-it verde**.

## Preguntas

1. Quita el namespace de `robot_b` y de `robot_c` (deja el `-name`). En Gazebo aparecen los tres.
   ¿Qué se ha roto en ROS 2? Pista: `ros2 node list` y `ros2 topic info /robot_description`.
2. Cada robot más son veinte líneas copiadas en las que hay que cambiar el nombre en cinco sitios.
   ¿Cómo lo harías con diez robots?

## Errores típicos

| Síntoma | Causa |
|---|---|
| `file 'almacen.launch.py' was not found` | Falta el `colcon build` de "Antes de empezar" |
| Sale solo `robot_a` | Los nodos nuevos no están en las listas del final del launch |
| Falta un robot, y `create` dice `Entity creation successful` | Dos `-name` iguales: Gazebo descarta el segundo sin avisar. Revisa el `-name` de cada bloque copiado |
| El robot cae girado, pero no como se esperaba | `-Y` va en radianes, no en grados |
| Un robot sale despedido al aparecer | Ha nacido dentro de un cargador o de una estantería: ajusta la pose |
