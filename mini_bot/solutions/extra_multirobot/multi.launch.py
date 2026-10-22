"""Tres mini_bot en el mismo mundo (solución del extra "Multi-robot a mano").

Lo que va una vez por mundo (Gazebo y /clock) está aquí; lo que va una vez por robot, en
spawn.launch.py, que se incluye tres veces.

Uso:
  ros2 launch mini_bot multi.launch.py
"""
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

ROBOTS = [
    # namespace,  x,     y,      yaw
    ('robot_a', '0.0', '0.0', '0.0'),
    ('robot_b', '0.0', '1.5', '0.0'),
    ('robot_c', '0.0', '-1.5', '0.0'),
]


def generate_launch_description():
    pkg = FindPackageShare('mini_bot')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])),
        launch_arguments={'gz_args': ['-r ', PathJoinSubstitution([pkg, 'worlds', 'workshop.sdf'])]}.items(),
    )

    # /clock una sola vez para todo el mundo, no una por robot.
    clock = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        output='screen',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
    )

    robots = [
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(PathJoinSubstitution([pkg, 'launch', 'spawn.launch.py'])),
            launch_arguments={'namespace': ns, 'x': x, 'y': y, 'yaw': yaw}.items(),
        )
        for ns, x, y, yaw in ROBOTS
    ]

    return LaunchDescription([gazebo, clock] + robots)
