# Extra — Aparca en la zona (15 min)

**Opcional**, para quien vaya adelantado.

**Qué haces:** deja el `mini_bot` dentro de una zona pintada en el suelo, mirando hacia donde
marca la flecha. Primero desde la consola, después con el ratón en el Model Importer. Y compara.

**Punto de partida:** el ejercicio 5 terminado (o su solución copiada) y, para la segunda parte,
el ejercicio 6 visto.

**Archivo que editas:** `mini_bot/launch/sim.launch.py`

> **No abras `workshop_zona.sdf`.** La pose de la zona está ahí escrita, y el ejercicio consiste
> justo en no saberla.

## Antes de empezar

El mundo `workshop_zona.sdf` es un fichero nuevo, así que compila una vez para que se instale. En la terminal del contenedor:

```bash
cd $WS && colcon build --packages-select mini_bot --symlink-install && source install/setup.bash
```

## Parte 1 — Desde la consola

El `sim.launch.py` acepta `x` e `y`, pero no la orientación. La zona está girada.

1. Añade a `sim.launch.py` un argumento `yaw` (por defecto `0.0`) y pásaselo a `create` como
   `'-Y', LaunchConfiguration('yaw')`. Es el giro alrededor del eje vertical, en radianes.
2. Lanza el mundo con la zona y mira dónde cae el robot:

   ```bash
   ros2 launch mini_bot sim.launch.py rviz:=false \
     world:=$(ros2 pkg prefix mini_bot)/share/mini_bot/worlds/workshop_zona.sdf \
     x:=0.0 y:=0.0 yaw:=0.0
   ```

3. Busca la zona amarilla en Gazebo. Pulsa Ctrl+C, cambia `x`, `y` y `yaw`, y vuelve a lanzar.
   Repite hasta que el robot quede **entero dentro de la zona y mirando como la flecha**.

⏱️ Apunta el tiempo y el número de intentos.

Pista: `yaw` va en radianes. 90° son 1.571 y 180° son 3.142.

## Parte 2 — Con el ratón

1. Lanza Gazebo con el importer en el mismo mundo:

   ```bash
   cd $WS/robots && ros2 launch gz_model_importer gazebo_importer.launch.py \
     world:=$(ros2 pkg prefix mini_bot)/share/mini_bot/worlds/workshop_zona.sdf
   ```

2. Pulsa **Browse** y elige `mini_bot.urdf.xacro`. Aparece el **preview** y la simulación queda congelada.
3. Haz clic en el robot del preview. Con la herramienta **Translate** (tecla `T`), arrástralo
   hasta la zona. Con **Rotate** (tecla `R`), gíralo hasta que mire como la flecha.
4. Mira los campos **Pose** del importer: se han rellenado solos con la posición del preview.
5. Pulsa **Import** y ▶.

⏱️ Apunta el tiempo.

## La comparación

En la consola, cada intento es lanzarlo todo otra vez y adivinar números. Con el preview
congelado, colocas el robot donde lo ves, y el importer da los números.

Esos números son los que irían en el launch. El ratón sirve para encontrarlos; el launch, para no
tener que volver a buscarlos.

## Preguntas

1. ¿Por qué el robot de la parte 1 no queda exactamente donde le dices? Pista: compara la `z`
   final con la que le pasas.
2. Copia los números del importer en el `ros2 launch`. ¿Cae en el mismo sitio?

## Errores típicos

| Síntoma | Causa |
|---|---|
| Gazebo no encuentra el mundo, o sale sin zona amarilla | Falta el `colcon build` de "Antes de empezar" |
| El robot cae girado, pero no como se esperaba | `yaw` va en radianes, no en grados |
| `-Y` no hace nada | Está en `DeclareLaunchArgument` pero no en los `arguments` de `create`, o al revés |
| El robot del preview no se mueve al arrastrarlo | Haz clic primero en el robot para seleccionarlo, y después pulsa `T` |
