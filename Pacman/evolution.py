import pygame as pg
import neat
from main import Game
from variables import display
import os
import pickle
class Evolution:
    def __init__(self) -> None:
        self.game = Game(display)    

    def get_best(self):
        best = pickle.load("winner.pkl")
        return best

    def run(self, config_path):
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation, config_path)
        p = neat.Population(config)
        p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-48")

        p.add_reporter(neat.StdOutReporter(True))
        p.add_reporter(neat.StatisticsReporter())
        p.add_reporter(neat.Checkpointer(5))

        p.run(self.game.main, 50)
        # filename = "winner.pkl"
        # with open(filename, 'wb') as f:
        #     pickle.dump(p.best_genome, filename)
        #     f.close


E = Evolution()

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    E.run(config_path)
