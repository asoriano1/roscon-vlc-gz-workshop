# Extra — Más robots de Robotnik (opcional)

En los post-ejercicios has importado un RB-Summit y, en sus extras, has puenteado sus sensores y lo
has conducido. En la carpeta `$WS/robots` hay más robots de
[`robotnik_description`](https://github.com/RobotnikAutomation/robotnik_description), con sus
mallas y sus sensores. El flujo es el mismo con todos.

> Aviso: sin GPU, la simulación va más lenta con cada robot. No importa: lo que se demuestra es que
> el flujo es el mismo con un robot de 50 kB y con uno de 50 MB.

## Pasos

**Opcional**, fuera del horario. Lanza Gazebo con la suite desde `$WS/robots`, como en los
post-ejercicios:

```bash
cd $WS/robots && ros2 launch mini_bot suite.launch.py
```

1. Importa un **RB-Vogui** (`rbvogui.urdf.xacro`) con *Namespace* `vogui_a` y *Frame prefix*
   `vogui_a/`.
2. Importa otro distinto al lado: un RB-Theron o, para tener brazo, un RB-Kairos+
   (`rbkairos_plus.urdf.xacro`), con su propio namespace y prefijo.
3. Con el Bridge Manager, mira qué sensores trae cada uno y puentea los que quieras ver.
4. Míralos en RViz: abre `rviz2`, pon como *Fixed Frame* el `base_footprint` de uno de ellos
   (`vogui_a/base_footprint`) y añade sus displays con **Add** → **By topic**.

El RB-Theron y el RB-Kairos+ también se conducen, igual que el Summit del post-ejercicio 3:
impórtalos con el *Frame prefix* **vacío**, activa `joint_state_broadcaster` y
`diff_drive_controller` en el Control Manager y lánzales el teleop con su namespace
(`ros2 launch mini_bot teleop_raton.launch.py namespace:=theron_a`). El Kairos+ tiene ruedas mecanum,
pero aquí se mueve como uno diferencial: avanza y gira, no se desplaza de lado; su brazo no se
mueve. El RB-Vogui solo trae sensores: sus controladores son de Robotnik y no son públicos.

## Comparación final

| | mini_bot | Un robot de Robotnik |
|---|---|---|
| Lo que escribiste | todo | nada |
| Geometría | primitivas | mallas |
| Tiempo hasta ver sus sensores en RViz | tu marca del ejercicio 2 | tu marca de ahora |

## Preguntas para el cierre

1. ¿Qué partes de lo que escribiste a mano siguen siendo necesarias en producción?
2. ¿Dónde te ha ahorrado tiempo de verdad la suite, y dónde no?
3. ¿Qué robot de tu trabajo importarías así?

## Si la simulación se arrastra

- Usa `worlds/workshop_lite.sdf`.
- Quédate con dos robots.
- Puentea solo los sensores que vayas a mirar: un sensor con suscriptores en ROS 2 se renderiza, y
  los de estos robots son caros.
