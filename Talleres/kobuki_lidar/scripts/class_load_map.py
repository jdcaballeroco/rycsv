#!/usr/bin/env python

import rospy

from rospy.numpy_msg import numpy_msg
import numpy as np
import numpy

import cv2
from cv_bridge import CvBridge, CvBridgeError

import sys
import tf2_ros

from nav_msgs.msg import OccupancyGrid
from nav_msgs.msg import MapMetaData

from geometry_msgs.msg import Pose
from geometry_msgs.msg import TransformStamped

from sensor_msgs.msg import Image

class Map_loader:

    #------------------------------------------------------#
    # Callback function for image
    def map_cb(self, data):

        self.map_width = data.info.width
        self.map_height = data.info.height
        self.map_res = data.info.resolution
        self.map_origin = data.info.origin

        self.datos_send_mapa.map_load_time = data.info.map_load_time
        self.datos_send_mapa.resolution = data.info.resolution
        self.datos_send_mapa.width = data.info.width
        self.datos_send_mapa.height = data.info.height
        self.datos_send_mapa.origin = data.info.origin
        
        #print(self.map_res)
        #print("Map origin")
        #print(self.map_origin.position.x)
        #print(self.map_origin.position.y)
        #print(self.map_origin.position.z)

        #print(self.map_origin.orientation.x)
        #print(self.map_origin.orientation.y)
        #print(self.map_origin.orientation.z)
        #print(self.map_origin.orientation.w)

        self.map = data.data

        #print("Map")
        #print(self.map.shape)
        #print(self.map)

        self.map = np.resize(self.map, [self.map_height, self.map_width])

        #print(self.map.shape)
        #print(self.map)
        #print([()])

        # Create image publisher
        self.image_pub = rospy.Publisher("map_image", Image, queue_size=1)


    #------------------------------------------------------#
    #------------------------------------------------------#
    #------------------------------------------------------#

    def __init__(self):

        self.map_width = None
        self.map_height = None
        self.map_res = None
        self.map_origin = None
        self.p=0
        self.t=0
        self.v=0
        self.u=0
        self.map = None
        self.datos_send_mapa = MapMetaData()
        self.new_data_map = OccupancyGrid()

        # Create CV bridge
        self.bridge = CvBridge()

        # Create image subscriber
        self.image_sub = rospy.Subscriber("/map", numpy_msg(OccupancyGrid), self.map_cb)
        
        ##Publicador del costmap
        self.pub_costmap = rospy.Publisher("/costmap", numpy_msg(OccupancyGrid), queue_size = 10)

        self.image_pub = None

        self.spin()

    #------------------------------------------------------#
    # Spin function
    def spin(self):

        rate = rospy.Rate(30)

        tfBuffer = tf2_ros.Buffer()
        listener = tf2_ros.TransformListener(tfBuffer) 

        while (not rospy.is_shutdown()):

            if(self.image_pub is not None):

                cv_image = np.zeros((self.map.shape[0],self.map.shape[1]), dtype = np.uint8)
                base_image = np.zeros((self.map.shape[0],self.map.shape[1]), dtype = np.uint8)
                cv_image[:,:] = self.map.copy() ##Se recibe la imagen del mapa
                base_image[:,:] = self.map.copy()
                new_img=cv_image
                """
                if self.p==0:
                    self.p=1
                    print("-----------------------------------------")
                    print("cv_image")
                    print(cv_image)"""

                trans = TransformStamped()
                try:
                    trans = tfBuffer.lookup_transform("map", "odom", rospy.Time())
                except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
                    pass

                pos_x_robot = self.map.shape[1] - (-(trans.transform.translation.x/self.map_res) - (self.map_origin.position.x/self.map_res))
                pos_y_robot = self.map.shape[0] - ((trans.transform.translation.y/self.map_res) - (self.map_origin.position.y/self.map_res))
                pos_x_robot = np.uint(pos_x_robot) ##hallamos la posicion actual del robot x,y
                pos_y_robot = np.uint(pos_y_robot)

                #print("Pos robot: ", pos_x_robot, "  ", pos_y_robot)
                
                kernel = np.ones((7,7),np.uint8)    ##Revisar si dejar 5 o 4 porque se agranda mucho y puede no pasar 
                
                new_img = cv2.dilate(cv_image,kernel,iterations = 2)
                
                for j in range(self.map.shape[0]) :   
                    for k in range(self.map.shape[1]) :
                        if base_image [j][k] == 100:
                            new_img [j][k] = 255
                """
                if self.t==0:
                    self.t=1
                    print("-------------------------------------------")
                    print(kernel)
                    print("Imagen recien filtrada")
                    print(new_img)
                    print """

                
                ##cv_image = cv2.flip(cv_image, 0) #Reflejamos la imagen para poderla ver correctamente

                for r in range(self.map.shape[0]) :   
                    for s in range(self.map.shape[1]) :  
                        if  (new_img [r][s] == 255 ) and (base_image [r][s] != 255) :
                            #print("Enter")
                            new_img [r][s] = 100
                """
                if self.v == 0:
                    self.v = 1
                    print("-------------------------------------------")
                    print("Imagen vuelta a normal")
                    print(new_img)
                    print(self.datos_send_mapa)
                    print("-------------------------------------------")
                    print("Imagen base")
                    print(base_image)"""
    
                #image_rqt = cv2.flip(new_img, 0) #Reflejamos la imagen para poderla ver correctamente
                image_rqt = new_img

                #cv2.circle(image_rqt,(pos_x_robot,pos_y_robot), 8, (100,255,255), 1)

                try:
                    #self.image_pub.publish(self.bridge.cv2_to_compressed_imgmsg(cv_image2))
                    self.image_pub.publish(self.bridge.cv2_to_imgmsg(image_rqt, "mono8"))
                except CvBridgeError as e:
                    print(e)
                
                
                costmap = numpy.zeros((self.map.shape[0],self.map.shape[1]), dtype = numpy.int8)
                
                for r in range(self.map.shape[0]) :   
                    for s in range(self.map.shape[1]) :  
                        costmap [r][s]=image_rqt[r][s] ##Enviar costmap "al derecho"
                        #costmap [r][s]=new_img[r][s]    ##Enviar costmap como el original
                        if (base_image[r][s] == 255):
                            costmap[r][s] = -1   
                """
                if self.u==0:
                    self.u=1
                    print("-----------------------------------------")
                    print("costmap")
                    print(costmap) """
                

                self.send_mapa = np.resize(costmap, [1, self.map.shape [1]*self.map.shape [0]])
                """    
                print(self.send_mapa[0])
                print(self.map.shape [1]*self.map.shape [0])"""

                self.new_data_map.info = self.datos_send_mapa
                self.new_data_map.data = self.send_mapa [0]
                self.pub_costmap.publish(self.new_data_map)
                 
            rate.sleep()


        print("Shutting down")
        cv2.destroyAllWindows()

#-----------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------#

if __name__ == '__main__':

    # Firt init the node and then the object to correctly find the parameters
    rospy.init_node('map_loader', anonymous=True)
    Map_loader()
    