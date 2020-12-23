#!/usr/bin/python

class Arbol:
    def __init__(self, elemento, arbolPadre,distancia):
        self.padre = arbolPadre
        self.elemento = elemento
        self.distancia = distancia
        self.hijos = []

    def buscarElemento(self, elemento):
        if self.elemento == elemento:
            return True
        for subarbol in self.hijos:
            arbolencontrado = subarbol.buscarElemento(elemento)
            if (arbolencontrado):
                return True
        return False

    def buscarSubarbol(self, elemento):
        if self.elemento == elemento:
            return self
        for subarbol in self.hijos:
            arbolBuscado = subarbol.buscarSubarbol(elemento)
            if (arbolBuscado != None):
                return arbolBuscado
        return None
    
    def hoja2padre(self,elemento):                          #Cuenta elemento
        if self.elemento == elemento:
            return [elemento]
        arbol = self.buscarSubarbol(elemento)
        if (arbol != None):
            camino = self.hoja2padre(arbol.padre.elemento)
            camino.append(elemento)
            return camino
        return []

    def agregarElemento(self, elemento, elementoPadre,delta):
        subarbol = self.buscarSubarbol(elementoPadre)
        if (subarbol != None):
            subarbol.hijos.append(Arbol(elemento,subarbol,subarbol.distancia+delta))
            #print("Se agrego correctamente")
        #else:
            #print("Error al agregar")
    
    def eliminarElemento(self, elemento):
        if(self.elemento != elemento):
            subarbol_h = self.buscarSubarbol(elemento)
            if (subarbol_h != None):
                subarbol_p = self.buscarSubarbol(subarbol_h.padre.elemento)
                if (subarbol_p != None):
                    for sub_arbol_hijo in subarbol_p.hijos:
                        if(sub_arbol_hijo.elemento == elemento):
                            try:
                                subarbol_p.hijos.remove(sub_arbol_hijo)
                                print("Se elimino correctamente")
                                break
                            except:
                                print("Error al eliminar")
                        
        else:
            print("Error al eliminar")
    
    def profundidad(self,elemento):                         #Cuenta elemento
        subarbol = self.buscarSubarbol(elemento)
        if len(subarbol.hijos) == 0: 
            return 1
        prof_max = 0
        for subarbol_ in subarbol.hijos:
            prof_max = max(prof_max,subarbol_.profundidad(subarbol_.elemento))
        return 1 + prof_max

    def grado(self,elemento):                               #No cuenta elemento
        subarbol = self.buscarSubarbol(elemento)
        if (subarbol != None):
            rango = 0
            for subarbol_ in subarbol.hijos:
                rango = rango + subarbol_.grado(subarbol_.elemento)
            return rango + len(subarbol.hijos)
        return 0