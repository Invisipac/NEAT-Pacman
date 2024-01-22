# from nodegroup import NodeGroup

from dots import Dot
from ghosts import RedGhost, PinkGhost, BlueGhost, OrangeGhost
from pacman import Pacman
from variables import *
import neat
from math import sqrt
from random import choice

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
        self.ghost_kill_count = 0
        self.ghost_timer = 0
        self.ghost_counter = 1
        self.point_counter = 0
        for j, y in enumerate(map):
            for i, x in enumerate(y):
                if x in DOTS:
                    self.dots.append(Dot((i, j)))
                if x in POWER_DOTS:
                    self.dots.append(Dot((i, j), True))

        ################################### NEAT VARIABLES ##################################
        self.gen = -1
        self.nets = []
        self.ge = []
        self.pacmen = []
        self.gen_timer_for_moving = 0
        self.visited_squares = []

        

    def reset(self):
        self.pacman = Pacman((13.5, 23), 39, RATIO[0] / 4, pacman_sprites, 3, self.pacman.lives - 1, self.pacman.points)
        self.redGhost = RedGhost((13.5, 11), 42, RATIO[0] / 3, ghost_sprites[0], 2)
        self.blueGhost = BlueGhost((11.5, 14), 42, RATIO[0] / 3, ghost_sprites[2], 2)
        self.pinkGhost = PinkGhost((13.5, 14), 42, RATIO[0] / 3, ghost_sprites[1], 2)
        self.orangeGhost = OrangeGhost((15.5, 14), 42, RATIO[0] / 3, ghost_sprites[3], 2)
        self.ghosts = [self.redGhost, self.pinkGhost, self.blueGhost, self.orangeGhost]

        self.ghost_timer = 0
        self.ghost_counter = 1
        self.point_counter = 0

    def pacman_eating_dots(self):
        slow_pacman = False
        for i in range(len(self.dots) - 1, -1, -1):
            dot = self.dots[i]
            dot.show(self.screen)
            if not self.pacman.dead:
                if self.pacman.eat(dot):
                    slow_pacman = True
                    self.pacman.points += 1
                    if self.pacman.lives < 3:
                        self.point_counter += 1
                    self.ghost_timer = 0
                    # if dot.power_dot:
                    #     self.score += 50
                    #     self.pacman.not_move = 3
                    #     for ghost in self.ghosts:
                    #         if ghost.state != "Dead":
                    #             ghost.change_mode("Frightened")
                    #             self.ghost_kill_count = 0
                    # else:
                    #     self.pacman.not_move = 1
                    #     self.score += 10
                    self.dots.remove(dot)
                else:
                    if not slow_pacman:
                        if self.pacman.not_move > 0:
                            self.pacman.not_move -= 1
            if len(self.dots) == 0:
                self.pacman.not_move = 0

    def pacman_eating_ghosts(self):
            if not self.pacman.dead:
                    for ghost in self.ghosts:
                        ghost.update(self.ghosts, self.clock.get_time(), self.pacman, self.ghost_timer)
                        ghost.show(self.screen)
                        # print(ghost.speed)
                        if self.pacman.eat(ghost, "ghost"):
                            self.ghost_timer = 0
                            if ghost.state == "Frightened":
                                ghost.state = "Dead"
                                self.ghost_kill_count += 1
                                # self.score += 100 * (2 ** self.ghost_kill_count)
                                # print(100 * (2 ** self.ghost_kill_count), "------------------")

                            if ghost.state in ["Chase", "Scattered"]:
                                self.pacman.frame = 0
                                self.pacman.dead = True
    
    def releasing_ghosts(self):
        if self.pacman.frame == 13:
            self.pacman.dead = False
            self.pacman.frame = 0
            self.reset()

        # print("\n----------\n")

        # print(self.pacman.points)
        # print(self.point_counter)
        # print(self.pacman.lives)
        # print(self.ghost_counter)
        # print(self.ghost_timer)

        release_ghosts = [0, 7, 17, 32]
        # print(release_ghosts[self.ghost_counter])
        # print(self.point_counter == release_ghosts[self.ghost_counter])

        if self.ghosts[self.ghost_counter].trapped:
            if (self.pacman.lives == 3 and (self.pacman.points == self.ghosts[self.ghost_counter].point_limit or self.ghost_timer > 4000)) or \
                (self.pacman.lives < 3 and (self.point_counter == release_ghosts[self.ghost_counter] or self.ghost_timer > 4000)):
                self.ghost_timer = 0
                self.ghosts[self.ghost_counter].trapped = False
                self.ghosts[self.ghost_counter].mode_changed = True
                self.ghosts[self.ghost_counter].target = (13.5, 11)

                if self.ghost_counter < 3:
                    self.ghost_counter += 1
    def dist_to_target(self, start, end):
        return sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)
    def draw_ghosts(self):
        for ghost in self.ghosts:
            ghost.update(self.ghosts, self.clock.get_time(), self.pacman, self.ghost_timer)
            ghost.show(self.screen)
    def reset_ghosts(self):
        self.redGhost = RedGhost((13.5, 11), 42, RATIO[0] / 3, ghost_sprites[0], 2)
        self.blueGhost = BlueGhost((11.5, 14), 42, RATIO[0] / 3, ghost_sprites[2], 2)
        self.pinkGhost = PinkGhost((13.5, 14), 42, RATIO[0] / 3, ghost_sprites[1], 2)
        self.orangeGhost = OrangeGhost((15.5, 14), 42, RATIO[0] / 3, ghost_sprites[3], 2)
        self.ghosts = [self.redGhost, self.pinkGhost, self.blueGhost, self.orangeGhost]

        self.ghost_timer = 0
        self.ghost_counter = 1
        self.point_counter = 0
    def update_pacmen(self):
        
        for idx, p in enumerate(self.pacmen):
            p.find_surrounding_walls()
            distances_to_ghosts = {}
            distances_to_ghosts["red_dist"] = self.dist_to_target(tuple(p.map_pos), tuple(self.redGhost.map_pos))
            distances_to_ghosts["blue_dist"] = self.dist_to_target(tuple(p.map_pos), tuple(self.blueGhost.map_pos))
            distances_to_ghosts["orange_dist"] = self.dist_to_target(tuple(p.map_pos), tuple(self.orangeGhost.map_pos))
            distances_to_ghosts["pink_dist"] = self.dist_to_target(tuple(p.map_pos), tuple(self.pinkGhost.map_pos))


            output = self.nets[idx].activate(
                (p.surrounding_walls[0],
                p.surrounding_walls[1],
                p.surrounding_walls[2],
                p.surrounding_walls[3],
                # 0, 
                # 0,
                # 0,
                # 0
                distances_to_ghosts["red_dist"],
                distances_to_ghosts["blue_dist"],
                distances_to_ghosts["orange_dist"],
                distances_to_ghosts["pink_dist"]
                )
            )
            for dist in distances_to_ghosts:
                if distances_to_ghosts[dist] > 10:
                    self.ge[idx].fitness += 0.3
                else:
                    self.ge[idx].fitness -= 4
            # print(f"WALLS {p.surrounding_walls}")
            # possible_output = []
            # for i, n in enumerate(p.surrounding_walls):
            #     if n == 1:
            #         possible_output.append(output[i])
            # p.update(pg.key.get_pressed())
            # print(idx, p.surrounding_walls, output)
            # print(idx, end=' ')
            # for i in range(4):
            #     print(self.ge[idx].nodes[i].bias, self.ge[idx].nodes[i].response)
            # if idx == 0:
            #     print(idx, output.index(val), p.surrounding_walls, list(round(o, 2) for o in output))
            # print(idx, possible_output, p.surrounding_walls)
            # if p.surrounding_walls[0]:
            #     self.ge[idx].fitness += 0.5
            # else:
            #     self.ge[idx].fitness -= 3
            
            # if p.is_turned():
            #     self.ge[idx].fitness -= 1
            # else:
            keys = {pg.K_w: (0, -1), pg.K_a: (-1, 0), pg.K_d: (1, 0), pg.K_s: (0, 1)}
            keys_dir = ['for', 'left', 'right', 'back']
            
            val = max(output)
            # self.pacman.update(pg.key.get_pressed())
            move = list(keys.keys())[output.index(val)]
            # p.ai_update(list(keys.keys())[output.index(val)])
            p.ai_update(keys_dir[output.index(val)], self.clock.get_time())
            # print(idx, self.gen, self.ge[idx].fitness)
            next_spot = get_map_letter((p.map_pos.x + keys[move][0]) % len(map[0]), (p.map_pos.y + keys[move][1]))

            # if next_spot in PATH:
            #     self.ge[idx].fitness += 0.3
            # else:
            #     self.ge[idx].fitness -= 5
            
            # if self.pacman.dead:
            #     self.ge[idx].fitness -= 10
            # else:
            #     self.ge[idx].fitness += 0.1
            value = p.found_new_square()
            for ghost in self.ghosts:
                if p.eat(ghost, 'ghost'):
                    self.ge[idx].fitness -= 3
            if value is not None:
                if value:
                    # self.visited_squares.append(p.map_pos.copy())
                    self.ge[idx].fitness += 0.5
                    # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                else:
                    self.ge[idx].fitness -= 1.5
            
            # print(idx, p.visited_squares)
            # #     self.ge[idx].fitness += 0.2

            # if p.found_new_square():
            #     self.ge[idx].fitness += 130
            # else:
            #     self.ge[idx].fitness -= 0.1
            # print(idx, self.ge[idx].fitness)
            
    def redraw_pacmen(self):
        for p in self.pacmen:
            p.show(self.screen)
    def reset_gen(self):
        # print(self.visited_squares)
        self.ge = []
        self.nets = []
        self.pacmen = []
        self.visited_squares = []
        
        self.gen_timer_for_moving = 0
    def main(self, genomes, config):
        
        self.gen += 1
        
        for _, g in genomes:
            
            net = neat.nn.FeedForwardNetwork.create(g, config)
            self.nets.append(net)
            self.pacmen.append(Pacman((13.5, 23), 39, RATIO[0] / 4, pacman_sprites, 3, 3))
            self.pacman = self.pacmen[0]
            g.fitness = 0
            self.ge.append(g)

        timer = 0
        self.clock = pg.time.Clock()
        run = True
        while run:
            timer += self.clock.get_time()
            self.gen_timer_for_moving += self.clock.get_time()
            self.ghost_timer += self.clock.get_time()
            if self.gen_timer_for_moving > 15000:# or self.pacman.dead:
                run = False
                # self.reset()
                self.reset_ghosts()
                self.reset_gen()
                # self.gen += 1
            
            # for i in self.ghosts:
            #     print(i.timer, end=", ")
            # print()
            # for i in self.ghosts:
            #     print(i.state, end=", ")
            # print()

            
            # self.pacman_eating_ghosts()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    self.gen += 1
            self.screen.blit(bg, (0, 0))
            
            self.pacman_eating_dots()
            self.draw_ghosts()
            # self.pacman_eating_ghosts()
            self.releasing_ghosts()
            
            # self.pacman.update(pg.key.get_pressed())
            self.update_pacmen()
            # self.pacman.show(self.screen)
            # print(clock.get_fps())
            self.redraw_pacmen()
            pg.display.update()
            self.clock.tick(60)


