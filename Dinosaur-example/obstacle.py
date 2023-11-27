import pygame as pg


class Obstacle:
    def __init__(self, pos: tuple, size: tuple, speed: tuple, o_type=0) -> None:
        self.pos, self.size = pg.math.Vector2(*pos), size
        self.rect = pg.Rect(*pos, *self.size)
        self.o_type = o_type
        self.colour = (50, 50, 200) if self.o_type == 1 else (50, 200, 50)  # bird else cacti
        self.vel = pg.math.Vector2(*speed)

    def move(self) -> None:
        self.pos += self.vel
        self.rect = pg.Rect(self.pos.x, self.pos.y, *self.size)

    def draw(self, screen: pg.Surface) -> None:
        pg.draw.rect(screen, self.colour, self.rect)


class Cacti(Obstacle):
    def __init__(self, pos: tuple, size: tuple, speed: tuple) -> None:
        super().__init__(pos, size, speed, 0)


class Bird(Obstacle):
    def __init__(self, pos: tuple, size: tuple, speed: tuple) -> None:
        super().__init__(pos, size, speed, 1)
