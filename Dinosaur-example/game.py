import pygame as pg
from pygame.math import Vector2 as vec
from obstacle import Obstacle
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
        self.obstacleList = [Obstacle(self.W + 30, self.ground.y, 20, randint(40, 60))]
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

    def updateObstacles(self):
        if len(self.obstacleList) < self.maxObstacles:
            lastX = self.obstacleList[-1].pos.x
            dist = self.W - lastX
            offset = randint(dist + 100, dist + 100 + 400) if dist > 0 else randint(300, 300 + 400)
            obs = Obstacle(lastX + offset, self.ground.y, 20, randint(40, 60))
            obs.vel = vec(self.obstacleSpeed, 0)
            self.obstacleList.append(obs)

        for o in self.obstacleList[::-1]:
            o.move(self.W)
            if o.pos.x < -20:
                self.obstacleList.remove(self.obstacleList[0])
            
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
