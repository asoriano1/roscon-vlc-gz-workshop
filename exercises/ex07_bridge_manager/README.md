# Ejercicio 7 — Bridge Manager (12 min)

**Punto de partida:** los tres `mini_bot` del ejercicio 6 en el mundo.

## Pasos

1. Abrir el panel **ROS 2 Bridge Manager** y pulsar **Refresh**.
2. Los topics aparecen agrupados por modelo. Marcar el LiDAR y la cámara de `robot_a` y `robot_b`.
3. Desplegar **Bridge command** y **leerlo antes de lanzarlo**.
4. **Run**, y a RViz.

## La comparación

Abrir a la vez el `config/bridge.yaml` del ejercicio 4 y el comando que acaba de generar el panel.
Son la misma información. La diferencia es que uno se escribió a mano mirando `gz topic -l`,
y el otro ha salido de recorrer el mundo.

Ahora, la cuenta: cuánto costaría escribir a mano el YAML de tres robots con dos sensores cada uno.

## Preguntas

1. ¿Qué topics de Gazebo no aparecen como puenteables y por qué?
2. Al añadir un sensor más, ¿reinicia el puente o lanza otro proceso?
3. ¿Los topics de ROS salen con el namespace de cada robot? Comprobarlo con `ros2 topic list`.

> Si en la tercera los topics salen sin el namespace del robot, conviene comentarlo en voz alta:
> es información útil para la suite.

## Micro-reto

Uno de los robots tiene un sensor sin puentear. Encontrarlo desde el panel, sin usar la terminal.
