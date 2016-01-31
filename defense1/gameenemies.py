#!/usr/bin/python
# encoding: UTF-8

# Intento de tower defense por deavid
import random

import pygame


from gameutilities import * # <- Eliminar asterisco
from gameentities import * # <- Eliminar asterisco
from gameboard import *

class GameDamage(GameObject):
    def __init__(self, *args, **kwargs):
        GameObject.__init__(self,*args,**kwargs)
        self.x += random.uniform(-5,5)
        self.y += random.uniform(-5,5)
        self.maxtime = 1.5
        self.curtime = 0
        self.z = -15
        
    def draw(self, screen):
        self.curtime += self.dtime
        r = int((self.maxtime - self.curtime) / float(self.maxtime) * 6)
        if r <1: r = 1
        pygame.draw.circle(screen, (200,255,255), (int(self.x),int(self.y)) , r)
        if self.curtime > self.maxtime: self.destruct()

class GameEnemy(GameObject):
    LIFE = 70
    MINVEL = 10
    MAXVEL = 50
    MONEY = 4
    def __init__(self, *args, **kwargs):
        GameObject.__init__(self,*args,**kwargs)
        self.z = 25
        self.posnum = 0
        self.x = GamePath.PATH[self.posnum].x + random.randint(-12,12)
        self.y = GamePath.PATH[self.posnum].y + random.randint(-12,12)
        self.posnum += 1
        self.velocity = 100
        self.minvelocity = self.MINVEL
        self.maxvelocity = self.MAXVEL
        self.life = self.LIFE
        self.money = self.MONEY

    def draw(self, screen):
        pygame.draw.circle(screen, (200,80,80), (int(self.x),int(self.y)) , 8)
        pygame.draw.circle(screen, (20,0,0), (int(self.x),int(self.y)) , 9, 1)
        pygame.draw.circle(screen, (255,100,100), (int(self.x),int(self.y)) , 8, 1)
    
    def receive_damage(self, damage):
        GameDamage(self.game, x=self.x, y=self.y)
        dealt = min(self.life, damage)
        self.life -= damage
        if self.life <= 0:
            self.death()
        return dealt

    def death(self):
        # enemy dead
        if not self.alive(): return # evitar contar dos veces.
        self.game.money += self.money
        self.destruct() # muerto

    def path_ended(self):
        # enemy won
        if not self.alive(): return # evitar descontar dos veces.
        self.game.money -= self.money
        self.destruct() # fin del camino

    def logic(self, new_time):
        GameObject.logic(self,new_time)
        if self.posnum not in GamePath.PATH:
            self.path_ended()
            return
        dstx,dsty = GamePath.PATH[self.posnum].x,GamePath.PATH[self.posnum].y
        dx, dy = dstx - self.x , dsty - self.y
        dst = math.hypot(dx,dy)
        ndx , ndy = dx / dst, dy / dst
        #self.dx += ndx * self.dtime * 60.0
        #self.dy += ndy * self.dtime * 60.0
        
        self.dx /= 1.5 ** self.dtime
        self.dy /= 1.5 ** self.dtime
        corr = coeff_correlacion_vectores(self.dx, self.dy, ndx, ndy)
        if corr < 0: corr = 0 # eliminamos negativos
        corr_f = corr - 0.90 # 10% accel, 90% frenado.
        self.velocity *= 1+(corr_f*30.00*self.dtime) # aplicar factor 30x/s
        self.velocity /= 1.5 ** self.dtime
        if self.velocity < self.minvelocity: self.velocity = self.minvelocity 
        if self.velocity > self.maxvelocity: self.velocity = self.maxvelocity 
        self.dx = (self.dx + ndx * self.velocity) / 2.0
        self.dy = (self.dy + ndy * self.velocity) / 2.0
        
        if dst < 12: self.posnum += 1
        dstx,dsty = GamePath.PATH[self.posnum-1].x,GamePath.PATH[self.posnum-1].y
        dx2, dy2 = dstx - self.x , dsty - self.y
        dx2 += dx
        dy2 += dy
        dst2 = abs(dx2) + abs(dy2)
        ndx2 , ndy2 = dx2 / dst2, dy2 / dst2
        if dst2 > 20:
            if abs(ndx2) > 0.3:
                self.x += ndx2 / 2
                if math.copysign(1,ndx2) != math.copysign(1,self.dx):
                    self.dx *= -0.6
            if abs(ndy2) > 0.3:
                self.y += ndy2 / 2
                if math.copysign(1,ndy2) != math.copysign(1,self.dy):
                    self.dy *= -0.6

