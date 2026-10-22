#!/usr/bin/env bash
# Comprueba que el entorno del taller está listo e imprime un código para enseñar en clase.
# Uso:  ./setup/check_setup.sh        (dentro del contenedor o en una instalación nativa)
set -u
ok=1
say() { printf '%-28s %s\n' "$1" "$2"; }
fail() { ok=0; }

# Los setup.bash de ROS usan variables sin definir: con set -u el shell muere al hacer source.
set +u
source /opt/ros/jazzy/setup.bash 2>/dev/null || true
WS="${WS:-/workshop_ws}"
[ -f "$WS/install/setup.bash" ] && source "$WS/install/setup.bash" 2>/dev/null || true
set -u

echo "=== Comprobación del entorno — ROSCon Valencia · Gazebo Model Runtime Suite ==="

if [ "${ROS_DISTRO:-}" = "jazzy" ]; then say "ROS 2" "jazzy OK"; else say "ROS 2" "FALTA (ROS_DISTRO=${ROS_DISTRO:-vacío})"; fail; fi

if command -v gz >/dev/null 2>&1; then
  gzv=$(gz sim --versions 2>/dev/null | head -1)
  say "Gazebo" "${gzv:-desconocida} OK"
else
  say "Gazebo" "FALTA (no se encuentra gz)"; fail
fi

for p in mini_bot gz_model_importer gz_ros2_bridge_manager gz_ros2_control_manager robotnik_description robotnik_sensors rqt_tf_tree; do
  if ros2 pkg prefix "$p" >/dev/null 2>&1; then say "$p" "OK"; else say "$p" "FALTA"; fail; fi
done

for lib in libGzModelImporter.so libRos2BridgeManagerGui.so libRos2ControlManagerGui.so; do
  if find "$WS/install" /opt/ros/jazzy -name "$lib" -print -quit 2>/dev/null | grep -q .; then
    say "${lib}" "OK"
  else
    say "${lib}" "FALTA"; fail
  fi
done

if [ -n "${DISPLAY:-}" ]; then say "DISPLAY" "${DISPLAY} OK"; else say "DISPLAY" "FALTA (sin GUI)"; fail; fi

if [ -e /dev/dri/renderD128 ]; then say "GPU" "/dev/dri disponible"; else say "GPU" "sin /dev/dri (irá por software, lento)"; fi

echo
if [ "$ok" = "1" ]; then
  echo "CÓDIGO: OK-JAZZY-HARMONIC-SUITE"
  echo "Enséñalo en tu post-it verde."
else
  echo "CÓDIGO: FALTA-ALGO — mira las líneas con FALTA de arriba."
  exit 1
fi
