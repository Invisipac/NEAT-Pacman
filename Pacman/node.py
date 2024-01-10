import pygame
from variables import *

class Node:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.neighbors = {}

    def show(self, display):
        for n in self.neighbors.keys():
            if self.neighbors[n]:
                line_start = self.pos
                line_end = self.neighbors[n].pos
                pygame.draw.line(display, (255, 255, 255), (line_start.x, line_start.y), (line_end.x, line_end.y), 4)
                pygame.draw.circle(display, (200, 50, 50), (self.pos.x, self.pos.y), 8)
