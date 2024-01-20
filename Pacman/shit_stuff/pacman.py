from variables import *


class Pacman:
    def __init__(self, pos, speed, sprites):
        self.pos = pg.Vector2(pos[0] * RATIO[0] + RATIO[0] / 2, pos[1] * RATIO[1] + RATIO[1] / 2)
        self.map_locs = pg.Vector2(*pos)
        self.size = 39
        self.dir = "UP"
        self.wannabe_dir = "UP"
        self.speed = speed
        self.sprites = sprites
        self.frame = 0
        self.frame_counter = 0
        self.frame_speed = 1

    def show(self, display):
        frame_translation = {"RIGHT": 0, "LEFT": 1, "UP": 2, "DOWN": 3}

        if self.frame != 2:
            display.blit(self.sprites[frame_translation[self.dir]][self.frame], (self.pos.x - self.size / 2, self.pos.y - self.size / 2))
        else:
            display.blit(self.sprites[4][0], (self.pos.x - self.size / 2, self.pos.y - self.size / 2))
        # pg.draw.circle(display, (200, 200, 50), (self.pos.x, self.pos.y), self.size)
        if self.wannabe_dir == "UP":
            pg.draw.rect(display, (255, 242, 149), (self.pos.x - 10, self.pos.y - 32, 20, 4))
            pg.draw.rect(display, (255, 242, 149), (self.pos.x - 6, self.pos.y - 36, 12, 4))
            pg.draw.rect(display, (255, 242, 149), (self.pos.x - 2, self.pos.y - 40, 4, 4))
        elif self.wannabe_dir == "DOWN":
            pg.draw.rect(display, (255, 242, 149), (self.pos.x - 10, self.pos.y + 28, 20, 4))
            pg.draw.rect(display, (255, 242, 149), (self.pos.x - 6, self.pos.y + 32, 12, 4))
            pg.draw.rect(display, (255, 242, 149), (self.pos.x - 2, self.pos.y + 36, 4, 4))
        elif self.wannabe_dir == "LEFT":
            pg.draw.rect(display, (255, 242, 149), (self.pos.x - 32, self.pos.y - 10, 4, 20))
            pg.draw.rect(display, (255, 242, 149), (self.pos.x - 36, self.pos.y - 6, 4, 12))
            pg.draw.rect(display, (255, 242, 149), (self.pos.x - 40, self.pos.y - 2, 4, 4))
        elif self.wannabe_dir == "RIGHT":
            pg.draw.rect(display, (255, 242, 149), (self.pos.x + 28, self.pos.y - 10, 4, 20))
            pg.draw.rect(display, (255, 242, 149), (self.pos.x + 32, self.pos.y - 6, 4, 12))
            pg.draw.rect(display, (255, 242, 149), (self.pos.x + 36, self.pos.y - 2, 4, 4))
            # pg.draw.circle(display, (200, 200, 50), (self.pos.x + 40, self.pos.y), self.size // 6)
        # pg.draw.circle(display, (200, 200, 50), (self.pos.x, self.pos.y), RATIO[0] * 8.5, 3)


    def update(self, keys):
        can_turn = self.snap_to_grid()

        if keys[pg.K_w]:
            self.wannabe_dir = "UP"
        elif keys[pg.K_s]:
            self.wannabe_dir = "DOWN"
        elif keys[pg.K_a]:
            self.wannabe_dir = "LEFT"
        elif keys[pg.K_d]:
            self.wannabe_dir = "RIGHT"

        moved = True
        if not self.move(self.wannabe_dir, can_turn):
            moved = self.move(self.dir, can_turn)

        self.frame_counter += 1

        if self.frame_counter > self.frame_speed and (moved or self.frame != 0):
            self.frame = (self.frame + 1) % 3
            self.frame_counter = 0

        # print(self.pos, self.map_locs, can_turn)
        # print(f"dir: {self.dir}, wannabe: {self.wannabe_dir}")

    def eat(self, dot):
        if self.map_locs.x == dot.map_pos[0] and self.map_locs.y == dot.map_pos[1]:
            return True
        return False

    def snap_to_grid(self):
        can_turn = [False, False]
        if (self.pos.x - RATIO[0] / 2) % RATIO[0] <= 5:
            self.map_locs.x = self.pos.x // RATIO[0]
            self.pos.x = self.map_locs.x * RATIO[0] + RATIO[0] / 2
            can_turn[1] = True
        if (self.pos.y - RATIO[1] / 2) % RATIO[1] <= 1:
            self.map_locs.y = self.pos.y // RATIO[1]
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

        if 0 <= self.map_locs.x <= len(map[0]) and 0 < self.map_locs.y < len(map) - 1 and \
                map[int(self.map_locs.y + current_move[1])][
                    int((self.map_locs.x + current_move[0]) % len(map[0]))] in PATH and turn:
            self.pos += pg.Vector2(current_move[0] * (RATIO[0] / self.speed), current_move[1] * (RATIO[1] / self.speed))
            self.dir = direction
            self.teleport()
            return True
        return False

    def teleport(self):
        if self.pos.x - self.size/2 > WIDTH:
            self.pos.x = -self.size/2
        elif self.pos.x < -self.size/2:
            self.pos.x = WIDTH + self.size/2
