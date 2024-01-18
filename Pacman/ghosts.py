from ghost import Ghost
from pacman import Pacman
from astar import astar
from variables import *

class RedGhost(Ghost):
    def __init__(self, pos, speed, colour, pacman: Pacman) -> None:
        super().__init__(pos, speed, colour, pacman)

    def chase_behaviour(self):
        self.target = (int(self.pacman.map_locs.y), int(self.pacman.map_locs.x))
        self.start = (int(self.map_locs.y), int(self.map_locs.x))
        # print(self.start, self.target, map)
        self.cur_path = list(reversed(astar(self.start, self.target, map, self.dir)))
        # print("YOO", self.cur_path)
        self.calculate_dir()

class PinkGhost(Ghost):
    def __init__(self, pos, speed, colour, pacman: Pacman) -> None:
        super().__init__(pos, speed, colour, pacman)

    def chase_behaviour(self):
        print(map[int(self.pacman.map_locs.y)][int(self.pacman.map_locs.x)])
        moves = {"UP": ((0, -1), 1), "DOWN": ((0, 1), 1), "LEFT": ((-1, 0), 0), "RIGHT": ((1, 0), 0)}
        move_ahead = 0
        for i in range(5):
            if map[int(self.pacman.map_locs.y) + (move_ahead + 1) * moves[self.pacman.dir][0][1]][int(self.pacman.map_locs.x) + (move_ahead + 1) * moves[self.pacman.dir][0][0]] in PATH:
                move_ahead += 1
                print("yay", move_ahead)
            else:
                break
        self.target = (int(self.pacman.map_locs.y) + move_ahead * moves[self.pacman.dir][0][1], int(self.pacman.map_locs.x) + move_ahead * moves[self.pacman.dir][0][0])
        self.start = (int(self.map_locs.y), int(self.map_locs.x))
        # print(self.start, self.target, map)
        self.cur_path = list(reversed(astar(self.start, self.target, map, self.dir)))
        self.calculate_dir()