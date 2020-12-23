#!/usr/bin/python

import  math
import  rospy
import  numpy                   as      np
from    rospy.numpy_msg         import  numpy_msg
from    arbol                   import  Arbol
from    nav_msgs.msg            import  OccupancyGrid

class PLANNING:  

    def __init__(self):
        self.trayectoria = []
        self.leer_mapa = True
        self.coordenadas = rospy.get_param("/coordenadas")
        self.ds = rospy.get_param("/ds")
        self.pixel = rospy.get_param("/pixel")

        rospy.Subscriber("/costmap", numpy_msg(OccupancyGrid), self.read_map)

        self.i = 0                                                                              #VARIABLE PARA RECORRER MATRIZ DE TRAYECTORIA

        self.rate = rospy.Rate(10)
        self.rate1 = rospy.Rate(10000)

        while (not rospy.is_shutdown()):
            
            self.rate.sleep()
    
    def read_map(self, data):
        if(self.leer_mapa):
            self.leer_mapa = False

            self.map_width = data.info.width
            self.map_height = data.info.height
            self.map_res = data.info.resolution
            self.map_origin = data.info.origin
            self.map = data.data
            self.map = np.resize(self.map, [self.map_height, self.map_width]).tolist()
            self.map_tamano = (self.map_width)*(self.map_height)

            self.BFP(self.map,self.coordenadas)

    def BFP(self,map,coordenadas):
        self.trayectoria = []
        rospy.loginfo("Comenzando algoritmo BFP")
        for i in xrange(len(coordenadas)-1):
            rospy.loginfo("-----------------Proceso----------------------")
            tray = self.__BFP(map,coordenadas[i][:],coordenadas[i+1][:])
            if(i>0 and math.sqrt((self.trayectoria[-1][0]-tray[0][0])**2+(self.trayectoria[-1][1]-tray[0][1])**2)<self.ds*3/4):
                tray.pop(0)

            for j in tray:
                self.trayectoria.append(j)
            rospy.set_param('/trayectoria', self.trayectoria)
            rospy.set_param('/num_coor_tray', len(self.trayectoria))
            
    def __BFP(self,map,coord1,coord2):
        tray = []
        j1 = int((coord1[0]-self.map_origin.position.x)/self.map_res)
        i1 = int((coord1[1]-self.map_origin.position.y)/self.map_res)
        j2 = int((coord2[0]-self.map_origin.position.x)/self.map_res)
        i2 = int((coord2[1]-self.map_origin.position.y)/self.map_res)
        rospy.loginfo([[i1,j1],[i2,j2]])

        if map[i1][j1] == 0 and map[i2][j2] == 0:
            self.abierto = []
            self.cerrado = []
            self.abierto.append(self.convert1(i1,j1))
            self.arbol = Arbol(self.convert1(i1,j1),"raiz",0)
            meta_encontrada = False
            while(~meta_encontrada):
                try:
                    casilla = self.abierto.pop(0)
                except:
                    casilla = []
                if(casilla != []):
                    self.cerrado.append(casilla)
                    for i in [0,-self.pixel,self.pixel]:
                        for j in [0,-self.pixel,self.pixel]:
                            if([i,j]!=[0,0] and ~meta_encontrada): #NO VERIFICAR LA CASILLA ACTUAL NI DIAGONALES
                                coor_casilla = self.convert2(casilla)
                                if(map[coor_casilla[0]+i][coor_casilla[1]+j]==0):
                                    casilla_ = self.convert1(coor_casilla[0]+i,coor_casilla[1]+j)
                                    if(not(casilla_ in self.abierto or casilla_ in self.cerrado)):                  #VERIFICAR SI YA SE ENCUENTRA EN PILA ABIERTA O CERRADA
                                        self.abierto.append(casilla_)
                                        self.arbol.agregarElemento(casilla_,casilla,math.sqrt(i**2+j**2)*self.map_res)
                                        coord_casilla_ = self.convert2(casilla_)
                                        if(abs(coord_casilla_[0]-i2)<self.pixel-1 and abs(coord_casilla_[1]-j2)<self.pixel-1):
                                            meta_encontrada = True
                                            rospy.loginfo("--------------------Meta encontrada----------------")
                                            tray_ = self.arbol.hoja2padre(casilla_)
                                            razon = int(self.ds/(self.map_res*self.pixel))

                                            tray_recortado = []                                                
                                            casilla_anterior = self.arbol.buscarSubarbol(tray_[razon-1])
                                            ultima_distancia = 0
                                            for i in range(len(tray_)-razon):
                                                casilla_actual = self.arbol.buscarSubarbol(tray_[razon+i])
                                                if(abs(casilla_anterior.distancia-casilla_actual.distancia)>self.ds):
                                                    casilla_anterior = casilla_actual
                                                    tray_recortado.append(tray_[razon+i])
                                                    ultima_distancia = casilla_actual.distancia
                                            
                                            if(abs(self.arbol.buscarSubarbol(tray_[-1]).distancia-ultima_distancia)<self.ds*3/4):
                                                tray_recortado.pop()
                                            
                                            tray_recortado.append(tray_[-1])

                                            for num in tray_recortado:
                                                coord_ = self.convert2(num)
                                                coord = [coord_[1]*self.map_res+self.map_origin.position.x,coord_[0]*self.map_res+self.map_origin.position.y]
                                                tray.append(coord)
                                            #rospy.loginfo(tray)
                                    else:
                                        if(self.arbol.buscarSubarbol(casilla_).distancia > self.arbol.buscarSubarbol(casilla).distancia+1):
                                            rospy.loginfo("Camino mas corto encontrado")
                                            casilla_hijos = self.arbol.buscarSubarbol(casilla_).hijos
                                            self.arbol.eliminarElemento(casilla_)
                                            self.arbol.agregarElemento(casilla_,casilla,math.sqrt(i**2+j**2)*self.map_res)
                                            self.arbol.buscarSubarbol(casilla_).hijos = casilla_hijos

                                            coord_casilla_ = self.convert2(casilla_)
                                            if(abs(coord_casilla_[0]-i2)<self.pixel-1 and abs(coord_casilla_[1]-j2)<self.pixel-1):
                                                meta_encontrada = True
                                                rospy.loginfo("--------------------Meta encontrada----------------")
                                                tray_ = self.arbol.hoja2padre(casilla_)
                                                razon = int(self.ds/(self.map_res*self.pixel))

                                                tray_recortado = []                                                
                                                casilla_anterior = self.arbol.buscarSubarbol(tray_[razon-1])
                                                ultima_distancia = 0
                                                for i in range(len(tray_)-razon):
                                                    casilla_actual = self.arbol.buscarSubarbol(tray_[razon+i])
                                                    if(abs(casilla_anterior.distancia-casilla_actual.distancia)>self.ds):
                                                        casilla_anterior = casilla_actual
                                                        tray_recortado.append(tray_[razon+i])
                                                        ultima_distancia = casilla_actual.distancia
                                                
                                                if(abs(self.arbol.buscarSubarbol(tray_[-1]).distancia-ultima_distancia)<self.ds*3/4):
                                                    tray_recortado.pop()
                                                
                                                tray_recortado.append(tray_[-1])

                                                for num in tray_recortado:
                                                    coord_ = self.convert2(num)
                                                    coord = [coord_[1]*self.map_res+self.map_origin.position.x,coord_[0]*self.map_res+self.map_origin.position.y]
                                                    tray.append(coord)
                                                #rospy.loginfo(tray)


                else:
                    rospy.loginfo("Fuera del alcance")
                    tray = []
                    meta_encontrada = True
                
                if(meta_encontrada):
                    break
                
        else:
            tray = []
            rospy.loginfo("Coordenadas dentro de una pared")

        return tray

    def convert1(self,i,j):
        return self.map_width*i+j
    
    def convert2(self,num):
        return [num/self.map_width,num%self.map_width]
