"""mini_bot en Gazebo — solución del ejercicio 3.

Crece a lo largo del taller:
  ex02  mundo + robot_state_publisher + spawn
  ex04  + ros_gz_bridge + RViz
  ex05  + spawners de controladores

Uso:
  ros2 launch mini_bot sim.launch.py
  ros2 launch mini_bot sim.launch.py x:=1.0 y:=0.5

Un robot por mundo. Este launch abre su propio Gazebo, y bridge.yaml usa topics absolutos (/scan):
con namespace:=robot_b los controladores funcionan, pero los sensores del robot publican en
/robot_b/scan y el puente no los ve. Para varios robots, ver el extra "Multi-robot a mano".
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg = FindPackageShare('mini_bot')

    # ── Argumentos ────────────────────────────────────────────────────────────────────────────
    # Lo que se puede cambiar desde la línea de comandos sin tocar el fichero:
    #   ros2 launch mini_bot sim.launch.py x:=1.0 y:=0.5
    args = [
        DeclareLaunchArgument('world', default_value=PathJoinSubstitution([pkg, 'worlds', 'workshop.sdf'])),
        DeclareLaunchArgument('namespace', default_value=''),
        DeclareLaunchArgument('prefix', default_value=''),
        DeclareLaunchArgument('name', default_value='mini_bot'),
        DeclareLaunchArgument('x', default_value='0.0'),
        DeclareLaunchArgument('y', default_value='0.0'),
        DeclareLaunchArgument('z', default_value='0.15'),
    ]

    ns = LaunchConfiguration('namespace')

    # ── La descripción del robot ──────────────────────────────────────────────────────────────
    # Ejecuta xacro al lanzar y guarda el URDF resultante, como texto, para dárselo a
    # robot_state_publisher. Por eso los cambios del xacro se ven al relanzar, sin recompilar.
    # ParameterValue(..., value_type=str): sin él, launch intenta leer el URDF como YAML y falla.
    robot_description = ParameterValue(Command([
        'xacro ', PathJoinSubstitution([pkg, 'urdf', 'mini_bot.urdf.xacro']),
        ' namespace:=', ns,
        ' prefix:=', LaunchConfiguration('prefix'),
    ]), value_type=str)

    # ── PASO 1 · Gazebo ───────────────────────────────────────────────────────────────────────
    # Incluye el launch que trae ros_gz_sim: arranca el servidor de simulación (la física) y la
    # ventana de Gazebo con el mundo indicado. '-r' lo pone en marcha nada más abrir; sin él,
    # Gazebo arranca en pausa. Gazebo no sabe nada de ROS 2: solo carga un fichero SDF.
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])),
        launch_arguments={'gz_args': ['-r ', LaunchConfiguration('world')]}.items(),
    )

    # ── PASO 2 · robot_state_publisher ────────────────────────────────────────────────────────
    # El nodo de ROS 2 que convierte el URDF en información útil para los demás:
    #   - publica el URDF completo en el topic /robot_description, para quien lo necesite
    #     (aquí, create; en el ejercicio 4, RViz);
    #   - publica TF: los joints fijos una vez, en /tf_static, y los móviles cada vez que
    #     llega un /joint_states (en el ejercicio 1 lo publicaban los sliders).
    # No tiene nada que ver con Gazebo: es el mismo nodo que en display.launch.py.
    # use_sim_time: True hace que use el reloj de la simulación (/clock, ejercicio 4) en vez del
    # reloj del ordenador.
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace=ns,
        output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
    )

    # ── PASO 3 · El spawn: create ─────────────────────────────────────────────────────────────
    # create es un programa de un solo uso: lee el URDF del topic robot_description, se lo pasa
    # a Gazebo (que lo convierte a SDF) para meter el robot en el mundo, y termina. Por eso, en
    # la salida del launch, "create" acaba con "process has finished cleanly": no es un error.
    #   -name   nombre del modelo en Gazebo; no puede repetirse en el mismo mundo
    #   -x -y -z  dónde aparece. z = 0.15: un poco por encima del suelo, para que caiga y se
    #             apoye en vez de nacer medio enterrado
    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        namespace=ns,
        output='screen',
        arguments=[
            '-topic', 'robot_description',
            '-name', LaunchConfiguration('name'),
            '-x', LaunchConfiguration('x'),
            '-y', LaunchConfiguration('y'),
            '-z', LaunchConfiguration('z'),
        ],
    )

    # Arranque ordenado. launch lanza todo a la vez, sin esperar a nadie. create ya se defiende
    # solo: reintenta hasta que el mundo de Gazebo responde y espera al mensaje de
    # /robot_description. Aun así, se lanza 3 s después del resto, para que el orden sea siempre
    # el mismo: primero el mundo y la descripción, y después el robot.
    spawn_delayed = TimerAction(period=3.0, actions=[spawn])

    # ── Lo que se lanza ───────────────────────────────────────────────────────────────────────
    # Solo se ejecuta lo que está en esta lista.
    return LaunchDescription(args + [
        gazebo,
        robot_state_publisher,
        spawn_delayed,
    ])
