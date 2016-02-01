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
    SOUND_FILE = "../resources/laser_e3.ogg"
    RANGE = 60
    SHOT_FREQ = 3.0
    COST = 25
    def __init__(self, *args, **kwargs):
        GameBoardBox.__init__(self,*args,**kwargs)
        self.z = 10  
        self.range = self.RANGE
        self.angle = random.uniform(-12,12)
        self.last_mouseover = 0
        self.last_shot = 0
        self.shot_freq = self.SHOT_FREQ
        self.sound = pygame.mixer.Sound(self.SOUND_FILE)
        self.sound.set_volume(0.25)
        

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
            targets += [(dist* random.uniform(0.9,1.1), gameobject)]
        targets.sort()
        
        if targets:
            dist, gameobject = targets[0]
            new_ang = GetAngleOfLineBetweenTwoPoints(self, gameobject, 
                                                     time_shift_p2=dist/100.0*0.5)
            self.angle = new_ang
            if self.time - self.last_shot > 1.0 / self.shot_freq and random.randint(0,2) == 0: 
                self.last_shot = self.time
                shot_angle = self.angle + random.uniform(-0.1,0.1)
                self.sound.stop()
                self.sound.play(maxtime=250)
                self.sound.set_volume(0.25)                
                self.sound.fadeout(250)
                
                shot = GameShot(self.game, target = gameobject, parent = self, angle = shot_angle)



class GameTower2(GameTower):
    SOUND_FILE = "../resources/laser_b3.ogg"
    RANGE = 80
    SHOT_FREQ = 0.5
    COST = 55
    

    def draw(self, screen):
        x,y = int(self.x),int(self.y)
        Rect = x-15,y-15,32,32
        pygame.draw.rect(screen, (120,100,60), Rect)
        pygame.draw.rect(screen, (170,160,120), Rect, 1)
        pygame.draw.circle(screen, (100,80,0), (x,y), 8, 0)
        pygame.draw.circle(screen, (150,120,100), (x,y), 8, 1)
        if self.game.cursor.px == self.px and self.game.cursor.py == self.py:
            self.last_mouseover = self.time
            
        if self.time - self.last_mouseover < 0.5:
            pygame.draw.circle(screen, (200,0,0), (x,y), self.range, 1)
        td = min([8, (self.time -self.last_shot) / 0.95 * 8])
        if td < 3: td = 3
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
            targets += [(dist* random.uniform(0.9,1.1), gameobject)]
        targets.sort()
        
        if targets:
            dist, gameobject = targets[0]
            new_ang = GetAngleOfLineBetweenTwoPoints(self, gameobject, 
                                                     time_shift_p2=dist/100.0*0.15)
            self.angle = new_ang
            if self.time - self.last_shot > 1.0 / self.shot_freq and random.randint(0,2) == 0: 
                self.last_shot = self.time
                shot_angle = self.angle + random.uniform(-0.01,0.01)
                self.sound.stop()
                self.sound.play(maxtime=250)
                self.sound.set_volume(0.25)                
                self.sound.fadeout(250)
                
                shot = GameShot2(self.game, 
                                 target = gameobject, parent = self, 
                                 angle = shot_angle)

class GameTower9(GameTower):
    SOUND_FILE = "../resources/laser_c5.ogg"
    RANGE = 250
    SHOT_FREQ = 5.0
    COST = 155
    

    def draw(self, screen):
        x,y = int(self.x),int(self.y)
        Rect = x-15,y-15,32,32
        pygame.draw.rect(screen, (60,150,60), Rect)
        pygame.draw.rect(screen, (100,170,100), Rect, 1)
        pygame.draw.circle(screen, (120,150,0), (x,y), 8, 0)
        pygame.draw.circle(screen, (150,200,40), (x,y), 8, 1)
        if self.game.cursor.px == self.px and self.game.cursor.py == self.py:
            self.last_mouseover = self.time
            
        if self.time - self.last_mouseover < 0.5:
            pygame.draw.circle(screen, (200,0,0), (x,y), self.range, 1)
        td = min([12, (self.time -self.last_shot) / 0.25 * 12])
        if td < 3: td = 3
        ax = int(x + math.cos(self.angle)*td)
        ay = int(y + math.sin(self.angle)*td)
        pygame.draw.circle(screen, (150,200,90), (ax,ay), 2, 1)

    def logic(self, new_time):
        GameBoardBox.logic(self,new_time)
        targets = []
        for gameobject in GameObject.OBJECT_LIST:
            if gameobject is self: continue
            if not isinstance(gameobject, GameEnemy): continue
            dist = math.hypot(self.x-gameobject.x, self.y-gameobject.y)
            if dist > self.range: continue
            targets += [(dist * random.uniform(0.9,1.1), gameobject)]
        targets.sort()
        
        if targets:
            dist, gameobject = targets[0]
            new_ang = GetAngleOfLineBetweenTwoPoints(self, gameobject, 
                                                     time_shift_p2=dist/100.0*0.15)
            self.angle = new_ang
            if self.time - self.last_shot > 1.0 / self.shot_freq and random.randint(0,2) == 0: 
                self.last_shot = self.time
                if dist > 150:
                    shot_angle = self.angle + random.uniform(-0.5,0.5)
                else:
                    shot_angle = self.angle + random.uniform(-0.05,0.05)
                    
                self.sound.stop()
                self.sound.play(maxtime=50)
                self.sound.set_volume(0.25)                
                self.sound.fadeout(50)
                
                shot = GameShot9(self.game, 
                                 target = gameobject, parent = self, 
                                 angle = shot_angle)
                if dist < 150:
                    shot.speed /= 2
