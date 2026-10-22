#!/usr/bin/env bash
set -e
source /usr/local/share/workshop_env.sh
if [ -n "${LIBGL_ALWAYS_SOFTWARE:-}" ]; then
  echo "[entrypoint] Sin /dev/dri: renderizado por software (Gazebo irá lento)."
fi
exec "$@"
