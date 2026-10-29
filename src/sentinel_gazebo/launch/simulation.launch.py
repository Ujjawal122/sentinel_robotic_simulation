import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    pkg_sentinel_gazebo = get_package_share_directory('sentinel_gazebo')
    pkg_sentinel_description = get_package_share_directory('sentinel_description')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    default_world = os.path.join(pkg_sentinel_gazebo, 'worlds', 'sentinel_world.sdf')
    default_bridge_config = os.path.join(pkg_sentinel_gazebo, 'config', 'ros_gz_bridge.yaml')
    default_xacro = os.path.join(pkg_sentinel_description, 'urdf', 'sentinel.urdf.xacro')
    default_rviz_config = os.path.join(pkg_sentinel_description, 'rviz', 'view_robot.rviz')

    world = LaunchConfiguration('world')
    rviz = LaunchConfiguration('rviz')
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    z = LaunchConfiguration('z')
    yaw = LaunchConfiguration('yaw')

    declare_world_cmd = DeclareLaunchArgument(
        name='world',
        default_value=default_world,
        description='Full path to world SDF file'
    )

    declare_rviz_cmd = DeclareLaunchArgument(
        name='rviz',
        default_value='true',
        description='Open RViz alongside simulation'
    )

    declare_x_cmd = DeclareLaunchArgument(name='x', default_value='0.0', description='Initial X position')
    declare_y_cmd = DeclareLaunchArgument(name='y', default_value='0.0', description='Initial Y position')
    declare_z_cmd = DeclareLaunchArgument(name='z', default_value='0.05', description='Initial Z position')
    declare_yaw_cmd = DeclareLaunchArgument(name='yaw', default_value='0.0', description='Initial Yaw angle')

    # Convert Xacro to URDF string
    robot_description = ParameterValue(
        Command(['xacro ', default_xacro]),
        value_type=str
    )

    # Robot State Publisher (Publishes /tf based on URDF and joint_states)
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'robot_description': robot_description
        }]
    )

    # Start Gazebo Sim (Harmonic)
    gazebo_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': PathJoinSubstitution(['-r ', world])}.items()
    )

    # Spawn Robot Entity in Gazebo from /robot_description
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=[
            '-name', 'sentinel',
            '-topic', '/robot_description',
            '-x', x,
            '-y', y,
            '-z', z,
            '-Y', yaw
        ]
    )

    # ROS <-> Gazebo Bridge
    ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        output='screen',
        parameters=[{
            'config_file': default_bridge_config,
            'use_sim_time': True
        }]
    )

    # RViz2 visualization
    rviz_node = Node(
        condition=IfCondition(rviz),
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', default_rviz_config],
        parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([
        declare_world_cmd,
        declare_rviz_cmd,
        declare_x_cmd,
        declare_y_cmd,
        declare_z_cmd,
        declare_yaw_cmd,
        gazebo_sim,
        robot_state_publisher_node,
        spawn_robot,
        ros_gz_bridge,
        rviz_node
    ])

