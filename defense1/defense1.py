#!/usr/bin/python
# encoding: UTF-8

# Intento de tower defense por deavid

# ------------------------- <IMPORTS>
# Primero los imports nativos de Python:
import os, random, sys
import math, time

print ("Python: " + sys.version)  # imprimimos la ver. de python para depurar
# ... seguramente ayude a saber porque no importa pygame, etc.

# Después los imports de las librerías instaladas que son necesarias:
import pygame
print ("Pygame: " + pygame.version.ver)

# Aquí los imports de otras librerias nuestras propias
from enum import Enum # enumeraciones al estilo C


# ------------------------- </IMPORTS>

# Estas variables las dejo como Globales porque sí parecen más configuración
# a nivel de juego:
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (15,30)
RESOLUTION = (800,600)
FPS = 60
BG_COLOR = (0, 0, 0)

ACTIONS = Enum(
    'NULL','QUIT',
    'PLAYER1_SHOOT',
               )

class GameObject(object):
    OBJECT_LIST = []
    # METODOS DE CLASE // CLASSMETHODS
    @classmethod
    def apply_logic_to_all(cls, frametime):
        for gameobject in cls.OBJECT_LIST:
            gameobject.logic(frametime)

    @classmethod
    def draw_all(cls, screen):
        for gameobject in cls.OBJECT_LIST:
            gameobject.draw(screen)
    
    # INSTANCIAS
    def __init__(self, new_time, x = 0, y = 0, dx = 0, dy = 0):
        self.time = new_time
        self.dtime = 0
        self.x = x
        self.y = y 
        self.dx = dx
        self.dy = dy
        self.OBJECT_LIST.append(self)

    def logic(self, new_time):
        # new_time: nuevo timestamp del frame
        self.dtime = new_time - self.time
        self.time = new_time

        self.x += self.dx * self.dtime
        self.y += self.dy * self.dtime
        
    def draw(self, screen):
        pygame.draw.circle(screen, (200,200,200), (int(self.x),int(self.y)) , 3)
    
class GamePath(GameObject):
    PATH = {}
    def __init__(self, pos, num, *args, **kwargs):
        #pos = kwargs.pop('pos', None)
        if pos:
            # Si nos pasan un param. llamado "pos" lo robamos y lo usamos
            # como pareja x,y del tablero. Lo traducimos a x,y.
            px,py = pos
            x = px*32 + 16
            y = py*32 + 16
            kwargs['x'] = x
            kwargs['y'] = y
        self.num = num
        self.pos = pos
        self.PATH[num] = self # autoregistro. 
        GameObject.__init__(self,*args,**kwargs)
        
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

class GameEnemy(GameObject):
    def __init__(self, *args, **kwargs):
        GameObject.__init__(self,*args,**kwargs)
        self.posnum = 0
        self.x = GamePath.PATH[self.posnum].x + random.randint(-12,12)
        self.y = GamePath.PATH[self.posnum].y + random.randint(-12,12)
        self.posnum += 1

    def draw(self, screen):
        pygame.draw.circle(screen, (200,80,80), (int(self.x),int(self.y)) , 8)
        pygame.draw.circle(screen, (20,0,0), (int(self.x),int(self.y)) , 9, 1)
        pygame.draw.circle(screen, (255,100,100), (int(self.x),int(self.y)) , 8, 1)

    def logic(self, new_time):
        GameObject.logic(self,new_time)
        if self.posnum not in GamePath.PATH:
            return
        dstx,dsty = GamePath.PATH[self.posnum].x,GamePath.PATH[self.posnum].y
        dx, dy = dstx - self.x , dsty - self.y
        dst = math.hypot(dx,dy)
        ndx , ndy = dx / dst, dy / dst
        self.dx += ndx * self.dtime * 60.0
        self.dy += ndy * self.dtime * 60.0
        
        self.dx /= 1.5 ** self.dtime
        self.dy /= 1.5 ** self.dtime
        
        if dst < 16: self.posnum += 1
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

# Creo una clase para llevar todo el juego
# ... esta estrategia es un poco al estilo Java (si, en serio, java)
# ... donde todo el programa va dentro de una clase.
# ... la ventaja es la ausencia de globales, y que existe un sitio 
# ... donde podemos ir a buscar las variables desde fuera.

