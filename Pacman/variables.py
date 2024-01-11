import pygame as pg

RATIO = (45, 45)
GRID_SIZE = (16, 19)
WIDTH, HEIGHT = RATIO[0] * GRID_SIZE[0], RATIO[1] * GRID_SIZE[1]

map = open("map.txt", "r").read().split()