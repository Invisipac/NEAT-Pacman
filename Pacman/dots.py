from variables import *

#class for dots
class Dot:
    def __init__(self, pos, power_dot=False):
        self.map_pos = pos #position in array
        self.pos = pg.Vector2((pos[0] + 0.5) * RATIO[0], (pos[1] + 0.5) * RATIO[1])
        self.eaten = False
        self.power_dot = power_dot #set the dot to be normal or power
        self.size = RATIO[0] / 4 if not self.power_dot else RATIO[0]
        self.frame = 0

    #function to animate and display the dots
    def show(self, screen: pg.Surface):
        self.frame += 0.075
        if not self.eaten:
            if not self.power_dot:
                pg.draw.rect(screen, (255, 183, 174),
                             (self.pos.x - self.size / 2, self.pos.y + (offset * RATIO[1]) - self.size / 2, self.size, self.size))
            else:
                if int(self.frame) % 2 == 0:
                    pg.draw.rect(screen, (255, 183, 174),
                                 (self.pos.x - self.size / 4, self.pos.y + (offset * RATIO[1]) - self.size / 2, self.size / 2, self.size))
                    pg.draw.rect(screen, (255, 183, 174),
                                 (self.pos.x - self.size / 2, self.pos.y + (offset * RATIO[1]) - self.size / 4, self.size, self.size / 2))
                    pg.draw.rect(screen, (255, 183, 174), (
                        self.pos.x - 3 * self.size / 8, self.pos.y + (offset * RATIO[1]) - 3 * self.size / 8, 3 * self.size / 4,
                        3 * self.size / 4))
