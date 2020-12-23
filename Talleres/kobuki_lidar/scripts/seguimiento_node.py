#!/usr/bin/python

import rospy
from class_seguimiento_polar  import POLAR

# Init of program
if __name__ == '__main__':

    rospy.init_node('CNTL_node', anonymous=True)
    rospy.loginfo("Creando nodo seguimiento...")
    POLAR()
    rospy.spin()