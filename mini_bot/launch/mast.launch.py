"""mast_bot en Gazebo — el launch del ejercicio 3.

Es el sim.launch.py del preámbulo 3 con otro robot (mast_bot), otro puente (mast_bridge.yaml) y
otro RViz. Falta el spawner del controlador del mástil: ese es el ejercicio.

  ros2 launch mini_bot mast.launch.py

Solución en  mini_bot/solutions/ejercicio_3/mast.launch.py
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg = FindPackageShare('mini_bot')

    # ── Argumentos ────────────────────────────────────────────────────────────────────────────────
    # Lo que se puede cambiar desde la línea de comandos sin tocar el fichero:
    #   ros2 launch mini_bot sim.launch.py x:=1.0 y:=0.5
    args = [
        DeclareLaunchArgument('world', default_value=PathJoinSubstitution([pkg, 'worlds', 'workshop.sdf'])),
        DeclareLaunchArgument('namespace', default_value=''),
        DeclareLaunchArgument('prefix', default_value=''),
        DeclareLaunchArgument('name', default_value='mast_bot'),
        DeclareLaunchArgument('x', default_value='0.0'),
        DeclareLaunchArgument('y', default_value='0.0'),
        DeclareLaunchArgument('z', default_value='0.15'),
        DeclareLaunchArgument('rviz', default_value='true'),
    ]

    ns = LaunchConfiguration('namespace')

    # ── La descripción del robot ──────────────────────────────────────────────────────────────────
    # Ejecuta xacro al lanzar y guarda el URDF resultante, como texto, para dárselo a
    # robot_state_publisher. Por eso los cambios del xacro se ven al relanzar, sin recompilar.
    # ParameterValue(..., value_type=str): sin él, launch intenta leer el URDF como YAML y falla.
    robot_description = ParameterValue(Command([
        'xacro ', PathJoinSubstitution([pkg, 'urdf', 'mast_bot.urdf.xacro']),
        ' namespace:=', ns,
        ' prefix:=', LaunchConfiguration('prefix'),
    ]), value_type=str)

    # ── Gazebo ────────────────────────────────────────────────────────────────────────────────────
    # Incluye el launch que trae ros_gz_sim: arranca el servidor de simulación (la física) y la
    # ventana de Gazebo con el mundo indicado. '-r' lo pone en marcha nada más abrir; sin él,
    # Gazebo arranca en pausa. Gazebo no sabe nada de ROS 2: solo carga un fichero SDF.
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])),
        launch_arguments={'gz_args': ['-r ', LaunchConfiguration('world')]}.items(),
    )

    # ── robot_state_publisher ─────────────────────────────────────────────────────────────────────
    # El nodo de ROS 2 que convierte el URDF en información útil para los demás:
    #   - publica el URDF completo en el topic /robot_description, para quien lo necesite
    #     (aquí, create, y RViz);
    #   - publica TF: los joints fijos una vez, en /tf_static, y los móviles cada vez que
    #     llega un /joint_states (en display.launch.py lo publicaban los sliders; en el
    #     preámbulo 3, joint_state_broadcaster).
    # No tiene nada que ver con Gazebo: es el mismo nodo que en display.launch.py.
    # use_sim_time: True hace que use el reloj de la simulación (/clock) en vez del reloj del
    # ordenador. /clock llega a ROS 2 con el puente.
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace=ns,
        output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
    )

    # ── El spawn: create ──────────────────────────────────────────────────────────────────────────
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

    # ── El puente y RViz ──────────────────────────────────────────────────────────────────────────
    # parameter_bridge copia topics de Gazebo a ROS 2 (o al revés), solo los que dice
    # config/bridge.yaml. Gazebo y ROS 2 son dos sistemas de mensajería distintos: sin este nodo,
    # los sensores publican en Gazebo y ROS 2 no ve nada.
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        namespace=ns,
        output='screen',
        parameters=[{
            'config_file': PathJoinSubstitution([pkg, 'config', 'mast_bridge.yaml']),
            'use_sim_time': True,
        }],
    )

    # RViz con una configuración guardada: modelo del robot, TF, LaserScan e imagen.
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        condition=IfCondition(LaunchConfiguration('rviz')),
        arguments=['-d', PathJoinSubstitution([pkg, 'rviz', 'mast_bot.rviz'])],
        parameters=[{'use_sim_time': True}],
    )

    # ── Los spawners de los controladores ─────────────────────────────────────────────────────────
    # El controller_manager lo arranca el plugin gz_ros2_control dentro de Gazebo, con los
    # controladores declarados en config/mast_controllers.yaml, pero sin cargar.
    # Cada spawner carga uno, lo configura, lo activa y termina. Esperan solos a que exista el
    # controller_manager.
    #   joint_state_broadcaster  lee la posición de las ruedas y la publica en /joint_states
    #   diff_drive_controller    convierte cmd_vel en velocidades de rueda y publica la odometría
    # 'controller_manager' sin barra: relativo al namespace del robot.
    jsb_spawner = Node(
        package='controller_manager',
        executable='spawner',
        namespace=ns,
        output='screen',
        arguments=['joint_state_broadcaster', '--controller-manager', 'controller_manager'],
    )

    diff_spawner = Node(
        package='controller_manager',
        executable='spawner',
        namespace=ns,
        output='screen',
        arguments=['diff_drive_controller', '--controller-manager', 'controller_manager'],
    )

    # EJERCICIO 3: pega aquí el spawner del controlador del mástil.

    # ── Lo que se lanza ───────────────────────────────────────────────────────────────────────────
    # Solo se ejecuta lo que está en esta lista. EJERCICIO 3: añade aquí el spawner nuevo.
    return LaunchDescription(args + [
        gazebo,
        robot_state_publisher,
        spawn_delayed,
        bridge,
        rviz,
        jsb_spawner,
        diff_spawner,
    ])
