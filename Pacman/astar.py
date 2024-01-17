from node import Node
import pygame as pg
from collections import deque
from queue import PriorityQueue
import math
from variables import OBSTACLES, GRID_SIZE, map
from minHeap import MinHeap
grid = []

W = 800
H = 600
n = 5
screen = pg.display.set_mode((W, H))

for i in range(n):
    grid.append([])
    for j in range(n):
        grid[i].append(Node(j*W/n, i*H/n))

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


# tp_node_left = ((14, -1), (14, 27))
# tp_node_right = ((14, 28), (14, 0))

tp_nodes_going_left = {(14, 0):(14, -1), (14, -1):(14, 27)}
tp_nodes_going_right = {(14, 27):(14, 28), (14, 28) : (14, 0)}

def find_neighbours(grid, i, j, direction):
    neighbours = []

    if direction == [-1, 0] and (i, j) in tp_nodes_going_left:
        neighbours.append(tp_nodes_going_left[(i, j)])
    elif direction == [1, 0] and (i, j) in tp_nodes_going_right:
        neighbours.append(tp_nodes_going_right[(i, j)])
    else:
        if i - 1 >=0 and not grid[i - 1][j] in OBSTACLES:
            neighbours.append((i - 1, j))
        if i + 1 <= GRID_SIZE[1] - 1 and not grid[i + 1][j] in OBSTACLES:
            neighbours.append((i + 1, j))
        if j - 1 >= 0 and not grid[i][j - 1] in OBSTACLES:
            neighbours.append((i, j - 1))
        if j + 1 <= GRID_SIZE[0] - 1 and not grid[i][j + 1] in OBSTACLES:
            neighbours.append((i, j + 1))
        
    return neighbours

def h(i, j, goal):
    return (goal[1] - j)**2 + (goal[0] - i)**2

def astar(start, goal, grid, direction, h = h):
    #openSet = [start]
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

        for n in find_neighbours(grid, current[0], current[1], direction):
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
                    #if n not in closedSet:
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

