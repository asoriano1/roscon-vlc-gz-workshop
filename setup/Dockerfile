# Imagen del taller: ROS 2 Jazzy + Gazebo Harmonic + Gazebo ROS 2 Model Runtime Suite
#
#   docker build -t ghcr.io/asoriano1/roscon-workshop:latest -f setup/Dockerfile .
#
# Los repos se fijan por SHA para que cualquier reconstrucción de la imagen tenga exactamente el
# mismo código que se ha probado. Para actualizar uno, cambia su SHA aquí y vuelve a probar.
# Versiones del 22-oct-2026: las mismas que la imagen validada el 9 de octubre.
FROM ros:jazzy-ros-base

ARG DEBIAN_FRONTEND=noninteractive
# main, 19-may-2026
ARG IMPORTER_REF=d472d95aa2e19e87cd7eb12386191da8f8bf9b74
ARG BRIDGE_REF=72773a816d2211a454c2f57eab3d0fd080dfe842
ARG CONTROL_REF=e86beb511e4fc7dc989d071460a2d126f53d252b
# jazzy-devel, 17-jul-2026 y 5-ago-2026
ARG DESCRIPTION_REF=4bc73425d090ead4591a7091e7ef7e7dc4fe862a
ARG SENSORS_REF=11852f4f14d6e0a561117396187f7674ed33ab2b

SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y --no-install-recommends \
      ros-jazzy-ros-gz \
      ros-jazzy-gz-ros2-control \
      ros-jazzy-ros2-controllers \
      ros-jazzy-controller-manager \
      ros-jazzy-ros2controlcli \
      ros-jazzy-robot-state-publisher \
      ros-jazzy-joint-state-publisher-gui \
      ros-jazzy-rviz2 \
      ros-jazzy-xacro \
      ros-jazzy-teleop-twist-keyboard \
      ros-jazzy-interactive-marker-twist-server \
      ros-jazzy-twist-stamper \
      ros-jazzy-rqt-graph \
      ros-jazzy-rqt-tf-tree \
      python3-colcon-common-extensions \
      git nano vim less tmux \
      mesa-utils libgl1-mesa-dri x11-apps \
      x11vnc xvfb novnc websockify supervisor \
    && rm -rf /var/lib/apt/lists/*

ENV WS=/workshop_ws
WORKDIR ${WS}/src

# git clone --branch no acepta un SHA: se trae ese commit concreto con fetch.
RUN clone() { git init -q "$1" && git -C "$1" fetch -q --depth 1 "https://github.com/$2.git" "$3" \
              && git -C "$1" checkout -q FETCH_HEAD; } \
 && clone gz_model_importer_plugin asoriano1/gz_model_importer_plugin          ${IMPORTER_REF} \
 && clone gz_ros2_bridge_manager   asoriano1/gz_ros2_bridge_manager            ${BRIDGE_REF} \
 && clone gz_ros2_control_manager  asoriano1/gz_ros2_control_manager           ${CONTROL_REF} \
 && clone robotnik_description     RobotnikAutomation/robotnik_description     ${DESCRIPTION_REF} \
 && clone robotnik_sensors         RobotnikAutomation/robotnik_sensors         ${SENSORS_REF}

# El paquete del taller se compila junto con la suite
COPY mini_bot ${WS}/src/mini_bot

WORKDIR ${WS}
RUN source /opt/ros/jazzy/setup.bash \
 && rosdep update --rosdistro jazzy \
 && apt-get update \
 && rosdep install --from-paths src --ignore-src -r -y \
 && rm -rf /var/lib/apt/lists/* \
 && colcon build --symlink-install --event-handlers console_direct+

# El RB-Summit trae sus controladores en robotnik_controllers/RBSummitController, que no es un
# paquete público. Su <ros2_control> ya expone las cuatro ruedas con interfaz de velocidad, así
# que lo movemos con diff_drive_controller en skid-steer (mini_bot/config/
# rbsummit_controllers_workshop.yaml). La ruta del YAML está escrita a mano dentro de
# rbsummit_control.urdf.xacro, así que sustituimos ese fichero por nuestra copia. Va después del
# build: con --symlink-install, install/ enlaza a src/, y el cambio se ve sin recompilar.
COPY setup/rbsummit/rbsummit_control.urdf.xacro \
     ${WS}/src/robotnik_description/simulators/gazebo_ignition/rbsummit/rbsummit_control.urdf.xacro

# Material del taller (ejercicios y documentación)
COPY exercises /workshop/exercises
COPY docs      /workshop/docs
COPY setup/check_setup.sh /usr/local/bin/check_setup.sh
COPY setup/entrypoint.sh  /usr/local/bin/entrypoint.sh
COPY setup/workshop_env.sh /usr/local/share/workshop_env.sh
RUN chmod +x /usr/local/bin/check_setup.sh /usr/local/bin/entrypoint.sh

# Segunda terminal (setup/shell.sh o un docker exec … bash a secas): docker exec no pasa por el
# entrypoint, así que el entorno se carga también desde el .bashrc.
RUN echo 'source /usr/local/share/workshop_env.sh' >> /root/.bashrc

# Los robots del taller en una carpeta corta: el Browse del importer se abre en el directorio
# desde el que se lanzó Gazebo (los post-ejercicios lo lanzan desde $WS/robots). Son enlaces, así que
# los de mini_bot y mast_bot apuntan a lo que el participante edita en su máquina.
RUN mkdir -p ${WS}/robots \
 && ln -s ${WS}/src/mini_bot/urdf/mini_bot.urdf.xacro ${WS}/robots/mini_bot.urdf.xacro \
 && ln -s ${WS}/src/mini_bot/urdf/mast_bot.urdf.xacro ${WS}/robots/mast_bot.urdf.xacro \
 && for r in rbsummit/rbsummit rbvogui/rbvogui rbtheron/rbtheron rbkairos/rbkairos_plus; do \
      ln -s ${WS}/src/robotnik_description/robots/$r.urdf.xacro ${WS}/robots/; \
    done

# Aceleración por software como red de seguridad: si no hay /dev/dri, Gazebo sigue arrancando.
# Los share de robotnik_description y robotnik_sensors: sin el segundo, las mallas de los sensores
# del RB-Summit (cámara, LiDAR, GPS, IMU) no cargan en Gazebo.
ENV GZ_SIM_RESOURCE_PATH=${WS}/install/mini_bot/share/mini_bot/worlds:${WS}/install/robotnik_description/share:${WS}/install/robotnik_sensors/share
ENV QT_SCALE_FACTOR=1.0
# El prompt arranca en el workspace: ahí se compila y se lanza.
WORKDIR ${WS}
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["bash"]
