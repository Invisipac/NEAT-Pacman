import pygame as pg
from random import randint

#obstacle class and inherited obstacles bird and cacti
#the obstacles are just rects with different positions and dimensions
class Obstacle:
    def __init__(self, pos: tuple, size: tuple, speed: tuple, colour: tuple) -> None:
        self.pos, self.size = pg.math.Vector2(*pos), size
        self.rect = pg.Rect(*pos, *self.size)
        self.colour = colour  # bird else cacti
        self.vel = pg.math.Vector2(*speed)

    def move(self) -> None:
        self.pos += self.vel
        self.rect = pg.Rect(self.pos.x, self.pos.y, *self.size)

    def draw(self, screen: pg.Surface) -> None:
        pg.draw.rect(screen, self.colour, self.rect)


class Cacti(Obstacle):
    def __init__(self, x_pos, ground_y) -> None:
        obstacle_size = 20, randint(40, 60)
        obstacle_pos = x_pos, ground_y - obstacle_size[1]
        colour = (50, 200, 50)
        super().__init__(obstacle_pos, obstacle_size, (-4, 0), colour)


class Bird(Obstacle):
    def __init__(self, x_pos, ground_y) -> None:
        obstacle_size = 40, 20
        obstacle_pos = x_pos, ground_y - 20 - 25 * randint(0, 2)
        colour = (50, 50, 200)
        super().__init__(obstacle_pos, obstacle_size, (-4, 0), colour)
