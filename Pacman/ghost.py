from variables import *
from pygame.math import Vector2 as vec
from astar import astar
from pacman import Pacman
class Ghost:
    def __init__(self, pos, speed, colour) -> None:
        self.pos = vec(pos[0]*RATIO[0], pos[1]*RATIO[1])
        self.map_locs = vec(*pos)
        self.speed = vec(speed, speed)
        self.dir = [0, 0]
        self.colour = colour
        self.r = 10
    
    def find_map_loc(self):
        if (self.pos.x - RATIO[0] / 2) % RATIO[0] <= 1:
            self.map_locs.x = self.pos.x // RATIO[0]
            self.pos.x = self.map_locs.x* RATIO[0] + RATIO[0] / 2 
        if (self.pos.y - RATIO[1] / 2) % RATIO[1] <= 1:
            self.map_locs.y = self.pos.y // RATIO[1]
            self.pos.y = self.map_locs.y * RATIO[1] + RATIO[1] / 2

    def calculate_path(self, pacman):
        start = (int(self.map_locs.y), int(self.map_locs.x))
        goal = (int(pacman.map_locs.y), int(pacman.map_locs.x))
        
        grid = map

        Astar_path = list(reversed(astar(start, goal, grid)))
        print(len(Astar_path))
        x_diff = -(start[1] - Astar_path[1][1])
        y_diff = -(start[0] - Astar_path[1][0])


        if x_diff != 0:
            self.dir[0] = (x_diff)/abs(x_diff)
        else:
            self.dir[0] = 0
        if y_diff != 0:
            self.dir[1] = (y_diff)/abs(y_diff)
        else:
            self.dir[1] = 0
    
    def move_ghost(self, pacman: Pacman):
        self.find_map_loc()

        row = int(self.map_locs.y + self.dir[1])
        col = int(self.map_locs.x + self.dir[0])

        self.calculate_path(pacman)

        if map[row][col] in PATH and self.pos.x >= 0 and self.pos.x <= WIDTH:
            self.pos += vec(self.dir[0]*RATIO[0]/self.speed[0], self.dir[1]*RATIO[1]/self.speed[1])

    def draw_ghost(self, screen: pg.Surface):
        pg.draw.circle(screen, self.colour, self.pos, 10)
    
