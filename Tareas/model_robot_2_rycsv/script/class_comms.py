#!/usr/bin/python

import rospy

from std_msgs.msg import Float64
from geometry_msgs.msg import Twist

import numpy
from   rospy.numpy_msg import numpy_msg

from class_model import Model_robot

class Communication_ROS:

    def __init__(self):

        # Atributos
        self.topicSubs = "/cmd_vel"

        self.topicPubFront = "/front_wheel_ctrl/command"
        self.topicPubLeft  = "/left_wheel_ctrl/command"
        self.topicPubRight = "/right_wheel_ctrl/command"
        self.topicPubBack = "/back_wheel_ctrl/command"

        self.vel_X   = 0.0
        self.vel_Y   = 0.0
        self.vel_ang = 0.0

        self.flagCmd = False

        self.modelo = Model_robot()

        # Publicador
        self.pubVelFront = rospy.Publisher(self.topicPubFront, numpy_msg(Float64), queue_size=10)
        self.pubVelLeft  = rospy.Publisher(self.topicPubLeft, numpy_msg(Float64), queue_size=10)
        self.pubVelRight = rospy.Publisher(self.topicPubRight, numpy_msg(Float64), queue_size=10)
        self.pubVelBack  = rospy.Publisher(self.topicPubBack, numpy_msg(Float64), queue_size=10)

        # Subscriptor
        rospy.Subscriber(self.topicSubs, numpy_msg(Twist), self.cmd_vel_CB, queue_size=10)

        # Polling con callbacks
        rate = rospy.Rate(50)
        while(not rospy.is_shutdown()):

            if(self.flagCmd):
                self.flagCmd = False
                vel2Send = self.modelo.calcVelWheels(self.vel_X, self.vel_Y, self.vel_ang)

                # Para rueda front
                msg = Float64()
                msg.data = vel2Send[0]
                self.pubVelFront.publish(msg)

                # Para rueda right
                msg = Float64()
                msg.data = vel2Send[1]
                self.pubVelRight.publish(msg)

                # Para rueda back
                msg = Float64()
                msg.data = vel2Send[2]
                self.pubVelBack.publish(msg)

                # Para rueda left
                msg = Float64()
                msg.data = vel2Send[3]
                self.pubVelLeft.publish(msg)

            rate.sleep()


    #---------------------------------------------------------------------------------#
    #---------------------------------------------------------------------------------#
    # Funcion de cb para el comando de velocidad
    def cmd_vel_CB(self, cmd):

        rospy.loginfo("received cmd message")

        self.vel_X = cmd.linear.x
        self.vel_Y = cmd.linear.y
        self.vel_ang = cmd.angular.z

        self.flagCmd = True