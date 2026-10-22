"""Un mini_bot en un Gazebo que ya está corriendo (solución del extra "Multi-robot a mano").

Es sim.launch.py del ejercicio 5 sin lo que va una sola vez por mundo (Gazebo, /clock, RViz), y
con lo que cambia de un robot a otro sacado a argumentos.

Uso (con Gazebo ya abierto):
  ros2 launch mini_bot spawn.launch.py namespace:=robot_b y:=1.5
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
        DeclareLaunchArgument('namespace', default_value='robot_a'),
        DeclareLaunchArgument('x', default_value='0.0'),
        DeclareLaunchArgument('y', default_value='0.0'),
        DeclareLaunchArgument('yaw', default_value='0.0'),
    ]

    ns = LaunchConfiguration('namespace')

    # El prefijo sale del namespace: namespace + barra, como espera ros2_control.
    # Así no hay forma de pasar uno sin el otro.
    robot_description = ParameterValue(Command([
        'xacro ', PathJoinSubstitution([pkg, 'urdf', 'mini_bot.urdf.xacro']),
        ' namespace:=', ns,
        ' prefix:=', ns, '/',
    ]), value_type=str)

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace=ns,
        output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
    )

    # -name: el nombre del modelo en Gazebo no puede repetirse. Usamos el namespace.
    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        namespace=ns,
        output='screen',
        arguments=[
            '-topic', 'robot_description',
            '-name', ns,
            '-x', LaunchConfiguration('x'),
            '-y', LaunchConfiguration('y'),
            '-z', '0.15',
            '-Y', LaunchConfiguration('yaw'),
        ],
    )

    # El bridge.yaml del ejercicio 4 tiene los topics escritos a mano (/scan): con namespace ya no
    # existen, porque el robot publica en /robot_b/scan. Aquí el topic se construye con el namespace.
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        namespace=ns,
        output='screen',
        arguments=[['/', ns, '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan']],
        parameters=[{'use_sim_time': True}],
    )

    # 'controller_manager' sin barra: relativo, así que es /<ns>/controller_manager.
    spawners = [
        Node(
            package='controller_manager',
            executable='spawner',
            namespace=ns,
            output='screen',
            arguments=[controller, '--controller-manager', 'controller_manager'],
        )
        for controller in ('joint_state_broadcaster', 'diff_drive_controller')
    ]

    return LaunchDescription(args + [robot_state_publisher, spawn, bridge] + spawners)
