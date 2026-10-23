# Post-ejercicio 1 — Lo mismo, con el Model Importer (15 min)

Primero, la demo del ponente. Después, repite el ejercicio 1 con el **Model Importer**: los tres
robots, cada uno en su estación, sin escribir una línea.

El importer es un plugin de la GUI de Gazebo. Hace lo que hace tu `almacen.launch.py`: expande el
xacro, lanza `robot_state_publisher` y crea el robot en el mundo. Pero antes enseña un preview
congelado que se mueve con el ratón.

## Lanza Gazebo con el importer

Cierra el launch del ejercicio 1 (Ctrl+C) y lanza el almacén con el importer:

```bash
cd $WS/robots && ros2 launch gz_model_importer gazebo_importer.launch.py \
  world:=$(ros2 pkg prefix mini_bot)/share/mini_bot/worlds/workshop_almacen.sdf
```

El `cd $WS/robots` importa: el *Browse* se abre en la carpeta desde la que lanzas, y ahí están
los xacros del taller.

## Pasos, para cada robot

1. Pulsa **Browse** y elige `mini_bot.urdf.xacro`. Es un enlace al mismo xacro que has editado.
2. Aparece el **preview** y la simulación queda congelada: el robot todavía no existe en el mundo.
3. Haz clic en el robot del preview. Con **Translate** (tecla `T`), arrástralo hasta su estación.
   Con **Rotate** (tecla `R`), gíralo hasta que mire al cargador.
4. Mira los campos **Pose** del importer: se han rellenado solos con la posición del preview.
5. Escribe *Namespace* `robot_a` y *Frame prefix* `robot_a/`, **con barra**. El importer los saca
   de los `<xacro:arg>` del robot y propone `mini_bot_1_`, con guion bajo: bórralo y escríbelo a
   mano. Deja marcado **robot_state_publisher**.
6. Pulsa **Import**. La simulación se queda en pausa después de importar: pulsa ▶ abajo a la
   izquierda.

Repite con `robot_b` en la estación azul y `robot_c` en la verde.

⏱️ Apunta el tiempo y compáralo con el del ejercicio 1.

## Comprueba

Los mismos comandos que en el ejercicio 1, con el mismo resultado:

```bash
gz model --list
ros2 node list
ros2 topic list | grep robot_description
```

## La comparación

A mano, cada intento es relanzarlo todo y adivinar números, y cada robot más son veinte líneas
copiadas. Con el importer, colocas el robot donde lo ves y el importer da los números; namespace,
prefijo y nombre son tres campos.

El launch no sobra: los números que da el importer son los que irían en el launch. El ratón sirve
para encontrarlos, mientras todavía no sabes qué robot quieres ni dónde; el launch, para no tener
que volver a buscarlos.

## Por qué la barra en el prefijo

`diff_drive_controller` publica la odometría como `robot_a/odom → robot_a/base_footprint`: cuando
corre en un namespace, prefija sus frames con el namespace y una barra. Es la convención de
ros2_control. Para que el TF de la odometría enlace con el URDF, los links tienen que llamarse
igual: `robot_a/base_footprint`, `robot_a/base_link`… Con `robot_a_` habría dos árboles sueltos.
Se ve en la sección 3.

## Si sobra tiempo: el modelo roto

Importa `broken/rb_broken_uris.urdf.xacro` y lee el informe de preflight. ¿Qué ha detectado?
¿Por qué lo reporta en vez de arreglarlo?

## Errores típicos

| Síntoma | Causa |
|---|---|
| Un robot importado no hace nada | La simulación se queda en pausa después de importar: pulsa ▶ |
| El robot del preview no se mueve al arrastrarlo | Haz clic primero en el robot para seleccionarlo, y después pulsa `T` |
| El *Browse* no enseña los xacros | Gazebo se lanzó desde otra carpeta: relánzalo con `cd $WS/robots && …` |
| Falta un robot | Mismo nombre de modelo que otro: Gazebo lo descarta sin avisar (`gz model --list`) |
| El campo de ruta del diálogo de ficheros sale con texto raro | Conserva lo que se escribió la vez anterior: Ctrl+A antes de escribir |
