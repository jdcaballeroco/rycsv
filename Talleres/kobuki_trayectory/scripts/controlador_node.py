#!/usr/bin/python

import rospy
from class_controlador_polar  import CONTROL
from class_controlador2_lineal import CONTROL_1

# Init of program
if __name__ == '__main__':

    rospy.init_node('CNTL_node', anonymous=True)
    rospy.loginfo("Creando nodo controlador...")
    CONTROL()  ##polar
    #CONTROL_1() ##lineal
    rospy.spin()