#!/usr/bin/python
# encoding: UTF-8

# Intento de tower defense por deavid
import random

import pygame


from gameutilities import * # <- Eliminar asterisco
from gameentities import * # <- Eliminar asterisco
        
class GameShot(GameObject):
    def __init__(self, *args, **kwargs):
        self.target = kwargs.pop('target', None)
        self.parent = kwargs.pop('parent', None)
        self.angle = kwargs.pop('angle', -1)
        self.speed = kwargs.pop('speed', 100)
        self.maxflytime = kwargs.pop('maxflytime', 1.0)
        GameObject.__init__(self,*args,**kwargs)
        self.z = -1
        self.flytime = 0
        self.damage = 8
        
        if self.parent:
            self.x = self.parent.x
            self.y = self.parent.y
            if self.angle == -1:
                self.angle = getattr(self.parent , "angle", -1)

    def look_for_new_target(self):
        from gameenemies import GameEnemy
        targets = []
        _range = 100
        for gameobject in self.OBJECT_LIST:
            if gameobject is self: continue
            if not isinstance(gameobject, GameEnemy): continue
            if not gameobject.alive(): continue 
            dist = math.hypot(self.x-gameobject.x, self.y-gameobject.y)
            if dist > _range: continue
            targets += [(dist, gameobject)]
        targets.sort()
                
        if targets:
            dist, enemy = targets[0]
            self.target = enemy
        
    def logic(self, new_time):
        GameObject.logic(self,new_time)
        ax, ay = math.cos(self.angle), math.sin(self.angle)
        
        if self.flytime == 0:
            # First frame!
            self.x += ax * 8
            self.y += ay * 8
        self.flytime += self.dtime
        if self.flytime > self.maxflytime:
            self.destruct()

        if not self.target.alive():
            self.look_for_new_target()
            return
        dist_to_target = GetDistanceBetweenTwoPints(self, self.target) 
        if dist_to_target < 9:
            self.destruct()
            self.target.receive_damage(self.damage)
            
        if self.flytime == 0:
            ax, ay = math.cos(self.angle), math.sin(self.angle)
            self.dx = ax * self.speed
            self.dy = ay * self.speed

        mass = 20.0 / (self.speed+50)
        self.dx = (self.dx * mass + ax * self.speed * self.dtime) / (mass + self.dtime)
        self.dy = (self.dy * mass + ay * self.speed * self.dtime) / (mass + self.dtime)
        current_speed = math.hypot(self.dx, self.dy)
        corr = coeff_correlacion_vectores(self.dx,self.dy,ax,ay)
        f_vel = (corr + 3)/3.0 - 1
        self.speed *= (1.0 + f_vel) ** (self.dtime * 4.0)
        
        self.dx *= self.speed/current_speed 
        self.dy *= self.speed/current_speed 
        if current_speed < self.speed * 0.30:
            self.destruct()
            
        if self.flytime > 0.1 and self.target:
            time_to_target = dist_to_target / self.speed
            self.angle = GetAngleOfLineBetweenTwoPoints(
                self, self.target,time_shift_p2=time_to_target*0.5)

    def draw(self, screen):
        linetime = 0.05
        start_pos =  (int(self.x),int(self.y))
        end_pos =  (int(self.x - self.dx * linetime),int(self.y - self.dy * linetime))
        
        #pygame.draw.circle(screen, (255,255,random.randint(1,250)), start_pos , 2)
        pygame.draw.line(screen, (0,0,0), start_pos, end_pos, 3)
        pygame.draw.line(screen, (255,255,random.randint(1,250)), start_pos, end_pos, 1)
            
