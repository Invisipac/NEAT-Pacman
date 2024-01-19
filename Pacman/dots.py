from variables import *


class Dot:
    def __init__(self, pos, power_dot=False):
        self.map_pos = pos
        self.pos = pg.Vector2((pos[0] + 0.5) * RATIO[0], (pos[1] + 0.5) * RATIO[1])
        self.eaten = False
        self.power_dot = power_dot
        self.size = RATIO[0] / 4 if not self.power_dot else RATIO[0]
        self.frame = 0

    def show(self, display: pg.Surface):
        self.frame += 0.2
        if not self.eaten:
            if not self.power_dot:
                pg.draw.rect(display, (255, 183, 174),
                             (self.pos.x - self.size / 2, self.pos.y - self.size / 2, self.size, self.size))
            else:
                if int(self.frame) % 2 == 0:
                    pg.draw.rect(display, (255, 183, 174),
                                 (self.pos.x - self.size / 4, self.pos.y - self.size / 2, self.size / 2, self.size))
                    pg.draw.rect(display, (255, 183, 174),
                                 (self.pos.x - self.size / 2, self.pos.y - self.size / 4, self.size, self.size / 2))
                    pg.draw.rect(display, (255, 183, 174), (
                    self.pos.x - 3 * self.size / 8, self.pos.y - 3 * self.size / 8, 3 * self.size / 4, 3 * self.size / 4))

