import math
import random

from pygame.math import Vector2 as vec

from astar import astar
from pacman import Pacman
from variables import *


class Ghost:
    def __init__(self, pos, speed, colour, pacman: Pacman) -> None:
        self.pos = vec(pos[0] * RATIO[0], pos[1] * RATIO[1])
        self.map_locs = vec(*pos)
        self.speed = vec(speed, speed)
        self.dir = [1, 0]
        self.colour = colour
        self.r = 10
        self.start = (int(self.map_locs.y), int(self.map_locs.x))
        self.cur_path = list(reversed(astar(self.start, self.start, map, self.dir)))
        self.cur_path = list(reversed(astar(self.start, self.start, map, self.dir)))
        self.pacman = pacman
        self.state = "Chase"
        self.target = (-10, -10)
        self.start_scared = True
        self.timer = 0
        self.can_move = True

    def find_map_loc(self):
        if (self.pos.x - RATIO[0] / 2) % RATIO[0] <= 1:
            self.map_locs.x = self.pos.x // RATIO[0]
            self.pos.x = self.map_locs.x * RATIO[0] + RATIO[0] / 2
            self.can_move = True
        if (self.pos.y - RATIO[1] / 2) % RATIO[1] <= 1:
            self.map_locs.y = (self.pos.y // RATIO[1]) % len(map)
            self.pos.y = self.map_locs.y * RATIO[1] + RATIO[1] / 2
            self.can_move = True

    def chase_behaviour(self):
        pass

    def update(self):
        self.timer += 0.1
        if self.state == "Chase":
            self.chase_behaviour()
            # if self.timer > 10:
            #     self.state = "Scared"
            #     self.timer = 0
        elif self.state == "Scared":
            self.move_scared()
            #print(self.dir, self.target, self.map_locs)
            if self.timer > 10:
                self.state = "Chase"
                self.timer = 0

    def dist_to_pacman(self):
        return math.sqrt((self.pos.x - self.pacman.pos.x) ** 2 + (self.pos.y - self.pacman.pos.y) ** 2)

    def move_towards(self, node):
        x_diff = node[0] - self.map_locs.x
        y_diff = node[1] - self.map_locs.y

        if x_diff != 0:
            self.dir[0] = (x_diff) // abs(x_diff)
        else:
            self.dir[0] = 0
        if y_diff != 0:
            self.dir[1] = (y_diff) // abs(y_diff)
        else:
            self.dir[1] = 0

    def move_scared(self):
        l, r = 0, 0
        if self.start_scared:

            self.dir = [0, 0]
            x_diff = self.pacman.map_locs.x - self.map_locs.x
            y_diff = self.pacman.map_locs.y - self.map_locs.y
            if x_diff == 0 and y_diff == 0:
                return
            if self.pacman.dir == "RIGHT" or self.pacman.dir == "LEFT":
                if x_diff != 0:
                    self.dir[0] = -int(x_diff / abs(x_diff))
                else:
                    self.dir[0] = 0
                    self.dir[1] = -int(y_diff / abs(y_diff))
            else:
                if y_diff != 0:
                    self.dir[1] = -int(y_diff / abs(y_diff))
                else:
                    self.dir[1] = 0
                    self.dir[0] = -int(x_diff / abs(x_diff))
            # print(self.pacman.dir, x_diff, y_diff, self.dir)
            self.start_scared = False

        row = int(self.map_locs.y)
        col = int(self.map_locs.x)
        # self.find_map_loc()
        # some bug that dir is not an int but a float but the value is right???
        # temp fix

        if self.can_move:
            possible_nodes = []
            possible_nodes.append((col + self.dir[0], row + self.dir[1]))
            possible_nodes.append((col + self.dir[1], row + self.dir[0]))
            possible_nodes.append((col - self.dir[1], row - self.dir[0]))
            for n in possible_nodes:
                if map[n[1]%GRID_SIZE[1]][n[0]%GRID_SIZE[0]] == 'w' or n == (int(col - self.dir[0]), int(row - self.dir[1])):
                    not_possible_nodes.append(n)
            for n in not_possible_nodes:
                possible_nodes.remove(n)
            self.target = random.choice(possible_nodes)
            # print(self.target, self.map_locs, possible_nodes)
            self.move_towards(self.target)
            self.can_move = False

    def calculate_dir(self):
        if len(self.cur_path) > 1:
            # print(self.cur_path)
            x_diff = self.cur_path[1][1] - self.start[1]
            y_diff = self.cur_path[1][0] - self.start[0]

            if x_diff != 0:
                self.dir[0] = (x_diff) // abs(x_diff)
            else:
                self.dir[0] = 0
            if y_diff != 0:
                self.dir[1] = (y_diff) // abs(y_diff)
            else:
                self.dir[1] = 0

        else:
            self.dir = [1, 0]

    def move_ghost(self):

        row = int(self.map_locs.y + self.dir[1])
        col = int(self.map_locs.x + self.dir[0])
        if map[row][col] in PATH and self.pos.x >= 0 and self.pos.x <= WIDTH:
            self.pos += vec(self.dir[0] * RATIO[0] / self.speed[0], self.dir[1] * RATIO[1] / self.speed[1])
        self.find_map_loc()

    def draw_ghost(self, screen: pg.Surface):
        pg.draw.circle(screen, self.colour, self.pos, 10)
        for i, point in enumerate(self.cur_path):
            if point != self.cur_path[-1]:
                if i != 0 and i != len(self.cur_path) - 2:
                    pg.draw.line(screen, self.colour, (point[1] * RATIO[0] + RATIO[0] / 2, point[0] * RATIO[1] + RATIO[1] / 2), (self.cur_path[i+1][1] * RATIO[0] + RATIO[0] / 2, self.cur_path[i+1][0] * RATIO[1] + RATIO[1] / 2), 5)
                elif i == 0:
                    pg.draw.line(screen, self.colour,
                                 self.pos, (
                                 self.cur_path[i + 1][1] * RATIO[0] + RATIO[0] / 2,
                                 self.cur_path[i + 1][0] * RATIO[1] + RATIO[1] / 2), 5)
                else:
                    # pass
                    pg.draw.line(screen, self.colour,
                                 (point[1] * RATIO[0] + RATIO[0] / 2, point[0] * RATIO[1] + RATIO[1] / 2), self.pacman.pos, 5)
