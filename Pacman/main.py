# from nodegroup import NodeGroup
import pygame.mouse

from pacman import Pacman
from dots import Dot
from variables import *
from ghosts import RedGhost, PinkGhost, BlueGhost, OrangeGhost
from time import time_ns

class Game:
    def __init__(self, screen) -> None:
        self.pacman = Pacman((13.5, 23), 4, pacman_sprites)
        # self.nodes = NodeGroup()
        # self.nodes.setupTestNodes(map)
        self.redGhost = RedGhost((5, 8), 4, ghost_sprites[0], self.pacman)
        self.pinkGhost = PinkGhost((10, 8), 4, ghost_sprites[1], self.pacman)
        self.blueGhost = BlueGhost((6, 12), 4, ghost_sprites[2], self.pacman)
        self.orangeGhost = OrangeGhost((6, 14), 4, ghost_sprites[3], self.pacman)
        self.ghosts = [self.redGhost, self.pinkGhost, self.blueGhost, self.orangeGhost]
        # self.ghost.scare_ghost(self.pacman)
        self.screen = screen
        self.dots = []
        for j, y in enumerate(map):
            for i, x in enumerate(y):
                if x in DOTS:
                    self.dots.append(Dot((i, j)))
                if x in POWER_DOTS:
                    self.dots.append(Dot((i, j), True))
    
    def main(self):
        timer = 0
        clock = pg.time.Clock()
        run = True
        while run:
            timer += clock.get_time()
            # if timer > 1:
            #     timer = 0
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
            self.pacman.update(pg.key.get_pressed())
            self.screen.blit(bg, (0, 0))
            # self.screen.fill((0, 0, 0))

            for i in range(len(self.dots)-1, -1, -1):
                dot = self.dots[i]
                dot.show(self.screen)
                if self.pacman.eat(dot):
                    if dot.power_dot:
                        for ghost in self.ghosts:
                            ghost.change_mode("Frightened")
                    self.dots.remove(dot)

            for j, y in enumerate(map):
                for i, x in enumerate(y):
                    if x in OBSTACLES:
                        pass
                        # pg.draw.rect(self.screen, (50, 50, 200), (i*RATIO[0], j*RATIO[1], RATIO[0], RATIO[1]))

            self.pacman.show(self.screen)
            for ghost in self.ghosts:
                # s = time_ns()
                ghost.update(self.ghosts, clock.get_time())
                # e = time_ns()
                # print(f"update, {e - s}")
                # s = time_ns()
                # print(ghost.dir)
                ghost.move_ghost()
                #self.ghost.find_scared_pos()
                # e = time_ns()
                # print(f"move, {e - s}")
                ghost.draw_ghost(self.screen)

            # print(clock.get_fps())
            pg.display.update()
            clock.tick(5)


game = Game(display)

game.main()
    
