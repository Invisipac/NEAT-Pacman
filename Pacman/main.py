# from nodegroup import NodeGroup

from dots import Dot
from ghosts import RedGhost, PinkGhost, BlueGhost, OrangeGhost
from pacman import Pacman
from variables import *


class Game:
    def __init__(self, screen) -> None:
        self.pacman = Pacman((13.5, 23), 39, 4, pacman_sprites, 3)
        self.redGhost = RedGhost((13.5, 11), 42, 4, ghost_sprites[0], 2)
        self.pinkGhost = PinkGhost((11.5, 14), 42, 6, ghost_sprites[1], 2)
        self.blueGhost = BlueGhost((13.5, 14), 42, 8, ghost_sprites[2], 2)
        self.orangeGhost = OrangeGhost((15.5, 14), 42, 6, ghost_sprites[3], 2)
        self.ghosts = [self.redGhost, self.pinkGhost, self.blueGhost, self.orangeGhost]

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
            # print("NEW FRAME __________________________")
            timer += clock.get_time()
            # if timer > 1:
            #     timer = 0
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
            # self.pacman.update(pg.key.get_pressed())
            self.screen.blit(bg, (0, 0))
            # self.screen.fill((0, 0, 0))
            print(self.pacman.points)
            for i in range(len(self.dots) - 1, -1, -1):
                dot = self.dots[i]
                dot.show(self.screen)
                if self.pacman.eat(dot):
                    self.pacman.points += 1
                    if dot.power_dot:
                        for ghost in self.ghosts:
                            ghost.change_mode("Frightened")
                    self.dots.remove(dot)
            print(f"MOUSEX: {pg.mouse.get_pos()[0]}, MOUSEY: {pg.mouse.get_pos()[1]}")
            print(self.ghosts[2].pos)
            for j, y in enumerate(map):
                for i, x in enumerate(y):
                    # pg.draw.rect(self.screen, (0,255,0),(i*RATIO[0], j*RATIO[0], RATIO[0], RATIO[0]), 1)
                    if x in OBSTACLES:
                        pass
                        # pg.draw.rect(self.screen, (50, 50, 200), (i*RATIO[0], j*RATIO[1], RATIO[0], RATIO[1]))

            self.pacman.update(pg.key.get_pressed())
            self.pacman.show(self.screen)
            for ghost in self.ghosts:
                ghost.update(self.ghosts, clock.get_time(), self.pacman)
                ghost.show(self.screen)
                # if self.pacman.eat(ghost):
                #     ghost.
            
            # print(clock.get_fps())
            pg.display.update()
            clock.tick(30)


game = Game(display)

game.main()
