"""Gazebo con los tres plugins de la suite, para los post-ejercicios.

Hace lo mismo que gazebo_importer.launch.py del Model Importer, pero con la GUI completa de
Gazebo (barra de formas, World stats con el RTF, Entity tree) y los tres paneles de la suite ya
acoplados: config/suite_gui.config.

  cd $WS/robots && ros2 launch mini_bot suite.launch.py

El cd importa: el Browse del importer se abre en la carpeta desde la que se lanza.
"""
import os

from ament_index_python.packages import get_package_prefix
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable, DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg = FindPackageShare('mini_bot')

    args = [
        DeclareLaunchArgument('world', default_value=PathJoinSubstitution([pkg, 'worlds', 'workshop.sdf'])),
    ]

    # Dónde busca Gazebo los paneles de la suite. En la imagen ya lo ponen los paquetes al
    # cargar el workspace; aquí se asegura también para la instalación nativa.
    plugin_paths = [
        AppendEnvironmentVariable('GZ_GUI_PLUGIN_PATH', os.path.join(get_package_prefix(p), 'lib'))
        for p in ('gz_model_importer', 'gz_ros2_bridge_manager', 'gz_ros2_control_manager')
    ]

    # Gazebo en marcha (-r) con la GUI del taller.
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])),
        launch_arguments={'gz_args': [
            '-r --gui-config ', PathJoinSubstitution([pkg, 'config', 'suite_gui.config']),
            ' ', LaunchConfiguration('world'),
        ]}.items(),
    )

    # /clock, para que los nodos con use_sim_time (robot_state_publisher, controladores, RViz)
    # vayan con el tiempo de la simulación.
    clock_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
        output='screen',
    )

    return LaunchDescription(args + plugin_paths + [gazebo, clock_bridge])
