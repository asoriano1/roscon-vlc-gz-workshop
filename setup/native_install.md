# Instalación nativa (Ubuntu 24.04 + ROS 2 Jazzy)

**La vía probada es Docker.** Esto es para quien ya tenga Jazzy y Gazebo Harmonic (`gz sim --versions`
→ 8.x) y sepa lo que hace: en la sala no habrá tiempo para depurar instalaciones.

```bash
# 1. Dependencias y el repo del taller
sudo apt install -y ros-jazzy-ros-gz ros-jazzy-gz-ros2-control ros-jazzy-ros2-controllers \
  ros-jazzy-ros2controlcli ros-jazzy-xacro ros-jazzy-teleop-twist-keyboard ros-jazzy-rqt-graph \
  ros-jazzy-rqt-tf-tree python3-colcon-common-extensions
git clone https://github.com/asoriano1/roscon-vlc-gz-workshop.git ~/roscon-vlc-gz-workshop
REPO=~/roscon-vlc-gz-workshop

# 2. Workspace: los cinco paquetes de la suite y Robotnik, y mini_bot enlazado desde el repo
export WS=~/workshop_ws
mkdir -p $WS/src && cd $WS/src
git clone https://github.com/asoriano1/gz_model_importer_plugin.git
git clone https://github.com/asoriano1/gz_ros2_bridge_manager.git
git clone https://github.com/asoriano1/gz_ros2_control_manager.git
git clone -b jazzy-devel https://github.com/RobotnikAutomation/robotnik_description.git
git clone -b jazzy-devel https://github.com/RobotnikAutomation/robotnik_sensors.git
# las mismas versiones que la imagen de Docker
git -C gz_model_importer_plugin checkout -q d472d95aa2e19e87cd7eb12386191da8f8bf9b74
git -C gz_ros2_bridge_manager   checkout -q 72773a816d2211a454c2f57eab3d0fd080dfe842
git -C gz_ros2_control_manager  checkout -q e86beb511e4fc7dc989d071460a2d126f53d252b
git -C robotnik_description     checkout -q 4bc73425d090ead4591a7091e7ef7e7dc4fe862a
git -C robotnik_sensors         checkout -q 11852f4f14d6e0a561117396187f7674ed33ab2b
ln -s $REPO/mini_bot $WS/src/mini_bot
cp $REPO/setup/rbsummit/rbsummit_control.urdf.xacro \
   robotnik_description/simulators/gazebo_ignition/rbsummit/   # controlador del ejercicio 9
cd $WS && source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y && colcon build --symlink-install

# 3. Entorno en cada terminal nueva (lo que en Docker hace la imagen)
cat >> ~/.bashrc <<'EOF'
export WS=~/workshop_ws
source /opt/ros/jazzy/setup.bash && source $WS/install/setup.bash
export GZ_SIM_RESOURCE_PATH=$WS/install/mini_bot/share/mini_bot/worlds:$WS/install/robotnik_description/share:$WS/install/robotnik_sensors/share
EOF
source ~/.bashrc

# 4. La carpeta robots/ para el Browse del importer (ejercicios 6 y 9)
mkdir -p $WS/robots && ln -s $WS/src/mini_bot/urdf/mini_bot.urdf.xacro $WS/robots/
for r in rbsummit/rbsummit rbvogui/rbvogui rbtheron/rbtheron rbkairos/rbkairos_plus; do
  ln -s $WS/src/robotnik_description/robots/$r.urdf.xacro $WS/robots/; done

# 5. Comprobación: debe terminar con CÓDIGO: OK-JAZZY-HARMONIC-SUITE
$REPO/setup/check_setup.sh
```

## Lo que cambia respecto a los enunciados

Los enunciados usan `$WS`, así que los comandos valen tal cual. Solo cambia esto:

| En el enunciado | En nativo |
|---|---|
| `./setup/run.sh` | Nada: abre una terminal. |
| `./setup/shell.sh` (otra terminal) | Abre otra terminal; el `.bashrc` ya hace el `source`. |
| Editar `mini_bot/` del repo en tu máquina | Igual: `$WS/src/mini_bot` es un enlace al repo. |
