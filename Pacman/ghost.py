import math
import random

from Object import Object
from variables import *


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

    def chase_behaviour(self, ghosts, pacman):
        pass

    def scattered_behaviour(self):
        pass

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

            if get_map_letter(*forward) in PATH:
                neighbors[forward] = self.dist_to_target(forward)
            if get_map_letter(*left) in PATH:
                neighbors[left] = self.dist_to_target(left)
            if get_map_letter(*right) in PATH:
                neighbors[right] = self.dist_to_target(right)

            print("C", neighbors)

            if self.state != "Frightened":
                min_coords = min(neighbors, key=neighbors.get)
            else:
                min_coords = random.choice(list(neighbors.keys()))
            return min_coords
        return 0, 0

    def get_dir(self, keys=None):
        # print(self.mode_changed)
        print("B", self.allow_turning)
        print("A", self.map_pos)
        print()
        if self.allow_turning != self.map_pos:
            min_coords = self.find_next()
            print("D", min_coords)
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
        print("E", self.dir)
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
        self.timer = 0
        self.count_flash = 0
        self.turn_off = False
        print("E MY BAD")

    def state_manager(self, ghosts, time, pacman):
        if self.state == "Chase":
            self.chase_behaviour(ghosts, pacman)
            self.timer += time
            if self.timer > 1500:
                pass
                # self.change_mode("Frightened")

        elif self.state == "Frightened":
            self.timer += time

            if self.timer > 4000:
                if (self.timer - 4000) > 250:
                    self.count_flash += 1
                    self.turn_off = not self.turn_off
                    self.timer = 4000
                if self.count_flash == 9:
                    # pass
                    self.change_mode("Chase")
        elif self.state == "Scattered":
            self.scattered_behaviour()

    def update(self, ghosts, time, pacman):
        self.state_manager(ghosts, time, pacman)
        self.move(self.dir)
        super().update_all()

    def show(self, screen):
        frame_translation = {(1, 0): 0, (-1, 0): 1, (0, -1): 2, (0, 1): 3}
        if self.state != "Frightened":
            screen.blit(self.animation[frame_translation[(self.dir[0], self.dir[1])]][self.frame],
                        (self.pos.x - self.size / 2, self.pos.y - self.size / 2))
        else:
            screen.blit(dead_ghost_sprites[1 if self.turn_off else 0][self.frame],
                        (self.pos.x - self.size / 2, self.pos.y - self.size / 2))

        # pygame.draw.circle(screen, (255, 0, 0), (self.target[0] * RATIO[0] + RATIO[0] / 2, self.target[1] * RATIO[1] + RATIO[1] / 2), self.size / 2)
