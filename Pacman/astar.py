import pygame as pg
from pygame import Vector2 as vec
from minHeap import MinHeap
from node import Node
from variables import OBSTACLES, GRID_SIZE

grid = []

W = 800
H = 600
n = 5
screen = pg.display.set_mode((W, H))

for i in range(n):
    grid.append([])
    for j in range(n):
        grid[i].append(Node(j * W / n, i * H / n))

grid[2][1].obstacle = True
grid[2][2].obstacle = True
grid[1][2].obstacle = True
grid[2][0].obstacle = True

grid[4][2].obstacle = True


def reconstruct(cameFrom: dict, current):
    totalPath = [current]
    while current in cameFrom.keys() and current != (0, 0):
        current = cameFrom[current]
        totalPath.append(current)
    return totalPath


def find_neighbours(grid, i, j, dir):
    neighbours = []

    if i + dir[1] >= 0 and not grid[i + dir[1]][j + dir[0]] in OBSTACLES:
        neighbours.append((i + dir[1], j + dir[0]))

    if i + dir[0] <= GRID_SIZE[1] - 1 and not grid[i + dir[0]][j + dir[1]] in OBSTACLES:
        neighbours.append((i + dir[0], j + dir[1]))

    print("yo", i-dir[0], j-dir[1])
    if j - dir[1] >= 0 and not grid[i - dir[0]][j - dir[1]] in OBSTACLES:
        neighbours.append((i - dir[0], j - dir[1]))

    print(dir)
    print(neighbours)
    # if j + 1 <= GRID_SIZE[0] - 1 and not grid[i][j + 1] in OBSTACLES:
    #     neighbours.append((i, j + 1))

    return neighbours


def h(i, j, goal):
    return (goal[1] - j) ** 2 + (goal[0] - i) ** 2


def astar(start, goal, grid, dir, h=h):
    # openSet = [start]
    openSet = MinHeap()
    openSet.push(start, 0)
    closedSet = []
    cameFrom = {}

    gScore = {}
    gScore[start] = 0

    fScore = {}
    fScore[start] = h(*start, goal=goal)

    while openSet.size() != 0:
        element = openSet.pop()
        current = element[0]
        if current == goal:
            return reconstruct(cameFrom, current)

        openSet.remove(element)
        closedSet.append(current)
        if cameFrom != {}:
            dir = list(vec(current[1] - cameFrom[current][1], current[0] - cameFrom[current][0]).normalize())
            dir = [int(dir[0]), int(dir[1])]
        for n in find_neighbours(grid, current[0], current[1], dir):
            tempG = gScore[current] + 1
            if n not in closedSet:
                if openSet.is_element(n):
                    if tempG < gScore[n]:
                        cameFrom[n] = current
                        gScore[n] = tempG
                        fScore[n] = tempG + h(*n, goal=goal)
                else:
                    gScore[n] = tempG
                    cameFrom[n] = current
                    fScore[n] = tempG + h(*n, goal=goal)
                    openSet.push(n, fScore[n])

    return -1

# Astar = astar((8, 1), (8, 3), map)
# print(Astar)
# # run = True

# while run:
#     for e in pg.event.get():
#         if e.type == pg.QUIT:
#             run = False

#     screen.fill(0)

#     for i in range(5):
#         for j in range(5):
#             if (i, j) not in Astar and not grid[i][j].obstacle:
#                 pg.draw.rect(screen, (255, 255, 255), (grid[i][j].pos.x, grid[i][j].pos.y, W/n, H/n), 1)
#             elif grid[i][j].obstacle:
#                 pg.draw.rect(screen, (255, 0, 0), (grid[i][j].pos.x + 0.5, grid[i][j].pos.y + 0.5, W/n - 1, H/n  - 1))
#             else:
#                 pg.draw.rect(screen, (0, 255, 0), (grid[i][j].pos.x + 0.5, grid[i][j].pos.y + 0.5, W/n - 1, H/n  - 1))

#     pg.display.update()

# pg.quit()
