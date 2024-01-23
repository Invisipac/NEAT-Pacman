import math

from Object import Object
from variables import *


class Pacman(Object):
    def __init__(self, map_pos, size, speed, animation, frame_lim, lives=3, points=0):
        super().__init__(map_pos, size, speed, animation, frame_lim, lives)
        self.wannabe_dir = (0, -1)
        self.points = points
        self.dead = False
        self.not_move = 0
        ####### AI VARIABLES #####
        self.surrounding_walls = []
        self.temp_dir = self.dir
        self.visited_squares = []
        self.time_since_move = 0
        self.prev_moves = []

    def found_new_square(self):
        if self.map_pos not in self.visited_squares:
            self.time_since_move = 0
            self.visited_squares.append(self.map_pos.copy())
            # print('a')
            return True
        else:
            if self.time_since_move > 500:
                self.time_since_move = 0
                return False
            return None
    def is_turned(self):
        if self.dir != self.temp_dir:
            self.temp_dir = self.dir
            return True
        else:
            return False
    def find_surrounding_walls(self):
        up = 1 if get_map_letter((self.map_pos.x + self.dir[0]) % len(map[0]), self.map_pos.y + self.dir[1]) in PATH else -1
        left = 1 if get_map_letter((self.map_pos.x + self.dir[1]) % len(map[0]), self.map_pos.y + self.dir[0]) in PATH else -1
        right = 1 if get_map_letter((self.map_pos.x - self.dir[1]) % len(map[0]), self.map_pos.y - self.dir[0]) in PATH else -1
        down = 1 if get_map_letter((self.map_pos.x - self.dir[0]) % len(map[0]), self.map_pos.y - self.dir[0]) in PATH else -1

        self.surrounding_walls = [int(up), int(left), int(right), int(down)]


    def eat(self, oj, tp="dot"):
        if tp == "dot":
            return self.map_pos == oj.map_pos
        else:
            return math.sqrt((self.map_pos.x - oj.map_pos.x) ** 2 + (self.map_pos.y - oj.map_pos.y) ** 2) <= 1

    def ai_update(self, key, time):
        super().update_all("", True, self.dead)
        self.time_since_move += time
        self.find_surrounding_walls()
        if len(self.prev_moves) < 2:
            self.prev_moves.append(key)
        else:
            self.prev_moves = [key, self.prev_moves[0]]
        # print(self.not_move, "dd")
        if not self.dead and self.not_move == 0:
            if key == 'for':#keys[pg.K_w]:
                self.wannabe_dir = self.dir
            elif key == 'left':#keys[pg.K_s]:
                self.wannabe_dir = (self.dir[1], self.dir[0])
            elif key == 'right':#keys[pg.K_a]:
                self.wannabe_dir = (-self.dir[1], -self.dir[0])
            elif key == 'back':#keys[pg.K_d]:
                self.wannabe_dir = (-self.dir[0], -self.dir[1])

            self.moved = True
            if not self.move(self.wannabe_dir):
                self.moved = self.move(self.dir)

    def update(self, keys):
        super().update_all("", True, self.dead)
        self.find_surrounding_walls()
        # print(self.not_move, "dd")
        if not self.dead and self.not_move == 0:
            if keys[pg.K_w]:
                self.wannabe_dir = (0, -1)
            elif keys[pg.K_s]:
                self.wannabe_dir = (0, 1)
            elif keys[pg.K_a]:
                self.wannabe_dir = (-1, 0)
            elif keys[pg.K_d]:
                self.wannabe_dir = (1, 0)

            self.moved = True
            if not self.move(self.wannabe_dir):
                self.moved = self.move(self.dir)


    def show(self, screen):
        frame_translation = {(1, 0): 0, (-1, 0): 1, (0, -1): 2, (0, 1): 3}

        if not self.dead:
            if self.frame != 2:
                display.blit(self.animation[0][frame_translation[self.dir]][self.frame],
                             (self.pos.x - self.size / 2, self.pos.y - self.size / 2))
            else:
                display.blit(self.animation[0][4][0], (self.pos.x - self.size / 2, self.pos.y - self.size / 2))

            if self.wannabe_dir == (0, -1):
                pg.draw.rect(display, (255, 242, 149), (self.pos.x - 10, self.pos.y - 32, 20, 4))
                pg.draw.rect(display, (255, 242, 149), (self.pos.x - 6, self.pos.y - 36, 12, 4))
                pg.draw.rect(display, (255, 242, 149), (self.pos.x - 2, self.pos.y - 40, 4, 4))
            elif self.wannabe_dir == (0, 1):
                pg.draw.rect(display, (255, 242, 149), (self.pos.x - 10, self.pos.y + 28, 20, 4))
                pg.draw.rect(display, (255, 242, 149), (self.pos.x - 6, self.pos.y + 32, 12, 4))
                pg.draw.rect(display, (255, 242, 149), (self.pos.x - 2, self.pos.y + 36, 4, 4))
            elif self.wannabe_dir == (-1, 0):
                pg.draw.rect(display, (255, 242, 149), (self.pos.x - 32, self.pos.y - 10, 4, 20))
                pg.draw.rect(display, (255, 242, 149), (self.pos.x - 36, self.pos.y - 6, 4, 12))
                pg.draw.rect(display, (255, 242, 149), (self.pos.x - 40, self.pos.y - 2, 4, 4))
            elif self.wannabe_dir == (1, 0):
                pg.draw.rect(display, (255, 242, 149), (self.pos.x + 28, self.pos.y - 10, 4, 20))
                pg.draw.rect(display, (255, 242, 149), (self.pos.x + 32, self.pos.y - 6, 4, 12))
                pg.draw.rect(display, (255, 242, 149), (self.pos.x + 36, self.pos.y - 2, 4, 4))
        else:
            print(self.frame)
            display.blit(self.animation[1][self.frame], (self.pos.x - 45 / 2, self.pos.y - 45 / 2))
