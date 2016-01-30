#!/usr/bin/python
# encoding: UTF-8
import pygame

from gameutilities import * # <- Eliminar asterisco
from gameentities import * # <- Eliminar asterisco


class GameBoardBox(GameEntity):
    # Nueva clase base, heredara de entity, para los objetos que están en el tablero
    # y tienen una posición fija.
    # Se indexaran por PX,PY y por defecto habrá error al crear uno encima de otro.
    GAME_BOARD = {}
    REGISTER_ON_BOARD = True    
    def __init__(self, *args, **kwargs):
        self.px = kwargs.pop('px', None)
        self.py = kwargs.pop('py', None)
        if self.REGISTER_ON_BOARD:
            if (self.px, self.py) in self.GAME_BOARD:
                raise ValueError, "Position on x,y (%r) already used by %r" % ((self.px, self.py), self.GAME_BOARD[(self.px,self.py)])
            else:
                self.GAME_BOARD[(self.px,self.py)] = self 

        GameEntity.__init__(self,*args,**kwargs)
        
    

class GamePath(GameBoardBox): # heredara de gamebox
    PATH = {}
    def __init__(self, *args, **kwargs):
        pos = kwargs.pop('pos', None)
        num = kwargs.pop('num', None)
        if pos:
            # Si nos pasan un param. llamado "pos" lo robamos y lo usamos
            # como pareja x,y del tablero. Lo traducimos a x,y.
            px,py = pos
            x = px*32 + 16
            y = py*32 + 16
            kwargs['x'] = x
            kwargs['y'] = y
            kwargs['px'] = px
            kwargs['py'] = py
        self.z = 75
        self.num = num
        self.pos = pos
        self.PATH[num] = self # autoregistro. 
        GameBoardBox.__init__(self,*args,**kwargs)
        
    def draw(self, screen):
        x,y = int(self.x),int(self.y)
        Rect = x-15,y-15,32,32
        pygame.draw.rect(screen, (100,100,120), Rect)
        pygame.draw.rect(screen, (0,0,20), Rect, 1)
        Rect = x-13,y-13,28,28
        # Coloreo incremental para facilitar el seguir el camino visualmente:
        # ... a veces produce colores feos, lo sé.
        pygame.draw.rect(screen, (int(120+math.sin(self.num/23.0)*100),
                                  int(120+math.sin(self.num/11.0)*100),
                                  int(120+math.sin(self.num/4.0)*100)), Rect)

class GameCursor(GameBoardBox): 
    # Tiene que heredar de GameBox, pero indicar que no ocupa
    # .. espacio y/o está en una capa diferente
    REGISTER_ON_BOARD = False
    def __init__(self, *args, **kwargs):
        GameBoardBox.__init__(self,*args,**kwargs)
        self.z = 0  # dibujar arriba
        self.px = 0
        self.py = 0
    def draw(self, screen):
        x,y = int(self.x),int(self.y)
        Rect = x-15,y-15,32,32
        pygame.draw.rect(screen, (255,255,255), Rect, 1)

