from setuptools import find_packages, setup
from glob import glob

package_name = 'cosmus_sil_control'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='drik',
    maintainer_email='asbdtup@gmail.com',
    description='Software-in-the-loop controller package for Cessna fixed-wing in Gazebo using ROS 2.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'cesna_pid_controller = cosmus_sil_control.cesna_pid_controller:main',
            'mission_node = cosmus_sil_control.mission_node:main',
        ],
    },
)