#!/usr/bin/python

import rospy
from arbol import Arbol

# Init of program
if __name__ == '__main__':
    rospy.init_node('arbolito', anonymous=True)
    rospy.loginfo("Creando nodo arbol...")
    arbol = Arbol(1,"raiz",1)
    arbol.agregarElemento(2,1)
    arbol.agregarElemento(3,1)
    arbol.agregarElemento(4,2)
    arbol.agregarElemento(5,4)
    arbol.agregarElemento(6,3)
    arbol.agregarElemento(7,3)

    arbol_imprimir = arbol
    array = []
    for subarbol in arbol_imprimir.hijos:
        array.append(subarbol.elemento)
    if(arbol_imprimir.padre=="raiz"):
        rospy.loginfo([[arbol_imprimir.padre],arbol_imprimir.elemento,arbol_imprimir.distancia,array])
    else:
        rospy.loginfo([[arbol_imprimir.padre.elemento],arbol_imprimir.elemento,arbol_imprimir.distancia,array])

    for subarbol in arbol_imprimir.hijos:
        arbol_imprimir = arbol.buscarSubarbol(subarbol.elemento)
        array = []
        for subarbol in arbol_imprimir.hijos:
            array.append(subarbol.elemento)
        if(arbol_imprimir.padre=="raiz"):
            rospy.loginfo([[arbol_imprimir.padre],arbol_imprimir.elemento,arbol_imprimir.distancia,array])
        else:
            rospy.loginfo([[arbol_imprimir.padre.elemento],arbol_imprimir.elemento,arbol_imprimir.distancia,array])

    arbol.eliminarElemento(7)

    arbol_imprimir = arbol
    array = []
    for subarbol in arbol_imprimir.hijos:
        array.append(subarbol.elemento)
    if(arbol_imprimir.padre=="raiz"):
        rospy.loginfo([[arbol_imprimir.padre],arbol_imprimir.elemento,array])
    else:
        rospy.loginfo([[arbol_imprimir.padre.elemento],arbol_imprimir.elemento,array])

    for subarbol in arbol_imprimir.hijos:
        arbol_imprimir = arbol.buscarSubarbol(subarbol.elemento)
        array = []
        for subarbol in arbol_imprimir.hijos:
            array.append(subarbol.elemento)
        if(arbol_imprimir.padre=="raiz"):
            rospy.loginfo([[arbol_imprimir.padre],arbol_imprimir.elemento,array])
        else:
            rospy.loginfo([[arbol_imprimir.padre.elemento],arbol_imprimir.elemento,array])

    camino = arbol.hoja2padre(5)
    rospy.loginfo(camino)
    profundidad = arbol.profundidad(1)
    rospy.loginfo(profundidad)
    grado = arbol.grado(1)
    rospy.loginfo(grado)
    #rospy.spin()