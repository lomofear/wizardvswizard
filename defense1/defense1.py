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
        for gameobject in sorted(cls.OBJECT_LIST, key=lambda obj: -obj.z):
            gameobject.draw(screen)
    
    # INSTANCIAS
    def __init__(self, game, x = 0, y = 0, dx = 0, dy = 0):
        self.game = game
        self.time = self.game.frametime
        self.dtime = 0
        self.x = x
        self.y = y 
        self.z = 50
        self.dx = dx
        self.dy = dy
        self.last_mouseover = 0
        self.OBJECT_LIST.append(self)

    def logic(self, new_time):
        # new_time: nuevo timestamp del frame
        self.dtime = new_time - self.time
        self.time = new_time

        self.x += self.dx * self.dtime
        self.y += self.dy * self.dtime
    def destruct(self):
        try:
            self.OBJECT_LIST.remove(self)
        except ValueError:
            pass # Intento de borrar un elemento ya borrado.
        
    def draw(self, screen):
        pygame.draw.circle(screen, (200,200,200), (int(self.x),int(self.y)) , 3)
    
class GamePath(GameObject):
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
        self.z = 75
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
def coeff_correlacion_vectores(x1,y1,x2,y2):
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
    
    
    # En la función estadistica de coeficiente, normalmente funciona del revés:
    #  - +1 : iguales
    #  -  0 : sin relación
    #  - -1 : relación inversa.
    
    # Como nos interesa (por similitud) que la salida se asemeje a la función
    # estadística, mapeamos los valores:
    
    coeff = 1 - dist3
    
    # nos daria:
    #     1 - 0.0 =  1.0
    #     1 - 0.5 =  0.5
    #     1 - 1.0 =  0.0
    #     1 - 1.5 = -0.5
    #     1 - 2.0 = -1.0
    
    return coeff

class GameCursor(GameObject):
    def __init__(self, *args, **kwargs):
        GameObject.__init__(self,*args,**kwargs)
        self.z = 0  # dibujar arriba
        self.px = 0
        self.py = 0
    def draw(self, screen):
        x,y = int(self.x),int(self.y)
        Rect = x-15,y-15,32,32
        pygame.draw.rect(screen, (255,255,255), Rect, 1)
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


class GameTower(GameObject):
    def __init__(self, *args, **kwargs):
        GameObject.__init__(self,*args,**kwargs)
        self.z = 10  
        self.px = 0
        self.py = 0
        self.range = 150
        self.angle = random.uniform(-12,12)
        self.last_mouseover = 0
        self.last_shot = 0

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
        
        ax = int(x + math.cos(self.angle)*10)
        ay = int(y + math.sin(self.angle)*10)
        pygame.draw.circle(screen, (160,200,220), (ax,ay), 3, 1)

    def logic(self, new_time):
        GameObject.logic(self,new_time)
        
        for gameobject in self.OBJECT_LIST:
            if gameobject is self: continue
            if not isinstance(gameobject, GameEnemy): continue
            dist = math.hypot(self.x-gameobject.x, self.y-gameobject.y)
            if dist > self.range: continue
            
            new_ang = GetAngleOfLineBetweenTwoPoints(self, gameobject, time_shift_p2=dist/300.0)
            self.angle = new_ang
            if self.time - self.last_shot > 0.05: 
                self.last_shot = self.time
                shot_angle = self.angle + random.uniform(-0.1,0.1)
                shot = GameShot(self.game, target = gameobject, parent = self, angle = shot_angle)
            break
        
class GameShot(GameObject):
    def __init__(self, *args, **kwargs):
        self.target = kwargs.pop('target', None)
        self.parent = kwargs.pop('parent', None)
        self.angle = kwargs.pop('angle', -1)
        self.speed = kwargs.pop('speed', 300)
        self.maxflytime = kwargs.pop('maxflytime', 0.5)
        GameObject.__init__(self,*args,**kwargs)
        self.z = -1
        self.flytime = 0
        self.damage = 1
        
        if self.parent:
            self.x = self.parent.x
            self.y = self.parent.y
            if self.angle == -1:
                self.angle = getattr(self.parent , "angle", -1)
                
            
    def logic(self, new_time):
        GameObject.logic(self,new_time)
        if self.flytime == 0:
            ax, ay = math.cos(self.angle), math.sin(self.angle)
            self.dx = ax * self.speed
            self.dy = ay * self.speed

        #if self.target:
        #    self.angle = GetAngleOfLineBetweenTwoPoints(self, self.target)
        ax, ay = math.cos(self.angle), math.sin(self.angle)
        mass = 5.0
        self.dx = (self.dx * mass + ax * self.speed * self.dtime) / (mass + self.dtime)
        self.dy = (self.dy * mass + ay * self.speed * self.dtime) / (mass + self.dtime)
        current_speed = math.hypot(self.dx, self.dy)
        if current_speed < self.speed * 0.60:
            self.destruct()
            
        if GetDistanceBetweenTwoPints(self, self.target) < 8:
            self.destruct()
            self.target.receive_damage(self.damage)
            
        if self.flytime == 0:
            # First frame!
            self.x += ax * 8
            self.y += ay * 8
        self.flytime += self.dtime
        if self.flytime > self.maxflytime:
            self.destruct()

    def draw(self, screen):
        pygame.draw.circle(screen, (255,255,random.randint(1,250)), (int(self.x),int(self.y)) , 2)
            

class GameEnemy(GameObject):
    def __init__(self, *args, **kwargs):
        GameObject.__init__(self,*args,**kwargs)
        self.z = 25
        self.posnum = 0
        self.x = GamePath.PATH[self.posnum].x + random.randint(-12,12)
        self.y = GamePath.PATH[self.posnum].y + random.randint(-12,12)
        self.posnum += 1
        self.velocity = 200
        self.minvelocity = 20
        self.maxvelocity = 200
        self.life = 70

    def draw(self, screen):
        pygame.draw.circle(screen, (200,80,80), (int(self.x),int(self.y)) , 8)
        pygame.draw.circle(screen, (20,0,0), (int(self.x),int(self.y)) , 9, 1)
        pygame.draw.circle(screen, (255,100,100), (int(self.x),int(self.y)) , 8, 1)
    
    def receive_damage(self, damage):
        self.life -= damage
        if self.life <= 0:
            self.destruct()

    def logic(self, new_time):
        GameObject.logic(self,new_time)
        if self.posnum not in GamePath.PATH:
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
            self.time_between_enemies /= 1 + 0.50 / self.enemy_n
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
    