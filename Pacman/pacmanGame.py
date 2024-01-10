import pygame as pg
from node import Node
from nodegroup import NodeGroup
from pacman import Pacman
from variables import *


class Game:
    def __init__(self) -> None:
        self.pacman = Pacman((5, 11), 10)
        self.nodes = NodeGroup()
        self.nodes.setupTestNodes(map)
        self.screen =  pg.display.set_mode((WIDTH, HEIGHT))
    
    def main(self):
        timer = 0
        clock = pg.time.Clock()
        run = True
        while run:
            timer += clock.get_time()
            if timer > 1:
                timer = 0
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
            self.pacman.update(pg.key.get_pressed(), timer)
            self.screen.fill((0, 0, 0))
            self.nodes.show(self.screen)
            self.pacman.show(self.screen)
            pg.display.update()
            clock.tick(30)


game = Game()

game.main()
    
