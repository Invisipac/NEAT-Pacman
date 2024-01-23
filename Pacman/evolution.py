import pygame as pg
import neat
from neat.six_util import itervalues
from main import Game
from variables import display
import os
import pickle
from neat.reporting import ReporterSet
class Evolution:
    def __init__(self) -> None:
        self.game = Game(display)    

    def get_best(self):
        best = pickle.load("winner.pkl")
        return best

    def run(self, config_path):
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation, config_path)
        best_nomes = []
        if not os.stat('winners.pkl').st_size == 0:
            with open('winners.pkl', 'rb') as f:
                best_nomes = pickle.load(f)
                f.close()
        

        p = neat.Population(config)
        print(p.population)
        # lst_pop = list(itervalues(p.population))
        for idx, n in enumerate(best_nomes):
            # lst_pop[idx].connections = n.connections
            # lst_pop[idx].nodes = n.nodes
            # lst_pop[idx].fitness = n.fitness
            p.population[idx + 1].connections = n.connections
            p.population[idx + 1].nodes = n.nodes
            p.population[idx + 1].fitness = 0

        # p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-49")

        p.add_reporter(neat.StdOutReporter(True))
        p.add_reporter(neat.StatisticsReporter())
        p.add_reporter(neat.Checkpointer(5))

        p.run(self.game.main, 50)
        filename = "winner.pkl"
        # winners = "winners.pkl"
        # best_genomes = []
        # # best_genomes = sorted([g for g in itervalues(p.population)])[:20]
        # for g in itervalues(p.population):
        #     print(g)
        # print(best_genomes)
        # # best_genomes = sorted(best_genomes, key= lambda x : x.fitness, reverse=True)
        # with open(winners, 'wb') as f:
        #     pickle.dump(best_genomes, f)
        #     f.close
        # with open(filename, 'wb') as f:
        #     pickle.dump(p.best_genome, f)
        #     f.close


E = Evolution()

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_stage2.txt")
    E.run(config_path)
