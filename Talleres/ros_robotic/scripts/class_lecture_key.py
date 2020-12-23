#!/usr/bin/python

import rospy
import numpy as np
import sys, select, termios, tty

from   std_msgs.msg         import Float64
from   geometry_msgs.msg    import Twist
from   rospy.numpy_msg      import numpy_msg

from   class_model          import Model_robot

class LECTURE_KEY:  

    def __init__(self):
        self.vel = Twist()

        key_timeout = rospy.get_param("~key_timeout", 0.0)
        if key_timeout == 0.0:
                key_timeout = None

        self.modelo = Model_robot()

        self.nameTopicPub1 = "/right_wheel_ctrl/command"
        self.nameTopicPub2 = "/left_wheel_ctrl/command"
        self.nameTopicPub3 = "/vel_ddrobot"

        self.pub1 = rospy.Publisher(self.nameTopicPub1,Float64,queue_size=10)
        self.pub2 = rospy.Publisher(self.nameTopicPub2,Float64,queue_size=10)
        self.pub3 = rospy.Publisher(self.nameTopicPub3,numpy_msg(Twist),queue_size=10)

        rate = rospy.Rate(10)
        vel_L = 0
        vel_R = 0


        while (not rospy.is_shutdown()):
            key = getKey(self,key_timeout)
            if key in moveBindings.keys():
                if ((key == 'q') | (key == 'Q')):
                    break
                elif (key == ' '):
                    vel_R = moveBindings[key][0]
                    vel_L = moveBindings[key][1]
                else:
                    vel_R = vel_R + moveBindings[key][0]
                    vel_L = vel_L + moveBindings[key][1]
                
                if (vel_R >= 29):
                    vel_R = 29
                elif (vel_R <= -29):
                    vel_R = -29
                
                if (vel_L >= 29):
                    vel_L = 29
                elif (vel_L <= -29):
                    vel_L = -29

            self.pub1.publish(vel_R)
            self.pub2.publish(vel_L)

            vel2send = self.modelo.calcVel(vel_R, vel_L)
            self.vel.linear.x = vel2send[0]
            self.vel.linear.y = vel2send[1]
            self.vel.angular.z = vel2send[2]
            self.pub3.publish(self.vel)
            rate.sleep()
                

settings = termios.tcgetattr(sys.stdin)

def getKey(self,key_timeout):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], key_timeout)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

moveBindings = {
        'a':(1.0,-1.0),
        'A':(1.0,-1.0),
        'd':(-1.0,1.0),
        'D':(-1.0,1.0),
        'w':(1.0,1.0),
        'W':(1.0,1.0),
        's':(-1.0,-1.0),
        'S':(-1.0,-1.0),
        ' ':(0.0,0.0),
        'q':(0.0,0.0),
        'Q':(0.0,0.0)
    }