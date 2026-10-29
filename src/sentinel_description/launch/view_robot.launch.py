import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    pkg_sentinel_description = get_package_share_directory('sentinel_description')

    default_model_path = os.path.join(pkg_sentinel_description, 'urdf', 'sentinel.urdf.xacro')
    default_rviz_path = os.path.join(pkg_sentinel_description, 'rviz', 'view_robot.rviz')

    use_sim_time = LaunchConfiguration('use_sim_time')
    model = LaunchConfiguration('model')
    rviz_config = LaunchConfiguration('rviz_config')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )

    declare_model_cmd = DeclareLaunchArgument(
        name='model',
        default_value=default_model_path,
        description='Absolute path to robot urdf/xacro file'
    )

    declare_rviz_config_cmd = DeclareLaunchArgument(
        name='rviz_config',
        default_value=default_rviz_path,
        description='Absolute path to RViz configuration file'
    )

    robot_description = ParameterValue(
        Command(['xacro ', model]),
        value_type=str
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': robot_description
        }]
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config]
    )

    return LaunchDescription([
        declare_use_sim_time_cmd,
        declare_model_cmd,
        declare_rviz_config_cmd,
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])

