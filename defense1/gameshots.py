#!/usr/bin/python
# encoding: UTF-8

# Intento de tower defense por deavid
import random

import pygame


from gameutilities import * # <- Eliminar asterisco
from gameentities import * # <- Eliminar asterisco
from gameenemies import GameEnemy
        
class GameShot(GameObject):
    SPEED = 100
    MAXTIME = 1.0
    DAMAGE = 8
    TRAMPLE = False
    MASS = 20.0
    def __init__(self, *args, **kwargs):
        self.target = kwargs.pop('target', None)
        self.parent = kwargs.pop('parent', None)
        self.angle = kwargs.pop('angle', -1)
        self.speed = kwargs.pop('speed', self.SPEED)
        self.maxflytime = kwargs.pop('maxflytime', self.MAXTIME)
        GameObject.__init__(self,*args,**kwargs)
        self.z = -1
        self.flytime = 0
        self.damage = self.DAMAGE
        self.oldtargets = [self.target]
        self.oldposition = []
        self.maxoldpos = 15
        self.mass = self.MASS
        if self.parent:
            self.x = self.parent.x
            self.y = self.parent.y
            if self.angle == -1:
                self.angle = getattr(self.parent , "angle", -1)

    def look_for_new_target(self):
        targets = []
        looktime = 0.5
        _range = self.SPEED * (self.maxflytime - self.flytime) + 100
        for gameobject in self.OBJECT_LIST:
            if gameobject is self: continue
            if not isinstance(gameobject, GameEnemy): continue
            if gameobject in self.oldtargets: continue 
            if not gameobject.alive(): continue 
            dist = math.hypot(self.x-gameobject.x, self.y-gameobject.y)
            corr = coeff_correlacion_vectores(
                gameobject.x-self.x+self.dx*looktime, 
                gameobject.y-self.y+self.dy*looktime,
                self.dx,self.dy) 
            if corr < 0.5: continue
            dist /= corr
            dist /= corr
            #if dist > _range: continue
            targets += [(dist, gameobject)]
        targets.sort()
                
        if targets:
            dist, enemy = targets[0]
            self.target = enemy
            self.oldtargets.append(enemy)
        
    def logic(self, new_time):
        GameObject.logic(self,new_time)
        if self.flytime < self.maxflytime:
            self.oldposition.append( (self.x, self.y) )
        else:
            if len(self.oldposition):
                self.oldposition[:1] = []
                
        if len(self.oldposition) > self.maxoldpos:
            self.oldposition[:-self.maxoldpos] = []

        ax, ay = math.cos(self.angle), math.sin(self.angle)
        if self.flytime == 0:
            # First frame!
            self.x += ax * 8
            self.y += ay * 8
        self.flytime += self.dtime
        if self.flytime > self.maxflytime:
            if len(self.oldposition) == 0 :
                self.destruct()
            return

        if self.target is None or not self.target.alive():
            self.look_for_new_target()
            return
        dist_to_target = GetDistanceBetweenTwoPints(self, self.target) 
        current_speed = math.hypot(self.dx, self.dy)
        if dist_to_target < 11:
            dealt = self.target.life
            self.target.receive_damage(self.damage)
            if self.TRAMPLE:
                self.target = None
                self.damage -= dealt / 2 + 5
                self.speed /= 1.2
                self.look_for_new_target()
            else:
                self.destruct()
        elif self.TRAMPLE:
            for gameobject in self.OBJECT_LIST:
                if gameobject is self: continue
                if not isinstance(gameobject, GameEnemy): continue
                if gameobject in self.oldtargets: continue 
                if not gameobject.alive(): continue 
                dist = math.hypot(self.x-gameobject.x, self.y-gameobject.y)
                if dist < 11:
                    self.target = gameobject
                    dealt = self.target.life
                    self.target.receive_damage(self.damage)
                    self.target = None
                    self.damage -= dealt / 2 + 5
                    self.speed /= 1.2
                    self.look_for_new_target()

        if self.damage <= 0:
            self.flytime = self.maxflytime + 1

        if self.flytime == 0:
            ax, ay = math.cos(self.angle), math.sin(self.angle)
            self.dx = ax * self.speed
            self.dy = ay * self.speed

        mass = max([self.mass / (self.speed+50),0.00005])
        if dist_to_target < 11 + current_speed/10:
            mass /= 10.0
        
        self.dx = (self.dx * mass + ax * self.speed * self.dtime) / (mass + self.dtime)
        self.dy = (self.dy * mass + ay * self.speed * self.dtime) / (mass + self.dtime)
        current_speed = math.hypot(self.dx, self.dy)
        corr = coeff_correlacion_vectores(self.dx,self.dy,ax,ay)
        if corr < 0.9:
            f = (corr + 1.1) / 2.0
            #print "%.3f" % f, "%.2f" % self.mass
            
            self.mass /= f ** (self.dtime * 6.0) # aumentar la masa conforme gira
        f_vel = (corr + 3)/3.0 - 1
        self.speed *= (1.0 + f_vel) ** (self.dtime * 4.0)
        
        self.dx *= self.speed/current_speed 
        self.dy *= self.speed/current_speed 
        #if current_speed < self.speed * 0.30:
        #    self.destruct()
            
        if self.flytime > self.dtime and self.target:
            time_to_target = dist_to_target / self.speed
            self.angle = GetAngleOfLineBetweenTwoPoints(
                self, self.target,time_shift_p2=time_to_target*1.5)
        

    def draw(self, screen):
        linetime = 0.05
        start_pos =  (int(self.x),int(self.y))
        end_pos =  (int(self.x - self.dx * linetime),int(self.y - self.dy * linetime))
        
        #pygame.draw.circle(screen, (255,255,random.randint(1,250)), start_pos , 2)
        pygame.draw.line(screen, (0,0,0), start_pos, end_pos, 3)
        pygame.draw.line(screen, (255,255,random.randint(1,250)), start_pos, end_pos, 1)
            
