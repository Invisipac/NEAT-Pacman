from ghost import Ghost


class RedGhost(Ghost):
    def __init__(self, map_pos, size, speed, animation, frame_lim):
        super().__init__(map_pos, size, speed, animation, frame_lim)

    def chase_behaviour(self, ghosts, pacman):
        self.target = (int(pacman.map_pos.x), int(pacman.map_pos.y))
        # print(self.map_pos)

    def scattered_behaviour(self):
        self.target = (25, -3)


class PinkGhost(Ghost):
    def __init__(self, map_pos, size, speed, animation, frame_lim):
        super().__init__(map_pos, size, speed, animation, frame_lim)
        self.point_limit = 15
        self.trapped = True
        self.dir = (0, -1)

    def chase_behaviour(self, ghosts, pacman):
        self.target = (int(pacman.map_pos.x) + 4 * pacman.dir[0],
                       int(pacman.map_pos.y) + 4 * pacman.dir[1])

    def scattered_behaviour(self):
        self.target = (2, -3)


class BlueGhost(Ghost):
    def __init__(self, map_pos, size, speed, animation, frame_lim):
        super().__init__(map_pos, size, speed, animation, frame_lim)
        self.trapped = True
        self.dir = (0, 1)
        self.point_limit = 30

    def chase_behaviour(self, ghosts, pacman):
        red_ghost_loc = ghosts[0].map_pos
        target = (int(pacman.map_pos.x) + 2 * pacman.dir[0],
                  int(pacman.map_pos.y) + 2 * pacman.dir[1])
        self.target = (2 * target[0] - red_ghost_loc.x,
                       2 * target[1] - red_ghost_loc.y)

    def scattered_behaviour(self):
        self.target = (27, 31)


class OrangeGhost(Ghost):
    def __init__(self, map_pos, size, speed, animation, frame_lim):
        super().__init__(map_pos, size, speed, animation, frame_lim)
        self.trapped = True
        self.dir = (0, 1)
        self.point_limit = 90

    def chase_behaviour(self, ghosts, pacman):
        if self.dist_to_pacman(pacman) < 8:
            self.target = (0, 30)
        else:
            self.target = (int(pacman.map_pos.x), int(pacman.map_pos.y))

    def scattered_behaviour(self):
        self.target = (0, 31)
