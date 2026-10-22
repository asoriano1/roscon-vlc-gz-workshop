# Ejercicio 9 — Robots reales, como prueba de concepto (15 min)

Hasta ahora todo ha sido un robot de cajas. Ahora entran robots de verdad, con mallas, sensores
reales y `ros2_control` ya montado: los de
[`robotnik_description`](https://github.com/RobotnikAutomation/robotnik_description).

> Aviso: aquí la simulación va a ir más lenta, sobre todo sin GPU. No importa.
> Lo que se demuestra es que el flujo es el mismo con un robot de 50 kB y con uno de 50 MB.

## Pasos

Sigue en el Gazebo del ejercicio 6. Si lo cerraste, vuelve a lanzarlo igual, desde `$WS/robots`:

```bash
cd $WS/robots && ros2 launch gz_model_importer gazebo_importer.launch.py \
  world:=$(ros2 pkg prefix mini_bot)/share/mini_bot/worlds/workshop.sdf
```

1. Con el importer (*Browse* → `rbsummit.urdf.xacro`), importa un **RB-Summit** con namespace
   `summit_a` y el campo *prefix* **vacío**. Aquí no vale `summit_a/`: los xacros de Robotnik
   ponen el prefijo también en los joints, y el YAML de controladores nombra las ruedas sin él.
2. Importa un segundo robot distinto: RB-Vogui, RB-Theron o, para tener brazo, un RB-Kairos+
   (los tres están en la misma carpeta).
3. Puentea sus sensores con el Bridge Manager.
4. Activa los controladores del RB-Summit con el Control Manager (*Load inactive* y *Activate*
   en `joint_state_broadcaster` y `diff_drive_controller`) y condúcelo desde otra terminal
   (lanza `./setup/shell.sh` en tu máquina, desde la raíz del repo):

   ```bash
   ros2 topic pub -r 10 /summit_a/diff_drive_controller/cmd_vel geometry_msgs/msg/TwistStamped \
     "{twist: {linear: {x: 0.5}, angular: {z: 0.4}}}"
   ```

> Mismo robot y mismo hardware interface (cuatro ruedas por velocidad) que en Robotnik, otro
> controlador: aquí lo mueve el `diff_drive_controller` de `mini_bot` en modo skid-steer.

## Comparación final

| | mini_bot | RB-Summit |
|---|---|---|
| Lo que escribiste | todo | nada |
| Geometría | primitivas | mallas |
| Tiempo hasta verlo rodar | tu marca de los ej. 1–5 | tu marca de ahora |

## Preguntas para el cierre

1. ¿Qué partes de lo que escribiste a mano siguen siendo necesarias en producción?
2. ¿Dónde te ha ahorrado tiempo de verdad la suite y dónde no?
3. ¿Qué robot de tu trabajo importarías así?

## Si la simulación se arrastra

- Usa `worlds/workshop_lite.sdf`.
- Quédate con dos robots.
- Puentea solo los sensores que vayas a mirar: un sensor con suscriptores en ROS 2 se
  renderiza, y los del RB-Summit son caros.
