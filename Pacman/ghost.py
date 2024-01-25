import math
import random

from Object import Object
from variables import *
from pygame.math import Vector2 as vec

class Ghost(Object):
    def __init__(self, map_pos, size, speed, animation, frame_lim):
        super().__init__(map_pos, size, speed, animation, frame_lim)
        self.state = "Scattered"
        self.target = (-10, -10)
        self.possible_path = PATH.copy()
        self.timer = 0
        self.frightened_timer = 0
        self.old_mode = "Scattered"
        self.mode_counter = 0
        self.point_limit = 0
        # this allows the ghost to turn only once ber grid square
        self.allow_turning = (0, 0)
        self.mode_changed = False
        self.trapped = False
        # controls flashing ghost
        self.turn_off = False
        self.count_flash = 0
        self.outside_box = self.map_pos.x < 10 or self.map_pos.x > 16 or self.map_pos.y < 12 or self.map_pos.y > 16

        self.score = 0
        self.show_score = False

    def chase_behaviour(self, ghosts, pacman):
        pass

    def scattered_behaviour(self):
        pass

    def dead_behaviour(self):
        if self.target[0] != 13.5:
            self.target = (13.5, 11)
        if self.map_pos == (13.5, 11):
            self.pos.x = 336
            self.target = (13.5, 13)
        if self.map_pos == (13.5, 13):
            self.change_mode(self.old_mode)
            self.trapped = False
            self.target = (13.5, 11)



    def dist_to_pacman(self, pacman):
        return math.sqrt((self.map_pos.x - pacman.map_pos.x) ** 2 + (self.map_pos.y - pacman.map_pos.y) ** 2)

    def dist_to_target(self, pos):
        return math.sqrt((pos[0] - self.target[0]) ** 2 + (pos[1] - self.target[1]) ** 2)

    def find_next(self):
        neighbors = {}
        if self.map_pos.x not in [0, GRID_SIZE[0] - 1]:
            forward = (self.map_pos.x + self.dir[0], self.map_pos.y + self.dir[1])
            left = (self.map_pos.x + self.dir[1], self.map_pos.y + self.dir[0])
            right = (self.map_pos.x - self.dir[1], self.map_pos.y - self.dir[0])
            backward = (self.map_pos.x - self.dir[0], self.map_pos.y - self.dir[1])
            if not self.trapped:
                self.outside_box = self.map_pos.x < 10 or self.map_pos.x > 16 or self.map_pos.y < 12 or self.map_pos.y > 16

            if self.trapped:
                if get_map_letter(*forward) in self.possible_path:
                    neighbors[forward] = self.dist_to_target(forward)
                elif get_map_letter(*backward) in self.possible_path:
                    neighbors[backward] = self.dist_to_target(backward)
            else:
                if get_map_letter(*forward) in self.possible_path:
                    neighbors[forward] = self.dist_to_target(forward)
                if get_map_letter(*left) in self.possible_path:
                    neighbors[left] = self.dist_to_target(left)
                if get_map_letter(*right) in self.possible_path:
                    neighbors[right] = self.dist_to_target(right)

            # print('A', self.map_pos, neighbors)

            if not self.outside_box and not self.trapped:
                self.speed = 24
                if self.map_pos.x < 13.5:
                    min_coords = (self.map_pos.x + 1, self.map_pos.y)
                elif self.map_pos.x > 13.5:
                    min_coords = (self.map_pos.x - 1, self.map_pos.y)
                else:
                    min_coords = min(neighbors, key=neighbors.get)
            else:
                if self.state != "Frightened" or self.trapped:
                    min_coords = min(neighbors, key=neighbors.get)
                else:
                    if self.outside_box:
                        min_coords = random.choice(list(neighbors.keys()))
                    else:
                        min_coords = min(neighbors, key=neighbors.get)
            return min_coords
        return 0, 0

    def get_dir(self, keys=None):
        # print(self.target, self.map_pos, self.pos)
        # print(self.mode_changed)
        # print("B", self.allow_turning)
        # print("A", self.map_pos)
        # print()
        if self.target == (13.5, 13):
            self.can_turn = [False, True]
            self.dir = (0, 1)
        elif self.trapped or (not self.trapped and not self.outside_box):
            min_coords = self.find_next()
            self.can_turn = [False, True]
            # print('B', self.map_pos,min_coords, get_map_letter(*min_coords) in self.possible_path, self.dir, self.can_turn)
            self.dir = (min_coords[0] - self.map_pos.x, min_coords[1] - self.map_pos.y)
        elif self.allow_turning != self.map_pos:
            min_coords = self.find_next()
            # print("D", min_coords)
            if min_coords != (0, 0):
                self.dir = (min_coords[0] - self.map_pos.x, min_coords[1] - self.map_pos.y)
                self.allow_turning = self.map_pos.copy()
        elif self.mode_changed:
            if self.can_turn == [True, True]:
                min_coords = self.find_next()
                if min_coords != (0, 0):
                    self.dir = (min_coords[0] - self.map_pos.x, min_coords[1] - self.map_pos.y)
                self.mode_changed = False

            # elif self.can_turn == [True, False] or self.can_turn == [False, True]:
            #     self.pos += pygame.Vector2(self.dir[0] * RATIO[0] / self.speed, self.dir[1] * RATIO[1] / self.speed)
            # self.pos.x = self.convert_map_to_pixel(self.map_pos, "x")
            # self.pos.y = self.convert_map_to_pixel(self.map_pos, "y")
        # print("E", self.dir)
        # else:
        #     if self.mode_changed:
        #         min_coords = self.find_next()
        #         # print(min_coords, "dddddddddd")
        #         if min_coords != (0, 0):
        #             self.dir = (min_coords[0] - self.map_pos.x, min_coords[1] - self.map_pos.y)
        #             self.mode_changed = False

    def change_mode(self, new_mode):
        self.dir = (self.dir[0] * -1, self.dir[1] * -1)
        self.state = new_mode
        self.mode_changed = True
        self.frightened_timer = 0
        self.count_flash = 0
        self.turn_off = False
        # print("E MY BAD")

    def state_manager(self, ghosts, time, pacman, ghost_timer):
        if self.state == "Chase":
            self.speed = 8
            self.timer += time

            if self.outside_box:
                self.chase_behaviour(ghosts, pacman)

            if self.mode_counter < len(times):
                if self.timer > times[self.mode_counter]:
                    self.change_mode("Scattered")
                    self.old_mode = "Scattered"
                    self.mode_counter += 1
                    self.timer = 0

        elif self.state == "Frightened":
            self.speed = 12
            self.frightened_timer += time

            if self.frightened_timer > 4000:
                if (self.frightened_timer - 4000) > 250:
                    self.count_flash += 1
                    self.turn_off = not self.turn_off
                    self.frightened_timer = 4000
                if self.count_flash == 9:
                    self.change_mode(self.old_mode)

        elif self.state == "Scattered":
            self.speed = 8
            self.timer += time

            if self.outside_box:
                self.scattered_behaviour()

            if self.timer > times[self.mode_counter]:
                self.change_mode("Chase")
                self.old_mode = "Chase"
                self.mode_counter += 1
                self.timer = 0

        elif self.state == "Dead":
            self.speed = 6
            self.dead_behaviour()

        if self.trapped:
            self.speed = 24

    def update(self, ghosts, time, pacman, ghost_timer):
        if not self.trapped:
            if not self.outside_box or self.state == "Dead":
                if EXIT not in self.possible_path:
                    self.possible_path.append(EXIT)
                # print('a', str(self.map_pos), str(self.possible_path))
            else:
                if EXIT in self.possible_path:
                    self.possible_path.remove(EXIT)
        if self.trapped:
            self.can_turn = [False, True]

        self.state_manager(ghosts, time, pacman, ghost_timer)

        if self.map_pos.y == 14 and (self.map_pos.x <= 5 or self.map_pos.x >= 22) and self.state != "Dead":
            self.speed = 12

        super().update_all(self.state, self.outside_box)
        self.move(self.dir, self.trapped, self.possible_path)

    def show(self, screen, nothing=False):
        frame_translation = {(1, 0): 0, (-1, 0): 1, (0, -1): 2, (0, 1): 3}
        if self.state in ["Chase", "Scattered"]:
            screen.blit(self.animation[frame_translation[(self.dir[0], self.dir[1])]][self.frame],
                        (self.pos.x - self.size / 2, self.pos.y + (offset * RATIO[1]) - self.size / 2))
        elif self.state == "Frightened":
            screen.blit(dead_ghost_sprites[1 if self.turn_off else 0][self.frame],
                        (self.pos.x - self.size / 2, self.pos.y + (offset * RATIO[1]) - self.size / 2))
        else:
            if not nothing:
                screen.blit(dead_ghost_sprites[2][frame_translation[(self.dir[0], self.dir[1])]],
                            (self.pos.x - self.size / 2, self.pos.y + (offset * RATIO[1]) - self.size / 2))

        # pygame.draw.circle(screen, (255, 0, 0), (self.target[0] * RATIO[0] + RATIO[0] / 2, self.target[1] * RATIO[1] + RATIO[1] / 2), self.size / 2)
