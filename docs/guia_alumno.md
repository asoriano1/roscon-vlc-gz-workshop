# Guía del alumno

Esta es la puerta de entrada. El material de trabajo son los README de cada ejercicio, en
`exercises/`.

## Qué se hace en el taller

Se construye un robot desde cero, se hace funcionar en Gazebo a mano y después se repite lo mismo
con tres plugins de la GUI de Gazebo. Al final se ven robots industriales reales con el mismo flujo.

1. **A mano, ejercicios 1 a 5.**
   - Dibujar `mini_bot` en xacro: una caja, dos ruedas y una rueda loca.
   - Meterlo en Gazebo con un launch.
   - Añadirle un LiDAR y una cámara.
   - Conectarlos a ROS 2 con un puente.
   - Conducirlo con ros2_control.
   - Apuntar el tiempo empleado.
2. **Con la suite, ejercicios 6 a 8.** Lo mismo con el *Model Importer*, el *Bridge Manager* y el
   *ROS 2 Control Manager*, y con tres robots a la vez. Apuntar de nuevo el tiempo.
3. **Robots reales, ejercicio 9.** Demostración: un RB-Summit de Robotnik importado con el mismo
   flujo.
4. **Reto por parejas** (`exercises/challenge/`) y cierre.

Para quien termine antes hay tres **extras** opcionales en `exercises/extra_*`: aparcar el robot
en una zona marcada, añadir un sensor y montar tres robots a mano con launch files.

## Antes del taller, en casa

La Wi-Fi de la sala no da para que todos descarguen la imagen a la vez. Estos pasos se hacen en
casa, y hay que llegar al último.

**Requisitos:** Linux con Docker y git. macOS o Windows también valen, con Docker Desktop (ver el
paso 4). Unos 10 GB libres en disco.

1. **Comprobar que Docker funciona sin `sudo`.** En una terminal de la máquina propia:

   ```bash
   docker run --rm hello-world
   ```

   Tiene que salir `Hello from Docker!`. Si sale `permission denied`, hay que añadir el usuario al
   grupo `docker` (`sudo usermod -aG docker $USER`), cerrar sesión y volver a entrar.

2. **Clonar el repositorio del taller**, por ejemplo en la carpeta de inicio:

   ```bash
   cd ~
   git clone https://github.com/asoriano1/roscon-vlc-gz-workshop.git
   cd roscon-vlc-gz-workshop
   ```

   A partir de aquí, **"la raíz del repo"** es esta carpeta, `~/roscon-vlc-gz-workshop`.
   Todos los `./setup/...` se lanzan desde ella.

3. **Descargar la imagen** (varios GB; tarda):

   ```bash
   docker pull ghcr.io/asoriano1/roscon-workshop:latest
   ```

4. **Arrancar el contenedor**, desde la raíz del repo:

   ```bash
   ./setup/run.sh          # Linux
   ./setup/run_novnc.sh    # macOS, Windows, o si run.sh no abre ventanas
   ```

   El prompt cambia a `root@…:/workshop#`: la terminal ya está **dentro del contenedor**. Con
   `run_novnc.sh`, las ventanas se ven en el navegador, en http://localhost:6080/vnc.html.

5. **Comprobar el entorno**, dentro del contenedor:

   ```bash
   check_setup.sh
   ```

   La última línea tiene que ser `CÓDIGO: OK-JAZZY-HARMONIC-SUITE`. Si sale `FALTA-ALGO`, las
   líneas con `FALTA` dicen qué falta.

6. **Comprobar que Gazebo abre ventana**, dentro del contenedor:

   ```bash
   gz sim workshop.sdf
   ```

   Tiene que aparecer el mundo del taller: una pared, dos cajas, un cilindro y el panel de
   Robotnik. Después, cerrar Gazebo y salir del contenedor con `exit`.

Si algún paso falla, conviene venir igualmente: se trabaja por parejas y habrá un USB con la
imagen.

## En la sala, al empezar

1. Abrir una terminal de la máquina propia e ir a la raíz del repo:

   ```bash
   cd ~/roscon-vlc-gz-workshop
   git pull                # por si hay cambios de última hora
   ```

2. Arrancar el contenedor: `./setup/run.sh` (o `./setup/run_novnc.sh`). Esta es la **terminal 1**.
3. Dentro, `check_setup.sh`. Con el código OK, post-it verde.
4. Abrir el editor en la carpeta `mini_bot/` del repo, **en la máquina propia**. Es lo único que
   se edita.
5. Abrir el enunciado del ejercicio 1: `exercises/ex01_geometria/README.md`, en el editor o en
   GitHub.

## Cómo se trabaja

- **Se edita en la máquina propia**, con el editor de siempre, en los ficheros de `mini_bot/` del
  repo. Los cambios se ven dentro del contenedor al momento, sin recompilar.
