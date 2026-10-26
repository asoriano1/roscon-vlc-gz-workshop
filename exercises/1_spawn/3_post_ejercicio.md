# Post-ejercicio 1 — Robots de Robotnik en el almacén, con el Model Importer (20 min)

Primero te lo enseño en directo, en el proyector. Después, llegan dos robots nuevos al almacén:
un **RB-Summit** y un **RB-Theron** de Robotnik, robots reales con mallas y sensores. Los tres
`mini_bot` siguen en sus estaciones, lanzados con tu `almacen.launch.py`. Los nuevos entran con el
**Model Importer**, con la simulación en marcha, y se quedan en la **zona de recepción**: el
rectángulo blanco del suelo.

El importer es un plugin de la GUI de Gazebo. Hace, para cada robot, lo que hace tu launch:
expande el xacro, lanza `robot_state_publisher` y crea el robot en el mundo. Antes enseña un
preview: una copia estática, sin física, que se coloca con el ratón.

## 1. El almacén, con el importer y con tu launch

Cierra el launch del ejercicio 1 (Ctrl+C) y lanza el almacén con el importer:

```bash
cd $WS/robots && ros2 launch gz_model_importer gazebo_importer.launch.py \
  world:=$(ros2 pkg prefix mini_bot)/share/mini_bot/worlds/workshop_almacen.sdf
```

El `cd $WS/robots` importa: el *Browse* se abre en la carpeta desde la que lanzas, y ahí están
los xacros del taller y los de Robotnik.

En otra terminal (`./setup/shell.sh`), lanza tus tres `mini_bot` sin abrir otro Gazebo:

```bash
ros2 launch mini_bot almacen.launch.py gazebo:=false
```

Aparecen en sus estaciones, en el Gazebo del importer: `create` busca solo el mundo que hay
abierto. El launch y el importer no se excluyen: aquí trabajan juntos.

## 2. Importa el RB-Summit

1. Pulsa **Browse** y elige `rbsummit.urdf.xacro`. Tarda un par de segundos más que el
   `mini_bot`: tiene mallas.
2. Aparece el **preview**. El robot todavía no existe en el mundo.
3. Haz clic en el preview. Con **Translate**, en la barra de herramientas de Gazebo, arrástralo
   dentro de la zona de recepción. Con **Rotate**, gíralo como quieras. No hay una pose exacta:
   vale cualquier sitio dentro del rectángulo.
4. Mira los campos **Pose** del importer: se han rellenado solos con la posición del preview.
5. Escribe *Namespace* `summit_a` y *Frame prefix* `summit_a/`, **con barra**, como en el
   ejercicio 1. El importer propone otro prefijo: bórralo y escríbelo a mano. Deja marcado
   **robot_state_publisher**.
6. Pulsa **Import**. La simulación se queda en pausa después de importar, y los `mini_bot` con
   ella: pulsa ▶ abajo a la izquierda.

## 3. Uno más

Repite con `rbtheron.urdf.xacro`: *Namespace* `theron_a`, *Frame prefix* `theron_a/`, al lado del
Summit y sin tocarlo.

En la carpeta hay más robots de Robotnik (`rbvogui.urdf.xacro`, `rbkairos_plus.urdf.xacro`). Si
sobra tiempo y la simulación va fluida, prueba uno.

## Comprueba

```bash
gz model --list                           # robot_a, robot_b, robot_c, summit_a y theron_a
ros2 node list                            # cinco robot_state_publisher
ros2 topic list | grep robot_description  # cinco /<robot>/robot_description
```

Cuenta las líneas que has escrito para los dos robots nuevos.

## La comparación

| | Launch | Importer |
|---|---|---|
| Colocar un robot | Números en el fichero | Arrastrar el preview, o escribir en *Pose* |
| Un robot más | Otro bloque de veinte líneas, y relanzarlo todo | *Browse* y tres campos, con la simulación en marcha |
| Otro modelo de robot | Otra ruta de xacro y sus argumentos | Otro fichero en el *Browse* |
| Repetirlo mañana | `ros2 launch` | Otra vez a mano |

Para colocar un robot, ninguno gana: lo mismo se consigue con Gazebo en pausa y sus herramientas
de mover. El importer ahorra el *setup* de cada robot: el xacro con sus argumentos, el
`robot_state_publisher` en su namespace y el `create`, con cualquier modelo y sin parar lo que ya
corre. El launch es lo que se versiona y se repite. El importer sirve para probar modelos y montar
escenas; cuando una escena funciona, sus números pasan al launch.

## Errores típicos

| Síntoma | Causa |
|---|---|
| Un robot importado no hace nada, y los `mini_bot` tampoco | La simulación se queda en pausa después de importar: pulsa ▶ |
| Se abre un segundo Gazebo | Falta `gazebo:=false` en `almacen.launch.py`: ciérralo y relánzalo con él |
| Solo aparece `robot_a`, en el centro | El ejercicio 1 está sin terminar: copia su solución, `cp mini_bot/solutions/ejercicio_1/almacen.launch.py mini_bot/launch/` |
| El robot del preview no se mueve al arrastrarlo | Haz clic primero en el robot para seleccionarlo, y después elige **Translate** en la barra de herramientas |
| El *Browse* no enseña los xacros | Gazebo se lanzó desde otra carpeta: relánzalo con `cd $WS/robots && …` |
| Falta un robot | Mismo nombre de modelo que otro: Gazebo lo descarta sin avisar (`gz model --list`) |
| El campo de ruta del diálogo de ficheros sale con texto raro | Conserva lo que se escribió la vez anterior: Ctrl+A antes de escribir |
| La simulación va muy lenta | Los Robotnik pesan más que el `mini_bot`: quédate con el Summit y no importes el segundo |
