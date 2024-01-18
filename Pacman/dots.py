from variables import *

class Dot:
    def __init__(self, pos, power_dot=False):
        self.map_pos = pos
        self.pos = pg.Vector2((pos[0] + 0.5) * RATIO[0], (pos[1] + 0.5) * RATIO[1])
        self.eaten = False
        self.power_dot = power_dot
        self.size = RATIO[0] / 6 if not self.power_dot else RATIO[0] / 3

    def show(self, display):
        if not self.eaten:
            pg.draw.circle(display, (255, 255, 255), (self.pos.x, self.pos.y), self.size)