class TowerGame(object):
    """Clase principal para el juego"""
    game = None
    def __init__(self, screen):
        """
        Inicialización/Constructor. Por convención en Python al
        construir, declaramos todas las variables que van a aparecer más tarde.
        """
        self.screen = screen
        self.clock = None
        self.frametime = 0 
        self.game = self # <- esto es un singleton chapucero.
        # Un singleton es un pattern de programación conocido. Busca en google.
        # es como una global con una instancia de la clase.
        # https://es.wikipedia.org/wiki/Singleton
        self.done = False
        self.logic_callbacks = []
        self.draw_callbacks = []
        self.last_enemy = 0
        
    def setup(self):
        """
        Método de configuración inicial. Pensado para lanzarse justo después de
        construir.
        ¿Porqué esto no esta dentro del constructor? Básicamente porque permite
        "cerrar" el juego y volverlo a inicializar las veces que queramos sin 
        tener que borrar el objeto entero. 
        """
        # initialize clock. used later in the loop.
        self.clock = pygame.time.Clock()
        self.frametime = time.time()
        self.done = False
        
        self.logic_callbacks[:] = []
        self.logic_callbacks.append(GameObject.apply_logic_to_all)
        self.draw_callbacks[:] = []
        self.draw_callbacks.append(GameObject.draw_all)
        self.last_enemy = self.frametime
        
    def main_loop(self):
        """
        Método de ayuda para crear un bucle sencillo.
        El bucle en si mismo va en otro método.
        Otro programa puede lanzar nuestro bucle interior sin estar atado 
        a lanzar también el exterior.
        """
        while self.done == False:
            self.loop()
    
    def loop(self):
        """
        Bucle principal del programa.
        Se ejecuta una vez por frame.
        """
        self.frametime = time.time()        
        
        self.process_events()
        self.apply_logic()
        self.clear_screen()
        self.draw_frame()
        
        pygame.display.update()
        self.clock.tick(FPS)
    
    def clear_screen(self):
        self.screen.fill(BG_COLOR) 
        
    def apply_logic(self):
        """ Sistema de lógica por callbacks.
        Se registran en setup() y aquí se lanzan todos en orden.
        Tiene la ventaja de que otros sistemas se pueden agregar desde fuera
        sin reprogramar.
        """
        for callback in self.logic_callbacks:
            callback(self.frametime)

        if self.frametime - self.last_enemy > 2:
            self.last_enemy = self.frametime
            GameEnemy(self.frametime)
            
          
    def draw_frame(self):
        """ Sistema de dibujo por callbacks.
        Se registran en setup() y aquí se lanzan todos en orden.
        Tiene la ventaja de que otros sistemas se pueden agregar desde fuera
        sin reprogramar.
        """
        for callback in self.draw_callbacks:
            callback(self.screen)
        
    def on_quit(self, event):
        self.done = True
    
    def on_mousemotion(self, event):
        mouse_x, mouse_y = event.pos
        #print "mouse at (%d, %d)" % (mouse_x,mouse_y)
        
    def on_mouse_button_left(self, event):
        mouse_x, mouse_y = event.pos

    def on_mouse_button_right(self, event):
        mouse_x, mouse_y = event.pos
        
    def on_keydown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.on_quit(event)
            

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.on_keydown(event)
            if event.type == pygame.QUIT:
                self.on_quit(event)
            if event.type == pygame.MOUSEMOTION:
                self.on_mousemotion(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.on_mouse_button_left(event)
                if event.button == 2:
                    self.on_mouse_button_right(event)
        
        

# Función MAIN donde se inicia el programa.
# contiene la ejecución básica.
def main():
    # initialize game engine
    pygame.init()
    # set screen width/height and caption
    screen = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption('Wizard VS Wizard')
    
    game = TowerGame(screen=screen)
    game.setup()
    pos = (1,-1) # Empieza fuera de pantalla. (para que las criaturas no aparezcan de golpe)
    # Esto es la pantalla: (si, en serio) (Usa WASD como las teclas de moverse con el CStrike)
    path = "ssssdddwwddssssddddwwaawwdddddssddssssaaaaasaaaawaaasaaaa "
    for n,c in enumerate(path):
        GamePath(new_time = game.frametime, pos=pos, num=n)
        if c == 'w': pos = (pos[0],pos[1]-1)
        if c == 'a': pos = (pos[0]-1,pos[1])
        if c == 's': pos = (pos[0],pos[1]+1)
        if c == 'd': pos = (pos[0]+1,pos[1])
    # Loop until the user clicks close button
    game.main_loop()

# Esto es el "truco" de python para evitar que si realizamos un "import defense1.py"
# no nos ejeucte el main. Es decir, que esto a la vez es un programa y una librería.
# Esto siempre se queda al final.
if __name__ == "__main__":
    # ... si nos están ejecutando como programa principal, entonces...
    main()
    