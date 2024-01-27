# from nodegroup import NodeGroup

from dots import Dot
from ghosts import RedGhost, PinkGhost, BlueGhost, OrangeGhost
from pacman import Pacman
from variables import *

base_speed = 8

#game class that combines everything together and runs the game
class Game:
    def __init__(self, screen) -> None:
        #initialize pacman and all the ghosts
        self.pacman = Pacman((13.5, 23), 39, RATIO[0] / 4, pacman_sprites, 3, 3)
        self.redGhost = RedGhost((13.5, 11), 42, RATIO[0] / 3, ghost_sprites[0], 2)
        self.blueGhost = BlueGhost((11.5, 14), 42, RATIO[0] / 3, ghost_sprites[2], 2)
        self.pinkGhost = PinkGhost((13.5, 14), 42, RATIO[0] / 3, ghost_sprites[1], 2)
        self.orangeGhost = OrangeGhost((15.5, 14), 42, RATIO[0] / 3, ghost_sprites[3], 2)
        self.ghosts = [self.redGhost, self.pinkGhost, self.blueGhost, self.orangeGhost]

        #create game variables
        self.clock = pg.time.Clock()
        self.screen = screen

        #set up dots and high score
        self.dots = []
        self.score = 0
        try:
            file = open("high-score.txt", "r")
            self.high_score = int(file.readline())
            file.close()
        except OSError:
            self.high_score = 0

        #variables to control points and win conditions
        self.ghost_kill_count = 0
        self.ghost_timer = 0
        self.ghost_counter = 1
        self.point_counter = 0
        self.starting_game_timer = 0
        self.pacman_ghost_pause = 500
        self.is_playing = False
        self.game_over = False
        self.win = False
        self.win_timer = 10000

        self.first_play = True
        self.played = (False, "a")
        self.once = True

        #initialize list of dots
        for j, y in enumerate(map):
            for i, x in enumerate(y):
                if x in DOTS:
                    self.dots.append(Dot((i, j)))
                if x in POWER_DOTS:
                    self.dots.append(Dot((i, j), True))

        intro.play()

    #function to reset dots and game
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
    
    #function to reset game
    def reset(self, death=True):
        self.pacman = Pacman((13.5, 23), 39, RATIO[0] / 4, pacman_sprites, 3,
                             (self.pacman.lives - 1) if death else self.pacman.lives + 1)
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

    #function that controls how pacman interacts with the dots
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

                    chomp[self.pacman.points % 2].play().set_volume(0.5)

                    # if the dot was a power dot, increase the score and don't move the pacman for 3 frames
                    if dot.power_dot:
                        self.score += 50
                        self.pacman.not_move = 3

                        siren.stop()
                        retreat.stop()
                        self.played = (False, "d")
                        self.once = True

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

    #function that controls how pacman interacts with the ghosts 
    def pacman_ghosts_management(self):
        if not self.pacman.dead:
            someone_frightened = False
            for ghost in self.ghosts:
                # move the ghosts
                ghost.update(self.ghosts, self.clock.get_time(), self.pacman, self.ghost_timer)

                if ghost.state == "Frightened":
                    someone_frightened = True

                # if pacman collided with a ghost
                if self.pacman.eat(ghost, "ghost"):
                    self.ghost_timer = 0

                    # eat the ghost if it's frightened
                    if ghost.state == "Frightened":
                        self.pacman_ghost_pause = 0
                        ghost.state = "Dead"
                        self.ghost_kill_count += 1

                        eat_ghost.play().set_volume(0.5)

                        # increase score and make the ghost return to its house
                        self.score += 100 * (2 ** self.ghost_kill_count)
                        ghost.score = 100 * (2 ** self.ghost_kill_count)
                        ghost.show_score = True

                        # kill the pacman if it isn't
                    if ghost.state in ["Chase", "Scattered"]:
                        self.pacman.frame = 0
                        self.pacman.dead = True
                        death.play().set_volume(0.5)
                        siren.stop()
                        retreat.stop()
                        self.played = (False, "a")

            if not someone_frightened:
                if self.once:
                    self.played = (False, "a")
                    retreat.stop()
                    self.once = False

    #function that controls pacman's movement and death
    def update_pacman(self, keys, allowed_to_move):
        # death management
        if self.pacman.frame == 13:
            self.pacman.dead = False
            self.pacman.frame = 0
            self.reset()

        self.pacman.update(keys, allowed_to_move)

    #function that releases the ghosts from the box based on certain times
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

    #main function that runs the game itself
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

            #play sound effects at different points in the game
            if self.win_timer >= win_sound.get_length() * 1000:
                if self.win:
                    self.played = (False, "a")
                    self.win_reset()

                self.starting_game_timer += self.clock.get_time()
                self.pacman_ghost_pause += self.clock.get_time()

                if self.starting_game_timer > (2000 if not self.first_play else intro.get_length()*1000) and self.pacman_ghost_pause > 500 and not self.game_over:
                    timer += self.clock.get_time()
                    self.ghost_timer += self.clock.get_time()

                    if self.first_play:
                        self.first_play = False

                    if not self.played[0] and not self.pacman.dead:
                        if self.played[1] == "a":
                            siren.play(-1).set_volume(0.15)
                        else:
                            retreat.play(-1).set_volume(0.5)
                        self.played = (True, "")

                    #call all relevant functions for pacman and the ghosts
                    self.pacman_dot_management()
                    self.pacman_ghosts_management()
                    self.releasing_ghosts()

                self.update_pacman(pg.key.get_pressed(),
                                   self.starting_game_timer > (
                                       2000 if not self.first_play else intro.get_length() * 1000) and self.pacman_ghost_pause > 500)

                #check if you have lost all of your lives and write a new high score to the txt file
                if self.pacman.lives == 0:
                    self.game_over = True
                    if self.score > self.high_score:
                        self.high_score = self.score
                        file = open("high-score.txt", "w")
                        file.write(str(self.high_score))
                        file.close()

                #check if all dots have been eaten and you won
                if len(self.dots) == 0:
                    self.win = True
                    self.win_timer = 0
                    win_sound.play()
                    siren.stop()
                    retreat.stop()


            #play win sound 
            self.screen.fill((0, 0, 0))
            self.screen.blit(bg[0 if self.win_timer > win_sound.get_length()*1000 else (self.win_timer//300) % 2], (0, 0 + (offset * RATIO[1])))
            self.draw_dots()

            #draw to the screen if game is not over
            if not self.game_over:
                self.draw_ghosts(self.pacman_ghost_pause < 500)
                if self.pacman_ghost_pause > 500:
                    self.draw_pacman()

                for i in range(self.pacman.lives):
                    self.screen.blit(lives, (10 + i * 37, 9 + RATIO[1] * (31 + offset)))

        #draw other text relevant to the game
                if self.starting_game_timer < (2000 if not self.first_play else intro.get_length()*1000):
                    text(self.screen, "READY!", (255, 255, 0), (336, 420 + (offset * RATIO[1])), "center", font2)
        
            else:
                text(self.screen, "GAME  OVER", (255, 0, 0), (336, 420 + (offset * RATIO[1])), "center", font2)

            text(self.screen, "SCORE", (255, 255, 255), (WIDTH / 4 - RATIO[0] / 2, 24), "center", font2)
            text(self.screen, "HIGH SCORE", (255, 255, 255), (WIDTH / 4 * 3 + RATIO[0] / 2, 24), "center", font2)
            text(self.screen, str(self.score), (255, 255, 255), (WIDTH / 4 - RATIO[0] / 2, 60), "center", font2)
            text(self.screen, str(self.high_score), (255, 255, 255), (WIDTH / 4 * 3 + RATIO[0] / 2, 60), "center",
                 font2)

            pg.display.update()
            self.clock.tick(60)


game = Game(display)

game.main()