game = Game(display)

#game.main()



# self.screen.fill((0, 0, 0))

            # slow_pacman = False
            # for i in range(len(self.dots) - 1, -1, -1):
            #     dot = self.dots[i]
            #     dot.show(self.screen)
            #     if not self.pacman.dead:
            #         if self.pacman.eat(dot):
            #             slow_pacman = True
            #             self.pacman.points += 1
            #             if self.pacman.lives < 3:
            #                 self.point_counter += 1
            #             self.ghost_timer = 0
            #             if dot.power_dot:
            #                 self.score += 50
            #                 self.pacman.not_move = 3
            #                 for ghost in self.ghosts:
            #                     if ghost.state != "Dead":
            #                         ghost.change_mode("Frightened")
            #                         self.ghost_kill_count = 0
            #             else:
            #                 self.pacman.not_move = 1
            #                 self.score += 10
            #             self.dots.remove(dot)
            #         else:
            #             if not slow_pacman:
            #                 if self.pacman.not_move > 0:
            #                     self.pacman.not_move -= 1
            # if len(self.dots) == 0:
            #     self.pacman.not_move = 0
            # print(self.pacman.not_move)
            # for j, y in enumerate(map):
            #     for i, x in enumerate(y):
            #         if x in OBSTACLES:
            #             pg.draw.rect(self.screen, (50, 50, 200), (i*RATIO[0], j*RATIO[1], RATIO[0], RATIO[1]))

            # if not self.pacman.dead:
            #     for ghost in self.ghosts:
            #         ghost.update(self.ghosts, self.clock.get_time(), self.pacman, self.ghost_timer)
            #         ghost.show(self.screen)
            #         # print(ghost.speed)
            #         if self.pacman.eat(ghost, "ghost"):
            #             self.ghost_timer = 0
            #             if ghost.state == "Frightened":
            #                 ghost.state = "Dead"
            #                 self.ghost_kill_count += 1
            #                 # self.score += 100 * (2 ** self.ghost_kill_count)
            #                 print(100 * (2 ** self.ghost_kill_count), "------------------")

            #             if ghost.state in ["Chase", "Scattered"]:
            #                 self.pacman.frame = 0
            #                 self.pacman.dead = True
            
            # if self.pacman.frame == 13:
            #     self.pacman.dead = False
            #     self.pacman.frame = 0
            #     self.reset()

            # print("\n----------\n")

            # print(self.pacman.points)
            # print(self.point_counter)
            # print(self.pacman.lives)
            # print(self.ghost_counter)
            # print(self.ghost_timer)

            # release_ghosts = [0, 7, 17, 32]
            # print(release_ghosts[self.ghost_counter])
            # # print(self.point_counter == release_ghosts[self.ghost_counter])

            # if self.ghosts[self.ghost_counter].trapped:
            #     if (self.pacman.lives == 3 and (self.pacman.points == self.ghosts[self.ghost_counter].point_limit or self.ghost_timer > 4000)) or \
            #         (self.pacman.lives < 3 and (self.point_counter == release_ghosts[self.ghost_counter] or self.ghost_timer > 4000)):
            #         self.ghost_timer = 0
            #         self.ghosts[self.ghost_counter].trapped = False
            #         self.ghosts[self.ghost_counter].mode_changed = True
            #         self.ghosts[self.ghost_counter].target = (13.5, 11)

            #         if self.ghost_counter < 3:
            #             self.ghost_counter += 1
            # print(self.ghost_timer)