import os
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.actions import TimerAction

# Caminhos do projeto
COSMUS_MODELS = '/home/drik/Projetos/_Mestrado/sim/COSMUS_gz2/models'
WORLD_FILE    = '/home/drik/Projetos/_Mestrado/sim/COSMUS_gz2/worlds/cosmus_airfield.sdf'
BRIDGE_YAML   = '/home/drik/Projetos/_Mestrado/sim/COSMUS_gz2/config/ros_gz_bridge.yaml'

def generate_launch_description():
    ros_gz_sim = get_package_share_directory('ros_gz_sim')

    set_gz_resource_path = AppendEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=COSMUS_MODELS
    )

    gz_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': f'-r -s -v2 {WORLD_FILE}',
            'on_exit_shutdown': 'true'
        }.items()
    )

    gz_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-g -v2'}.items()
    )

    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        output='screen',
        parameters=[{
            'config_file': BRIDGE_YAML,
            'use_sim_time': True
        }]
    )

    return LaunchDescription([
        set_gz_resource_path,
        gz_server,
        gz_client,
        TimerAction(period=5.0, actions=[bridge_node]),
    ])