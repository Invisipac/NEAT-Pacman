from variables import *

class Pacman:
    def __init__(self, pos, speed):
        self.pos = pg.Vector2(pos[0] * RATIO[0], pos[1] * RATIO[1])
        self.map_locs = pg.Vector2(*pos)
        self.size = 15
        self.dir = "UP"
        self.wannabe_dir = "UP"
        self.speed = speed

    def show(self, display):
        pg.draw.circle(display, (200, 200, 50), (self.pos.x, self.pos.y), self.size)
        if self.wannabe_dir == "UP":
            pg.draw.circle(display, (50, 50, 200), (self.pos.x, self.pos.y - 25), self.size // 2)
        elif self.wannabe_dir == "DOWN":
            pg.draw.circle(display, (50, 50, 200), (self.pos.x, self.pos.y + 25), self.size // 2)
        elif self.wannabe_dir == "LEFT":
            pg.draw.circle(display, (50, 50, 200), (self.pos.x - 25, self.pos.y), self.size // 2)
        elif self.wannabe_dir == "RIGHT":
            pg.draw.circle(display, (50, 50, 200), (self.pos.x + 25, self.pos.y), self.size // 2)

    def update(self, keys, timer):
        can_turn = [False, False]
        if self.pos.x % RATIO[0] <= 1:
            self.map_locs.x = self.pos.x // RATIO[0]
            can_turn[1] = True
        if self.pos.y % RATIO[1] <= 1:
            self.map_locs.y = self.pos.y // RATIO[1]
            can_turn[0] = True

        if self.map_locs.x == -1:
            self.map_locs.x = 0
        if self.map_locs.x == 17:
            self.map_locs.x = 16

        if keys[pg.K_w]:
            self.wannabe_dir = "UP"
        elif keys[pg.K_s]:
            self.wannabe_dir = "DOWN"
        elif keys[pg.K_a]:
            self.wannabe_dir = "LEFT"
        elif keys[pg.K_d]:
            self.wannabe_dir = "RIGHT"

        if timer == 0:
            moved = False
            if self.wannabe_dir == "UP" and 0 <= self.pos[0] <= WIDTH and 0 <= self.pos[1] <= HEIGHT:
                if self.map_locs.y > 0 and map[int(self.map_locs.y - 1)][int(self.map_locs.x)] in ["*", "-"] and can_turn[1]:
                    self.pos.y -= RATIO[1] / self.speed
                    self.dir = "UP"
                    moved = True
            elif self.wannabe_dir == "DOWN" and 0 <= self.pos[0] <= WIDTH and 0 <= self.pos[1] <= HEIGHT:
                if self.map_locs.y < len(map) - 1 and map[int(self.map_locs.y + 1)][int(self.map_locs.x)] in ["*", "-"] and can_turn[1]:
                    self.pos.y += RATIO[1] / self.speed
                    self.dir = "DOWN"
                    moved = True
            elif self.wannabe_dir == "LEFT":
                if self.map_locs.x > 0 and map[int(self.map_locs.y)][int(self.map_locs.x - 1)] in ["*", "-"] and can_turn[0]:
                    self.pos.x -= RATIO[0] / self.speed
                    self.dir = "LEFT"
                    moved = True
                if self.map_locs.x == 0 and self.map_locs.y == 9:
                    if self.pos.x > -25:
                        self.pos.x -= RATIO[0] / self.speed
                    else:
                        self.pos.x = WIDTH + 50
                    self.dir = "LEFT"
                    moved = True
            elif self.wannabe_dir == "RIGHT":
                if self.map_locs.x < len(map[0]) - 1 and map[int(self.map_locs.y)][int(self.map_locs.x + 1)] in ["*", "-"] and can_turn[0]:
                    self.pos.x += RATIO[0] / self.speed
                    self.dir = "RIGHT"
                    moved = True
                if self.map_locs.x == 16 and self.map_locs.y == 9:
                    if self.pos.x < WIDTH + 25:
                        self.pos.x += RATIO[0] / self.speed
                    else:
                        self.pos.x = -50
                    self.dir = "RIGHT"
                    moved = True
            if not moved:
                if self.dir == "UP":
                    if self.map_locs.y > 0 and map[int(self.map_locs.y - 1)][int(self.map_locs.x)] in ["*", "-"] and can_turn[1]:
                        self.pos.y -= RATIO[1] / self.speed
                elif self.dir == "DOWN":
                    if self.map_locs.y < len(map) - 1 and map[int(self.map_locs.y + 1)][int(self.map_locs.x)] in ["*", "-"] and can_turn[1]:
                        self.pos.y += RATIO[1] / self.speed
                elif self.dir == "LEFT":
                    if self.map_locs.x > 0 and map[int(self.map_locs.y)][int(self.map_locs.x - 1)] in ["*", "-"] and can_turn[0]:
                        self.pos.x -= RATIO[0] / self.speed
                    if self.map_locs.x == 0 and self.map_locs.y == 9:
                        self.pos.x = WIDTH + 50
                elif self.dir == "RIGHT":
                    if self.map_locs.x < len(map[0]) - 1 and map[int(self.map_locs.y)][int(self.map_locs.x + 1)] in ["*", "-"] and can_turn[0]:
                        self.pos.x += RATIO[0] / self.speed
                    if self.map_locs.x == 16 and self.map_locs.y == 9:
                        self.pos.x = -50

        print(self.pos, self.map_locs, can_turn)
        print(f"dir: {self.dir}, wannabe: {self.wannabe_dir}")