from variables import *
from pygame.math import Vector2 as vec
from astar import astar
from pacman import Pacman
import random
class Ghost:
    def __init__(self, pos, speed, colour, pacman: Pacman) -> None:
        self.pos = vec(pos[0]*RATIO[0], pos[1]*RATIO[1])
        self.map_locs = vec(*pos)
        self.speed = vec(speed, speed)
        self.dir = [0, 0]
        self.colour = colour
        self.r = 10
        self.start = (int(self.map_locs.y), int(self.map_locs.x))
        self.cur_path = list(reversed(astar(self.start, self.start, map)))
        self.pacman = pacman
        self.state = "Scatter"
        self.random_target = self.find_random_pos()
        # self.random_pos = (0, 0)


    def find_map_loc(self):
        if (self.pos.x - RATIO[0] / 2) % RATIO[0] <= 1:
            self.map_locs.x = self.pos.x // RATIO[0]
            self.pos.x = self.map_locs.x* RATIO[0] + RATIO[0] / 2 
        if (self.pos.y - RATIO[1] / 2) % RATIO[1] <= 1:
            self.map_locs.y = self.pos.y // RATIO[1]
            self.pos.y = self.map_locs.y * RATIO[1] + RATIO[1] / 2
    
    def update(self, target):
        if self.state == "Chase":
            target = (int(self.pacman.map_locs.y), int(self.pacman.map_locs.x))
        elif self.state == "Scatter":
            target = self.random_target
            if len(self.cur_path) < 4:
                target = self.find_random_pos()
                self.random_target = target
        self.find_map_loc()
        self.start = (int(self.map_locs.y), int(self.map_locs.x))        
        self.cur_path = list(reversed(astar(self.start, target, map)))

    def calculate_dir(self):
        # Astar_path = list(reversed(astar(start, goal, grid)))
        # print(Astar_path)
        if len(self.cur_path) > 1:
            #print(self.cur_path)
            x_diff = self.cur_path[1][1] - self.start[1] 
            y_diff = self.cur_path[1][0] - self.start[0]

            if x_diff != 0:
                self.dir[0] = (x_diff)/abs(x_diff)
            else:
                self.dir[0] = 0
            if y_diff != 0:
                self.dir[1] = (y_diff)/abs(y_diff)
            else:
                self.dir[1] = 0
        
        else:
            self.dir = [0, 0]
    
    
    def find_random_pos(self):
        not_obs = []
        for i, l in enumerate(map):
            for j, c in enumerate(l):
                if c in NODES or c in POWER_DOTS:
                    not_obs.append((i, j))
        
        return random.choice(not_obs)
        
        # self.move_ghost(random_pos)
    def move_scared_ghost(self):
        pass
    
    def move_ghost(self):

        row = int(self.map_locs.y + self.dir[1])
        col = int(self.map_locs.x + self.dir[0])

        self.calculate_dir()

        if map[row][col] in PATH and self.pos.x >= 0 and self.pos.x <= WIDTH:
            self.pos += vec(self.dir[0]*RATIO[0]/self.speed[0], self.dir[1]*RATIO[1]/self.speed[1])

    def draw_ghost(self, screen: pg.Surface):
        pg.draw.circle(screen, self.colour, self.pos, 10)
    
