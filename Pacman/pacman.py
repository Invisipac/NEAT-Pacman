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

    def eat(self, oj, tp="dot"):
        if tp == "dot":
            return self.map_pos == oj.map_pos
        else:
            return math.sqrt((self.map_pos.x - oj.map_pos.x) ** 2 + (self.map_pos.y - oj.map_pos.y) ** 2) <= 1

    def update(self, keys, allowed_to_move):
        super().update_all("", True, self.dead)

        if not self.dead and self.not_move == 0:
            if keys[pg.K_w]:
                self.wannabe_dir = (0, -1)
            elif keys[pg.K_s]:
                self.wannabe_dir = (0, 1)
            elif keys[pg.K_a]:
                self.wannabe_dir = (-1, 0)
            elif keys[pg.K_d]:
                self.wannabe_dir = (1, 0)

            if allowed_to_move:
                self.moved = True
                if not self.move(self.wannabe_dir):
                    self.moved = self.move(self.dir)

    def show(self, screen, nothing=False):
        frame_translation = {(1, 0): 0, (-1, 0): 1, (0, -1): 2, (0, 1): 3}

        if not self.dead:
            if self.frame != 2:
                display.blit(self.animation[0][frame_translation[self.dir]][self.frame],
                             (self.pos.x - self.size / 2, self.pos.y + (offset * RATIO[1]) - self.size / 2))
            else:
                display.blit(self.animation[0][4][0], (self.pos.x - self.size / 2, self.pos.y + (offset * RATIO[1]) - self.size / 2))

            if self.wannabe_dir == (0, -1):
                pg.draw.rect(display, (255, 242, 149), (self.pos.x - 10, self.pos.y + (offset * RATIO[1]) - 32, 20, 4))
                pg.draw.rect(display, (255, 242, 149), (self.pos.x - 6, self.pos.y + (offset * RATIO[1]) - 36, 12, 4))
                pg.draw.rect(display, (255, 242, 149), (self.pos.x - 2, self.pos.y + (offset * RATIO[1]) - 40, 4, 4))
            elif self.wannabe_dir == (0, 1):
                pg.draw.rect(display, (255, 242, 149), (self.pos.x - 10, self.pos.y + (offset * RATIO[1]) + 28, 20, 4))
                pg.draw.rect(display, (255, 242, 149), (self.pos.x - 6, self.pos.y + (offset * RATIO[1]) + 32, 12, 4))
                pg.draw.rect(display, (255, 242, 149), (self.pos.x - 2, self.pos.y + (offset * RATIO[1]) + 36, 4, 4))
            elif self.wannabe_dir == (-1, 0):
                pg.draw.rect(display, (255, 242, 149), (self.pos.x - 32, self.pos.y + (offset * RATIO[1]) - 10, 4, 20))
                pg.draw.rect(display, (255, 242, 149), (self.pos.x - 36, self.pos.y + (offset * RATIO[1]) - 6, 4, 12))
                pg.draw.rect(display, (255, 242, 149), (self.pos.x - 40, self.pos.y + (offset * RATIO[1]) - 2, 4, 4))
            elif self.wannabe_dir == (1, 0):
                pg.draw.rect(display, (255, 242, 149), (self.pos.x + 28, self.pos.y + (offset * RATIO[1]) - 10, 4, 20))
                pg.draw.rect(display, (255, 242, 149), (self.pos.x + 32, self.pos.y + (offset * RATIO[1]) - 6, 4, 12))
                pg.draw.rect(display, (255, 242, 149), (self.pos.x + 36, self.pos.y + (offset * RATIO[1]) - 2, 4, 4))
        else:
            display.blit(self.animation[1][self.frame], (self.pos.x - 45 / 2, self.pos.y + (offset * RATIO[1]) - 45 / 2))
