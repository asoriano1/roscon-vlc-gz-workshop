# Del xacro al robot que conduce — Taller de 3 h

Taller de ROSCon Valencia. Se construye un robot desde cero en URDF, se hace funcionar en Gazebo
a mano y después se repite lo mismo con la **Gazebo ROS 2 Model Runtime Suite**: tres plugins de
GUI que permiten importar, puentear y controlar robots sin salir de Gazebo.

- [Model Importer](https://github.com/asoriano1/gz_model_importer_plugin) — importa URDF, XACRO y SDF con preview y spawn.
- [Bridge Manager](https://github.com/asoriano1/gz_ros2_bridge_manager) — descubre topics de sensores y lanza `ros_gz_bridge`.
- [ROS 2 Control Manager](https://github.com/asoriano1/gz_ros2_control_manager) — descubre controller managers y carga, configura y activa controladores.

Entorno: **ROS 2 Jazzy + Gazebo Harmonic**. Al final se usan robots reales de
[`robotnik_description`](https://github.com/RobotnikAutomation/robotnik_description).

---

## Antes del taller (en casa, no en la sala)

La Wi-Fi de un congreso no da para 25 descargas de varios GB.

Los pasos, uno a uno y con lo que debe verse en cada uno, están en la
[guía del alumno](docs/guia_alumno.md), "Antes del taller, en casa". Allí también: qué se hace y
en qué orden, cómo se trabaja con el contenedor, las reglas de la sala y qué hacer si algo no
funciona. Aquí, el resumen.

### Opción A — Docker (recomendada)

```bash
git clone https://github.com/asoriano1/roscon-vlc-gz-workshop.git
cd roscon-vlc-gz-workshop
docker pull ghcr.io/asoriano1/roscon-workshop:latest
./setup/run.sh                 # Linux con X11
./setup/run_novnc.sh           # macOS, Windows o si X11 falla → http://localhost:6080
```

Dentro del contenedor:

```bash
check_setup.sh                 # debe terminar en CÓDIGO: OK-JAZZY-HARMONIC-SUITE
```

**Se edita en la máquina propia; el contenedor solo ejecuta.** La carpeta `mini_bot/` del repo se
monta dentro del contenedor (en `/workshop_ws/src/mini_bot`): los ficheros se abren con el editor
de siempre y los cambios se ven dentro al momento, sin recompilar. Como viven en el disco propio,
no se pierden al cerrar el contenedor.

**Otra terminal dentro del contenedor:** `./setup/shell.sh` desde la raíz del repo. Sale con
ROS 2 y el workspace ya cargados. `tmux` también está en la imagen.

### Opción B — Instalación nativa

Ubuntu 24.04 con Jazzy ya instalado: [setup/native_install.md](setup/native_install.md).

### Si nada funciona

Conviene venir igualmente: se trabaja por parejas y habrá un USB con la imagen en la sala.

---

## El robot del taller: `mini_bot`

Una caja con dos ruedas, una rueda loca, un LiDAR de 180 muestras a 5 Hz y una cámara de
320 × 240 a 10 Hz. Sin mallas y con sensores baratos a propósito: así la simulación va fluida
en un portátil sin GPU, y toda la atención queda en el flujo de trabajo, no en los polígonos.

Se construye por capas. En `mini_bot/urdf/mini_bot.urdf.xacro` está el esqueleto con los nombres
de links y joints ya puestos, y en `mini_bot/solutions/exNN/`, la solución de cada ejercicio.

## Programa

| Hora | Bloque | Ejercicio |
|---|---|---|
| 0:00–0:10 | Presentación y comprobación de entorno | |
| 0:10–0:25 | Anatomía de un robot simulado | [anatomía](docs/anatomia.md) |
| 0:25–0:40 | Geometría del mini_bot | [ex01](exercises/ex01_geometria/) |
| 0:40–0:52 | Launch y primer spawn | [ex02](exercises/ex02_gazebo_launch/) |
| 0:52–1:04 | Sensores en el URDF | [ex03](exercises/ex03_sensores/) |
| 1:04–1:14 | Descanso | |
| 1:14–1:29 | El puente, a mano | [ex04](exercises/ex04_bridge/) |
| 1:29–1:44 | ros2_control y controladores | [ex05](exercises/ex05_control/) |
| 1:44–1:56 | Model Importer | [ex06](exercises/ex06_importer/) |
| 1:56–2:08 | Bridge Manager | [ex07](exercises/ex07_bridge_manager/) |
| 2:08–2:20 | Control Manager | [ex08](exercises/ex08_control_manager/) |
| 2:20–2:35 | Robots de Robotnik | [ex09](exercises/ex09_robotnik/) |
| 2:35–2:50 | Reto por parejas | [challenge](exercises/challenge/) |
| 2:50–3:00 | Cierre | |

**Extras opcionales**, para quien termine antes. Cada uno hace lo mismo a mano y con la suite:

- [Aparcar en la zona](exercises/extra_zona/): dejar el robot en una zona marcada, primero
  adivinando coordenadas desde la consola y después arrastrándolo con el ratón en el importer.
- [Un sensor más](exercises/extra_sensor/): añadir una IMU y llevarla a ROS 2, con el
  `bridge.yaml` y con el Bridge Manager.
- [Multi-robot a mano](exercises/extra_multirobot/): tres robots desde launch files, con sus
  namespaces, prefijos y controladores.

Qué hace cada pieza (xacro, `robot_state_publisher`, `create`, bridge, ros2_control, controladores):
[docs/anatomia.md](docs/anatomia.md).

## Estructura del repo

| Carpeta | Contenido |
|---|---|
| `mini_bot/` | El paquete ROS 2 del taller: esqueleto, soluciones por ejercicio, launch, configs y mundos |
| `exercises/` | Un README por ejercicio, con pasos, comprobaciones y errores típicos |
| `setup/` | Dockerfile, scripts de arranque, instalación nativa y `check_setup.sh` |
| `broken/` | Modelos rotos a propósito para los micro-retos |
| `docs/` | Guía del alumno y anatomía de un robot simulado |

## Licencia

Apache-2.0.

Ángel Soriano — [Robotnik Automation](https://robotnik.es)
