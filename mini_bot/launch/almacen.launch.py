"""Ejercicio 1 — tres mini_bot en el almacén, con un solo launch. ESQUELETO.

Abre el almacén y mete un robot, robot_a, en la pose (0, 0, 0). El ejercicio:
  1. Repite el bloque de robot_a para robot_b y robot_c, y lánzalos los tres.
  2. Pon cada robot en su estación, con las poses de la tabla del enunciado.

  ros2 launch mini_bot almacen.launch.py

Solución en  mini_bot/solutions/ejercicio_1/almacen.launch.py
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
    xacro_file = PathJoinSubstitution([pkg, 'urdf', 'mini_bot.urdf.xacro'])

    # ── El mundo: una vez, para todos los robots ──────────────────────────────────────────────
    # gazebo:=false no abre Gazebo y mete los robots en el que ya esté abierto (el del importer,
    # en el post-ejercicio 1): create busca solo el mundo en marcha.
    gazebo_arg = DeclareLaunchArgument('gazebo', default_value='true')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])),
        launch_arguments={'gz_args': ['-r ', PathJoinSubstitution([pkg, 'worlds', 'workshop_almacen.sdf'])]}.items(),
        condition=IfCondition(LaunchConfiguration('gazebo')),
    )

    # ── robot_a: estación amarilla ──────────────────────────────────────────────────────────────
    # Tres cosas cambian de un robot a otro, y las tres tienen que ser distintas:
    #   - el namespace (robot_a): sin él, los tres robot_state_publisher se llamarían igual y
    #     publicarían los tres en el mismo /robot_description;
    #   - el prefijo de frames (robot_a/), que el xacro pone delante de cada link;
    #   - el nombre del modelo en Gazebo (-name robot_a): Gazebo no admite dos iguales.
    robot_a_description = ParameterValue(Command([
        'xacro ', xacro_file, ' namespace:=robot_a', ' prefix:=robot_a/',
    ]), value_type=str)

    robot_a_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace='robot_a',
        output='screen',
        parameters=[{'robot_description': robot_a_description, 'use_sim_time': True}],
    )

    # -topic robot_description es relativo: con namespace robot_a, lee /robot_a/robot_description.
    # TODO (parte 2): la pose de la estación amarilla, de la tabla del enunciado. -Y es el giro
    # alrededor del eje vertical, en radianes.
    robot_a_spawn = Node(
        package='ros_gz_sim',
        executable='create',
        namespace='robot_a',
        output='screen',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'robot_a',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.15',
            '-Y', '0.0',
        ],
    )

    # TODO (parte 1): robot_b (estación azul) y robot_c (estación verde). Copia el bloque de
    # robot_a y cambia todo lo que diga robot_a. Añade los nodos nuevos a las dos listas de abajo.

    # Los spawns, 3 s después del resto (como en sim.launch.py).
    spawns = TimerAction(period=3.0, actions=[
        robot_a_spawn,
    ])

    return LaunchDescription([
        gazebo_arg,
        gazebo,
        robot_a_state_publisher,
        spawns,
    ])
