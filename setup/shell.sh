#!/usr/bin/env bash
# Abre otra terminal dentro del contenedor del taller, con ROS 2 y el workspace ya cargados.
# Uso:  ./setup/shell.sh
for name in roscon-workshop roscon-workshop-novnc; do
  if docker ps --format '{{.Names}}' | grep -qx "$name"; then
    exec docker exec -it -w /workshop_ws "$name" bash
  fi
done
echo "No hay ningún contenedor del taller corriendo. Arráncalo antes con ./setup/run.sh (o run_novnc.sh)."
exit 1
