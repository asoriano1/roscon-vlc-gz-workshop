# Entorno del taller. Lo cargan el entrypoint (primera terminal) y /root/.bashrc (cualquier
# docker exec … bash, incluido setup/shell.sh), para que todas las terminales sean iguales.
source /opt/ros/jazzy/setup.bash
# Raíz del workspace. Los enunciados usan $WS para que valgan igual en Docker y en nativo.
export WS=/workshop_ws
source $WS/install/setup.bash
# Sin GPU accesible, forzamos renderizado por software para que Gazebo no muera al arrancar.
if [ ! -e /dev/dri/renderD128 ]; then
  export LIBGL_ALWAYS_SOFTWARE=1
fi
