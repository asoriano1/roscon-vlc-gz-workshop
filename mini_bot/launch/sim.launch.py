"""mini_bot en Gazebo — ESQUELETO DEL TALLER.

Este launch va creciendo contigo:
  ex02  mundo + robot_state_publisher + spawn      <- empiezas aquí
  ex04  + ros_gz_bridge + RViz
  ex05  + spawners de controladores

Soluciones en  mini_bot/solutions/exNN/sim.launch.py
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg = FindPackageShare('mini_bot')

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

    # El URDF se expande aquí mismo, en tiempo de lanzamiento.
    # ParameterValue(..., value_type=str): sin él, launch intenta leer el URDF como YAML y falla.
    robot_description = ParameterValue(Command([
        'xacro ', PathJoinSubstitution([pkg, 'urdf', 'mini_bot.urdf.xacro']),
        ' namespace:=', ns,
        ' prefix:=', LaunchConfiguration('prefix'),
    ]), value_type=str)

    # TODO (2a): incluye el launch de Gazebo que trae ros_gz_sim y pásale el mundo.
    #   paquete: ros_gz_sim     fichero: launch/gz_sim.launch.py
    #   argumento: gz_args = ['-r ', LaunchConfiguration('world')]
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])),
        launch_arguments={}.items(),
    )

    # TODO (2b): robot_state_publisher con el robot_description de arriba y use_sim_time.
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace=ns,
        output='screen',
        parameters=[{}],
    )

    # TODO (2c): haz el spawn del robot leyendo el topic robot_description.
    #   paquete ros_gz_sim, ejecutable create
    #   argumentos: -topic robot_description, -name, -x, -y, -z
    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        namespace=ns,
        output='screen',
        arguments=[],
    )

    # TODO (4): aquí irán el parameter_bridge (config/bridge.yaml) y RViz.

    # TODO (5): aquí irán los spawners de joint_state_broadcaster y diff_drive_controller.

    return LaunchDescription(args + [
        gazebo,
        robot_state_publisher,
        spawn,
    ])
