# Ejercicio 6 — El mismo robot, con el Model Importer (12 min)

Ya hay un robot que funciona, y se sabe lo que cuesta montarlo. Ahora, lo mismo desde la GUI.

```bash
cd $WS/robots && ros2 launch gz_model_importer gazebo_importer.launch.py \
  world:=$(ros2 pkg prefix mini_bot)/share/mini_bot/worlds/workshop.sdf
```

El `cd $WS/robots` importa: el *Browse* se abre en la carpeta desde la que se lanza, y ahí están
los xacros del taller.

## Pasos

1. **Browse** → `mini_bot.urdf.xacro`. Es un enlace al xacro escrito en los
   ejercicios 1 a 5.
2. El **preview**: la simulación está en pausa y el robot todavía no existe en el mundo.
3. Los campos **Namespace** y **Frame prefix** salen de los `<xacro:arg>` del robot: el importer los detecta.
4. *Namespace* `robot_a` y *Frame prefix* `robot_a/`, **con barra**. El importer propone
   `mini_bot_1_`, con guion bajo: hay que borrarlo y escribirlo a mano. Colocar la pose y dejar
   marcado **robot_state_publisher**.
5. **Import**. La simulación se queda en pausa después de importar: hay que pulsar ▶ abajo a la izquierda.

⏱️ Apuntar el tiempo y compararlo con el de los ejercicios 1 a 5.

## Paso 2 — dos robots más

Importar `robot_b` y `robot_c` en poses distintas, con prefijo `robot_b/` y `robot_c/`. Comprobación en otra terminal (`./setup/shell.sh` en la máquina propia, desde la raíz del repo):

```bash
gz topic -l | grep -c robot_
ros2 node list | grep robot_state_publisher
```

## Por qué la barra

`diff_drive_controller` publica la odometría como `robot_a/odom → robot_a/base_footprint`:
cuando corre en un namespace, prefija sus frames con el namespace y una barra. No es una
convención del taller, es la de ros2_control. Para que el TF de la odometría enlace con el URDF,
los links tienen que llamarse igual: `robot_a/base_footprint`, `robot_a/base_link`… Con
`robot_a_` habría dos árboles sueltos y RViz no pintaría el robot desde `robot_a/odom`.

## Lo importante de este ejercicio

El `sim.launch.py` del ejercicio 5 hace una cosa muy bien: **ese** robot, en **ese** mundo, con **esa**
configuración. El importer no lo sustituye: sirve para la fase en la que todavía no se sabe
qué robot se quiere, dónde ni con qué namespace. Cuando ya se sabe, el launch gana.

## Micro-reto: el modelo roto

Importar `broken/rb_broken_uris.urdf.xacro` y leer el informe de preflight.
¿Qué ha detectado? ¿Por qué lo reporta en vez de arreglarlo?
