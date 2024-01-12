from variables import *
from pygame.math import Vector2 as vec


class Ghost:
    def __init__(self, pos, speed, colour) -> None:
        self.pos = vec(pos[0]*RATIO[0], pos[1]*RATIO[1])
        self.map_locs = vec(*pos)
        self.speed = vec(speed, speed)
        self.dir = (0, 0)
        self.dir = None
        self.colour = colour
        self.r = 10
    
    def find_map_loc(self):
        if (self.pos.x - RATIO[0] / 2) % RATIO[0] <= 1:
            self.map_locs.x = self.pos.x // RATIO[0]
            self.pos.x = self.map_locs.x* RATIO[0] + RATIO[0] / 2 
        if (self.pos.y - RATIO[1] / 2) % RATIO[1] <= 1:
            self.map_locs.y = self.pos.y // RATIO[1]
            self.pos.y = self.map_locs.y * RATIO[1] + RATIO[1] / 2

    def move_ghost(self, dir = (1, 0)):

        self.dir = dir

        self.find_map_loc()

        row = int(self.map_locs.y + 1*dir[1])
        col = int(self.map_locs.x + 1*dir[0])

        if map[row][col] in PATH and self.pos.x >= 0 and self.pos.x <= WIDTH:
            self.pos += vec(self.dir[0]*RATIO[0]/self.speed[0], self.dir[1]*RATIO[1]/self.speed[1])

    def draw_ghost(self, screen: pg.Surface):
        pg.draw.circle(screen, self.colour, self.pos, 10)
    
