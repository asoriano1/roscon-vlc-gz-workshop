# Ejercicio 5 — ros2_control y los controladores (15 min)

**Qué se construye:** el bloque `<ros2_control>` del URDF, el plugin de Gazebo y los
spawners en el launch. Al final, el robot se conduce con el teclado.

**Archivos que se editan:** `mini_bot/urdf/mini_bot.urdf.xacro` y `mini_bot/launch/sim.launch.py`
**Soluciones:** `mini_bot/solutions/ex05/`
**Ya viene hecho:** `mini_bot/config/controllers.yaml`

> **Qué hace cada pieza:** el plugin, el `controller_manager`, los spawners, el *broadcaster* y el
> `diff_drive_controller`, en [Anatomía de un robot simulado](../../docs/anatomia.md).

## Pasos

1. En el URDF, un bloque `<ros2_control name="${prefix}GazeboSimSystem" type="system">` con:

   - `<plugin>gz_ros2_control/GazeboSimSystem</plugin>`
   - los dos joints de las ruedas, cada uno con `command_interface` de velocidad y
     `state_interface` de posición y velocidad.

2. El plugin del sistema, que carga los controladores:

   ```xml
   <gazebo>
     <plugin filename="gz_ros2_control-system" name="gz_ros2_control::GazeboSimROS2ControlPlugin">
       <parameters>$(find mini_bot)/config/controllers.yaml</parameters>
       <ros><namespace>${ns}</namespace></ros>
     </plugin>
   </gazebo>
   ```

3. En el launch, dos spawners: `joint_state_broadcaster` y `diff_drive_controller`.

## Comprobación

```bash
ros2 launch mini_bot sim.launch.py
```

En otra terminal (`./setup/shell.sh` en la máquina propia, desde la raíz del repo):

```bash
ros2 control list_controllers
ros2 control list_hardware_interfaces
```

Y a conducir:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -p stamped:=true -r cmd_vel:=/diff_drive_controller/cmd_vel
```

> Como en el ejercicio 4: todo lo que mide `ros2 topic hz` (`/scan`, `/camera/image`,
> `/diff_drive_controller/odom`) sale multiplicado por el RTF. Con RTF 0.7, un 5 Hz nominal llega
> a ~3.5 Hz reales. **No es un error**, y para conducir sobra.

## La odometría no es la verdad

`/diff_drive_controller/odom` no sabe dónde está el robot: lo calcula contando vueltas de rueda.
Hay que compararla con la pose real que da Gazebo:

```bash
ros2 topic echo /diff_drive_controller/odom --once --field pose.pose.position
gz model -m mini_bot -p
```

Primero en línea recta y después dando vueltas un rato. ¿Coinciden? Si no, ¿de dónde sale la
diferencia?

## Preguntas

1. ¿Qué diferencia hay entre una `command_interface` y una `state_interface`?
2. ¿Quién publica la odometría ahora: el bridge o el controlador? ¿Por qué no hace falta puentearla?
3. ¿Qué pasa si el spawner se lanza antes de que exista el `controller_manager`?

## Sobre el `prefix`

Los joints del bloque `<ros2_control>` van **sin** `${prefix}`, igual que en el resto del URDF
(ejercicio 1): el prefijo es para los frames, y los frames son los links. Gracias a eso,
`controllers.yaml` nombra `left_wheel_joint` y `right_wheel_joint` a secas y vale para cualquier
robot. Cada robot tiene su propio `controller_manager` en su namespace
(`/robot_a/controller_manager`), así que no hay dos `left_wheel_joint` en el mismo sitio.

Si el prefijo fuera también en los joints, `prefix:=robot_a/` dejaría al controlador buscando
`left_wheel_joint` en un robot que solo tiene `robot_a/left_wheel_joint`, y no se activaría.

La barra del prefijo tampoco es capricho: con namespace, este controlador publica su TF como
`robot_a/odom → robot_a/base_footprint`. Se ve en el ejercicio 6.

## Errores típicos

| Síntoma | Causa |
|---|---|
| `Controller manager not available` | El plugin no se cargó: revisar `GZ_SIM_SYSTEM_PLUGIN_PATH` y el nombre del filename |
| El controlador carga pero el robot no se mueve | Está en `inactive`, o se publica en el `cmd_vel` equivocado |
| El teleop no mueve el robot y el controlador está `active` | Falta `-p stamped:=true` (o está fuera de `--ros-args`): en Jazzy el controlador solo acepta `TwistStamped` |
| El robot gira sobre sí mismo | Ruedas intercambiadas en `controllers.yaml` o signo de `reflect` al revés |
