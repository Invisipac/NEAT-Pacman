import random
from random import randint
#Uncomment the visualize if you want to display statistics, but it requires certain dependencies
#import visualize
import neat
import pygame as pg
from pygame.math import Vector2 as vec

from dinosaur import Dinosaur
from ground import Ground
from obstacle import Cacti, Bird

import pickle

pg.font.init()

textFont = pg.font.SysFont('Comic Sans', 20)

#main game class 
class Game:
    def __init__(self, screen: pg.Surface) -> None:
        self.screen = screen
        self.W, self.H = screen.get_width(), screen.get_height()
        self.ground = Ground(self.H - 100)

        #variables for the neat algorithm such as genomes, neural nets, and the dinos
        self.dinos = []
        self.nets = []
        self.ge = []
        self.bestGenome = []
        self.gen = 0
        self.speed = 1

        #list of obstacles
        self.obstacleList = []
        self.maxObstacles = 15

        #score and various timers for the game
        self.dinoScore = 0
        self.scoreTimer = 0
        self.speedUpTimer = 0
        self.obstacleSpeed = -4
        self.clock = pg.time.Clock()

        self.config = None
        self.p = None
        self.replay = False
    
    #function speed up the obstacles after a certain periond of time
    def speedUp(self):
        self.speedUpTimer += 1
        if self.speedUpTimer >= 10000 // 60:
            self.obstacleSpeed -= 0.2
            for o in self.obstacleList:
                o.vel = vec(self.obstacleSpeed, 0)
            self.speedUpTimer = 0

    #increase score and fitness after certain time 
    #also display information about the current generation
    def increaseScore(self):
        self.scoreTimer += 1
        if self.scoreTimer >= 100:
            self.dinoScore += 1
            for g in self.ge:
                g.fitness += 0.2
            self.scoreTimer = 0
        score = textFont.render(f"Score: {self.dinoScore}", 1, (0, 0, 0))
        self.screen.blit(score, (self.W - 200, 30))

        gen = textFont.render(f"Gen: {self.gen}", 1, (0, 0, 0))
        self.screen.blit(gen, (self.W - 200, 60))

        dinos = textFont.render(f"Dinos alive: {len(self.dinos)}", 1, (0, 0, 0))
        self.screen.blit(dinos, (self.W - 200, 90))

        speed = textFont.render(f"Game speed: {self.speed}", 1, (0, 0, 0))
        self.screen.blit(speed, (self.W - 200, 120))

    #spawn the obstacles on the right of the map
    def spawnObstacles(self):
        if len(self.obstacleList) < self.maxObstacles:
            o_type = 0 if random.randint(0, 100) < 90 else 1
            difficulty = 500 - 25 * self.obstacleSpeed
            if len(self.obstacleList) > 0:
                lastX = self.obstacleList[-1].pos.x + self.obstacleList[-1].size[0]
                dist = self.W - lastX
                offset = randint(int(dist), int(dist + difficulty)) if dist > 0 else randint(int(difficulty), int(difficulty*2))
            else:
                lastX = self.W
                offset = randint(100, 100 + int(difficulty))

            if o_type == 0:
                self.obstacleList.append(Cacti(lastX + offset, self.ground.y))
            elif o_type == 1:
                self.obstacleList.append(Bird(lastX + offset, self.ground.y))

    #move all of the obstacles and check for collisions
    def updateObstacles(self):
        self.spawnObstacles()
        self.speedUp()

        for o in self.obstacleList[::-1]:
            o.move()
            if o.pos.x < -o.size[0]:
                self.obstacleList.remove(o)

            #if the dino collides with an obstacle decrease its fitness and remove its AI data
            for i, dino in enumerate(self.dinos):
                if dino.collide(o):
                    self.ge[i].fitness -= 1
                    self.dinos.pop(i)
                    self.nets.pop(i)
                    self.ge.pop(i)

    #update function move the obstacles and calculates the output of the neural network (NN)
    def update(self):
        self.speedUp()
        self.updateObstacles()
        self.increaseScore()
        for i, dino in enumerate(self.dinos):
            dino.move(self.ground.y)
            #pass in all relevant inputs and get the output of the NN
            output = self.nets[i].activate((dino.pos.x + dino.w, dino.pos.y + dino.h, self.obstacleList[0].pos.x,
                                            self.obstacleList[0].pos.y,
                                            self.obstacleList[0].pos.y + self.obstacleList[0].size[1], self.obstacleSpeed))

            #if the output is greater than zero then the dinos jump
            if output[0] > 0.5:
                dino.jump()

    #draw everything in the game
    def redraw(self):
        for o in self.obstacleList:
            o.draw(self.screen)
        self.ground.draw(self.screen, self.W)
        for dino in self.dinos:
            dino.draw(self.screen)

    #reset all of the AI data for the new generation
    def resetGen(self):
        self.nets = []
        self.ge = []
        self.dinos = []
        self.obstacleList = []
        self.dinoScore = 0
        self.obstacleSpeed = -4
    
    #function to save the best genome to a file
    def saveGenome(self, best):
        with open("winner.pkl", "wb") as f:
            pickle.dump(best, f)
            f.close()

    #main gameplay function, also serves as the fitness function for the NEAT algorithm
    def main(self, genomes, config):
        self.resetGen()
        
        if self.replay:
            genomes = self.bestGenome #play the best genome
        
        for _, g in genomes: #initialize all of the AI data 
            net = neat.nn.FeedForwardNetwork.create(g, config)
            self.nets.append(net)
            self.dinos.append(Dinosaur(20, self.ground.y))
            g.fitness = 0
            self.ge.append(g)

        
        run = True
        while run:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    run = False
                    if not self.replay:
                        self.saveGenome(self.p.best_genome)
                    pg.quit()

            for i in range(self.speed): #use key presses to speed up the game so you don't have to wait as long
                keys = pg.key.get_pressed()
                if keys[pg.K_1]:
                    self.speed = 1
                    break
                elif keys[pg.K_2]:
                    self.speed = 10
                    break
                elif keys[pg.K_3]:
                    self.speed = 50
                    break
                elif keys[pg.K_4]:
                    self.speed = 100
                    break
                elif keys[pg.K_5]:
                    self.speed = 500
                    break
                elif keys[pg.K_6]:
                    self.speed = 10000
                    break
                if len(self.dinos) == 0 and not self.replay:
                    run = False
                    self.gen += 1
                    print(f"Final Score: {self.dinoScore}")
                    break
                elif len(self.dinos) == 0 and self.replay:
                    run = False
                    return

                self.screen.fill((255, 255, 255))
                self.update()
                self.redraw()
                pg.display.update()
            self.clock.tick(60)

    #function to replay the best genome
    def replayGenome(self, config_path, genome_path = "winner.pkl"):
        self.config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation, config_path)
        
        with open (genome_path, "rb") as f:
            genome = pickle.load(f)
            f.close()
        
        self.bestGenome = [(1, genome)]
        self.replay = True
        self.p = neat.Population(self.config)
        self.p.run(self.main, 1)

    #function to run the AI normally
    def run(self, config_path):
        self.config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation, config_path)
        # population
        self.p = neat.Population(self.config)

        self.p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        self.p.add_reporter(stats)

        # get the winner of the population
        winner = self.p.run(self.main, 2)


        # -------- Uncomment to draw the statistics ----------- #
        winner_net = neat.nn.FeedForwardNetwork.create(winner, self.config)
        # visualize.draw_net(self.config, winner, True)
        # visualize.plot_stats(stats, ylog=False, view=True)
        # visualize.plot_species(stats, view=True)


        self.saveGenome(winner)  # fitness function, num of generations
        print(winner)
