from variables import *
from pygame.math import Vector2 as vec
from astar import astar
from pacman import Pacman
import random
import math
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
        self.state = "Chase"
        self.target = (0, 0)
        self.start_scared = True
        self.timer = 0
        self.can_move = True
        # self.random_target = self.find_random_pos()
        # self.need_new_scared_path = True
        # self.scared_positions = []
        # self.scare_radius = 8
        #self.scared_pos = self.find_scared_pos()
        # self.random_pos = (0, 0)


    def find_map_loc(self):
        if (self.pos.x - RATIO[0] / 2) % RATIO[0] <= 1:
            self.map_locs.x = self.pos.x // RATIO[0]
            self.pos.x = self.map_locs.x* RATIO[0] + RATIO[0] / 2 
            self.can_move = True
        if (self.pos.y - RATIO[1] / 2) % RATIO[1] <= 1:
            self.map_locs.y = self.pos.y // RATIO[1]
            self.pos.y = self.map_locs.y * RATIO[1] + RATIO[1] / 2
            self.can_move = True
    
    def update(self):
        self.timer += 0.1
        if self.state == "Chase":
            self.target = (int(self.pacman.map_locs.y), int(self.pacman.map_locs.x))
            self.find_map_loc()
            self.start = (int(self.map_locs.y), int(self.map_locs.x))        
            self.cur_path = list(reversed(astar(self.start, self.target, map)))
            self.calculate_dir()
            if self.timer > 10:
                self.state = "Scared"
                self.start_scared = True
                self.timer = 0
        elif self.state == "Scared":
            self.move_scared()
            if self.timer > 10:
                self.state = "Chase"
                self.timer = 0
        # elif self.state == "Scatter":
        #     #target = self.random_target
        #     if len(self.cur_path) == 1:
        #         self.target = self.find_random_pos()
        #         #self.random_target = target
        # elif self.state == "Scared":
        #     self.find_scared_pos()
        
    
    def dist_to_pacman(self):
        return math.sqrt((self.pos.x - self.pacman.pos.x)**2 + (self.pos.y - self.pacman.pos.y)**2)

    def move_towards(self, node):
        x_diff = node[0] - self.map_locs.x 
        y_diff = node[1] - self.map_locs.y

        if x_diff != 0:
            self.dir[0] = (x_diff)//abs(x_diff)
        else:
            self.dir[0] = 0
        if y_diff != 0:
            self.dir[1] = (y_diff)//abs(y_diff)
        else:
            self.dir[1] = 0
        

    def move_scared(self):
        l, r = 0, 0
        if self.start_scared:
            
            self.dir = [0, 0]
            x_diff = self.pacman.pos.x - self.pos.x
            y_diff = self.pacman.pos.y - self.pos.y

            if self.pacman.dir == "RIGHT" or self.pacman.dir == "LEFT":
                if x_diff != 0:
                    self.dir[0] = -int(x_diff/abs(x_diff))
                else:
                    self.dir[0] = 0
                    self.dir[1] = -int(y_diff/abs(y_diff))
            else:
                if y_diff != 0:
                    self.dir[1] = -int(y_diff/abs(y_diff))
                else:
                    self.dir[1] = 0
                    self.dir[0] = -int(x_diff/abs(x_diff))
            print(self.pacman.dir, x_diff, y_diff, self.dir)
            self.start_scared = False

        
        row = int(self.map_locs.y) 
        col = int(self.map_locs.x)
        # self.find_map_loc()
        #some bug that dir is not an int but a float but the value is right???
        #temp fix

        if self.can_move:
            possible_nodes = []
            possible_nodes.append((col + self.dir[0], row + self.dir[1]))
            possible_nodes.append((col + self.dir[1], row + self.dir[0]))
            possible_nodes.append((col - self.dir[1], row - self.dir[0]))
            for n in possible_nodes:
                if map[int(n[1])][int(n[0])] in OBSTACLES:
                    possible_nodes.remove(n)
            self.target = random.choice(possible_nodes)
            print(self.target, self.map_locs, possible_nodes)
            self.move_towards(self.target)
            self.can_move = False

            
    def calculate_dir(self):
        # Astar_path = list(reversed(astar(start, goal, grid)))
        # print(Astar_path)
        if len(self.cur_path) > 1:
            #print(self.cur_path)
            x_diff = self.cur_path[1][1] - self.start[1] 
            y_diff = self.cur_path[1][0] - self.start[0]

            if x_diff != 0:
                self.dir[0] = (x_diff)//abs(x_diff)
            else:
                self.dir[0] = 0
            if y_diff != 0:
                self.dir[1] = (y_diff)//abs(y_diff)
            else:
                self.dir[1] = 0
        
        else:
            self.dir = [0, 0]
    
    
    
    
    def move_ghost(self):

        row = int(self.map_locs.y + self.dir[1])
        col = int(self.map_locs.x + self.dir[0])
        if map[row][col] in PATH and self.pos.x >= 0 and self.pos.x <= WIDTH:
            self.pos += vec(self.dir[0]*RATIO[0]/self.speed[0], self.dir[1]*RATIO[1]/self.speed[1])
        self.find_map_loc()


    def draw_ghost(self, screen: pg.Surface):
        pg.draw.circle(screen, self.colour, self.pos, 10)
    
