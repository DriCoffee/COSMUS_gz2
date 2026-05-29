import os
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable, IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

# =========================================================
# AJUSTE ESSES CAMINHOS SE NECESSÁRIO
# =========================================================
WORLD_FILE  = '/home/drik/Projetos/_Mestrado/sim/COSMUS_gz2/worlds/cosmus_cessna.sdf'
MODELS_PATH = '/home/drik/Projetos/_Mestrado/sim/COSMUS_gz2/models'
# =========================================================

def generate_launch_description():
    ros_gz_sim = get_package_share_directory('ros_gz_sim')

    set_models_path = AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        MODELS_PATH
    )

    gz_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': f'-r -s -v4 {WORLD_FILE}',
            'on_exit_shutdown': 'true'
        }.items()
    )

    gz_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': '-g -v4'
        }.items()
    )

    return LaunchDescription([
        set_models_path,
        gz_server,
        gz_client,
    ])
