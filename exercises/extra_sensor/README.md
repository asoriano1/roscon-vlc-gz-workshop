# Extra — Un sensor más (15 min)

**Opcional**, para quien vaya adelantado.

**Qué se hace:** añadir una IMU al `mini_bot` y llevarla hasta ROS 2. Primero a mano, como en los
ejercicios 3 y 4. Después con el importer y el Bridge Manager. Y contar lo que se ha tocado en
cada caso.

**Punto de partida:** el ejercicio 5 terminado (o su solución copiada) y, para la segunda parte,
los ejercicios 6 y 7 vistos.

**Archivos que se editan:** `mini_bot/urdf/mini_bot.urdf.xacro` y `mini_bot/config/bridge.yaml`
**Solución:** `mini_bot/solutions/extra_sensor/`

## Parte 1 — A mano

1. **El sensor, en el xacro.** Añadir este bloque antes de la sección de ros2_control. Va en
   `base_link`, así que no hace falta link nuevo:

   ```xml
   <gazebo reference="${prefix}base_link">
     <sensor name="imu" type="imu">
       <topic>${tns}/imu</topic>
       <gz_frame_id>${prefix}base_link</gz_frame_id>
       <update_rate>50</update_rate>
       <always_on>true</always_on>
     </sensor>
   </gazebo>
   ```

2. **Lanzar y comprobar** en Gazebo, en la terminal del contenedor:

   ```bash
   ros2 launch mini_bot sim.launch.py
   ```

   Y en otra terminal (`./setup/shell.sh` en la máquina propia, desde la raíz del repo):

   ```bash
   gz topic -l | grep imu      # Gazebo ya la publica
   ros2 topic list | grep imu  # ROS 2 no ve nada
   ```

   Es lo mismo que al final del ejercicio 3: el sensor existe, pero nadie lo ha puenteado.

3. **El puente.** Añadir la IMU a `config/bridge.yaml`. Tipo ROS `sensor_msgs/msg/Imu`, tipo
   Gazebo `gz.msgs.IMU`.
4. Ctrl+C en el launch y volver a lanzarlo: el bridge solo lee el YAML al arrancar.
5. Comprobación:

   ```bash
   ros2 topic hz /imu          # unos 50 Hz × RTF
   ros2 topic echo /imu --once --field linear_acceleration
   ```

   Con el robot parado, la `z` tiene que ser casi 9,8: es la gravedad.

⏱️ Apuntar el tiempo y **cuántos ficheros se han tocado**.

## Parte 2 — Con la suite

El xacro ya tiene la IMU de la parte 1.

1. Lanzar Gazebo con el importer, como en el ejercicio 6, e importar un `mini_bot` con namespace
   `robot_a` y prefijo `robot_a/`. Pulsar ▶.
2. Abrir el **ROS 2 Bridge Manager** y pulsar **Refresh**. Buscar la IMU de `robot_a`.
3. Marcarla junto al LiDAR, y **Run**.
4. Comprobarlo con `ros2 topic list | grep imu`.

⏱️ Apuntar el tiempo y cuántos ficheros se han tocado.

## La comparación

A mano, un sensor nuevo son dos sitios: el xacro, que describe el robot, y el `bridge.yaml`, que
dice qué sale a ROS 2. Si se olvida el segundo, el sensor existe y nadie lo ve. Además, el puente
hay que reiniciarlo.

Con la suite solo se toca el xacro. El Bridge Manager encuentra el sensor recorriendo el mundo.

## Preguntas

1. En la parte 1, ¿por qué no ha hecho falta `colcon build` después de cambiar el xacro y el YAML?
2. Con el robot parado, ¿la aceleración en `x` es exactamente 0? ¿Qué dice eso de cómo está
   apoyado el robot?
3. Con tres robots con IMU, ¿cuántas entradas tendría el `bridge.yaml`?

## Errores típicos

| Síntoma | Causa |
|---|---|
| `gz topic -l` no muestra `/imu` | El bloque está fuera de `<robot>`, o falta el `<topic>` |
| `ros2 topic list` no muestra `/imu` tras editar el YAML | Falta relanzar: el bridge lee el YAML al arrancar |
| El bridge arranca y se cae al leer el YAML | Indentación: copiar la forma de la entrada del LiDAR |
| La IMU no aparece en el Bridge Manager | Falta **Refresh**, o el robot se importó antes de añadir la IMU al xacro |
