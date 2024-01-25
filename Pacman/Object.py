from pygame.math import Vector2 as vec

from variables import *


class Object:
    def __init__(self, map_pos, size, speed, animation, frame_lim, lives=3, points=0):
        self.map_pos = vec(*map_pos)
        self.pos = vec((self.map_pos.x + 0.5) * RATIO[0], (self.map_pos.y + 0.5) * RATIO[1])

        self.size = size

        self.dir = (0, -1)
        self.speed = speed

        self.animation = animation
        self.frame = 0
        self.frame_lim = frame_lim
        self.frame_counter = 0
        self.frame_speed = 7

        self.can_turn = [False, False]

        self.moved = False
        self.lives = lives

    @staticmethod
    def convert_map_to_pixel(map_pos, coordinate_type):
        return (map_pos.x * RATIO[0] + RATIO[0] / 2) if coordinate_type == "x" else (
                map_pos.y * RATIO[1] + RATIO[1] / 2)

    def snap_to_grid(self, state="", outside_box=True):
        # if not trapped:
        self.can_turn = [False, False]
        if (self.pos.x - RATIO[0] / 2) % RATIO[0] <= 5:
            self.map_pos.x = self.pos.x // RATIO[0]
            # self.pos.x = self.convert_map_to_pixel(self.map_pos, "x")
            self.can_turn[1] = True
        elif (self.pos.x + RATIO[0] / 2) % RATIO[0] <= 5:
            self.map_pos.x = self.pos.x // RATIO[0] + 1
            # self.pos.x = self.convert_map_to_pixel(self.map_pos, "x")
            self.can_turn[1] = True

        if not outside_box or state == "Dead":
            # print(abs(self.pos.x - 336))
            if abs(self.pos.x - 336) < 3:
                self.map_pos.x = 13.5
                self.pos.x = 336
                self.can_turn[1] = True
            # elif (self.pos.x + RATIO[0] / 2) % RATIO[0] <= 5:
            #     self.map_pos.x = self.pos.x // RATIO[0] + 1
            #     # self.pos.x = self.convert_map_to_pixel(self.map_pos, "x")
            #     self.can_turn[1] = True
        # else:
        #     if (self.pos.x - RATIO[0] / 2) % (RATIO[0]/2) <= 2:
        #         self.map_pos.x = (self.pos.x // (RATIO[0]/2)) / 2
        #         self.can_turn[1] = True
        #     elif (self.pos.x + RATIO[0] / 2) % (RATIO[0]/2) <= 2:
        #         self.map_pos.x = (self.pos.x // (RATIO[0]/2)) / 2 + 1
        #         self.can_turn[1] = True

        if (self.pos.y - RATIO[1] / 2) % RATIO[1] <= 5:
            self.map_pos.y = self.pos.y // RATIO[1]
            # self.pos.y = self.convert_map_to_pixel(self.map_pos, "y")
            self.can_turn[0] = True
        elif (self.pos.y + RATIO[1] / 2) % RATIO[1] <= 5:
            self.map_pos.y = self.pos.y // RATIO[1] + 1
            # self.pos.y = self.convert_map_to_pixel(self.map_pos, "y")
            self.can_turn[0] = True

        self.map_pos.x = 0 if self.map_pos.x == -1 else self.map_pos.x
        self.map_pos.x = GRID_SIZE[0] - 1 if self.map_pos.x == GRID_SIZE[0] else self.map_pos.x

    def teleport(self):
        if self.pos.x - self.size / 2 > WIDTH:
            self.pos.x = -self.size / 2
        elif self.pos.x < -self.size / 2:
            self.pos.x = WIDTH + self.size / 2

    def update_animation(self, dead=False):
        self.frame_counter += 1
        if not dead:
            if self.frame_counter > self.frame_speed and ((self.moved or self.frame != 0) or self.frame_lim == 2):
                self.frame = (self.frame + 1) % self.frame_lim
                self.frame_counter = 0
        else:
            if self.frame_counter > self.frame_speed:
                if self.frame < 13:
                    self.frame += 1
                self.frame_counter = 0

    def move(self, direction, trapped=False, possible_path=PATH):
        turn_translator = {(1, 0): 0, (-1, 0): 0, (0, 1): 1, (0, -1): 1}
        # print(direction, "yy")
        # print("F", self.frame_lim, self.can_turn[turn_translator[direction]])
        # print("H", get_map_letter((self.map_pos.x + direction[0]) % len(map[0]), self.map_pos.y + direction[1]) in PATH)
        # print("I", 0 <= self.map_pos.x <= len(map[0]) and 0 < self.map_pos.y < len(map) - 1)
        # print("J", self.can_turn, self.pos)

        if (self.can_turn == [True, False] or self.can_turn == [False, True]) and self.frame_lim == 2 and not trapped:
            if get_map_letter(*self.map_pos) in possible_path:
                self.pos += pygame.Vector2(self.dir[0] * RATIO[0] / self.speed, self.dir[1] * RATIO[1] / self.speed)

        else:
            if trapped:
                if get_map_letter((self.map_pos.x + direction[0]) % len(map[0]), self.map_pos.y + direction[1]) in possible_path:
                    if (14 * RATIO[1]) < self.pos.y < (15 * RATIO[1]):
                        self.pos += pygame.Vector2(self.dir[0] * RATIO[0] / self.speed, self.dir[1] * RATIO[1] / self.speed)
                    else:
                        if self.pos.y > 348:
                            self.map_pos.y = 15
                        else:
                            self.map_pos.y = 13
                        self.pos += pygame.Vector2(self.dir[0] * RATIO[0] / self.speed,
                                                   self.dir[1] * RATIO[1] / self.speed)

            else:
                if get_map_letter((self.map_pos.x + direction[0]) % len(map[0]), self.map_pos.y + direction[1]) in possible_path and \
                        0 <= self.map_pos.x <= len(map[0]) and 0 < self.map_pos.y < len(map) - 1 and self.can_turn[
                    turn_translator[direction]]:
                    self.pos += vec(direction[0] * RATIO[0] / self.speed, direction[1] * RATIO[1] / self.speed)
                    # print("YAY MOVING")
                    self.teleport()
                    self.dir = direction
                    return True
        return False

    def update_all(self, state="", outside_box=True, dead=False):
        self.update_animation(dead)
        self.snap_to_grid(state, outside_box)
        self.get_dir()
        self.teleport()

    def get_dir(self):
        pass

    def show(self, screen, nothing=False):
        pass
