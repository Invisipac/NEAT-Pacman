# from nodegroup import NodeGroup

from dots import Dot
from ghosts import RedGhost, PinkGhost, BlueGhost, OrangeGhost
from pacman import Pacman
from variables import *

base_speed = 8


class Game:
    def __init__(self, screen) -> None:
        self.pacman = Pacman((13.5, 23), 39, RATIO[0] / 4, pacman_sprites, 3, 3)
        self.redGhost = RedGhost((13.5, 11), 42, RATIO[0] / 3, ghost_sprites[0], 2)
        self.blueGhost = BlueGhost((11.5, 14), 42, RATIO[0] / 3, ghost_sprites[2], 2)
        self.pinkGhost = PinkGhost((13.5, 14), 42, RATIO[0] / 3, ghost_sprites[1], 2)
        self.orangeGhost = OrangeGhost((15.5, 14), 42, RATIO[0] / 3, ghost_sprites[3], 2)
        # self.ghosts = [self.redGhost]
        self.ghosts = [self.redGhost, self.pinkGhost, self.blueGhost, self.orangeGhost]
        self.clock = pg.time.Clock()
        self.screen = screen
        self.dots = []
        self.score = 0
        self.high_score = 0
        self.ghost_kill_count = 0
        self.ghost_timer = 0
        self.ghost_counter = 1
        self.point_counter = 0
        self.starting_game_timer = 0
        self.pacman_ghost_pause = 500
        self.game_over = False
        self.win = False
        self.win_timer = 1000
        for j, y in enumerate(map):
            for i, x in enumerate(y):
                if x in DOTS:
                    self.dots.append(Dot((i, j)))
                if x in POWER_DOTS:
                    self.dots.append(Dot((i, j), True))

    def win_reset(self):
        self.reset(False)
        self.dots = []
        for j, y in enumerate(map):
            for i, x in enumerate(y):
                if x in DOTS:
                    self.dots.append(Dot((i, j)))
                if x in POWER_DOTS:
                    self.dots.append(Dot((i, j), True))
        self.win = False

    def reset(self, death=True):
        self.pacman = Pacman((13.5, 23), 39, RATIO[0] / 4, pacman_sprites, 3, (self.pacman.lives - 1) if death else self.pacman.lives)
        self.redGhost = RedGhost((13.5, 11), 42, RATIO[0] / 3, ghost_sprites[0], 2)
        self.blueGhost = BlueGhost((11.5, 14), 42, RATIO[0] / 3, ghost_sprites[2], 2)
        self.pinkGhost = PinkGhost((13.5, 14), 42, RATIO[0] / 3, ghost_sprites[1], 2)
        self.orangeGhost = OrangeGhost((15.5, 14), 42, RATIO[0] / 3, ghost_sprites[3], 2)
        self.ghosts = [self.redGhost, self.pinkGhost, self.blueGhost, self.orangeGhost]

        self.ghost_timer = 0
        self.ghost_counter = 1
        self.point_counter = 0
        self.starting_game_timer = 0

    def draw_dots(self):
        # drawing the dots
        for i in range(len(self.dots) - 1, -1, -1):
            dot = self.dots[i]
            dot.show(self.screen)

    def draw_ghosts(self, nothing):
        # display the ghosts
        if not self.pacman.dead:
            for ghost in self.ghosts:
                ghost.show(self.screen, nothing)
                if ghost.state == "Dead" and nothing and ghost.show_score:
                    text(self.screen, str(ghost.score), (0, 255, 255), (ghost.pos.x, ghost.pos.y + (offset * RATIO[1])),
                         "center")
                if ghost.state == "Dead" and not nothing:
                    ghost.show_score = False

    def draw_pacman(self):
        self.pacman.show(self.screen)

    def pacman_dot_management(self):
        slow_pacman = False
        for i in range(len(self.dots) - 1, -1, -1):
            if not self.pacman.dead:
                dot = self.dots[i]

                # if pacman ate a dot
                if self.pacman.eat(dot):
                    # slow pacman
                    slow_pacman = True

                    # increase its dot counter
                    self.pacman.points += 1

                    # global counter if less than 3 lives
                    if self.pacman.lives < 3:
                        self.point_counter += 1

                    self.ghost_timer = 0

                    # if the dot was a power dot, increase the score and don't move the pacman for 3 frames
                    if dot.power_dot:
                        self.score += 50
                        self.pacman.not_move = 3

                        # change all ghosts to frightened
                        for ghost in self.ghosts:
                            if ghost.state != "Dead":
                                ghost.change_mode("Frightened")
                                self.ghost_kill_count = 0
                    else:
                        # increase the score and don't move pacman for 1 frame
                        self.pacman.not_move = 1
                        self.score += 10

                    # remove that dot
                    self.dots.remove(dot)
                else:
                    # don't move pacman
                    if not slow_pacman:
                        if self.pacman.not_move > 0:
                            self.pacman.not_move -= 1

        if len(self.dots) == 0:
            self.pacman.not_move = 0

    def pacman_ghosts_management(self):
        if not self.pacman.dead:
            for ghost in self.ghosts:
                # move the ghosts
                ghost.update(self.ghosts, self.clock.get_time(), self.pacman, self.ghost_timer)

                # if pacman collided with a ghost
                if self.pacman.eat(ghost, "ghost"):
                    self.ghost_timer = 0
                    # eat the ghost if it's frightened
                    if ghost.state == "Frightened":
                        self.pacman_ghost_pause = 0
                        ghost.state = "Dead"
                        self.ghost_kill_count += 1

                        # increase score and make the ghost return to its house
                        self.score += 100 * (2 ** self.ghost_kill_count)
                        ghost.score = 100 * (2 ** self.ghost_kill_count)
                        ghost.show_score = True

                        # kill the pacman if it isn't
                    if ghost.state in ["Chase", "Scattered"]:
                        self.pacman.frame = 0
                        self.pacman.dead = True

    def update_pacman(self, keys, allowed_to_move):
        # death management
        if self.pacman.frame == 13:
            self.pacman.dead = False
            self.pacman.frame = 0
            self.reset()

        self.pacman.update(keys, allowed_to_move)

    def releasing_ghosts(self):
        release_ghosts = [0, 7, 17, 32]

        if self.ghosts[self.ghost_counter].trapped:
            if (self.pacman.lives == 3 and (
                    self.pacman.points >= self.ghosts[self.ghost_counter].point_limit or self.ghost_timer > 4000)) or \
                    (self.pacman.lives < 3 and (
                            self.point_counter >= release_ghosts[self.ghost_counter] or self.ghost_timer > 4000)):
                self.ghost_timer = 0
                self.ghosts[self.ghost_counter].trapped = False
                self.ghosts[self.ghost_counter].mode_changed = True
                self.ghosts[self.ghost_counter].target = (13.5, 11)

                if self.ghost_counter < 3:
                    self.ghost_counter += 1

    def main(self):
        timer = 0
        self.clock = pg.time.Clock()
        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

            if self.win:
                self.win_timer += self.clock.get_time()

            if self.win_timer >= 1000:
                if self.win:
                    self.win_reset()

                self.starting_game_timer += self.clock.get_time()
                self.pacman_ghost_pause += self.clock.get_time()

                if self.starting_game_timer > 2000 and self.pacman_ghost_pause > 500 and not self.game_over:
                    timer += self.clock.get_time()
                    self.ghost_timer += self.clock.get_time()

                    self.pacman_dot_management()
                    self.pacman_ghosts_management()
                    self.releasing_ghosts()

                self.screen.fill((0, 0, 0))
                self.screen.blit(bg, (0, 0 + (offset * RATIO[1])))
                self.draw_dots()

                if not self.game_over:
                    self.draw_ghosts(self.pacman_ghost_pause < 500)
                    if self.pacman_ghost_pause > 500:
                        self.draw_pacman()

                    for i in range(self.pacman.lives):
                        self.screen.blit(lives, (10 + i * 37, 9 + RATIO[1] * (31 + offset)))

                    if self.starting_game_timer < 2000:
                        text(self.screen, "READY!", (255, 255, 0), (336, 420 + (offset * RATIO[1])), "center", font2)

                else:
                    text(self.screen, "GAME  OVER", (255, 0, 0), (336, 420 + (offset * RATIO[1])), "center", font2)

                text(self.screen, "SCORE", (255, 255, 255), (WIDTH / 4 - RATIO[0] / 2, 24), "center", font2)
                text(self.screen, "HIGH SCORE", (255, 255, 255), (WIDTH / 4 * 3 + RATIO[0] / 2, 24), "center", font2)
                text(self.screen, str(self.score), (255, 255, 255), (WIDTH / 4 - RATIO[0] / 2, 60), "center", font2)
                text(self.screen, str(self.high_score), (255, 255, 255), (WIDTH / 4 * 3 + RATIO[0] / 2, 60), "center",
                     font2)

                self.update_pacman(pg.key.get_pressed(), self.starting_game_timer > 2000 and self.pacman_ghost_pause > 500)

                if self.pacman.lives == 0:
                    self.game_over = True
                    if self.score > self.high_score:
                        self.high_score = self.score

                if len(self.dots) == 0:
                    self.win = True
                    self.win_timer = 0

            pg.display.update()
            self.clock.tick(60)


game = Game(display)

game.main()
