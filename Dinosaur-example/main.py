import pygame as pg
import os

from game import Game

W, H = 800, 600

screen = pg.display.set_mode((W, H))
game = Game(screen)

# game.main()

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    game.run(config_path)
    # -------- run replay after at least one run of the game.run function ------------
    # game.replayGenome(config_path)
