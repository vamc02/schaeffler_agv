#!/usr/bin/env python

import os
import sys
import rospy
import roslaunch
import xacro
import roslib.packages


def main():
    # Initialize the ROS node
    rospy.init_node('custom_launch_script', anonymous=True)

    # Check if 'use_sim_time' argument is provided
    use_sim_time = rospy.get_param('~use_sim_time', False)

    # Process the Xacro file to generate the URDF
    try:
        pkg_path = roslib.packages.get_pkg_dir('schaeffler_robot_urdf')
        xacro_file = os.path.join(pkg_path, 'urdf/robot.urdf.xacro')

        if not os.path.exists(xacro_file):
            rospy.logerr(f"Xacro file not found: {xacro_file}")
            sys.exit(1)

        # Parse the Xacro file
        robot_description_config = xacro.process_file(xacro_file).toxml()
        rospy.set_param('robot_description', robot_description_config)

    except Exception as e:
        rospy.logerr(f"Failed to process Xacro file: {e}")
        sys.exit(1)

    # Set use_sim_time parameter
    rospy.set_param('/use_sim_time', use_sim_time)

    # Launch the robot_state_publisher node
    try:
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)

        # Define the launch file
        rsp_launch_file = os.path.join(
            roslib.packages.get_pkg_dir("robot_state_publisher"),
            "launch",
            "robot_state_publisher.launch"
        )

        if not os.path.exists(rsp_launch_file):
            rospy.logerr(f"Launch file not found: {rsp_launch_file}")
            sys.exit(1)

        launch = roslaunch.parent.ROSLaunchParent(uuid, [rsp_launch_file])
        rospy.loginfo("Starting robot_state_publisher...")
        launch.start()
        rospy.spin()

    except Exception as e:
        rospy.logerr(f"Failed to launch robot_state_publisher: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

