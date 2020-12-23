#!/usr/bin/python

import rospy
import math

import tf2_ros
import tf2_msgs.msg
from tf.transformations import quaternion_from_euler

from    geometry_msgs.msg   import TransformStamped
from    std_msgs.msg        import Bool

class TF:  

    def __init__(self):
        #PARAMETROS
        self.xi = rospy.get_param("/x")
        self.yi = rospy.get_param("/y")
        self.theta = - rospy.get_param("/theta")* 3.141592 / 180.0
        self.ds = rospy.get_param("/ds")
        self.f = rospy.get_param("/f")
        self.alpha = math.atan2(self.yi,self.xi)
        self.r = math.sqrt(self.xi**2+self.yi**2)

        #CREACION DE BROADCAST
        self.pub_tf = rospy.Publisher("/tf", tf2_msgs.msg.TFMessage, queue_size=5)
        self.broadcts  = tf2_ros.TransformBroadcaster()
        self.transform = TransformStamped()

        #SUBSCRIPCION AL TOPICO DE COMUNICACION ENTRE TF_NODE Y CONTROLADOR_NODE
        self.pub_meta = rospy.Publisher("/Meta", Bool, queue_size=5)
        rospy.Subscriber("/next_coord",Bool,self.callback_next)
        self.meta = Bool()                  
        self.meta.data = True

        rate = rospy.Rate(self.f)

        self.i = 0                              #VARIABLE PARA RECORRER MATRIZ SELF.TRAY (COORDENADAS DE TRAYECTORIA EN EL SISTEMA DEL ROBOT)

        self.num_coor_tray = 0
        while(self.num_coor_tray == 0):
            self.num_coor_tray = rospy.get_param("/num_coor_tray")
            self.update_TF_map()
            rate.sleep()    
        self.trayectoria = rospy.get_param("/trayectoria")

        rospy.loginfo("Nodo TF inicio correctamente ")
        
        while (not rospy.is_shutdown()):
            if(self.i < self.num_coor_tray):
                self.update_goal(self.i)
                self.update_prox_goal(self.i)
                self.update_TF_map()                
            else:
                self.pub_meta.publish(self.meta)

            if(self.num_coor_tray != rospy.get_param("/num_coor_tray")):
                self.num_coor_tray = rospy.get_param("/num_coor_tray")
                self.trayectoria = rospy.get_param("/trayectoria")
            rate.sleep()              

    def callback_next(self,data):               #FUNCION DE INTERRUPION PARA CAMBIAR A LA SIGUIENTE COORDENADA DE TRAYECTORIA
        if self.i < self.num_coor_tray:
            self.i = self.i + 1

    def update_goal(self, i):                   #FUNCION PARA ACTUALIZAR LA MATRIZ DE TRANSFORMACION ODOM-GOAL PERIODICAMENTE
        t = TransformStamped()
        t.header.frame_id = "map"
        t.header.stamp = rospy.Time.now()
        t.child_frame_id = "Goal"
        t.transform.translation.x = self.trayectoria[i][0]
        t.transform.translation.y = self.trayectoria[i][1]
        t.transform.translation.z = 0.0

        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        self.broadcts.sendTransform(t)  
    
    def update_prox_goal(self, i):                   #FUNCION PARA ACTUALIZAR LA MATRIZ DE TRANSFORMACION ODOM-GOAL PERIODICAMENTE
        if(i+1<self.num_coor_tray):
            t = TransformStamped()
            t.header.frame_id = "map"
            t.header.stamp = rospy.Time.now()
            t.child_frame_id = "Prox_goal"
            t.transform.translation.x = self.trayectoria[i+1][0]
            t.transform.translation.y = self.trayectoria[i+1][1]
            t.transform.translation.z = 0.0

            t.transform.rotation.x = 0.0
            t.transform.rotation.y = 0.0
            t.transform.rotation.z = 0.0
            t.transform.rotation.w = 1.0

            self.broadcts.sendTransform(t) 

    def update_TF_map(self):                    #FUNCION PARA ACTUALIZAR LA MATRIZ DE TRANSFORMACION ODOM-GOAL PERIODICAMENTE
        t = TransformStamped()
        t.header.frame_id = "map"
        t.header.stamp = rospy.Time.now()
        t.child_frame_id = "odom"
        t.transform.translation.x = self.r*math.cos(self.alpha)
        t.transform.translation.y = self.r*math.sin(self.alpha)
        t.transform.translation.z = 0.0

        quad = quaternion_from_euler(0,0,-self.theta)

        t.transform.rotation.x = quad[0]
        t.transform.rotation.y = quad[1]
        t.transform.rotation.z = quad[2]
        t.transform.rotation.w = quad[3]

        self.broadcts.sendTransform(t)  