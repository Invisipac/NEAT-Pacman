from Object import Object
from variables import *
import math


class Ghost(Object):
    def __init__(self, map_pos, size, speed, animation, frame_lim):
        super().__init__(map_pos, size, speed, animation, frame_lim)
        self.state = "Chase"
        self.target = (-10, -10)

        self.timer = 0

        # this allows the ghost to turn only once ber grid square
        self.allow_turning = (0, 0)
        self.mode_changed = False

        # controls flashing ghost
        self.turn_off = False
        self.count_flash = 0

    def chase_behaviour(self, ghosts):
        pass

    def scattered_behaviour(self):
        pass

    def dist_to_target(self, pos):
        return math.sqrt((pos[0] - self.target[0]) ** 2 + (pos[1] - self.target[1]) ** 2)

    def find_neighbors(self):
        neighbors = {}
        if self.map_pos.x not in [0, GRID_SIZE[0] - 1]:
            forward = (self.map_pos.x + self.dir.x, self.map_pos.y + self.dir.y)
            left = (self.map_pos.x + self.dir.y, self.map_pos.y + self.dir.x)
            right = (self.map_pos.x - self.dir.y, self.map_pos.y - self.dir.x)

            if get_map_letter(*forward) in PATH:
                neighbors[forward] = self.dist_to_target()
            if map[row + self.dir[1]][col + self.dir[0]] in PATH:
                neighbors[(row + self.dir[1], col + self.dir[0])] = self.dist_to_target(
                    (row + self.dir[1], col + self.dir[0]))
            if map[row + self.dir[0]][col + self.dir[1]] in PATH:
                neighbors[(row + self.dir[0], col + self.dir[1])] = self.dist_to_target(
                    (row + self.dir[0], col + self.dir[1]))
            if map[row - self.dir[0]][col - self.dir[1]] in PATH:
                neighbors[(row - self.dir[0], col - self.dir[1])] = self.dist_to_target(
                    (row - self.dir[0], col - self.dir[1]))
