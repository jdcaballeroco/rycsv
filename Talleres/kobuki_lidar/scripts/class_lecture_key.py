#!/usr/bin/python

from os import waitpid
import rospy
import numpy as np
import sys, select, termios, tty

from   std_msgs.msg         import Float64
from   geometry_msgs.msg    import Twist
from   rospy.numpy_msg      import numpy_msg

class LECTURE_KEY:  

    def __init__(self):
        self.order = Twist()

        key_timeout = rospy.get_param("~key_timeout", 0.0)
        if key_timeout == 0.0:
                key_timeout = None

        self.pub = rospy.Publisher("/vel_order",Twist,queue_size=50)

        rate = rospy.Rate(10)
        v = 0
        w = 0


        while (not rospy.is_shutdown()):
            key = getKey(self,key_timeout)
            if key in moveBindings.keys():
                if ((key == 'q') | (key == 'Q')):
                    break
                elif (key == ' '):
                    v = moveBindings[key][0]
                    w = moveBindings[key][1]
                else:
                    v = v + moveBindings[key][0]
                    w = w + moveBindings[key][1]
                
                if (v >= 3):
                    v = 3
                elif (v <= -3):
                    v = -3
                
                if (w >= 6.3):
                    w = 6.3
                elif (w <= -6.3):
                    w = -6.3

            self.order.linear.x = v
            self.order.angular.z = w
            self.pub.publish(self.order)
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
        's':(-0.1,0.0),
        'S':(-0.1,0.0),
        'w':(0.1,0.0),
        'W':(0.1,0.0),
        'a':(0.0,0.3),
        'A':(0.0,0.3),
        'd':(0.0,-0.3),
        'D':(0.0,-0.3),
        ' ':(0.0,0.0),
        'q':(0.0,0.0),
        'Q':(0.0,0.0)
    }