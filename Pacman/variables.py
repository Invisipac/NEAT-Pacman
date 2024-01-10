RATIO = (50, 45)
GRID_SIZE = (16, 19)
WIDTH, HEIGHT = RATIO[0] * GRID_SIZE[0], RATIO[1] * GRID_SIZE[1]

map = open("Pacman\map.txt", "r").read().split()