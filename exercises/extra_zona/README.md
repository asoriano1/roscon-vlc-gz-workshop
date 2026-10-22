# Extra — Aparcar en la zona (15 min)

**Opcional**, para quien vaya adelantado.

**Qué se hace:** dejar el `mini_bot` dentro de una zona pintada en el suelo, mirando hacia donde
marca la flecha. Primero desde la consola, después con el ratón en el Model Importer. Y comparar.

**Punto de partida:** el ejercicio 5 terminado (o su solución copiada) y, para la segunda parte,
el ejercicio 6 visto.

**Archivo que se edita:** `mini_bot/launch/sim.launch.py`

> **Sin abrir `workshop_zona.sdf`.** La pose de la zona está ahí escrita, y el ejercicio consiste
> justo en no saberla.

## Antes de empezar

El mundo `workshop_zona.sdf` es un fichero nuevo, así que hay que compilar una vez para que se
instale. En la terminal del contenedor:

```bash
cd $WS && colcon build --packages-select mini_bot --symlink-install && source install/setup.bash
```

## Parte 1 — Desde la consola

El `sim.launch.py` acepta `x` e `y`, pero no la orientación. La zona está girada.

1. Añadir a `sim.launch.py` un argumento `yaw` (por defecto `0.0`) y pasárselo a `create` como
   `'-Y', LaunchConfiguration('yaw')`. Es el giro alrededor del eje vertical, en radianes.
2. Lanzar el mundo con la zona y ver dónde cae el robot:

   ```bash
   ros2 launch mini_bot sim.launch.py rviz:=false \
     world:=$(ros2 pkg prefix mini_bot)/share/mini_bot/worlds/workshop_zona.sdf \
     x:=0.0 y:=0.0 yaw:=0.0
   ```

3. Buscar la zona amarilla en Gazebo. Ctrl+C, cambiar `x`, `y` y `yaw`, y volver a lanzar.
   Repetir hasta que el robot quede **entero dentro de la zona y mirando como la flecha**.

⏱️ Apuntar el tiempo y el número de intentos.

Pista: `yaw` va en radianes. 90° son 1.571 y 180° son 3.142.

## Parte 2 — Con el ratón

1. Lanzar Gazebo con el importer en el mismo mundo:

   ```bash
   cd $WS/robots && ros2 launch gz_model_importer gazebo_importer.launch.py \
     world:=$(ros2 pkg prefix mini_bot)/share/mini_bot/worlds/workshop_zona.sdf
   ```

2. **Browse** → `mini_bot.urdf.xacro`. Aparece el **preview** y la simulación queda congelada.
3. Clic en el robot del preview. Con la herramienta **Translate** (tecla `T`), arrastrarlo hasta
   la zona. Con **Rotate** (tecla `R`), girarlo hasta que mire como la flecha.
4. Los campos **Pose** del importer se han rellenado solos con la posición del preview.
5. **Import** y ▶.

⏱️ Apuntar el tiempo.

## La comparación

En la consola, cada intento es lanzarlo todo otra vez y adivinar números. Con el preview
congelado, el robot se coloca donde se ve, y el importer da los números.

Esos números son los que irían en el launch. El ratón sirve para encontrarlos; el launch, para no
tener que volver a buscarlos.

## Preguntas

1. ¿Por qué el robot de la parte 1 no queda exactamente donde se le dice? Una pista: comparar la
   `z` final con la que se le pasa.
2. Con los números del importer en el `ros2 launch`, ¿cae en el mismo sitio?

## Errores típicos

| Síntoma | Causa |
|---|---|
| Gazebo no encuentra el mundo, o sale sin zona amarilla | Falta el `colcon build` de "Antes de empezar" |
| El robot cae girado, pero no como se esperaba | `yaw` va en radianes, no en grados |
| `-Y` no hace nada | Está en `DeclareLaunchArgument` pero no en los `arguments` de `create`, o al revés |
| El robot del preview no se mueve al arrastrarlo | Primero hay que hacer clic en el robot para seleccionarlo, y después `T` |
