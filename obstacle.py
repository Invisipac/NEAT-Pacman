import pygame as pg
from random import randint
class Obstacle:
    def __init__(self, x, groundLevel, w, h) -> None:
        self.x, self.y = x, groundLevel
        self.w, self.h = w, h
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.colour = (0, 0, 0)
        self.pos = pg.math.Vector2(x, self.y - self.h)
        self.vel = pg.math.Vector2(-4, 0)

    def setPos(self, x, y):
        self.x, self.y = x, y
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.pos = pg.math.Vector2(x, y)
    
    def move(self, rightBound):
        self.pos += self.vel
        self.rect = pg.Rect(self.pos.x, self.pos.y, self.w, self.h)
        
    
    def draw(self, screen: pg.Surface):
        pg.draw.rect(screen, self.colour, self.rect)

class Bird(Obstacle):
    def __init__(self, x, groundLevel, w, h) -> None:
        super().__init__(x, groundLevel, w, h)