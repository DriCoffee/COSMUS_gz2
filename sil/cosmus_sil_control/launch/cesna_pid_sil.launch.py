import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    package_share_dir = get_package_share_directory('cosmus_sil_control')
    config_file = os.path.join(package_share_dir, 'config', 'cesna_pid.yaml')

    cesna_pid_controller = Node(
        package='cosmus_sil_control',
        executable='cesna_pid_controller',
        name='cesna_pid_controller',
        output='screen',
        parameters=[config_file]
    )

    mission_node = Node(
        package='cosmus_sil_control',
        executable='mission_node',
        name='mission_node',
        output='screen'
    )

    return LaunchDescription([
        cesna_pid_controller,
        mission_node,
    ])