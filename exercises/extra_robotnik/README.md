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
2. Importa otro distinto al lado: un RB-Theron (`rbtheron.urdf.xacro`), con su propio namespace y
   prefijo.
3. Con el Bridge Manager, mira qué sensores trae cada uno y puentea los que quieras ver.
4. Míralos en RViz: abre `rviz2`, pon como *Fixed Frame* el `base_footprint` de uno de ellos
   (`vogui_a/base_footprint`) y añade sus displays con **Add** → **By topic**.

Solo el RB-Summit tiene controladores preparados en la imagen. Los demás declaran controladores de
Robotnik que no son públicos: aquí se quedan quietos.

El RB-Kairos+ (`rbkairos_plus.urdf.xacro`) también se importa, con su brazo, pero sin sensores: su
brazo UR no expande con los sensores de Gazebo activados en Jazzy.

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
