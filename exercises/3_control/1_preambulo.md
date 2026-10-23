# Preámbulo 3 — ros2_control y los controladores (12 min)

**Qué haces:** activa el control de las ruedas del `mini_bot`, condúcelo con el teclado y maneja
el ciclo de vida de los controladores desde la consola: lo mismo que el Control Manager hará
después con botones.

**Punto de partida:** el preámbulo 2 terminado (o su solución copiada). El ejercicio 2 no hace
falta.

**Archivos que editas:** `mini_bot/urdf/mini_bot.urdf.xacro` (PASO 11) y
`mini_bot/launch/sim.launch.py` (PASO 12)
**Ya viene hecho:** `mini_bot/config/controllers.yaml`
**Solución:** `mini_bot/solutions/preambulo_3/`

> Qué hacen el plugin, el `controller_manager`, los spawners, el *broadcaster* y el
> `diff_drive_controller`, en detalle: [Anatomía de un robot simulado](../../docs/anatomia.md).

## 1. Activa el control (PASOS 11 y 12)

1. En el xacro, busca la sección `PREÁMBULO 3: ros2_control`, lee su comentario y activa el
   PASO 11: borra las dos líneas marcadas.
2. Abre `mini_bot/config/controllers.yaml` y léelo: declara los dos controladores y da los
   parámetros del diferencial (separación y radio de las ruedas).
3. En `sim.launch.py`, lee el bloque del PASO 12 y descomenta sus dos líneas en la lista del final:
   `jsb_spawner` y `diff_spawner`.
4. Ctrl+C y vuelve a lanzar:

   ```bash
   ros2 launch mini_bot sim.launch.py
   ```

## 2. Comprueba y conduce

En otra terminal:

```bash
ros2 control list_controllers            # los dos, active
ros2 control list_hardware_interfaces    # velocidad de cada rueda: [claimed]
```

Conduce, desde otra terminal (`./setup/shell.sh`). El robot se mueve con las teclas `i`, `j`,
`l`, `,` y `k` (parar), con el foco en esa terminal:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -p stamped:=true -r cmd_vel:=/diff_drive_controller/cmd_vel
```

En RViz, las ruedas giran: ahora `/joint_states` lo publica `joint_state_broadcaster`.

## 3. El ciclo de vida de un controlador

Un controlador pasa por estados: `unconfigured` → `inactive` → `active`. Los spawners del launch
hacen todo el recorrido de golpe. Hazlo a mano, con el teleop abierto:

```bash
ros2 control set_controller_state diff_drive_controller inactive
ros2 control list_controllers            # diff_drive_controller: inactive
```

Prueba a conducir: el robot no se mueve. El controlador sigue cargado, pero no manda.

```bash
ros2 control set_controller_state diff_drive_controller active
```

Y vuelve a moverse. Esto es lo que el Control Manager hace con botones, en el post-ejercicio 3.

## La odometría no es la verdad

`/diff_drive_controller/odom` no sabe dónde está el robot: lo calcula contando vueltas de rueda.
Compárala con la pose real que da Gazebo, después de dar unas vueltas:

```bash
ros2 topic echo /diff_drive_controller/odom --once --field pose.pose.position
gz model -m mini_bot -p
```

## Preguntas

1. ¿Qué diferencia hay entre una `command_interface` y una `state_interface`?
2. ¿Quién publica la odometría: el bridge o el controlador? ¿Por qué no hace falta puentearla?
3. ¿Qué diferencia hay entre desactivar un controlador y descargarlo?
4. Los joints del bloque `<ros2_control>` no llevan `${prefix}`. ¿Por qué?

## Errores típicos

| Síntoma | Causa |
|---|---|
| `Controller manager not available` | Falta el PASO 11, o solo se ha borrado una de sus dos líneas |
| Los spawners no hacen nada | Falta el PASO 12: `jsb_spawner` y `diff_spawner` en la lista del launch |
| El teleop no mueve el robot y el controlador está `active` | Falta `-p stamped:=true`, o la ventana del teleop no tiene el foco |
| El controlador carga pero el robot no se mueve | Está en `inactive`: `ros2 control list_controllers` |
