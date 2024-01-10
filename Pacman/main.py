import math

import pygame

pygame.init()

RATIO = (50, 45)
GRID_SIZE = (16, 19)
WIDTH, HEIGHT = RATIO[0] * GRID_SIZE[0], RATIO[1] * GRID_SIZE[1]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

map = open("map.txt", "r").read().split()



class Node:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.neighbors = {}

    def show(self, display):
        for n in self.neighbors.keys():
            if self.neighbors[n]:
                line_start = self.pos
                line_end = self.neighbors[n].pos
                pygame.draw.line(display, (255, 255, 255), (line_start.x, line_start.y), (line_end.x, line_end.y), 4)
                pygame.draw.circle(display, (200, 50, 50), (self.pos.x, self.pos.y), 8)


class NodeGroup:
    def __init__(self):
        self.nodeList = {}

    def setupTestNodes(self, map):
        for i, row in enumerate(map):
            for j, tile in enumerate(row):
                if tile == "*":
                    self.nodeList[(i, j)] = Node(j * RATIO[0], i * RATIO[1])

        for i, row in enumerate(map):
            for j, tile in enumerate(row):
                if tile == "*":
                    # self.nodeList[(i, j)] = Node(i * 50, j * 50)

                    print("YOOOO", i, j)
                    # down
                    current_i, current_j = i + 1, j
                    while current_i < len(map) and map[current_i][current_j] in ["*", "-"]:
                        if map[current_i][current_j] == "*":
                            print(f"Node under at {current_i, current_j}")
                            self.nodeList[(i, j)].neighbors["DOWN"] = self.nodeList[(current_i, current_j)]
                            current_i = len(map)
                        current_i += 1
                    # right
                    current_i, current_j = i, j + 1
                    while current_j < len(row) and map[current_i][current_j] in ["*", "-"]:
                        if map[current_i][current_j] == "*":
                            print(f"Node right at {current_i, current_j}")
                            self.nodeList[(i, j)].neighbors["RIGHT"] = self.nodeList[(current_i, current_j)]
                            current_j = len(row)
                        current_j += 1
                    # up
                    current_i, current_j = i - 1, j
                    while current_i >= 0 and map[current_i][current_j] in ["*", "-"]:
                        if map[current_i][current_j] == "*":
                            print(f"Node above at {current_i, current_j}")
                            self.nodeList[(i, j)].neighbors["UP"] = self.nodeList[(current_i, current_j)]
                            current_i = 0
                        current_i -= 1
                    # left
                    current_i, current_j = i, j - 1
                    while current_j >= 0 and map[current_i][current_j] in ["*", "-"]:
                        if map[current_i][current_j] == "*":
                            print(f"Node left at {current_i, current_j}")
                            self.nodeList[(i, j)].neighbors["LEFT"] = self.nodeList[(current_i, current_j)]
                            current_j = 0
                        current_j -= 1

    def show(self, display):
        for node in self.nodeList.values():
            node.show(display)


class Pacman:
    def __init__(self, pos, speed):
        self.pos = pygame.Vector2(pos[0] * RATIO[0], pos[1] * RATIO[1])
        self.map_locs = pygame.Vector2(*pos)
        self.size = 15
        self.dir = "UP"
        self.wannabe_dir = "UP"
        self.speed = speed

    def show(self, display):
        pygame.draw.circle(display, (200, 200, 50), (self.pos.x, self.pos.y), self.size)
        if self.wannabe_dir == "UP":
            pygame.draw.circle(display, (50, 50, 200), (self.pos.x, self.pos.y - 25), self.size // 2)
        elif self.wannabe_dir == "DOWN":
            pygame.draw.circle(display, (50, 50, 200), (self.pos.x, self.pos.y + 25), self.size // 2)
        elif self.wannabe_dir == "LEFT":
            pygame.draw.circle(display, (50, 50, 200), (self.pos.x - 25, self.pos.y), self.size // 2)
        elif self.wannabe_dir == "RIGHT":
            pygame.draw.circle(display, (50, 50, 200), (self.pos.x + 25, self.pos.y), self.size // 2)

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

        if keys[pygame.K_w]:
            self.wannabe_dir = "UP"
        elif keys[pygame.K_s]:
            self.wannabe_dir = "DOWN"
        elif keys[pygame.K_a]:
            self.wannabe_dir = "LEFT"
        elif keys[pygame.K_d]:
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



def main():
    nodes = NodeGroup()
    nodes.setupTestNodes(map)

    pacman = Pacman((5, 11), 10)

    timer = 0

    run = True
    while run:
        timer += clock.get_time()
        if timer > 1:
            timer = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pacman.update(pygame.key.get_pressed(), timer)
        screen.fill((0, 0, 0))
        nodes.show(screen)
        pacman.show(screen)
        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    main()
