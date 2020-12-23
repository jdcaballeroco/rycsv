#!/usr/bin/python

import rospy

from class_comms import Communication_ROS
from class_model import Model_robot

# Init of program
if __name__ == '__main__':

    rospy.init_node('modelo_robot_rycsv', anonymous=True)

    rospy.loginfo("Node init")

    Communication_ROS()

    rospy.spin()