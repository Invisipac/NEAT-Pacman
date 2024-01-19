import math
import random

from pygame.math import Vector2 as vec

from pacman import Pacman
from variables import *


class Ghost:
    def __init__(self, pos, speed, image_list, pacman: Pacman) -> None:
        self.pos = vec(pos[0] * RATIO[0] + RATIO[0] / 2, pos[1] * RATIO[1] + RATIO[1] / 2)
        self.map_locs = vec(*pos)
        self.speed = vec(speed, speed)
        self.dir = [1, 0]
        self.image_list = image_list
        self.frame = 0
        self.frame_counter = 0
        self.frame_speed = 4
        self.r = 21
        self.pacman = pacman
        self.state = "Chase"
        self.target = (-10, -10)
        # self.start_scared = True
        self.timer = 0
        # self.can_move = True
        self.turn = (0, 0)
        self.mode_changed = False
        self.turn_off = False
        self.count_flash = 0

    def find_map_loc(self):

        if get_map_letter((self.pos.x // RATIO[0]) % GRID_SIZE[0], self.pos.y // RATIO[1]) in PATH:
            if (self.pos.x - RATIO[0] / 2) % RATIO[0] <= 5:
                self.map_locs.x = self.pos.x // RATIO[0]
                self.pos.x = self.map_locs.x * RATIO[0] + RATIO[0] / 2
            # elif (self.pos.x + RATIO[0] / 2) % RATIO[0] <= 5:
            #     self.map_locs.x = self.pos.x // RATIO[0] + 1
            #     self.pos.x = self.map_locs.x * RATIO[0] + RATIO[0] / 2
            if (self.pos.y - RATIO[1] / 2) % RATIO[1] <= 5:
                self.map_locs.y = self.pos.y // RATIO[1]
                self.pos.y = self.map_locs.y * RATIO[1] + RATIO[1] / 2
            # elif (self.pos.y + RATIO[1] / 2) % RATIO[1] <= 5:
            #     self.map_locs.y = self.pos.y // RATIO[1] + 1
            #     self.pos.y = self.map_locs.y * RATIO[1] + RATIO[1] / 2



        if self.map_locs.x == -1:
            self.map_locs.x = 0
        if self.map_locs.x == GRID_SIZE[0]:
            self.map_locs.x = GRID_SIZE[0] - 1

    def chase_behaviour(self, ghosts):
        pass

    def scattered_behaviour(self):
        pass

    def update(self, ghosts, time):
        self.frame_counter += 1
        # print(self.timer)
        # print(self.map_locs)
        if self.frame_counter > self.frame_speed:
            self.frame = (self.frame + 1) % 2
            self.frame_counter = 0

        if self.state == "Chase":
            self.chase_behaviour(ghosts)
            self.timer += time

            if self.timer > 500:
                # pass
                self.change_mode("Frightened")

        elif self.state == "Frightened":
            self.timer += time

            if self.timer > 500:
                if (self.timer - 4000) > 250:
                    self.count_flash += 1
                    self.turn_off = not self.turn_off
                    self.timer = 4000
                if self.count_flash == 0:
                    pass
                    # self.change_mode("Chase")
        elif self.state == "Scattered":
            self.scattered_behaviour()

    def dist_to_pacman(self):
        return math.sqrt(
            (self.map_locs.x - self.pacman.map_locs.x) ** 2 + (self.map_locs.y - self.pacman.map_locs.y) ** 2)

    def dist_to_target(self, pos):
        return math.sqrt((pos[0] - self.target[0]) ** 2 + (pos[1] - self.target[1]) ** 2)

    def change_mode(self, new_mode):
        # self.dir = [self.dir[0] * -1, self.dir[1] * -1]
        self.state = new_mode
        self.mode_changed = True
        self.timer = 0
        self.count_flash = 0
        self.turn_off = False

    def teleport(self):
        if self.pos.x - self.r > WIDTH:
            self.pos.x = -self.r
        elif self.pos.x < -self.r:
            self.pos.x = WIDTH + self.r

    def move_ghost(self):
        row = int(self.map_locs.y)
        col = int(self.map_locs.x)

        ################################ BIG BUG - GHOSTS SOMETIMES IGNORE THE LAWS OF PHYSICS AND TURN IN THE SAME
        ################################ TIME BECAUSE OF THIS CODE, NEEDS TO BE PREVENTED, HELP PLEASE

        neighbors = {}
        if col not in [0, 27]:
            if map[row + self.dir[1]][col + self.dir[0]] in PATH:
                neighbors[(row + self.dir[1], col + self.dir[0])] = self.dist_to_target(
                    (row + self.dir[1], col + self.dir[0]))
            if map[row + self.dir[0]][col + self.dir[1]] in PATH:
                neighbors[(row + self.dir[0], col + self.dir[1])] = self.dist_to_target(
                    (row + self.dir[0], col + self.dir[1]))
            if map[row - self.dir[0]][col - self.dir[1]] in PATH:
                neighbors[(row - self.dir[0], col - self.dir[1])] = self.dist_to_target(
                    (row - self.dir[0], col - self.dir[1]))

            if self.state != "Frightened":
                min_coords = min(neighbors, key=neighbors.get)
            else:
                min_coords = random.choice(list(neighbors.keys()))
            # print(self.map_locs, neighbors, "AHHHHHHHHH")
            # if self.mode_changed:
            #     self.turn = vec(self.map_locs.x + self.dir[0], self.map_locs.y + self.dir[1])
            #     self.dir = [self.dir[0] * -1, self.dir[1] * -1]
            #     self.mode_changed = False
            if self.turn != self.map_locs:
                if [min_coords[1] - col, min_coords[0] - row] != self.dir:
                    self.dir = [min_coords[1] - col, min_coords[0] - row]
                    self.turn = self.map_locs.copy()
            # if self.mode_changed:
            #     self.dir = [self.dir[0] * -1, self.dir[1] * -1]
            #     print(list(neighbors.keys()), "---------")
            #     if (row + self.dir[0] * -1, col + self.dir[1] * -1) in list(neighbors.keys()):
            #         print("ADWAJKDHWAIUDHWAUIDHWAIUD")
            #     self.mode_changed = False

        if map[row + self.dir[1]][(col + self.dir[0]) % len(map[0])] in PATH and 0 <= self.map_locs.x <= len(map[0]):
            # print("BBBBBBBBB")
            self.pos += vec(self.dir[0] * RATIO[0] / self.speed[0], self.dir[1] * RATIO[1] / self.speed[1])
            self.teleport()
        self.find_map_loc()

    def draw_ghost(self, screen: pg.Surface):
        frame_translation = {(1, 0): 0, (-1, 0): 1, (0, -1): 2, (0, 1): 3}
        if self.state != "Frightened":
            screen.blit(self.image_list[frame_translation[(self.dir[0], self.dir[1])]][self.frame],
                        (self.pos.x - self.r, self.pos.y - self.r))
        else:
            screen.blit(dead_ghost_sprites[1 if self.turn_off else 0][self.frame],
                        (self.pos.x - self.r, self.pos.y - self.r))

        # pg.draw.circle(screen, (255, 0, 0), (self.target[1] * RATIO[1] + RATIO[1] / 2, self.target[0] * RATIO[0] + RATIO[0] / 2), 15)
