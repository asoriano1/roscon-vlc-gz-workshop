#!/usr/bin/env bash
# Arranca el contenedor del taller con GUI nativa (Linux + X11).
# Uso:  ./setup/run.sh [comando]      por defecto abre una bash
# mini_bot/ se monta desde tu máquina: edita fuera, el contenedor solo ejecuta.
set -e
IMAGE="${IMAGE:-ghcr.io/asoriano1/roscon-workshop:latest}"
# Rutas desde la raíz del repo, no desde $PWD: si montas una carpeta que no existe, Docker la
# crea vacía y el contenedor se queda sin mini_bot.
REPO="$(cd "$(dirname "$0")/.." && pwd)"

if [ "$(uname)" != "Linux" ]; then
  echo "Este script es para Linux. En macOS o Windows usa setup/run_novnc.sh (Gazebo en el navegador)."
  exit 1
fi

xhost +local:docker >/dev/null 2>&1 || true

GPU_ARGS=()
[ -e /dev/dri ] && GPU_ARGS+=(--device /dev/dri)

docker run --rm -it \
  --name roscon-workshop \
  -e DISPLAY="$DISPLAY" \
  -e QT_X11_NO_MITSHM=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v "$HOME/.Xauthority:/root/.Xauthority:rw" \
  -v "$REPO/exercises:/workshop/exercises:rw" \
  -v "$REPO/mini_bot:/workshop_ws/src/mini_bot:rw" \
  --network host \
  --ipc host \
  "${GPU_ARGS[@]}" \
  "$IMAGE" "${@:-bash}"
