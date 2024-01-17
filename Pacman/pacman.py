from variables import *


class Pacman:
    def __init__(self, pos, speed):
        self.pos = pg.Vector2(pos[0] * RATIO[0] + RATIO[0] / 2, pos[1] * RATIO[1] + RATIO[1] / 2)
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
        can_turn = self.snap_to_grid()

        if keys[pg.K_w]:
            self.wannabe_dir = "UP"
        elif keys[pg.K_s]:
            self.wannabe_dir = "DOWN"
        elif keys[pg.K_a]:
            self.wannabe_dir = "LEFT"
        elif keys[pg.K_d]:
            self.wannabe_dir = "RIGHT"

        if timer == 0:
            if not self.move(self.wannabe_dir, can_turn):
                self.move(self.dir, can_turn)

        #print(self.pos, self.map_locs, can_turn)
        #print(f"dir: {self.dir}, wannabe: {self.wannabe_dir}")

    def eat(self, dot):
        if self.map_locs.x == dot.map_pos[0] and self.map_locs.y == dot.map_pos[1]:
            return True
        return False

    def snap_to_grid(self):
        can_turn = [False, False]
        if (self.pos.x - RATIO[0] / 2) % RATIO[0] <= 1:
            self.map_locs.x = (self.pos.x // RATIO[0]) % len(map[0])
            self.pos.x = self.map_locs.x * RATIO[0] + RATIO[0] / 2
            can_turn[1] = True
        if (self.pos.y - RATIO[1] / 2) % RATIO[1] <= 1:
            self.map_locs.y = (self.pos.y // RATIO[1]) % len(map)
            self.pos.y = self.map_locs.y * RATIO[1] + RATIO[1] / 2
            can_turn[0] = True

        if self.map_locs.x == -1:
            self.map_locs.x = 0
        if self.map_locs.x == GRID_SIZE[0]:
            self.map_locs.x = GRID_SIZE[0] - 1

        return can_turn

    def move(self, direction, can_turn):
        moves = {"UP": ((0, -1), 1), "DOWN": ((0, 1), 1), "LEFT": ((-1, 0), 0), "RIGHT": ((1, 0), 0)}
        reader = moves[direction]
        current_move, turn = reader[0], can_turn[reader[1]]

        if 0 <= self.map_locs.x <= len(map[0]) - 1 and 0 < self.map_locs.y < len(map) - 1 and \
                map[int(self.map_locs.y + current_move[1])][
                    int((self.map_locs.x + current_move[0]) % len(map[0]))] in PATH and turn:
            self.pos += pg.Vector2(current_move[0] * (RATIO[0] / self.speed), current_move[1] * (RATIO[1] / self.speed))
            self.dir = direction
            #self.teleport(direction)
            return True
        return False

    def teleport(self, direction):
        if self.map_locs.x == 0 and self.map_locs.y == 14 and direction == "LEFT":
            if self.pos.x > -RATIO[0] / 2:
                self.pos.x -= RATIO[0] / self.speed
            else:
                self.pos.x = WIDTH + RATIO[0]
        if self.map_locs.x == 27 and self.map_locs.y == 14 and direction == "RIGHT":
            if self.pos.x < WIDTH + RATIO[0] / 2:
                self.pos.x += RATIO[0] / self.speed
            else:
                self.pos.x = -RATIO[0]
