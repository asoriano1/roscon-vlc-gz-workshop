# De URDF/XACRO a ROS 2 en Gazebo Harmonic sin pasar por consola

Taller de 3 h de ROSCon Valencia. Construye un robot desde cero en URDF, hazlo funcionar en
Gazebo a mano y después repite lo mismo con la **Gazebo ROS 2 Model Runtime Suite**: tres plugins
de GUI para importar, puentear y controlar robots sin salir de Gazebo.

- [Model Importer](https://github.com/asoriano1/gz_model_importer_plugin) — importa URDF, XACRO y SDF con preview y spawn.
- [Bridge Manager](https://github.com/asoriano1/gz_ros2_bridge_manager) — descubre topics de sensores y lanza `ros_gz_bridge`.
- [ROS 2 Control Manager](https://github.com/asoriano1/gz_ros2_control_manager) — descubre controller managers y carga, configura y activa controladores.

Entorno: **ROS 2 Jazzy + Gazebo Harmonic**. Al final, robots reales de
[`robotnik_description`](https://github.com/RobotnikAutomation/robotnik_description).

---

## Prepara el entorno

Todo el taller corre en una imagen de Docker. La guía del alumno tiene los pasos uno a uno, con
lo que debe aparecer en cada uno: [docs/guia_alumno.md](docs/guia_alumno.md). Aquí, el resumen.

### 1. Clona el repositorio

```bash
git clone https://github.com/asoriano1/roscon-vlc-gz-workshop.git
cd roscon-vlc-gz-workshop
```

### 2. Consigue la imagen

**Desde internet:**

```bash
docker pull ghcr.io/asoriano1/roscon-workshop:latest
```

**Desde un USB.** Pesa varios GB y la Wi-Fi de la sala no da para que todos la descarguen a la
vez, así que en la sala habrá varios USB con la imagen.

> **La imagen del USB es solo para amd64** (portátiles con procesador Intel o AMD). Comprueba la
> arquitectura de tu máquina con `uname -m`: tiene que salir `x86_64`. Si sale `arm64` o
> `aarch64` (por ejemplo, un Mac con Apple Silicon), usa `docker pull`, que descarga la versión
> para tu arquitectura.

Con el USB conectado, busca dónde se ha montado. En Ubuntu está en `/media/<tu usuario>/`:

```bash
ls /media/$USER/
```

Copia la imagen a tu disco y devuelve el USB en cuanto termine la copia, para que pase a la
siguiente persona:

```bash
cp /media/$USER/NOMBRE_DEL_USB/roscon-workshop.tar.gz ~/
```

Cárgala en Docker:

```bash
docker load -i ~/roscon-workshop.tar.gz
```

Tiene que terminar con `Loaded image: ghcr.io/asoriano1/roscon-workshop:latest`. Después, borra la
copia para liberar espacio: `rm ~/roscon-workshop.tar.gz`.

### 3. Arranca el contenedor

Desde la raíz del repo:

```bash
./setup/run.sh                 # Linux con X11
./setup/run_novnc.sh           # macOS, Windows o si X11 falla → http://localhost:6080
```

Dentro del contenedor:

```bash
check_setup.sh                 # debe terminar en CÓDIGO: OK-JAZZY-HARMONIC-SUITE
```

**Edita en tu máquina; el contenedor solo ejecuta.** La carpeta `mini_bot/` del repo se monta
dentro del contenedor: abre los ficheros con tu editor de siempre y los cambios se ven dentro al
momento, sin recompilar. Como viven en tu disco, no se pierden al cerrar el contenedor.

Dentro del contenedor hay dos carpetas con nombre parecido:

| Carpeta | Qué hay |
|---|---|
| `/workshop` | Donde arranca el prompt: `exercises/`, `docs/` y `broken/`, para consulta |
| `/workshop_ws` (`$WS`) | El workspace de ROS 2. Tu `mini_bot` está en `$WS/src/mini_bot` |

Compruébalo con `ls $WS/src/mini_bot`: es la misma carpeta que editas en tu máquina.

**Para otra terminal dentro del contenedor**, lanza `./setup/shell.sh` desde la raíz del repo.
Sale con ROS 2 y el workspace ya cargados. `tmux` también está en la imagen.

### Sin Docker

Con Ubuntu 24.04 y Jazzy ya instalados, sigue [setup/native_install.md](setup/native_install.md).

---

## El robot del taller: `mini_bot`

Una caja con dos ruedas, una rueda loca, un LiDAR de 180 muestras a 5 Hz y una cámara de
320 × 240 a 10 Hz. Sin mallas y con sensores baratos a propósito: así la simulación va fluida
en un portátil sin GPU, y toda la atención queda en el flujo de trabajo, no en los polígonos.

Constrúyelo por capas. En `mini_bot/urdf/mini_bot.urdf.xacro` está el esqueleto con los nombres
de links y joints ya puestos, y en `mini_bot/solutions/exNN/`, la solución de cada ejercicio.

## Programa

| Hora | Bloque | Ejercicio |
|---|---|---|
| 0:00–0:10 | Presentación y preparación del entorno | |
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

**Extras opcionales**, para acabar antes de tiempo. Cada uno hace lo mismo a mano y con la suite:

- [Aparca en la zona](exercises/extra_zona/): deja el robot en una zona marcada, primero
  adivinando coordenadas desde la consola y después arrastrándolo con el ratón en el importer.
- [Un sensor más](exercises/extra_sensor/): añade una IMU y llévala a ROS 2, con el
  `bridge.yaml` y con el Bridge Manager.
- [Multi-robot a mano](exercises/extra_multirobot/): monta tres robots desde launch files, con sus
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
