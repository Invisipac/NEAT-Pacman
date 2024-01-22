import pygame as pg
import pygame.image

pg.init()

RATIO = (24, 24)
GRID_SIZE = (28, 31)
WIDTH, HEIGHT = RATIO[0] * GRID_SIZE[0], RATIO[1] * GRID_SIZE[1]

display = pg.display.set_mode((WIDTH, HEIGHT))

fix_files = "./Pacman/"
# fix_files = ""

map = open(f"{fix_files}true-map.txt", "r").read().split()

EXIT = "E"
NODES = ["n", "N", "&"]
PATH = ["n", "N", "&", "p", "P", "e"]
DOTS = ["p", "n"]
POWER_DOTS = ["P", "N"]
OBSTACLES = ["w"]

times = [7000, 20000, 7000, 20000, 5000, 20000, 5000]


def get_map_letter(x, y):
    return map[int(y)][int(x)]


def loadify(filename):
    return pygame.image.load(filename).convert_alpha()


bg = loadify(f"{fix_files}Sprites//Background//bg.png")

ghost_sprites = []
ghost_names = ["Blinky", "Pinky", "Inky", "Clyde"]
for i in range(4):
    ghost_sprites.append([])
    for j in range(8):
        if j % 2 == 0:
            ghost_sprites[i].append([])
        ghost_sprites[i][j // 2].append(loadify(f"{fix_files}Sprites//Ghosts//{ghost_names[i]}//ghost{j}.png"))

dead_ghost_sprites = []
for i in range(4):
    if i % 2 == 0:
        dead_ghost_sprites.append([])
    dead_ghost_sprites[i // 2].append(loadify(f"{fix_files}Sprites//Ghosts//Dead//deadghost{i}.png"))

dead_ghost_sprites.append([])
for i in range(4):
    dead_ghost_sprites[2].append(loadify(f"{fix_files}Sprites//Ghosts//Eyes//eyes{i}.png"))

pacman_sprites = []
pacman_sprites.append([])
for i in range(9):
    if i % 2 == 0:
        pacman_sprites[0].append([])
    pacman_sprites[0][i // 2].append(loadify(f"{fix_files}Sprites//Pacman//pacman{i}.png"))
pacman_sprites.append([])
for i in range(14):
    pacman_sprites[1].append(loadify(f"{fix_files}Sprites//Pacman//Dying-animation//pacman{i}.png"))

print(pacman_sprites)