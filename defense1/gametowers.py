#!/usr/bin/python
# encoding: UTF-8

# Intento de tower defense por deavid
import random

import pygame

from gameutilities import * # <- Eliminar asterisco
from gameentities import * # <- Eliminar asterisco
from gameboard import GameBoardBox
from gameenemies import * 
from gameshots import *

class GameTower(GameBoardBox):
    def __init__(self, *args, **kwargs):
        GameBoardBox.__init__(self,*args,**kwargs)
        self.z = 10  
        self.range = 100
        self.angle = random.uniform(-12,12)
        self.last_mouseover = 0
        self.last_shot = 0
        self.shot_freq = 2.0

    def draw(self, screen):
        x,y = int(self.x),int(self.y)
        Rect = x-15,y-15,32,32
        pygame.draw.rect(screen, (80,100,120), Rect)
        pygame.draw.rect(screen, (150,165,165), Rect, 1)
        pygame.draw.circle(screen, (10,80,100), (x,y), 13, 0)
        pygame.draw.circle(screen, (100,120,150), (x,y), 13, 1)
        if self.game.cursor.px == self.px and self.game.cursor.py == self.py:
            self.last_mouseover = self.time
            
        if self.time - self.last_mouseover < 0.5:
            pygame.draw.circle(screen, (200,0,0), (x,y), self.range, 1)
        td = min([10,10 - (self.time -self.last_shot) / 0.15 * 5])
        if td < 5: td = 5
        ax = int(x + math.cos(self.angle)*td)
        ay = int(y + math.sin(self.angle)*td)
        pygame.draw.circle(screen, (160,200,220), (ax,ay), 2, 1)

    def logic(self, new_time):
        GameBoardBox.logic(self,new_time)
        targets = []
        for gameobject in GameObject.OBJECT_LIST:
            if gameobject is self: continue
            if not isinstance(gameobject, GameEnemy): continue
            dist = math.hypot(self.x-gameobject.x, self.y-gameobject.y)
            if dist > self.range: continue
            targets += [(dist, gameobject)]
        targets.sort()
        
        if targets:
            dist, gameobject = targets[0]
            new_ang = GetAngleOfLineBetweenTwoPoints(self, gameobject, time_shift_p2=dist/100.0*0.5)
            self.angle = new_ang
            if self.time - self.last_shot > 1.0 / self.shot_freq and random.randint(0,2) == 0: 
                self.last_shot = self.time
                shot_angle = self.angle + random.uniform(-0.1,0.1)
                shot = GameShot(self.game, target = gameobject, parent = self, angle = shot_angle)
