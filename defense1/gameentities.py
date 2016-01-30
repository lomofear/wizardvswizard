#!/usr/bin/python
# encoding: UTF-8

# Intento de tower defense por deavid


import random

import pygame





class GameEntity(object):
    ENTITY_LIST = []
    # METODOS DE CLASE // CLASSMETHODS
    @classmethod
    def apply_logic_to_all(cls, frametime):
        for gameobject in cls.ENTITY_LIST:
            gameobject.logic(frametime)

    @classmethod
    def draw_all(cls, screen):
        for gameobject in sorted(cls.ENTITY_LIST, key=lambda obj: -obj.z):
            gameobject.draw(screen)
    
    # INSTANCIAS
    def __init__(self, game, x = 0, y = 0):
        self.game = game
        self.time = self.game.frametime
        self.dtime = 0
        self.x = x
        self.y = y 
        self.z = 50
        self.last_mouseover = 0
        self.living = True
        self.ENTITY_LIST.append(self)

    def logic(self, new_time):
        # new_time: nuevo timestamp del frame
        self.dtime = new_time - self.time
        self.time = new_time

    def alive(self):
        return self.living
    def destruct(self):
        self.living = False
        try:
            self.ENTITY_LIST.remove(self)
        except ValueError:
            pass # Intento de borrar un elemento ya borrado.

    def draw(self, screen):
        pygame.draw.circle(screen, (200,200,200), (int(self.x),int(self.y)) , 1)



class GameObject(GameEntity):
    # Eliminar de aqui la mayor parte de codigo genérico y moverlo a una clase GameEntity
    # GameObject pasará a heredar GameEntity y será para los objetos que se mueven
    OBJECT_LIST = []
    
    # INSTANCIAS
    def __init__(self, game, x = 0, y = 0, dx = 0, dy = 0):
        GameEntity.__init__(self, game, x, y)
        self.dx = dx
        self.dy = dy
        self.OBJECT_LIST.append(self)

    def logic(self, new_time):
        # new_time: nuevo timestamp del frame
        self.dtime = new_time - self.time
        self.time = new_time

        self.x += self.dx * self.dtime
        self.y += self.dy * self.dtime

    def destruct(self):
        GameEntity.destruct(self)
        try:
            self.OBJECT_LIST.remove(self)
        except ValueError:
            pass # Intento de borrar un elemento ya borrado.
        
    def draw(self, screen):
        pygame.draw.circle(screen, (200,200,200), (int(self.x),int(self.y)) , 3)


class GameText(GameEntity): 
    def __init__(self, *args, **kwargs):
        GameEntity.__init__(self,*args,**kwargs)
        self.z = -50
        self.text = ""
        self.fontfamily = None
        self.fontsize = 18
        self.color = (255,255,255)
        self.antialias = 1
        self.alignment = 0        
        self.font = None
        self.text_bmp = None
        self.text_position = None
        self.ox = 0
        self.oy = 0

    def setFont(self, family = None, size = None):    
        if family:
            if family == "": family = None
            self.fontfamily = family
        if size: self.fontsize = size
        self.font = None
        self.text_bmp = None
        self.text_position = None

    def setText(self, text = None, antialias = None, color = None):
        if text: self.text = text
        if antialias: self.antialias = antialias
        if color: self.color = color
        self.text_bmp = None
        self.text_position = None
    
    def setPosition(self, pos, aligment = None):
        if pos: self.x, self.y = pos
        if aligment: self.aligment = aligment
        self.text_position = None
        
        
    def draw(self, screen):
        if self.font is None:
            self.font = pygame.font.Font(self.fontfamily, self.fontsize)
        if self.text_bmp is None:
            self.text_bmp = font.render(self.text, self.antialias, self.color)
        if self.text_position is None:
            self.text_position = text.get_rect()
            if bool(self.aligment & ALIGN_LEFT):   self.ox = self.text_position.left
            if bool(self.aligment & ALIGN_CENTER): self.ox = self.text_position.centerx
            if bool(self.aligment & ALIGN_RIGHT):  self.ox = self.text_position.right

            if bool(self.aligment & ALIGN_TOP):    self.oy = self.text_position.top
            if bool(self.aligment & ALIGN_MIDDLE): self.oy = self.text_position.centery
            if bool(self.aligment & ALIGN_BOTTOM): self.oy = self.text_position.bottom
                
            
        
        screen.blit(self.text_bmp, (self.x - self.ox, self.y - self.oy))


