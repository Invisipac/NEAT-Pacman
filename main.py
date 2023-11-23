import pygame as pg
from game import Game
W, H = 800, 600

screen = pg.display.set_mode((W, H))
game = Game(screen)

game.main()
