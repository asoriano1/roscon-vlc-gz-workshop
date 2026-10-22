#!/usr/bin/env bash
# Plan B para macOS, Windows o cualquier portátil donde X11 dé problemas:
# Gazebo dentro del contenedor, visible en el navegador en http://localhost:6080
set -e
IMAGE="${IMAGE:-ghcr.io/asoriano1/roscon-workshop:latest}"
# Rutas desde la raíz del repo, no desde $PWD: si montas una carpeta que no existe, Docker la
# crea vacía y el contenedor se queda sin mini_bot.
REPO="$(cd "$(dirname "$0")/.." && pwd)"

docker run --rm -it \
  --name roscon-workshop-novnc \
  -p 6080:6080 \
  -v "$REPO/exercises:/workshop/exercises:rw" \
  -v "$REPO/mini_bot:/workshop_ws/src/mini_bot:rw" \
  "$IMAGE" bash -lc '
    Xvfb :1 -screen 0 1600x900x24 &
    sleep 2
    export DISPLAY=:1
    x11vnc -display :1 -forever -nopw -quiet &
    websockify --web /usr/share/novnc 6080 localhost:5900 &
    echo "Gazebo, en el navegador: http://localhost:6080/vnc.html"
    exec bash'
