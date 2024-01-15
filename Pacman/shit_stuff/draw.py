import pygame
pygame.init()

RATIO = (16, 16)
GRID_SIZE = (28, 31)
WIDTH, HEIGHT = RATIO[0] * GRID_SIZE[0], RATIO[1] * GRID_SIZE[1]

map = open("../true-map.txt", "r").read().split()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            screen.fill((0,255,0))
    for j, y in enumerate(map):
        for i, x in enumerate(y):
            if x == "w":
                pygame.draw.rect(screen, (0, 0, 255), (i * RATIO[0], j * RATIO[1], RATIO[0], RATIO[1]))
            if x == "*":
                pygame.draw.rect(screen, (0, 255, 255), (i * RATIO[0], j * RATIO[1], RATIO[0], RATIO[1]))
            if x == "p":
                pygame.draw.rect(screen, (255, 0, 255), (i * RATIO[0], j * RATIO[1], RATIO[0], RATIO[1]))
            if x == "e":
                pygame.draw.rect(screen, (0, 0, 0), (i * RATIO[0], j * RATIO[1], RATIO[0], RATIO[1]))
    pygame.display.flip()

for j, y in enumerate(map):
    for i, x in enumerate(y):
        try:
            if x == "p" or x == "e":
                neighbors_x = 0
                neighbors_y = 0
                have_p = False
                if map[j-1][i] in ["p", "e"]:
                    neighbors_y += 1
                    if map[j-1][i] == "p":
                        have_p = True
                if map[j+1][i] in ["p", "e"]:
                    neighbors_y += 1
                    if map[j+1][i] == "p":
                        have_p = True
                if map[j][i-1] in ["p", "e"]:
                    neighbors_x += 1
                    if map[j][i-1] == "p":
                        have_p = True
                if map[j][i+1] in ["p", "e"]:
                    neighbors_x += 1
                    if map[j][i+1] == "p":
                        have_p = True
                if neighbors_x >= 1 and neighbors_y >= 1 and have_p:
                    map[j] = map[j][:i] + "*" + map[j][i+1:]
        except:
            pass
# for i in map:
#     #print(i)
# #print(map)