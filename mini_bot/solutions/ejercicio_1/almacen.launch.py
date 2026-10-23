"""Ejercicio 1 — tres mini_bot en el almacén, con un solo launch. Solución.

  ros2 launch mini_bot almacen.launch.py

Poses de las estaciones (las mismas que en worlds/workshop_almacen.sdf):
  amarilla  robot_a   x  3.45  y -1.10  yaw  0.0
  azul      robot_b   x -1.00  y -2.15  yaw -1.571
  verde     robot_c   x -1.60  y  1.50  yaw  2.356
"""
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg = FindPackageShare('mini_bot')
    xacro_file = PathJoinSubstitution([pkg, 'urdf', 'mini_bot.urdf.xacro'])

    # ── El mundo: una vez, para todos los robots ──────────────────────────────────────────────
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])),
        launch_arguments={'gz_args': ['-r ', PathJoinSubstitution([pkg, 'worlds', 'workshop_almacen.sdf'])]}.items(),
    )

    # ── robot_a: estación amarilla ───────────────────────────────────────────────────────────────
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
    robot_a_spawn = Node(
        package='ros_gz_sim',
        executable='create',
        namespace='robot_a',
        output='screen',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'robot_a',
            '-x', '3.45',
            '-y', '-1.10',
            '-z', '0.15',
            '-Y', '0.0',
        ],
    )

    # ── robot_b: estación azul ───────────────────────────────────────────────────────────────────
    robot_b_description = ParameterValue(Command([
        'xacro ', xacro_file, ' namespace:=robot_b', ' prefix:=robot_b/',
    ]), value_type=str)

    robot_b_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace='robot_b',
        output='screen',
        parameters=[{'robot_description': robot_b_description, 'use_sim_time': True}],
    )

    robot_b_spawn = Node(
        package='ros_gz_sim',
        executable='create',
        namespace='robot_b',
        output='screen',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'robot_b',
            '-x', '-1.00',
            '-y', '-2.15',
            '-z', '0.15',
            '-Y', '-1.571',
        ],
    )

    # ── robot_c: estación verde ──────────────────────────────────────────────────────────────────
    robot_c_description = ParameterValue(Command([
        'xacro ', xacro_file, ' namespace:=robot_c', ' prefix:=robot_c/',
    ]), value_type=str)

    robot_c_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace='robot_c',
        output='screen',
        parameters=[{'robot_description': robot_c_description, 'use_sim_time': True}],
    )

    robot_c_spawn = Node(
        package='ros_gz_sim',
        executable='create',
        namespace='robot_c',
        output='screen',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'robot_c',
            '-x', '-1.60',
            '-y', '1.50',
            '-z', '0.15',
            '-Y', '2.356',
        ],
    )

    # Los spawns, 3 s después del resto (como en sim.launch.py).
    spawns = TimerAction(period=3.0, actions=[
        robot_a_spawn,
        robot_b_spawn,
        robot_c_spawn,
    ])

    return LaunchDescription([
        gazebo,
        robot_a_state_publisher,
        robot_b_state_publisher,
        robot_c_state_publisher,
        spawns,
    ])
