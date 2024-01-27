import pygame as pg
from pygame.math import Vector2 as vec
from obstacle import Obstacle

#dinosaur class
class Dinosaur:
    def __init__(self, x, y) -> None:
        self.w, self.h = 20, 40
        self.pos = pg.math.Vector2(x, y - self.h) #dino position vector
        self.rect = pg.Rect(self.pos.x, self.pos.y, self.w, self.h)

        self.canJump = True #bool for jumping
        self.dead = False #bool for dead or alive

        #vectors for velocity , gravity, and normal force from the ground
        self.vel = pg.math.Vector2(0, 0)
        self.accGravity = pg.math.Vector2(0, 0.7)
        self.accNormal= pg.math.Vector2(0, -self.accGravity.y)
        self.dir = 0

    def kill(self):
        self.dead = True

    #function move the dino into the air
    def jump(self):
        if self.canJump:
            self.vel += vec(0, -15)
            self.accNormal = vec(0, 0)
            self.canJump = False

    #function to move the dino across the ground
    def move(self, ground):
        self.vel += self.accGravity + self.accNormal #when gravity = -normal this does nothing
        
        self.pos += self.vel + pg.math.Vector2(self.dir*3, 0) #add velocity to position

        if self.pos.y + self.h >= ground - 10: #if the dino is close enough to the ground snap it to the ground
            self.accNormal = vec(0, -self.accGravity.y)
            self.canJump = True
            self.pos.y = ground - self.h
        
        self.rect = pg.Rect(self.pos.x, self.pos.y, self.w, self.h)
        
    def collide(self, other: Obstacle):
        return self.rect.colliderect(other.rect)
            
    def draw(self, screen: pg.Surface):
        if not self.dead:
            pg.draw.rect(screen, (255, 0, 0), self.rect)
            pg.draw.rect(screen, (0, 0, 0), self.rect, 2)