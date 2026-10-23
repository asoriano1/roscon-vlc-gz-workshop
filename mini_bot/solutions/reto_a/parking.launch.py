"""Reto A — tres mini_bot aparcados, a mano. Solución.

  ros2 launch mini_bot parking.launch.py

Poses de las plazas (las mismas que en worlds/workshop_parking.sdf):
  amarilla  robot_a   x  1.0  y -2.6  yaw  2.356
  azul      robot_b   x -1.2  y  2.2  yaw -1.571
  verde     robot_c   x  2.6  y  2.6  yaw  0.524
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
        launch_arguments={'gz_args': ['-r ', PathJoinSubstitution([pkg, 'worlds', 'workshop_parking.sdf'])]}.items(),
    )

    # ── robot_a: plaza amarilla ───────────────────────────────────────────────────────────────
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
            '-x', '1.0',
            '-y', '-2.6',
            '-z', '0.15',
            '-Y', '2.356',
        ],
    )

    # ── robot_b: plaza azul ───────────────────────────────────────────────────────────────────
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
            '-x', '-1.2',
            '-y', '2.2',
            '-z', '0.15',
            '-Y', '-1.571',
        ],
    )

    # ── robot_c: plaza verde ──────────────────────────────────────────────────────────────────
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
            '-x', '2.6',
            '-y', '2.6',
            '-z', '0.15',
            '-Y', '0.524',
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
