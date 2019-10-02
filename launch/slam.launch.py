import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable
from launch_ros.actions import Node


def generate_launch_description():

    rviz_config_dir = os.path.join(get_package_share_directory('omni_ros2_slam'), 'rviz', 'omni_ros2_slam.rviz')

    return LaunchDescription([
        SetEnvironmentVariable('RCUTILS_CONSOLE_STDOUT_LINE_BUFFERED', '1'),
        Node(
            package='cartographer_ros', 
            node_executable='cartographer_node', 
            output='screen',
            arguments=[
                '-configuration_directory', get_package_share_directory('omni_ros2_slam') + '/config',
                '-configuration_basename', 'cartographer.lua'
                ],
            remappings=[
                ('imu', 'imu/data')
                ],
            ),
        Node(
            package='cartographer_ros',
            node_executable='occupancy_grid_node',
            output='screen',
            arguments=['-resolution', '0.02', '-publish_period_sec', '1.0']
            ),

        Node(
            package='rviz2',
            node_executable='rviz2',
            arguments=['-d', rviz_config_dir],
            parameters=[{'use_sim_time':'false'}],
            output='screen'),

        ])
