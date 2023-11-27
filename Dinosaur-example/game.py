import random

import pygame as pg
from obstacle import Cacti, Bird
from ground import Ground
from random import randint, sample, choice
from dinosaur import Dinosaur
pg.font.init()

textFont = pg.font.SysFont('Comic Sans', 20)
class Game:
    def __init__(self, screen: pg.Surface) -> None:
        self.screen = screen
        self.W, self.H = screen.get_width(), screen.get_height()
        self.ground = Ground(self.H - 100)
        self.dino = Dinosaur(20, self.ground.y)

        self.obstacleList = []
        self.maxObstacles = 15

        self.dinoScore = 0
        self.scoreTimer = 0
        self.clock = pg.time.Clock()
    
    def increaseScore(self):
        self.scoreTimer += 1
        if self.scoreTimer >= 100 and not self.dino.dead:
            self.dinoScore += 1
            self.scoreTimer = 0
        score = textFont.render(f"Score: {self.dinoScore}", 1, (0, 0, 0))
        self.screen.blit(score, (self.W - 150, 30))

    def updateObstacles(self):
        if len(self.obstacleList) < self.maxObstacles:
            o_type = 0 if random.randint(0, 100) < 5 else 1
            difficulty = 400
            if len(self.obstacleList) > 0:
                lastX = self.obstacleList[-1].pos.x + self.obstacleList[-1].size[0]
                dist = self.W - lastX
                offset = randint(dist, dist + difficulty) if dist > 0 else randint(100, 100 + difficulty)
            else:
                lastX = self.W
                offset = randint(100, 100 + difficulty)

            obstacle_size = 20, randint(40, 60)
            if o_type == 1:
                obstacle_size = 40, 20

            obstacle_pos = lastX + offset, self.ground.y - obstacle_size[1]
            if o_type == 1:
                obstacle_pos = lastX + offset, self.ground.y - 20 - 25 * randint(0, 2)

            if o_type == 0:
                self.obstacleList.append(Cacti(obstacle_pos, obstacle_size, (-4, 0)))
            elif o_type == 1:
                self.obstacleList.append(Bird(obstacle_pos, obstacle_size, (-4, 0)))

        for o in self.obstacleList[::-1]:
            o.move()
            if o.pos.x < -o.size[0]:
                self.obstacleList.remove(o)
            
            if self.dino.collide(o):
                self.dino.kill()
                


    def update(self):
        keys = pg.key.get_pressed()
        
        if keys[pg.K_SPACE]:
            self.dino.jump()

        self.updateObstacles()
        self.increaseScore()
        self.dino.move(self.ground.y)

    def redraw(self):
        for o in self.obstacleList:
            o.draw(self.screen)
        self.ground.draw(self.screen, self.W)
        self.dino.draw(self.screen)

    def main(self):
        run = True
        while run:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    run = False
            
            self.screen.fill((255, 255, 255))
            self.update()
            self.redraw()
            self.clock.tick(60)
            pg.display.update()
        
        pg.quit()
