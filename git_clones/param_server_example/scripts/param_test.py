#!/usr/bin/python

import rospy

from rospy.numpy_msg import numpy_msg
import numpy as np

import Tkinter as tki
import ttk

from dynamic_reconfigure.server import Server
from param_server_example.cfg import ParamServerExampleConfig

from ParamTestClass import Parameter_server_test

#-----------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------#

if __name__ == '__main__':

    # Firt init the node and then the object to correctly find the parameters
    rospy.init_node('param_server_test', anonymous=True)
    rospy.loginfo("Node init")

    ParamTestGUI = Parameter_server_test()
    ParamTestGUI.root.after(100, ParamTestGUI.updateGUI())
    ParamTestGUI.root.mainloop()
        
    try:
        rospy.spin()
        ParamTestGUI.root.update_idletasks()
        ParamTestGUI.root.update()
        ParamTestGUI.updateGUI()
    except KeyboardInterrupt:
        print("Shutting down")
        rospy.signal_shutdown("Request shutdown")