- **Se ejecuta en el contenedor**: `ros2 launch`, `gz`, `colcon`. Las terminales ya salen con ROS 2
  cargado.
- **Cuando un ejercicio dice "en otra terminal"**: abrir otra terminal de la máquina propia, ir a
  la raíz del repo y lanzar `./setup/shell.sh`. Entra en el mismo contenedor.
- **¿Contenedor o máquina propia?** Si el prompt empieza por `root@` y acaba en `/workshop#` o
  similar, es el contenedor. Si sale el usuario propio, es la máquina: ahí no hay ROS 2.
- Al cerrar el contenedor, los ficheros siguen en el disco.

## Reglas

- **Por parejas.** El compañero es el primer soporte técnico.
- **Regla de los 3 minutos.** Tres minutos atascado → copiar la solución y seguir. Están en
  `mini_bot/solutions/exNN/`. Cada ejercicio necesita el anterior funcionando.
- **Semáforo.** Post-it verde en la pantalla al terminar un paso; rojo si hay un atasco.
- **No maximizar Gazebo.** Sin tarjeta gráfica, una ventana grande lo hace todo más lento.

## Rendimiento

Sin tarjeta gráfica, Gazebo irá algo lento y los sensores publicarán un poco por debajo de lo
anunciado. Es normal y no hay que arreglarlo. Con los robots de Robotnik irá muy lento, y también
es normal.

## Glosario

Qué hace cada pieza de un robot simulado y cómo se hablan entre ellas, en detalle:
[Anatomía de un robot simulado](anatomia.md). Aquí, la versión corta.

| Término | Qué es |
|---|---|
| **URDF** | El formato de ROS para describir un robot: piezas (*links*) unidas por articulaciones (*joints*). |
| **xacro** | URDF con variables y macros. Se convierte en URDF normal antes de usarlo. |
| **SDF** | El formato de Gazebo. Describe mundos enteros, no solo robots. Gazebo convierte el URDF a SDF. |
| **world** | El escenario de Gazebo: suelo, luz, obstáculos y física. El del taller es `workshop.sdf`. |
| **spawn** | Meter un robot en un mundo que ya está corriendo. |
| **TF** | El sistema de ROS 2 que sabe dónde está cada pieza respecto a las demás. Cada pieza es un *frame*. |
| **topic** | Un canal con nombre por el que se publican mensajes. Gazebo y ROS 2 tienen los suyos, por separado. |
| **bridge** | `ros_gz_bridge`: copia topics de Gazebo a ROS 2 (o al revés), uno a uno, solo los que se le piden. |
| **RTF** | *Real Time Factor*: lo rápido que va la simulación respecto al reloj de verdad. 0,7 = al 70 %. Aparece abajo a la derecha en Gazebo. |
| **/clock y use_sim_time** | El reloj de la simulación, y la opción que hace que un nodo lo use en vez de la hora del ordenador. |
| **ros2_control** | El marco que separa el hardware (aquí, Gazebo) de los controladores que lo mueven. |
| **controller_manager** | El nodo que carga, activa y ejecuta los controladores. |
| **namespace** | Prefijo de los topics y nodos de ROS 2 de un robot: `/robot_a/scan`. |
| **prefijo de frames** | Prefijo de los nombres de los links (los frames de TF), para que dos robots no se pisen: `robot_a/base_link`. Con barra, como espera ros2_control. Los joints no lo llevan. |
| **nombre del modelo** | Cómo se llama el robot dentro de Gazebo. No puede repetirse en el mismo mundo. |

## Si algo no funciona

| Síntoma | Qué probar |
|---|---|
| Un robot importado no hace nada | La simulación se queda en pausa después de importar: pulsar ▶ abajo a la izquierda en Gazebo |
| El teleop no mueve el robot | ¿Está el `-p stamped:=true`? ¿Tiene el foco la ventana del teleop? |
| `ros2 topic hz` da menos de lo que pone en el URDF | Es normal: frecuencia real = la del URDF × RTF |
| Un comando se queda esperando sin hacer nada | Ctrl+C en todas las terminales y volver a lanzar. Si sigue, `exit` y `./setup/run.sh` |
| "Command not found", o ROS 2 no encuentra el paquete | Esa terminal no es del contenedor: abrir otra con `./setup/shell.sh` |
| `./setup/run.sh: No such file or directory` | La terminal no está en la raíz del repo: `cd ~/roscon-vlc-gz-workshop` |
| `run.sh` arranca, pero Gazebo no abre ventana | Salir con `exit` y usar `./setup/run_novnc.sh` (Gazebo en el navegador) |

Si nada de esto lo arregla y han pasado 3 minutos: copiar la solución y post-it rojo.
