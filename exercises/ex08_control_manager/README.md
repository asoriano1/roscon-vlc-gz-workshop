# Ejercicio 8 — ROS 2 Control Manager (12 min)

**Punto de partida:** el ejercicio 7, con el puente en marcha.

## Pasos

1. Abre el panel **ROS 2 Control Manager** y pulsa **Refresh**. Debe haber un `controller_manager` por robot.
2. Activa el modo **Debug** y revisa los componentes hardware y sus interfaces.
3. En `robot_a`, carga, configura y activa `joint_state_broadcaster` y `diff_drive_controller`.
   Observa cómo cambia el estado: `unconfigured` → `inactive` → `active`.
4. Repite con `robot_b`.
5. Conduce los dos a la vez, cada uno desde una terminal (lanza `./setup/shell.sh` en tu máquina, desde la raíz del repo, una vez por robot):

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -p stamped:=true -r cmd_vel:=/robot_a/diff_drive_controller/cmd_vel
```

## La comparación

En el ejercicio 5 bastaron dos spawners en el launch. Aquí aparece el ciclo de vida completo,
y desactivar y reactivar en caliente es un clic. Son dos usos distintos: el launch para lo que ya
está decidido, el panel para la fase de pruebas.

## Preguntas

1. ¿De dónde salen los controladores que aparecen declarados pero no cargados?
2. ¿Qué diferencia hay entre desactivar y descargar un controlador?
3. En un despliegue real sin GUI, ¿qué parte de esto acaba en un launch file?

## Micro-reto

Un robot tiene el controlador cargado pero el teleop no lo mueve. Diagnostícalo solo desde el panel.
