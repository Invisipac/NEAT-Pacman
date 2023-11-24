import pygame as pg
#ariel
class Ground:
    def __init__(self, y) -> None:
        self.y = y
    
    def draw(self, screen: pg.Surface, width):
        pg.draw.line(screen, (0, 0, 0), (0, self.y), (width, self.y))