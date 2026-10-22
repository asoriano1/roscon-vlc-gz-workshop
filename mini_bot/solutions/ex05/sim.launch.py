"""mini_bot en Gazebo — launch completo (solución del ejercicio 5).

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
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
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
        DeclareLaunchArgument('rviz', default_value='true'),
        DeclareLaunchArgument('gui', default_value='true'),
    ]

    ns = LaunchConfiguration('namespace')
    prefix = LaunchConfiguration('prefix')

    # ParameterValue(..., value_type=str): sin él, launch intenta leer el URDF como YAML y falla.
    robot_description = ParameterValue(Command([
        'xacro ', PathJoinSubstitution([pkg, 'urdf', 'mini_bot.urdf.xacro']),
        ' namespace:=', ns,
        ' prefix:=', prefix,
    ]), value_type=str)

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])),
        launch_arguments={'gz_args': ['-r ', LaunchConfiguration('world')]}.items(),
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace=ns,
        output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
    )

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

    # >>> BRIDGE
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        namespace=ns,
        output='screen',
        parameters=[{
            'config_file': PathJoinSubstitution([pkg, 'config', 'bridge.yaml']),
            'use_sim_time': True,
        }],
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        condition=IfCondition(LaunchConfiguration('rviz')),
        arguments=['-d', PathJoinSubstitution([pkg, 'rviz', 'mini_bot.rviz'])],
        parameters=[{'use_sim_time': True}],
    )
    # <<< BRIDGE

    # >>> CONTROL
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
    # <<< CONTROL

    return LaunchDescription(args + [
        gazebo,
        robot_state_publisher,
        spawn,
        bridge,
        rviz,
        jsb_spawner,
        diff_spawner,
    ])
