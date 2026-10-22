# Guía del alumno

Esta es la puerta de entrada. El material de trabajo son los README de cada ejercicio, en
`exercises/`.

## El taller, de un vistazo

Construye un robot desde cero, hazlo funcionar en Gazebo a mano y después repite lo mismo con tres
plugins de la GUI de Gazebo. Al final, mira cómo funcionan robots industriales reales con el mismo
flujo.

1. **A mano, ejercicios 1 a 5.**
   - Dibuja `mini_bot` en xacro: una caja, dos ruedas y una rueda loca.
   - Mételo en Gazebo con un launch.
   - Añádele un LiDAR y una cámara.
   - Conéctalos a ROS 2 con un puente.
   - Condúcelo con ros2_control.
   - Apunta el tiempo.
2. **Con la suite, ejercicios 6 a 8.** Haz lo mismo con el *Model Importer*, el *Bridge Manager* y
   el *ROS 2 Control Manager*, y con tres robots a la vez. Apunta de nuevo el tiempo.
3. **Robots reales, ejercicio 9.** Demostración: un RB-Summit de Robotnik importado con el mismo
   flujo.
4. **Reto por parejas** (`exercises/challenge/`) y cierre.

Al terminar antes de tiempo, prueba los tres **extras** opcionales de `exercises/extra_*`: aparcar el robot
en una zona marcada, añadir un sensor y montar tres robots a mano con launch files.

## Prepara el entorno

**Requisitos:** Linux con Docker y git. En macOS o Windows, Docker Desktop (ver el paso 4). Unos
10 GB libres en disco.

1. **Comprueba que Docker funciona sin `sudo`.** En una terminal de tu máquina:

   ```bash
   docker run --rm hello-world
   ```

   Tiene que salir `Hello from Docker!`. Si sale `permission denied`, añade tu usuario al grupo
   `docker` (`sudo usermod -aG docker $USER`), cierra sesión y vuelve a entrar.

2. **Clona el repositorio del taller**, por ejemplo en tu carpeta de inicio:

   ```bash
   cd ~
   git clone https://github.com/asoriano1/roscon-vlc-gz-workshop.git
   cd roscon-vlc-gz-workshop
   ```

   A partir de aquí, **"la raíz del repo"** es esta carpeta, `~/roscon-vlc-gz-workshop`.
   Lanza todos los `./setup/...` desde ella.

3. **Consigue la imagen.** Pesa varios GB. Elige una de las dos vías:

   - **Desde internet:**

     ```bash
     docker pull ghcr.io/asoriano1/roscon-workshop:latest
     ```

   - **Desde un USB**, solo en portátiles **amd64** (Intel o AMD). La Wi-Fi de la sala no da para
     que todos descarguen la imagen a la vez, así que habrá varios USB circulando con ella.

     Comprueba primero la arquitectura con `uname -m`: tiene que salir `x86_64`. Si sale `arm64`
     o `aarch64` (por ejemplo, un Mac con Apple Silicon), la imagen del USB no sirve: usa
     `docker pull`.

     Busca dónde se ha montado el USB (en Ubuntu, en `/media/<tu usuario>/`), copia el fichero a
     tu disco y devuelve el USB en cuanto termine la copia:

     ```bash
     ls /media/$USER/
     cp /media/$USER/NOMBRE_DEL_USB/roscon-workshop.tar.gz ~/
     ```

     Cárgalo en Docker:

     ```bash
     docker load -i ~/roscon-workshop.tar.gz
     ```

     Al terminar, `docker load` escribe `Loaded image: ghcr.io/asoriano1/roscon-workshop:latest`.
     Después, borra la copia para liberar espacio: `rm ~/roscon-workshop.tar.gz`.

4. **Arranca el contenedor**, desde la raíz del repo:

   ```bash
   ./setup/run.sh          # Linux
   ./setup/run_novnc.sh    # macOS, Windows, o si run.sh no abre ventanas
   ```

   El prompt cambia a `root@…:/workshop#`: la terminal ya está **dentro del contenedor**. Con
   `run_novnc.sh`, las ventanas se ven en el navegador, en http://localhost:6080/vnc.html.
   Esta es tu **terminal 1**.

5. **Comprueba el entorno**, dentro del contenedor:

   ```bash
   check_setup.sh
   ```

   La última línea tiene que ser `CÓDIGO: OK-JAZZY-HARMONIC-SUITE`. Si sale `FALTA-ALGO`, revisa
   las líneas con `FALTA`. Con el código OK, pon el post-it verde.

6. **Comprueba que Gazebo abre ventana**, dentro del contenedor:

   ```bash
   gz sim workshop.sdf
   ```

   Tiene que aparecer el mundo del taller: una pared, dos cajas, un cilindro y el panel de
   Robotnik. Después, cierra Gazebo.

