# Imagen del taller: ROS 2 Jazzy + Gazebo Harmonic + Gazebo ROS 2 Model Runtime Suite
#
#   docker build -t ghcr.io/asoriano1/roscon-workshop:latest -f setup/Dockerfile .
#
# Los SHA de los repos se fijan en el build para que todos los asistentes tengan
# exactamente el mismo código. Antes del taller: sustituir los "main" por los SHA reales.
FROM ros:jazzy-ros-base

ARG DEBIAN_FRONTEND=noninteractive
ARG IMPORTER_REF=main
ARG BRIDGE_REF=main
ARG CONTROL_REF=main
ARG DESCRIPTION_REF=jazzy-devel
ARG SENSORS_REF=jazzy-devel

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
      ros-jazzy-rqt-graph \
      python3-colcon-common-extensions \
      git nano vim less tmux \
      mesa-utils libgl1-mesa-dri x11-apps \
      x11vnc xvfb novnc websockify supervisor \
    && rm -rf /var/lib/apt/lists/*

ENV WS=/workshop_ws
WORKDIR ${WS}/src

RUN git clone --depth 1 --branch ${IMPORTER_REF}    https://github.com/asoriano1/gz_model_importer_plugin.git \
 && git clone --depth 1 --branch ${BRIDGE_REF}      https://github.com/asoriano1/gz_ros2_bridge_manager.git \
 && git clone --depth 1 --branch ${CONTROL_REF}     https://github.com/asoriano1/gz_ros2_control_manager.git \
 && git clone --depth 1 --branch ${DESCRIPTION_REF} https://github.com/RobotnikAutomation/robotnik_description.git \
 && git clone --depth 1 --branch ${SENSORS_REF}     https://github.com/RobotnikAutomation/robotnik_sensors.git

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

# Material del taller (ejercicios, mundos, modelos rotos, chuleta)
COPY exercises /workshop/exercises
COPY broken    /workshop/broken
COPY docs      /workshop/docs
COPY setup/check_setup.sh /usr/local/bin/check_setup.sh
COPY setup/entrypoint.sh  /usr/local/bin/entrypoint.sh
COPY setup/workshop_env.sh /usr/local/share/workshop_env.sh
RUN chmod +x /usr/local/bin/check_setup.sh /usr/local/bin/entrypoint.sh

# Segunda terminal (setup/shell.sh o un docker exec … bash a secas): docker exec no pasa por el
# entrypoint, así que el entorno se carga también desde el .bashrc.
RUN echo 'source /usr/local/share/workshop_env.sh' >> /root/.bashrc

# Los robots del taller en una carpeta corta: el Browse del importer se abre en el directorio
# desde el que se lanzó Gazebo (los ejercicios 6 y 9 lo lanzan desde $WS/robots). Son enlaces, así que
# el de mini_bot apunta a lo que el participante edita en su máquina.
RUN mkdir -p ${WS}/robots \
 && ln -s ${WS}/src/mini_bot/urdf/mini_bot.urdf.xacro ${WS}/robots/mini_bot.urdf.xacro \
 && for r in rbsummit/rbsummit rbvogui/rbvogui rbtheron/rbtheron rbkairos/rbkairos_plus; do \
      ln -s ${WS}/src/robotnik_description/robots/$r.urdf.xacro ${WS}/robots/; \
    done

# Aceleración por software como red de seguridad: si no hay /dev/dri, Gazebo sigue arrancando.
# Los share de robotnik_description y robotnik_sensors: sin el segundo, las mallas de los sensores
# del RB-Summit (cámara, LiDAR, GPS, IMU) no cargan en Gazebo.
ENV GZ_SIM_RESOURCE_PATH=${WS}/install/mini_bot/share/mini_bot/worlds:${WS}/install/robotnik_description/share:${WS}/install/robotnik_sensors/share
ENV QT_SCALE_FACTOR=1.0
WORKDIR /workshop
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["bash"]
