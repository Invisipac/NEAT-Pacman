from variables import *
from pygame.math import Vector2 as vec


class Ghost:
    def __init__(self, pos, speed, colour) -> None:
        self.pos = vec(pos[0]*RATIO[0], pos[1]*RATIO[1])
        self.speed = speed
        self.dir = None
        self.colour = colour
        self.r = 10
    
    def draw_ghost(self, screen: pg.Surface):
        pg.draw.circle(screen, self.colour, self.pos, 10)
    