7. **Abre tu editor** en la carpeta `mini_bot/` del repo, **en tu máquina**. Edita solo
   ahí.
8. **Abre el enunciado del ejercicio 1**: `exercises/ex01_geometria/README.md`, en el editor o en
   GitHub.

Si algún paso falla, pon el post-it rojo y trabaja en el portátil de tu pareja mientras tanto.

## Cómo trabajar

- **Edita en tu máquina**, con tu editor de siempre, los ficheros de `mini_bot/` del repo. Los
  cambios se ven dentro del contenedor al momento, sin recompilar.
- **Dentro del contenedor, `mini_bot` está en `$WS/src/mini_bot`** (`/workshop_ws/src/mini_bot`),
  no en `/workshop`, que es donde arranca el prompt. `/workshop` solo tiene `exercises/`, `docs/`
  y `broken/`, para consulta. Compruébalo con `ls $WS/src/mini_bot`.
- **Ejecuta en el contenedor**: `ros2 launch`, `gz`, `colcon`. Las terminales ya salen con ROS 2
  cargado.
- **Cuando un ejercicio diga "en otra terminal"**, abre otra terminal de tu máquina, ve a la raíz
  del repo y lanza `./setup/shell.sh`. Entra en el mismo contenedor.
- **¿Contenedor o máquina?** Si el prompt empieza por `root@` y acaba en `/workshop#` o similar,
  es el contenedor. Si sale tu usuario, es tu máquina, y ahí no hay ROS 2.
- Al cerrar el contenedor, tus ficheros siguen en tu disco.

## Reglas

- **Por parejas.** Tu compañero es tu primer soporte técnico.
- **Regla de los 3 minutos.** Tres minutos atascado → copia la solución y sigue. Están en
  `mini_bot/solutions/exNN/`. Cada ejercicio necesita el anterior funcionando.
- **Semáforo.** Pon el post-it verde en la pantalla al terminar un paso, y el rojo ante un atasco.
- **No maximices Gazebo.** Sin tarjeta gráfica, una ventana grande lo hace todo más lento.

## Rendimiento

Sin tarjeta gráfica, Gazebo irá algo lento y los sensores publicarán un poco por debajo de lo
anunciado. Es normal: no intentes arreglarlo. Con los robots de Robotnik irá muy lento, y también
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
| **bridge** | `ros_gz_bridge`: copia topics de Gazebo a ROS 2 (o al revés), uno a uno, solo los que le pidas. |
| **RTF** | *Real Time Factor*: lo rápido que va la simulación respecto al reloj de verdad. 0,7 = al 70 %. Aparece abajo a la derecha en Gazebo. |
| **/clock y use_sim_time** | El reloj de la simulación, y la opción que hace que un nodo lo use en vez de la hora del ordenador. |
| **ros2_control** | El marco que separa el hardware (aquí, Gazebo) de los controladores que lo mueven. |
| **controller_manager** | El nodo que carga, activa y ejecuta los controladores. |
| **namespace** | Prefijo de los topics y nodos de ROS 2 de un robot: `/robot_a/scan`. |
| **prefijo de frames** | Prefijo de los nombres de los links (los frames de TF), para que dos robots no se pisen: `robot_a/base_link`. Con barra, como espera ros2_control. Los joints no lo llevan. |
| **nombre del modelo** | Cómo se llama el robot dentro de Gazebo. No puede repetirse en el mismo mundo. |

## Si algo no funciona

| Síntoma | Prueba esto |
|---|---|
| Un robot importado no hace nada | La simulación se queda en pausa después de importar: pulsa ▶ abajo a la izquierda en Gazebo |
| El teleop no mueve el robot | Comprueba que está el `-p stamped:=true` y que la ventana del teleop tiene el foco |
| `ros2 topic hz` da menos de lo que pone en el URDF | Es normal: frecuencia real = la del URDF × RTF |
| Un comando se queda esperando sin hacer nada | Pulsa Ctrl+C en todas las terminales y vuelve a lanzar. Si sigue, `exit` y `./setup/run.sh` |
| "Command not found", o ROS 2 no encuentra el paquete | Esa terminal no es del contenedor: abre otra con `./setup/shell.sh` |
| `./setup/run.sh: No such file or directory` | La terminal no está en la raíz del repo: `cd ~/roscon-vlc-gz-workshop` |
| `run.sh` arranca, pero Gazebo no abre ventana | Sal con `exit` y usa `./setup/run_novnc.sh` (Gazebo en el navegador) |
| `docker load` falla a mitad | El fichero se copió incompleto: vuelve a copiarlo del USB |

Si nada de esto lo arregla en 3 minutos, copia la solución y pon el post-it rojo.
