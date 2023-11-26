import random
from random import randint

import pygame as pg
from pygame.math import Vector2 as vec
from obstacle import Obstacle
from ground import Ground
from random import randint, sample, choice
from dinosaur import Dinosaur
from ground import Ground
from obstacle import Cacti, Bird

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
        self.speedUpTimer = 0
        self.obstacleSpeed = -4
        self.clock = pg.time.Clock()
    
    def speedUp(self):
        self.speedUpTimer += 1
        if self.speedUpTimer >= 10000//60:
            self.obstacleSpeed -= 0.2
            for o in self.obstacleList:
                o.vel = vec(self.obstacleSpeed, 0)
            self.speedUpTimer = 0


    def increaseScore(self):
        self.scoreTimer += 1
        if self.scoreTimer >= 100 and not self.dino.dead:
            self.dinoScore += 1
            self.scoreTimer = 0
        score = textFont.render(f"Score: {self.dinoScore}", 1, (0, 0, 0))
        self.screen.blit(score, (self.W - 150, 30))

    def spawnObstacles(self):
        if len(self.obstacleList) < self.maxObstacles:
            o_type = 0 if random.randint(0, 100) < 75 else 1
            difficulty = 400
            if len(self.obstacleList) > 0:
                lastX = self.obstacleList[-1].pos.x + self.obstacleList[-1].size[0]
                dist = self.W - lastX
                offset = randint(dist, dist + difficulty) if dist > 0 else randint(100, 100 + difficulty)
            else:
                lastX = self.W
                offset = randint(100, 100 + difficulty)

            if o_type == 0:
                self.obstacleList.append(Cacti(lastX + offset, self.ground.y))
            elif o_type == 1:
                self.obstacleList.append(Bird(lastX + offset, self.ground.y))

    def updateObstacles(self):
        self.spawnObstacles()

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
        self.speedUp()
        print(self.obstacleSpeed)
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
