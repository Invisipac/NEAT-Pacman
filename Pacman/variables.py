import pygame as pg
import pygame.image

pg.init()
pygame.font.init()
pygame.mixer.init()

RATIO = (24, 24)
GRID_SIZE = (28, 36.5)
offset = 3.5
WIDTH, HEIGHT = RATIO[0] * GRID_SIZE[0], RATIO[1] * GRID_SIZE[1]

display = pg.display.set_mode((WIDTH, HEIGHT))

# file_fix = "./Pacman/"
file_fix = ""

map = open(f"{file_fix}true-map.txt", "r").read().split()

font = pygame.font.Font(f"{file_fix}Sprites//Fonts//Joystix.TTF", RATIO[0])
font2 = pygame.font.Font(f"{file_fix}Sprites//Fonts//Joystix.TTF", 36)

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


def text(surface, _string, color, pos, mode, _font=font):
    string = _font.render(_string, True, color)
    string_rect = string.get_rect()

    if mode == "top-left":
        string_rect.topleft = pos
    elif mode == "top-right":
        string_rect.topright = pos
    else:
        string_rect.center = pos

    surface.blit(string, string_rect)


# bg = loadify(f"{file_fix}Sprites//Background//bg1.png")
bg = [loadify(f"{file_fix}Sprites//Background//bg{i}.png") for i in range(2)]

ghost_sprites = []
ghost_names = ["Blinky", "Pinky", "Inky", "Clyde"]
for i in range(4):
    ghost_sprites.append([])
    for j in range(8):
        if j % 2 == 0:
            ghost_sprites[i].append([])
        ghost_sprites[i][j // 2].append(loadify(f"{file_fix}Sprites//Ghosts//{ghost_names[i]}//ghost{j}.png"))

dead_ghost_sprites = []
for i in range(4):
    if i % 2 == 0:
        dead_ghost_sprites.append([])
    dead_ghost_sprites[i // 2].append(loadify(f"{file_fix}Sprites//Ghosts//Dead//deadghost{i}.png"))

dead_ghost_sprites.append([])
for i in range(4):
    dead_ghost_sprites[2].append(loadify(f"{file_fix}Sprites//Ghosts//Eyes//eyes{i}.png"))

pacman_sprites = []
pacman_sprites.append([])
for i in range(9):
    if i % 2 == 0:
        pacman_sprites[0].append([])
    pacman_sprites[0][i // 2].append(loadify(f"{file_fix}Sprites//Pacman//pacman{i}.png"))
pacman_sprites.append([])
for i in range(14):
    pacman_sprites[1].append(loadify(f"{file_fix}Sprites//Pacman//Dying-animation//pacman{i}.png"))

lives = pygame.transform.scale(pacman_sprites[0][1][0], (32, 32))

chomp = [pygame.mixer.Sound(f"{file_fix}Sprites/Sounds/Chomp{i}.wav") for i in range(2)]
siren = pygame.mixer.Sound(f"{file_fix}Sprites/Sounds/Siren.mp3")
retreat = pygame.mixer.Sound(f"{file_fix}Sprites/Sounds/Retreating.wav")
eat_ghost = pygame.mixer.Sound(f"{file_fix}Sprites/Sounds/eat_ghost.wav")
death = pygame.mixer.Sound(f"{file_fix}Sprites/Sounds/Death.wav")
intro = pygame.mixer.Sound(f"{file_fix}Sprites/Sounds/Intro.wav")
win_sound = pygame.mixer.Sound(f"{file_fix}Sprites/Sounds/Extra-life.mp3")