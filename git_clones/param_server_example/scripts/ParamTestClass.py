#!/usr/bin/env python

import rospy

from rospy.numpy_msg import numpy_msg
import numpy as np

import Tkinter as tki
import ttk

from dynamic_reconfigure.server import Server
from param_server_example.cfg import ParamServerExampleConfig

class Parameter_server_test:

    #------------------------------------------------------#
    #------------------------------------------------------#
    #------------------------------------------------------#

    def __init__(self):

        self.localParam = None
        self.globalParam = None

        #--------#
        # Load parameters from parameter server
        self.getParameters()

        # Check that the parameters where correctly loaded
        if(self.localParam is None or self.globalParam is None):
            rospy.signal_shutdown("Parameters not declared")
        else:
            rospy.loginfo("Parameters found")

        #-------------#
        #-------------#
        # GUI init
        self.image = None
        self.imageCounter = 0
        
        self.root = tki.Tk()
        self.root.title("Parameter Server Test")

        self.LabelFrame_1 = tki.LabelFrame(self.root, text='Parameters', width=300, height=300)
        self.LabelFrame_1.grid(row=0, column=0, columnspan=3, rowspan=3,sticky="w e n s",padx=10, pady=10)

        # Create Label and textbox1 for local parameter
        self.Label1 = tki.Label(self.LabelFrame_1, text = "Local Parameter") 
        self.Label1.grid(row=0, column=0, columnspan=1, rowspan=1,sticky="w e n s",padx=10, pady=10)

        self.textbox1 = tki.Entry(self.LabelFrame_1)
        self.textbox1.grid(row=0, column=1, columnspan=1, rowspan=1,sticky="w e n s",padx=10, pady=10)

        self.textbox1.delete(0, tki.END)
        self.textbox1.insert(0, str(self.localParam))
        self.textbox1.config(state="readonly")

        # Create Label and textbox for global parameter
        self.Label2 = tki.Label(self.LabelFrame_1, text = "Global Parameter") 
        self.Label2.grid(row=1, column=0, columnspan=1, rowspan=1,sticky="w e n s",padx=10, pady=10)

        self.textbox2 = tki.Entry(self.LabelFrame_1)
        self.textbox2.grid(row=1, column=1, columnspan=1, rowspan=1,sticky="w e n s",padx=10, pady=10)

        self.textbox2.delete(0, tki.END)
        self.textbox2.insert(0, str(self.globalParam))
        self.textbox2.config(state="readonly")

        #---------#
        # Link shutdown function
        rospy.on_shutdown(self.Close)

        #--------#
        #--------#
        # Link DynamicReconfigure Callback
        srv = Server(ParamServerExampleConfig, self.DynConfCB)

    #-------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------#
    # Function to get parameters
    def getParameters(self):

        if rospy.has_param('~local_param'):     self.localParam = rospy.get_param('~local_param')
        if rospy.has_param("global_param"):     self.globalParam = rospy.get_param("global_param")

    #-------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------#
    def Close(self):
        self.root.quit()
        return 1

    #-------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------#
    def DynConfCB(self, config, level):
        print(config)

        #self.localParam = config.local_param
        #self.globalParam = config.global_param
        
        if rospy.has_param('~local_param'):     self.localParam = rospy.get_param('~local_param')
        if rospy.has_param("global_param"):     self.globalParam = rospy.get_param("global_param")

        rospy.set_param('global_param', config.global_param)

        self.updateGUI()

        return config

    #-------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------#
    def updateGUI(self):
        
        self.textbox1.config(state=tki.NORMAL)
        self.textbox1.delete(0, tki.END)
        self.textbox1.insert(0, str(self.localParam))
        self.textbox1.config(state="readonly")

        self.textbox2.config(state=tki.NORMAL)
        self.textbox2.delete(0, tki.END)
        self.textbox2.insert(0, str(self.globalParam))
        self.textbox2.config(state="readonly")
