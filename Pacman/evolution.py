import pygame as pg
import neat
from main import Game
from variables import display
import os
class Evolution:
    def __init__(self) -> None:
        self.game = Game(display)    

    def run(self, config_path):
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation, config_path)

        p = neat.Population(config)

        p.add_reporter(neat.StdOutReporter(True))
        p.add_reporter(neat.StatisticsReporter())
        # p.add_reporter(neat.Checkpointer(1))

        p.run(self.game.main, 50)

E = Evolution()

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    E.run(config_path)
