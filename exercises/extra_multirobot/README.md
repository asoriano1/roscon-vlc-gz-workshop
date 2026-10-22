# Extra — Multi-robot a mano (25 min)

**Opcional**, para quien vaya adelantado. Es el más largo de los extras.

**Qué haces:** monta tres `mini_bot` en el mismo mundo, cada uno con su namespace, su prefijo de
frames y sus controladores, todo desde launch files. Es lo que en el ejercicio 6 fueron tres
clics.

**Punto de partida:** el ejercicio 5 terminado (o su solución copiada).

**Archivos que creas:** `mini_bot/launch/spawn.launch.py` y `mini_bot/launch/multi.launch.py`
**Solución:** `mini_bot/solutions/extra_multirobot/`

## Por qué no basta con lanzar el mismo launch tres veces

El `sim.launch.py` del ejercicio 5 hace cinco cosas: abre Gazebo, mete el robot, lanza el bridge,
abre RViz y arranca los controladores. Lanzado tres veces, abre tres Gazebo. Sepáralo en dos:

- **Una vez por mundo:** Gazebo y el puente de `/clock`.
- **Una vez por robot:** `robot_state_publisher`, `create`, el puente de sus sensores y sus
  spawners.

## Pasos

1. **`spawn.launch.py`: un robot en un Gazebo que ya está corriendo.** Parte de una copia de
   `sim.launch.py` y:
   - Quita Gazebo y RViz.
   - Deja como argumentos `namespace`, `x`, `y` y `yaw`.
   - Pasa al xacro `prefix:=` *namespace + barra*, construido a partir del namespace, para que
     no se pueda pasar uno sin el otro: `' prefix:=', ns, '/'`.
   - Usa el namespace como `-name` de `create`: el nombre del modelo en Gazebo no puede
     repetirse.
2. **El puente de cada robot.** El `bridge.yaml` dice `/scan`, pero con namespace el robot
   publica en `/robot_b/scan`. Sustituye el YAML por el topic construido con el namespace:

   ```python
   arguments=[['/', ns, '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan']],
   ```

3. **`multi.launch.py`: el mundo y tres robots.** Pon Gazebo, un único puente de `/clock` y tres
   `IncludeLaunchDescription` de `spawn.launch.py`: `robot_a` en (0, 0), `robot_b` en (0, 1.5) y
   `robot_c` en (0, −1.5).
4. Son ficheros nuevos, así que compila una vez antes de lanzar:

   ```bash
   cd $WS && colcon build --packages-select mini_bot --symlink-install && source install/setup.bash
   ros2 launch mini_bot multi.launch.py
   ```

⏱️ Apunta el tiempo.

## Comprueba

En otra terminal (lanza `./setup/shell.sh` en tu máquina, desde la raíz del repo):

```bash
ros2 control list_controllers -c /robot_b/controller_manager   # dos controladores, active
ros2 topic list | grep scan                                    # /robot_a/scan, /robot_b/scan, /robot_c/scan
ros2 topic echo /robot_b/scan --once --field header.frame_id   # robot_b/lidar_link
```

Y conduce uno:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -p stamped:=true -r cmd_vel:=/robot_b/diff_drive_controller/cmd_vel
```

## La comparación

Repasa todo lo que has tenido en cuenta: el namespace en cada nodo, el prefijo con barra,
un nombre de modelo distinto, el puente con los topics construidos, `/clock` una sola vez y los
spawners apuntando al `controller_manager` de su robot. En el ejercicio 6 fueron tres campos de
texto por robot.

A cambio, ahora hay un fichero que levanta los tres robots igual, siempre. Eso es lo que no da el
panel.

## Preguntas

1. ¿Por qué el spawner usa `'controller_manager'`, sin barra delante? ¿Qué pasaría con
   `'/controller_manager'`?
2. Lanza un `spawn.launch.py` más con `namespace:=robot_b`: ¿qué pasa?
3. ¿Por qué `/clock` va en `multi.launch.py` y no en `spawn.launch.py`?

## Errores típicos

| Síntoma | Causa |
|---|---|
| Se abren tres Gazebo | `spawn.launch.py` todavía incluye `gz_sim.launch.py` |
| El segundo robot no aparece y `create` da error | Todos los robots con el mismo `-name` |
| `/robot_b/scan` no existe en ROS 2 | El puente usa todavía el `bridge.yaml`, con `/scan` fijo |
| Los spawners esperan para siempre | `--controller-manager /controller_manager` con barra: busca uno sin namespace |
| En RViz el robot no se engancha a `robot_b/odom` | Prefijo sin barra (`robot_b_`): ver el ejercicio 6, "Por qué la barra" |
