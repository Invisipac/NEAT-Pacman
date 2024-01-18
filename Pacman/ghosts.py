from ghost import Ghost
from pacman import Pacman


class RedGhost(Ghost):
    def __init__(self, pos, speed, colour, pacman: Pacman) -> None:
        super().__init__(pos, speed, colour, pacman)

    def chase_behaviour(self, ghosts):
        self.target = (int(self.pacman.map_locs.y), int(self.pacman.map_locs.x))


class PinkGhost(Ghost):
    def __init__(self, pos, speed, colour, pacman: Pacman) -> None:
        super().__init__(pos, speed, colour, pacman)

    def chase_behaviour(self, ghosts):
        moves = {"UP": ((0, -1), 1), "DOWN": ((0, 1), 1), "LEFT": ((-1, 0), 0), "RIGHT": ((1, 0), 0)}
        self.target = (int(self.pacman.map_locs.y) + 4 * moves[self.pacman.dir][0][1],
                       int(self.pacman.map_locs.x) + 4 * moves[self.pacman.dir][0][0])


class BlueGhost(Ghost):
    def __init__(self, pos, speed, colour, pacman: Pacman) -> None:
        super().__init__(pos, speed, colour, pacman)

    def chase_behaviour(self, ghosts):
        moves = {"UP": ((0, -1), 1), "DOWN": ((0, 1), 1), "LEFT": ((-1, 0), 0), "RIGHT": ((1, 0), 0)}
        red_ghost_loc = ghosts[0].map_locs
        target = (int(self.pacman.map_locs.y) + 2 * moves[self.pacman.dir][0][1],
                  int(self.pacman.map_locs.x) + 2 * moves[self.pacman.dir][0][0])
        self.target = (2 * target[0] - red_ghost_loc.y,
                       2 * target[1] - red_ghost_loc.x)


class OrangeGhost(Ghost):
    def __init__(self, pos, speed, colour, pacman: Pacman) -> None:
        super().__init__(pos, speed, colour, pacman)

    def chase_behaviour(self, ghosts):
        if self.dist_to_pacman() < 8:
            self.target = (30, 0)
        else:
            self.target = (int(self.pacman.map_locs.y), int(self.pacman.map_locs.x))