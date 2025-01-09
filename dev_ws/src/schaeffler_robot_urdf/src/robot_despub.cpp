#include <ros/ros.h>
#include <std_msgs/String.h>

int main(int argc, char** argv) {
    // Initialize the ROS node
    ros::init(argc, argv, "robot_description_publisher");
    ros::NodeHandle nh;

    // Create a publisher for the /robot_description topic
    ros::Publisher robot_description_pub = nh.advertise<std_msgs::String>("/robot_description", 10);

    // Retrieve the robot_description parameter
    std::string robot_description;
    if (!nh.getParam("robot_description", robot_description)) {
        ROS_ERROR("Failed to retrieve 'robot_description' parameter from the parameter server.");
        return 1; // Exit if the parameter does not exist
    }

    // Log success
    ROS_INFO("Successfully retrieved 'robot_description' parameter.");

    // Publish the parameter value periodically
    ros::Rate loop_rate(1); // 1 Hz
    while (ros::ok()) {
        std_msgs::String msg;
        msg.data = robot_description;
        robot_description_pub.publish(msg);

        ROS_INFO_ONCE("Published 'robot_description' to /robot_description topic.");
        ros::spinOnce();
        loop_rate.sleep();
    }

    return 0;
}

