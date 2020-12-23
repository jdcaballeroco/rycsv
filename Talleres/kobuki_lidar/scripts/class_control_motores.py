#!/usr/bin/python

import rospy

from   geometry_msgs.msg    import Twist

class CONTROL_MOTORES:  

    def __init__(self):
        self.order = Twist()
        rospy.Subscriber("/vel_order",Twist,self.callback)
        self.pub = rospy.Publisher("/mobile_base/commands/velocity",Twist,queue_size=50)

        rate = rospy.Rate(10)

        while (not rospy.is_shutdown()):
            self.control_ruedas()
            rate.sleep()
    
    def callback(self,order):
        self.order = order

    def control_ruedas(self):
        self.pub.publish(self.order)
