"""mini_bot en RViz, sin Gazebo (ejercicio 1).

Arranca robot_state_publisher, el joint_state_publisher_gui para mover las ruedas
a mano, y RViz. Sirve para comprobar la geometría y el árbol de TF antes de simular.

  ros2 launch mini_bot display.launch.py
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg = FindPackageShare('mini_bot')

    args = [
        DeclareLaunchArgument('namespace', default_value=''),
        DeclareLaunchArgument('prefix', default_value=''),
    ]
    ns = LaunchConfiguration('namespace')

    # ParameterValue(..., value_type=str): sin él, launch intenta leer el URDF como YAML y falla.
    robot_description = ParameterValue(Command([
        'xacro ', PathJoinSubstitution([pkg, 'urdf', 'mini_bot.urdf.xacro']),
        ' namespace:=', ns,
        ' prefix:=', LaunchConfiguration('prefix'),
    ]), value_type=str)

    return LaunchDescription(args + [
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             namespace=ns, output='screen',
             parameters=[{'robot_description': robot_description}]),
        Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui',
             namespace=ns, output='screen'),
        Node(package='rviz2', executable='rviz2', output='screen',
             arguments=['-d', PathJoinSubstitution([pkg, 'rviz', 'mini_bot.rviz'])]),
    ])