class GameShot2(GameShot):
    SPEED = 200
    MAXTIME = 1.0
    DAMAGE = 150
    TRAMPLE = True
    MASS = 30.0
    def draw(self, screen):
        linetime = 0.0
        if self.flytime > self.maxflytime:
            lifetime = 0
        start_pos =  (int(self.x + self.dx * linetime),int(self.y + self.dy * linetime))
        #end_pos =  (int(self.x - self.dx * linetime),int(self.y - self.dy * linetime))
        end_pos =  (int(self.x),int(self.y))
        if self.flytime < self.maxflytime:
            pygame.draw.line(screen, (0,0,0), start_pos, end_pos, 5)
        for i in range(min([15,len(self.oldposition)])):            
            start_pos = end_pos
            x,y = self.oldposition[-i-1]
            end_pos = (int(x), int(y))
            if i == 0 and self.flytime > self.maxflytime: continue
            
            pygame.draw.line(screen, (0,0,0), start_pos, end_pos, 5)


        start_pos =  (int(self.x + self.dx * linetime),int(self.y + self.dy * linetime))
        #end_pos =  (int(self.x - self.dx * linetime),int(self.y - self.dy * linetime))
        end_pos =  (int(self.x),int(self.y))
        if self.flytime < self.maxflytime:
            pygame.draw.line(screen, (255,random.randint(125,250),
                                  random.randint(0,125)), 
                         start_pos, end_pos, 2)
        for i in range(min([15,len(self.oldposition)])):            
            start_pos = end_pos
            x,y = self.oldposition[-i-1]
            end_pos = (int(x), int(y))
            if i == 0 and self.flytime > self.maxflytime: continue
            pygame.draw.line(screen, (255,random.randint(125,250),
                                      random.randint(0,125)), start_pos, end_pos, 2)
            
class GameShot9(GameShot):
    SPEED = 800
    MAXTIME = 0.35
    DAMAGE = 50
    TRAMPLE = False
    MASS = 15.0
    def draw(self, screen):
        linetime = 0.0
        if self.flytime > self.maxflytime:
            lifetime = 0
        start_pos =  (int(self.x + self.dx * linetime),int(self.y + self.dy * linetime))
        #end_pos =  (int(self.x - self.dx * linetime),int(self.y - self.dy * linetime))
        end_pos =  (int(self.x),int(self.y))
        if self.flytime < self.maxflytime:
            pygame.draw.line(screen, (0,0,0), start_pos, end_pos, 5)
        for i in range(min([2,len(self.oldposition)])):            
            start_pos = end_pos
            x,y = self.oldposition[-i-1]
            end_pos = (int(x), int(y))
            if i == 0 and self.flytime > self.maxflytime: continue
            
            pygame.draw.line(screen, (0,0,0), start_pos, end_pos, 5)


        start_pos =  (int(self.x + self.dx * linetime),int(self.y + self.dy * linetime))
        #end_pos =  (int(self.x - self.dx * linetime),int(self.y - self.dy * linetime))
        end_pos =  (int(self.x),int(self.y))
        if self.flytime < self.maxflytime:
            pygame.draw.line(screen, (0,random.randint(125,250),
                                  0), 
                         start_pos, end_pos, 2)
        for i in range(min([2,len(self.oldposition)])):            
            start_pos = end_pos
            x,y = self.oldposition[-i-1]
            end_pos = (int(x), int(y))
            if i == 0 and self.flytime > self.maxflytime: continue
            pygame.draw.line(screen, (0,random.randint(125,250),
                                      0), start_pos, end_pos, 2)

