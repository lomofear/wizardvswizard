#!/usr/bin/python
# encoding: UTF-8

# Intento de tower defense por deavid
import random, math

import pygame

from enum import Enum # enumeraciones al estilo C

ACTIONS = Enum(
    'NULL','QUIT',
    'PLAYER1_SHOOT',
               )
ALIGN_LEFT = 0
ALIGN_CENTER = 1
ALIGN_RIGHT = 2

ALIGN_TOP = 4
ALIGN_MIDDLE = 8
ALIGN_BOTTOM = 16




def correlacion_vectores(x1,y1,x2,y2):
    """
    Coeficiente de correlación entre vectores. Básicamente, obtener un
    número entre 0 y 1 que nos indique la similitud de la dirección entre
    ambos. 0, van en direcciones que no tienen nada que ver, 1, van en la misma
    dirección.
    
    Para qué usamos esta función:
    - Enemigos: Al hacerlos seguir un camino (Path), es interesante que aceleren
      en las rectas. Para ello hay que saber si van en la dirección correcta o
      si están girando. Comparando su vector de dirección con "hacia donde queremos
      que vayan" sabemos si están en momento de aceleración o de frenado.
    """
    dist1 = math.hypot(x1,y1)
    dist2 = math.hypot(x2,y2)
    if dist1 < 0.00001 or dist2 < 0.00001:
        # no puede haber o calcularse relación de dirección si uno de los dos
        # ... no tiene distancia
        return 0
    
    # normalizar v1 y v2:
    x1 /= dist1
    y1 /= dist1
    x2 /= dist2
    y2 /= dist2
    
    # Calculamos el vector de diferencia entre v1 y v2:
    dx = x1 - x2
    dy = y1 - y2
    
    dist3 = math.hypot(dx,dy)
    # dist3 - tamaño del vector de diferencia (módulo del vector)
    #  ... nos indica cuan diferentes son:
    #  - 0.0 : totalmente iguales
    #  - 0.5 : 45 grados de diferencia approx.
    #  - 1.0 : 90 grados de diferencia
    #  - 2.0 : 180 grados de diferencia.
    #  
    #  supuestamente no puede dar ningún valor fuera del rango 0..2 porque:
    #   - un módulo, distancia u hipotenusa siempre es positivo
    #   - la mínima distancia posible es cero, cuando el vector es 0,0
    #   - como ambos módulos son normalizados (distancia 1.0) la máxima 
    #     distancia posible resulta de que se sumaran las dos y 1 + 1 = 2.
    #     Para sumar las dos distancias basta con que un vector sea el contrario
    #     del otro y conseguir, efectivamente, una suma.
    return dist3
    
def coeff_correlacion_vectores(x1,y1,x2,y2):
    # En la función estadistica de coeficiente, normalmente funciona del revés:
    #  - +1 : iguales
    #  -  0 : sin relación
    #  - -1 : relación inversa.
    
    # Como nos interesa (por similitud) que la salida se asemeje a la función
    # estadística, mapeamos los valores:
    corr = correlacion_vectores(x1,y1,x2,y2)
    coeff = 1 - corr
    
    # nos daria:
    #     1 - 0.0 =  1.0
    #     1 - 0.5 =  0.5
    #     1 - 1.0 =  0.0
    #     1 - 1.5 = -0.5
    #     1 - 2.0 = -1.0
    
    return coeff


def GetAngleOfLineBetweenTwoPoints(p1, p2,time_shift_p2=0): 
    p2x = p2.x + p2.dx * time_shift_p2
    p2y = p2.y + p2.dy * time_shift_p2
    xDiff = p2x - p1.x 
    yDiff = p2y - p1.y 
    return math.atan2(yDiff, xDiff)

def GetDistanceBetweenTwoPints(p1,p2, minimum_distance=0.000001):
    dist = math.hypot(p1.x-p2.x, p1.y-p2.y)
    if dist < minimum_distance: return minimum_distance # avoid divide by zero
    return dist
