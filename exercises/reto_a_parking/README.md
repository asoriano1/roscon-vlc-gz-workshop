# Reto A — Aparca tres robots (30 min)

**El problema:** un parking con tres plazas pintadas en el suelo (amarilla, azul y verde). Aparca un
`mini_bot` en cada una, entero dentro de la plaza y mirando hacia donde marca su flecha.

Primero a mano, con un launch (15 min). Después, con el **Model Importer** (15 min, con la demo).

**Punto de partida:** el ejercicio 2 terminado (o sus soluciones copiadas).

> **No abras `workshop_parking.sdf`.** Las poses de las plazas están ahí escritas, y la primera
> mitad del reto consiste justo en no saberlas.

## Parte 1 — A mano, con un launch (15 min)

**Archivo que editas:** `mini_bot/launch/parking.launch.py`
**Solución:** `mini_bot/solutions/reto_a/parking.launch.py`

### Antes de empezar

`parking.launch.py` y el mundo del parking son ficheros nuevos, así que compila una vez para que
se instalen. En la terminal del contenedor:

```bash
cd $WS && colcon build --packages-select mini_bot --symlink-install && source install/setup.bash
```

Abre `mini_bot/launch/parking.launch.py` en tu editor. Trae el mundo y un robot completo,
`robot_a`, en la pose `(0, 0, 0)`. Lee el comentario del bloque de `robot_a`: explica las tres
cosas que tienen que cambiar de un robot a otro.

### Pasos

1. Lanza el launch tal cual y busca las tres plazas en Gazebo:

   ```bash
   ros2 launch mini_bot parking.launch.py
   ```

2. Pon `robot_a` en la plaza amarilla: cambia `-x`, `-y` y `-Y` en su `create`, guarda, pulsa
   Ctrl+C y vuelve a lanzar. Repite hasta que quede **entero dentro de la plaza y mirando como la
   flecha**. El frontal del robot es el lado de la rueda loca.
3. Copia el bloque de `robot_a` dos veces, para `robot_b` (plaza azul) y `robot_c` (plaza verde).
   Cambia todo lo que diga `robot_a` y añade los nodos nuevos a las dos listas del final: la del
   `TimerAction` y la de `LaunchDescription`.
4. Encuentra sus poses igual que la de `robot_a`.

⏱️ Apunta el tiempo y el número de intentos.

Pistas:

- La rejilla del suelo de Gazebo es de 1 m. El origen `(0, 0)` es donde nace el robot del
  ejercicio 2. Mirando hacia el panel de Robotnik, delante es +Y y a la derecha, +X.
- `-Y` va en radianes: 90° son 1.571 y 180° son 3.142. Positivo, giro a la izquierda.

### Comprueba

En otra terminal (`./setup/shell.sh` desde la raíz del repo):

```bash
gz model --list
ros2 node list
ros2 topic list | grep robot_description
```

Tres modelos `robot_a`, `robot_b` y `robot_c` en Gazebo; tres `robot_state_publisher`, cada uno en su
namespace; y tres `/robot_x/robot_description`.

## Parte 2 — Con el Model Importer (15 min)

Primero, la demo del ponente. Después, repite el reto: los tres robots, en las tres plazas.

Cierra el launch de la parte 1 (Ctrl+C) y lanza Gazebo con el importer en el mismo mundo:

```bash
cd $WS/robots && ros2 launch gz_model_importer gazebo_importer.launch.py \
  world:=$(ros2 pkg prefix mini_bot)/share/mini_bot/worlds/workshop_parking.sdf
```

El `cd $WS/robots` importa: el *Browse* se abre en la carpeta desde la que lanzas, y ahí están
los xacros del taller.

### Pasos, para cada robot

1. Pulsa **Browse** y elige `mini_bot.urdf.xacro`. Es un enlace al mismo xacro de los ejercicios.
2. Aparece el **preview** y la simulación queda congelada: el robot todavía no existe en el mundo.
3. Haz clic en el robot del preview. Con **Translate** (tecla `T`), arrástralo hasta su plaza. Con
   **Rotate** (tecla `R`), gíralo hasta que mire como la flecha.
4. Mira los campos **Pose** del importer: se han rellenado solos con la posición del preview.
5. Fíjate en **Namespace** y **Frame prefix**: el importer los saca de los `<xacro:arg>` del robot.
   Escribe *Namespace* `robot_a` y *Frame prefix* `robot_a/`, **con barra**. El importer propone
   `mini_bot_1_`, con guion bajo: bórralo y escríbelo a mano. Deja marcado
   **robot_state_publisher**.
6. Pulsa **Import**. La simulación se queda en pausa después de importar: pulsa ▶ abajo a la
   izquierda.

Repite con `robot_b` en la plaza azul y `robot_c` en la verde.

⏱️ Apunta el tiempo y compáralo con el de la parte 1.

Comprueba con los mismos comandos que en la parte 1: el resultado tiene que ser el mismo.

## La comparación

A mano, cada intento es relanzarlo todo y adivinar números, y cada robot más son veinte líneas
copiadas en las que hay que cambiar el nombre en cinco sitios. Con el importer, colocas el robot
donde lo ves y el importer da los números; namespace, prefijo y nombre son tres campos.

El launch no sobra: los números que da el importer son los que irían en el launch. El ratón sirve
para encontrarlos, mientras todavía no sabes qué robot quieres ni dónde; el launch, para no tener
que volver a buscarlos.

## Por qué la barra en el prefijo

`diff_drive_controller` publica la odometría como `robot_a/odom → robot_a/base_footprint`:
cuando corre en un namespace, prefija sus frames con el namespace y una barra. No es una
convención del taller, es la de ros2_control. Para que el TF de la odometría enlace con el URDF,
los links tienen que llamarse igual: `robot_a/base_footprint`, `robot_a/base_link`… Con
`robot_a_` habría dos árboles sueltos. Se ve en el ejercicio 5.

## Preguntas

1. Quita el namespace de `robot_b` y de `robot_c` en tu launch (deja el `-name`). En Gazebo
   aparecen los tres. ¿Qué se ha roto en ROS 2? Pista: `ros2 node list`, y
   `ros2 topic info /robot_description`.
2. ¿Por qué el robot no queda exactamente a la altura que le dices? Compara la `z` que le pasas con
   la que da `gz model -m robot_a -p`.
3. Copia los números de la pose del importer en tu launch. ¿Cae en el mismo sitio?

## Micro-reto: el modelo roto

Importa `broken/rb_broken_uris.urdf.xacro` y lee el informe de preflight.
¿Qué ha detectado? ¿Por qué lo reporta en vez de arreglarlo?

## Errores típicos

| Síntoma | Causa |
|---|---|
| `file 'parking.launch.py' was not found` | Falta el `colcon build` de "Antes de empezar" |
| Sale solo `robot_a` | Los nodos nuevos no están en las listas del final del launch |
| Falta un robot, y `create` dice `Entity creation successful` | Dos `-name` iguales: Gazebo descarta el segundo sin avisar. Revisa el `-name` de cada bloque copiado |
| El robot cae girado, pero no como se esperaba | `-Y` va en radianes, no en grados |
| Un robot importado no hace nada | La simulación se queda en pausa después de importar: pulsa ▶ |
| El robot del preview no se mueve al arrastrarlo | Haz clic primero en el robot para seleccionarlo, y después pulsa `T` |
