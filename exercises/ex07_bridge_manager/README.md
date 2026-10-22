# Ejercicio 7 — Bridge Manager (12 min)

**Punto de partida:** los tres `mini_bot` del ejercicio 6 en el mundo.

## Pasos

1. Abre el panel **ROS 2 Bridge Manager** y pulsa **Refresh**.
2. Los topics aparecen agrupados por modelo. Marca el LiDAR y la cámara de `robot_a` y `robot_b`.
3. Despliega **Bridge command** y **léelo antes de lanzarlo**.
4. Pulsa **Run** y abre RViz.

## La comparación

Abre a la vez el `config/bridge.yaml` del ejercicio 4 y el comando que acaba de generar el panel.
Son la misma información. La diferencia es que uno lo escribiste a mano mirando `gz topic -l`,
y el otro ha salido de recorrer el mundo.

Ahora echa la cuenta: cuánto costaría escribir a mano el YAML de tres robots con dos sensores cada uno.

## Preguntas

1. ¿Qué topics de Gazebo no aparecen como puenteables y por qué?
2. Al añadir un sensor más, ¿reinicia el puente o lanza otro proceso?
3. ¿Los topics de ROS salen con el namespace de cada robot? Compruébalo con `ros2 topic list`.

> Si en la tercera los topics salen sin el namespace del robot, dilo en voz alta: es información
> útil para la suite.

## Micro-reto

Uno de los robots tiene un sensor sin puentear. Encuéntralo desde el panel, sin usar la terminal.
