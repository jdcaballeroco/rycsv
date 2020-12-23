#!/usr/bin/python

import math
import rospy
import numpy as np
from tf.transformations import euler_from_quaternion

import tf2_ros
import tf2_msgs.msg
import tf_conversions

from    geometry_msgs.msg   import Twist
from    nav_msgs.msg        import Odometry
from    std_msgs.msg        import Bool

class CONTROL:  

    last_x_value=0
    last_w_value=0

    def __init__(self):
        #PARAMETROS
        self.f = rospy.get_param("/f")
        self.vel_cruc = rospy.get_param("/vel_cruc")
        self.w_max = rospy.get_param("/w_max")
        self.Kp = rospy.get_param("/Kp")
        self.num_coor_tray = 0                  #NUMERO DE COORDENADAS DE LA TRAYECTORIA QUE SE CALCULA EN TF_NODE

        #CREACION DEL LISTENER
        self.pub_tf = rospy.Publisher("/tf", tf2_msgs.msg.TFMessage, queue_size=1)
        self.tfBuffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tfBuffer)

        #COMUNICACION ENTRE EL CONTROLADOR_NODE Y KOBUKI
        self.pub1 = rospy.Publisher("/mobile_base/commands/velocity",Twist,queue_size=50)
        rospy.Subscriber("/odom",Odometry,self.callback_odom)

        #CREACION DEL NODO DE COMUNICACION ENTRE TF_NODE Y CONTROLADOR_NODE
        self.pub_next_coord = rospy.Publisher("/next_coord", Bool, queue_size=1)
        
        #MENSAJES PARA PUBLICACION EN TOPICOS
        self.next = Bool()                      #VARIABLE PARA LA COMUNICACION ENTRE TF_NODE Y CONTROLADOR_NODE
        self.next.data = True
        self.newmsg = Twist()

        rate = rospy.Rate(self.f)

        self.j=0                                #VARIABLE QUE INDICA CUANTOS CAMBIOS DE COORDENADAS SE HAN REALIZADO
        self.MTH = [0]                          #MATRIZ DE TRANSFORMACION ODOM-GOAL

        while(self.num_coor_tray == 0):
            self.num_coor_tray = rospy.get_param("/num_coor_tray")

        rospy.loginfo("Nodo controlador inicio correctamente ")
        
        while (not rospy.is_shutdown()):
            if(self.j < self.num_coor_tray):
                self.j = self.j + 1
                MTH = [0]
                while(len(self.MTH) == 1):
                    self.MTH = self.Calcular_MTH()
                    rate.sleep()

                self.rho    = 1
                self.theta  = 0
                while (self.rho >= self.vel_cruc/self.Kp[0]+0.05):
                    self.MTH = self.Calcular_MTH()
                    if(len(self.MTH) != 1):
                        self.Controlador_polar()
                    
                    rate.sleep()
                
                self.pub_next_coord.publish(self.next)
                rate.sleep()

    def callback_odom(self,data):               #FUNCION PARA CALCULAR LA ORIENTACION MEDIANTE EL TOPICO DE ODOMETRIA DEL KOBUKI
        a = euler_from_quaternion([data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w])
        self.theta = a[2]
        #rospy.loginfo(data.twist.twist.linear.x)
    
    def Calcular_MTH(self):                     #FUNCION PARA CALCULAR LA MATRIZ DE TRANSFORMACION ENTRE KOBUKI-GOAL
        try:
            trans_base_marker = self.tfBuffer.lookup_transform("base_footprint", "Goal", rospy.Time())
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rospy.logwarn("Error trying to look for transform")
            return [0]
        quat_from_ROS = np.array([trans_base_marker.transform.rotation.x, \
                                    trans_base_marker.transform.rotation.y, \
                                    trans_base_marker.transform.rotation.z, \
                                    trans_base_marker.transform.rotation.w])
        rt_mat_from_ROS = tf_conversions.transformations.quaternion_matrix(quat_from_ROS)
        MTH_GOAL = rt_mat_from_ROS.copy()
        MTH_GOAL[0,3] = trans_base_marker.transform.translation.x
        MTH_GOAL[1,3] = trans_base_marker.transform.translation.y
        
        return MTH_GOAL
    
    def Controlador_polar(self):                #FUNCION PARA EL CONTROL EN SISTEMA POLAR DEL KOBUKI
        self.dx     =  self.MTH[0,3]
        self.dy     =  self.MTH[1,3]
        self.rho    =  math.sqrt(self.dx**2+self.dy**2)
        self.beta   = -math.atan2(self.dy,self.dx)
        self.alpha  = -self.theta - self.beta

        self.newmsg.linear.x    = self.Kp[0]*self.rho
        self.newmsg.linear.y    = 0
        self.newmsg.linear.z    = 0
        self.newmsg.angular.x   = 0
        self.newmsg.angular.y   = 0
        self.newmsg.angular.z   = self.Kp[1]*self.alpha + self.Kp[2]*self.beta
        
        if self.newmsg.linear.x > self.vel_cruc:
            self.newmsg.linear.x = self.vel_cruc
        elif self.newmsg.linear.x < -self.vel_cruc:
            self.newmsg.linear.x = -self.vel_cruc

        if self.newmsg.angular.z > self.w_max:
            self.newmsg.angular.z = self.w_max
        elif self.newmsg.angular.z < -self.w_max:
            self.newmsg.angular.z = -self.w_max
        
        self.last_x_value = self.newmsg.linear.x
        self.last_w_value = self.newmsg.angular.z
        self.pub1.publish(self.newmsg)

