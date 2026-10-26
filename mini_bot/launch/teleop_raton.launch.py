"""Teleop con el ratón, en RViz, para cualquier robot con diff_drive_controller.

Son los dos nodos del teleop de mast.launch.py, sueltos para usarlos con un robot importado:

  ros2 launch mini_bot teleop_raton.launch.py namespace:=summit_a

En RViz hace falta un display InteractiveMarkers con el namespace <namespace>/twist_server.
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    ns = LaunchConfiguration('namespace')
    frame = LaunchConfiguration('frame')

    args = [
        DeclareLaunchArgument('namespace', default_value=''),
        # El link al que se pegan las flechas: el base_footprint del robot, con su prefijo si lo tiene.
        DeclareLaunchArgument('frame', default_value='base_footprint'),
    ]

    # marker_server pinta las flechas y publica Twist en mouse_vel al arrastrarlas (hasta 0,5 m/s).
    twist_marker = Node(
        package='interactive_marker_twist_server',
        executable='marker_server',
        name='twist_server_node',
        namespace=ns,
        output='screen',
        parameters=[{
            'link_name': frame,
            'linear_scale': {'x': 0.5},
            'max_positive_linear_velocity': {'x': 0.5},
            'max_negative_linear_velocity': {'x': -0.5},
            'use_sim_time': True,
        }],
        remappings=[('cmd_vel', 'mouse_vel')],
    )

    # diff_drive_controller solo acepta TwistStamped: twist_stamper le pone la cabecera.
    twist_stamper = Node(
        package='twist_stamper',
        executable='twist_stamper',
        namespace=ns,
        output='screen',
        parameters=[{'frame_id': frame, 'use_sim_time': True}],
        remappings=[('cmd_vel_in', 'mouse_vel'), ('cmd_vel_out', 'diff_drive_controller/cmd_vel')],
    )

    return LaunchDescription(args + [twist_marker, twist_stamper])
