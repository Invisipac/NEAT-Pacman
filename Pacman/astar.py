from node import Node
import pygame as pg
from collections import deque
from queue import PriorityQueue
import math
grid = []

W = 800
H = 600
n = 5
screen = pg.display.set_mode((W, H))

for i in range(n):
    grid.append([])
    for j in range(n):
        grid[i].append(Node(j*W/n, i*H/n))



def reconstruct(cameFrom: dict, current):
    totalPath = [current]
    while current in cameFrom.keys() and current != (0, 0):
        current = cameFrom[current]
        totalPath.append(current)
    return totalPath

def find_neighbours(i, j):
    neighbours = []
    if i - 1 >=0:
        neighbours.append((i - 1, j))
    if i + 1 <= n - 1:
        neighbours.append((i + 1, j))
    if j - 1 >= 0:
        neighbours.append((i, j - 1))
    if j + 1 <= n-1:
        neighbours.append((i, j + 1))
    
    return neighbours

def h(i, j, goal):
    return (goal[1] - j)**2 + (goal[0] - i)**2

def astar(start, goal, h = h):
    openSet = [start]

    cameFrom = {}

    gScore = {}
    gScore[start] = 0

    fScore = {}
    fScore[start] = h(*start, goal=goal)

    while len(openSet) != 0:
        current = openSet[0]
        
        if current == goal:
            return reconstruct(cameFrom, current)
    
        openSet.remove(current)

        for n in find_neighbours(current[0], current[1]):
            tempG = gScore[current] + 1
            if n in openSet:
                if tempG < gScore[n]:
                    cameFrom[n] = current
                    gScore[n] = tempG
                    fScore[n] = tempG + h(*n, goal=goal)
            else:
                gScore[n] = tempG
                cameFrom[n] = current
                openSet.append(n)

    return -1

Astar = astar((0, 0), ((n - 1) - 2, (n - 1) - 3))

run = True

while run:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False

    screen.fill(0)

    for i in range(5):
        for j in range(5):
            if (i, j) not in Astar:
                pg.draw.rect(screen, (255, 255, 255), (grid[i][j].pos.x, grid[i][j].pos.y, W/n, H/n), 1)
            else:
                pg.draw.rect(screen, (0, 255, 0), (grid[i][j].pos.x + 0.5, grid[i][j].pos.y + 0.5, W/n - 1, H/n  - 1))
    
    pg.display.update()

pg.quit()

