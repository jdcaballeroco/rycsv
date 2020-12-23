#!/usr/bin/python

import rospy
from class_planning import PLANNING

# Init of program
if __name__ == '__main__':

    rospy.init_node('planning', anonymous=True)

    rospy.loginfo("Iniciando Nodo de planeacion de trayectorias")

    PLANNING()

    rospy.spin()