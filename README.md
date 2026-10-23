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
| `/workshop_ws` (`$WS`) | Donde arranca el prompt. El workspace de ROS 2: aquí se compila (`colcon build`). Tu `mini_bot` está en `src/mini_bot` |
| `/workshop` | `exercises/` y `docs/`, para consulta |

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

En `mini_bot/urdf/mini_bot.urdf.xacro` está el robot entero, escrito y comentado por pasos que se
activan a lo largo del taller. En `mini_bot/solutions/`, la solución de cada preámbulo y cada
ejercicio.

## Programa

Tres secciones con la misma forma:

1. **Preámbulo:** lo básico, ya escrito y comentado. Léelo, actívalo paso a paso y entiende qué
   hace cada pieza.
2. **Ejercicio:** un problema de verdad, resuelto a mano con launch files y configuración.
3. **Post-ejercicio:** el mismo problema, resuelto con un plugin de la suite.

| Hora | Bloque | Material |
|---|---|---|
| 0:00–0:10 | Presentación y preparación del entorno | |
| 0:10–0:20 | Anatomía de un robot simulado | [anatomía](docs/anatomia.md) |
| 0:20–0:35 | **1. Spawn.** Preámbulo: un robot en Gazebo | [preámbulo 1](exercises/1_spawn/1_preambulo.md) |
| 0:35–0:50 | Ejercicio 1: tres robots en el almacén | [ejercicio 1](exercises/1_spawn/2_ejercicio.md) |
| 0:50–1:10 | Post-ejercicio 1: robots de Robotnik con el Model Importer | [post-ejercicio 1](exercises/1_spawn/3_post_ejercicio.md) |
| 1:10–1:20 | Descanso | |
| 1:20–1:32 | **2. Sensores.** Preámbulo: sensores y puente | [preámbulo 2](exercises/2_sensores/1_preambulo.md) |
| 1:32–1:52 | Ejercicio 2: dos sensores más | [ejercicio 2](exercises/2_sensores/2_ejercicio.md) |
| 1:52–2:05 | Post-ejercicio 2: Bridge Manager | [post-ejercicio 2](exercises/2_sensores/3_post_ejercicio.md) |
| 2:05–2:17 | **3. Control.** Preámbulo: ros2_control | [preámbulo 3](exercises/3_control/1_preambulo.md) |
| 2:17–2:37 | Ejercicio 3: el control del mástil | [ejercicio 3](exercises/3_control/2_ejercicio.md) |
| 2:37–2:52 | Post-ejercicio 3: todo con la suite | [post-ejercicio 3](exercises/3_control/3_post_ejercicio.md) |
| 2:52–3:00 | Cierre | |

**Extra opcional**, fuera del horario: [robots de Robotnik](exercises/extra_robotnik/), robots
reales con mallas y sensores completos, con el mismo flujo de la suite.

Qué hace cada pieza (xacro, `robot_state_publisher`, `create`, bridge, ros2_control, controladores):
[docs/anatomia.md](docs/anatomia.md).

## Estructura del repo

| Carpeta | Contenido |
|---|---|
| `mini_bot/` | El paquete ROS 2 del taller: los robots (`mini_bot` y `mast_bot`), launch, configs, mundos y soluciones |
| `exercises/` | Una carpeta por sección, con su preámbulo, su ejercicio y su post-ejercicio |
| `setup/` | Dockerfile, scripts de arranque, instalación nativa y `check_setup.sh` |
| `docs/` | Guía del alumno y anatomía de un robot simulado |

## Licencia

Apache-2.0.

Ángel Soriano — [Robotnik Automation](https://robotnik.es)
