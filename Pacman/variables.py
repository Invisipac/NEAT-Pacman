import pygame as pg

RATIO = (24, 24)
GRID_SIZE = (28, 31)
WIDTH, HEIGHT = RATIO[0] * GRID_SIZE[0], RATIO[1] * GRID_SIZE[1]

map = open("./Pacman/true-map.txt", "r").read().split()

NODES = ["n", "N", "&"]
PATH = ["n", "&", "p", "P", "e"]
DOTS = ["p", "n"]
POWER_DOTS = ["P"]
OBSTACLES = ["w"]