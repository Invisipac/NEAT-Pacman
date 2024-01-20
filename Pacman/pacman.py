from Object import Object
from variables import *


class Pacman(Object):
    def __init__(self, map_pos, size, speed, animation, frame_lim):
        super().__init__(map_pos, size, speed, animation, frame_lim)
        self.wannabe_dir = (0, -1)
        self.points = 0

    def eat(self, dot):
        return self.map_pos == dot.map_pos

    def update(self, keys):
        super().update_all()

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

        if self.frame != 2:
            display.blit(self.animation[frame_translation[self.dir]][self.frame],
                         (self.pos.x - self.size / 2, self.pos.y - self.size / 2))
        else:
            display.blit(self.animation[4][0], (self.pos.x - self.size / 2, self.pos.y - self.size / 2))

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
