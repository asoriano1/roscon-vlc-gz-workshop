# Ejercicio 3 — El control del mástil (20 min)

**El problema:** `mast_bot` es un `mini_bot` con un mástil, y la cámara en lo alto, sobre una
cabeza que gira (`mast_joint`, ±90°). Llega con el control de las ruedas puesto, el del preámbulo
3. Integra el control del mástil y gíralo desde ROS 2.

Sigue los pasos copiando y pegando. Lo importante es entender qué pieza va en cada fichero y
comprobar que cada una funciona.

**Archivos que editas:** `mini_bot/urdf/mast_bot.urdf.xacro`, `mini_bot/config/mast_controllers.yaml`
y `mini_bot/launch/mast.launch.py`
**Solución:** `mini_bot/solutions/ejercicio_3/`

## Antes de empezar

`mast_bot` y su launch son ficheros nuevos para ROS 2: compila una vez. En el contenedor:

```bash
colcon build --packages-select mini_bot --symlink-install && source install/setup.bash
ros2 launch mini_bot mast.launch.py
```

Conduce como en el preámbulo 3: las ruedas funcionan. Además del teleop de teclado, aquí puedes
conducir con el ratón en RViz: alrededor del robot salen unas flechas. Arrastra la flecha roja
para avanzar o retroceder y gira el anillo azul para girar. Al soltar, el robot se para.

Ahora mira el mástil:

```bash
ros2 control list_hardware_interfaces    # no hay nada de mast_joint
```

En RViz, la cabeza del mástil no tiene TF: nadie publica la posición de `mast_joint`. El mástil
existe en Gazebo, pero ros2_control no sabe que se puede mover. Cierra el launch (Ctrl+C).

## 1. El joint, en `<ros2_control>`

En `mast_bot.urdf.xacro`, dentro del bloque `<ros2_control>`, pega esto debajo del comentario
`EJERCICIO 3: pega aquí el joint del mástil`:

```xml
    <joint name="mast_joint">
      <command_interface name="position">
        <param name="min">-1.57</param>
        <param name="max">1.57</param>
      </command_interface>
      <state_interface name="position"/>
      <state_interface name="velocity"/>
    </joint>
```

Las ruedas aceptan órdenes de **velocidad**; el mástil, de **posición**: le dices un ángulo y va.

## 2. El controlador, en el YAML

En `mast_controllers.yaml`, dos pegados. Debajo de `EJERCICIO 3 (1 de 2)`, dentro de
`controller_manager`, la declaración:

```yaml
      mast_controller:
        type: position_controllers/JointGroupPositionController
```

Y debajo de `EJERCICIO 3 (2 de 2)`, al final del fichero, sus parámetros:

```yaml
  mast_controller:
    ros__parameters:
      joints: ["mast_joint"]
```

Respeta la sangría: la declaración va al nivel de `diff_drive_controller:` dentro de
`controller_manager`, y los parámetros, al nivel de `diff_drive_controller:` de abajo.
`JointGroupPositionController` recibe una lista de ángulos, uno por joint, y se la pasa tal cual
a la `command_interface` de posición.

## 3. El spawner, en el launch

En `mast.launch.py`, pega esto debajo de `EJERCICIO 3: pega aquí el spawner del controlador del
mástil`:

```python
    mast_spawner = Node(
        package='controller_manager',
        executable='spawner',
        namespace=ns,
        output='screen',
        arguments=['mast_controller', '--controller-manager', 'controller_manager'],
    )
```

Y añade `mast_spawner,` a la lista del final, debajo de `diff_spawner,`.

## Comprueba

```bash
ros2 launch mini_bot mast.launch.py
```

En otra terminal, uno a uno:

```bash
ros2 control list_controllers                  # tres, active: también mast_controller
ros2 control list_hardware_interfaces | grep mast   # mast_joint/position [claimed]
ros2 topic echo /joint_states --once | grep -A3 name   # ahora sale mast_joint
```

Gira el mástil con el slider, como los de las ruedas en el preámbulo 1:

```bash
ros2 run mini_bot mast_slider.py
```

Cada vez que mueves el slider, publica el ángulo en `/mast_controller/commands`. Es lo mismo que
esta orden desde la consola:

```bash
ros2 topic pub --once /mast_controller/commands std_msgs/msg/Float64MultiArray "{data: [1.0]}"
```

Lleva el slider a 1.0 y comprueba que ha llegado:

```bash
ros2 topic echo /joint_states --once           # mast_joint: 1.0
ros2 run tf2_ros tf2_echo base_link mast_camera_link   # yaw de 57° (Ctrl+C)
```

En RViz, la cabeza del mástil gira y la imagen de la cámara cambia. Las ruedas siguen funcionando,
con el teleop o con las flechas de RViz.

Cuando el mástil obedezca, **pon el post-it verde**.

## Preguntas

1. ¿Qué tres ficheros has tocado y qué pieza va en cada uno?
2. El slider llega a ±1.57. Manda `{data: [3.0]}` con el `ros2 topic pub`. ¿Qué pasa, y por qué?
3. ¿Por qué el controlador del mástil no necesita `stamped:=true` y el teleop sí?

## Errores típicos

| Síntoma | Causa |
|---|---|
| `file 'mast.launch.py' was not found` | Falta el `colcon build` de "Antes de empezar" |
| `mast_controller` no aparece en `list_controllers` | Falta el spawner en la lista del launch |
| Gazebo se cierra al aparecer el robot, y el log dice `Couldn't parse params file` … `Cannot have a value before ros__parameters` | El YAML está mal sangrado: la declaración tiene que ir al nivel de `diff_drive_controller:` dentro de `controller_manager` |
| El controlador no se activa y el log habla de `mast_joint` | El joint no está en `<ros2_control>`, o tiene otro nombre |
| El mástil no se mueve con el slider ni con el `pub` | El controlador no está `active`, o el topic no es `/mast_controller/commands` |
| En RViz no salen las flechas alrededor del robot | El display *Teleop* está desactivado, o el launch es de antes del taller: relanza `mast.launch.py` |
| `No executable found` con `mast_slider.py` | Falta el `colcon build` de "Antes de empezar" |
