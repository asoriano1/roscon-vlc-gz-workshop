# Ejercicio 8 — ROS 2 Control Manager (12 min)

**Punto de partida:** el ejercicio 7, con el puente en marcha.

## Pasos

1. Abrir el panel **ROS 2 Control Manager** → **Refresh**. Debería haber un `controller_manager` por robot.
2. Activar el modo **Debug** y revisar los componentes hardware y sus interfaces.
3. Para `robot_a`: cargar, configurar y activar `joint_state_broadcaster` y `diff_drive_controller`.
   El estado cambia así: `unconfigured` → `inactive` → `active`.
4. Lo mismo con `robot_b`.
5. Conducir los dos a la vez, cada uno desde una terminal (`./setup/shell.sh` en la máquina propia, desde la raíz del repo, una vez por robot):

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -p stamped:=true -r cmd_vel:=/robot_a/diff_drive_controller/cmd_vel
```

## La comparación

En el ejercicio 5 bastaron dos spawners en el launch. Aquí se ve el ciclo de vida completo
y se puede desactivar y reactivar en caliente. Son dos usos distintos: el launch para lo que ya
se sabe que se quiere, el panel para la fase de pruebas.

## Preguntas

1. ¿De dónde salen los controladores que aparecen declarados pero no cargados?
2. ¿Qué diferencia hay entre desactivar y descargar un controlador?
3. En un despliegue real sin GUI, ¿qué parte de esto acaba en un launch file?

## Micro-reto

Un robot tiene el controlador cargado pero el teleop no lo mueve. Diagnosticarlo solo desde el panel.
