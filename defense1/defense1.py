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

from gameutilities import * # <- Eliminar asterisco
from gameentities import * # <- Eliminar asterisco
from gameboard import * # <- Eliminar asterisco
from gameenemies import * # <- Eliminar asterisco
from gameshots import * # <- Eliminar asterisco
from gametowers import * # <- Eliminar asterisco


# ------------------------- </IMPORTS>

# Estas variables las dejo como Globales porque sí parecen más configuración
# a nivel de juego:
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (15,30)
RESOLUTION = (800,600)
FPS = 60
BG_COLOR = (0, 0, 0)

    


            
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
        self.enemy_n = 0
        self.cursor = None
        
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
        self.last_enemy = 0
        self.time_between_enemies = 8
        self.cursor = GameCursor(self)
        # dinero al iniciar, 100$
        
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

        if self.frametime - self.last_enemy > self.time_between_enemies:
            self.last_enemy = self.frametime
            self.enemy_n += 1
            time_k = min(1.0,self.time_between_enemies) ** 2.0
            self.time_between_enemies /= 1 + ((0.50 / self.enemy_n) 
                                * time_k)
            GameEnemy(self)
            
          
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
        px,py = mouse_x / 32 , mouse_y/32
        x = px*32 + 16
        y = py*32 + 16
        
        self.cursor.x = x
        self.cursor.y = y
        self.cursor.px = px
        self.cursor.py = py
        """for gameobject in GameObject.OBJECT_LIST:
            dist = math.hypot(x-gameobject.x, y-gameobject.y)
            if dist > 16: continue
            gameobject.last_mouseover = self.frametime
        """
        #print "mouse at (%d, %d)" % (mouse_x,mouse_y)
        
    def on_mouse_button_left(self, event):
        mouse_x, mouse_y = event.pos
        px,py = mouse_x / 32 , mouse_y/32
        x = px*32 + 16
        y = py*32 + 16
        
        self.cursor.x = x
        self.cursor.y = y
        self.cursor.px = px
        self.cursor.py = py
        tower = GameTower(self)
        tower.x = x
        tower.y = y
        tower.px = px
        tower.py = py

    def on_mouse_button_right(self, event):
        mouse_x, mouse_y = event.pos
        
    def on_keydown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.on_quit(event)
        # Seleccionar tipo de torreta con los numeros 1-9
        

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
        GamePath(game, pos=pos, num=n)
        if c == 'w': pos = (pos[0],pos[1]-1)
        if c == 'a': pos = (pos[0]-1,pos[1])
        if c == 's': pos = (pos[0],pos[1]+1)
        if c == 'd': pos = (pos[0]+1,pos[1])
    # Loop until the user clicks close button
    game.main_loop()
    del game
    pygame.quit() 
    sys.exit(0)
# Esto es el "truco" de python para evitar que si realizamos un "import defense1.py"
# no nos ejeucte el main. Es decir, que esto a la vez es un programa y una librería.
# Esto siempre se queda al final.
if __name__ == "__main__":
    # ... si nos están ejecutando como programa principal, entonces...
    main()
    