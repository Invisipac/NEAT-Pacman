import pygame
from node import Node
from variables import *

class NodeGroup:
    def __init__(self):
        self.nodeList = {}

    def setupTestNodes(self, map):
        for i, row in enumerate(map):
            for j, tile in enumerate(row):
                if tile == "*":
                    self.nodeList[(i, j)] = Node(j * RATIO[0], i * RATIO[1])

        for i, row in enumerate(map):
            for j, tile in enumerate(row):
                if tile == "*":
                    # self.nodeList[(i, j)] = Node(i * 50, j * 50)

                    print("YOOOO", i, j)
                    # down
                    current_i, current_j = i + 1, j
                    while current_i < len(map) and map[current_i][current_j] in ["*", "-"]:
                        if map[current_i][current_j] == "*":
                            print(f"Node under at {current_i, current_j}")
                            self.nodeList[(i, j)].neighbors["DOWN"] = self.nodeList[(current_i, current_j)]
                            current_i = len(map)
                        current_i += 1
                    # right
                    current_i, current_j = i, j + 1
                    while current_j < len(row) and map[current_i][current_j] in ["*", "-"]:
                        if map[current_i][current_j] == "*":
                            print(f"Node right at {current_i, current_j}")
                            self.nodeList[(i, j)].neighbors["RIGHT"] = self.nodeList[(current_i, current_j)]
                            current_j = len(row)
                        current_j += 1
                    # up
                    current_i, current_j = i - 1, j
                    while current_i >= 0 and map[current_i][current_j] in ["*", "-"]:
                        if map[current_i][current_j] == "*":
                            print(f"Node above at {current_i, current_j}")
                            self.nodeList[(i, j)].neighbors["UP"] = self.nodeList[(current_i, current_j)]
                            current_i = 0
                        current_i -= 1
                    # left
                    current_i, current_j = i, j - 1
                    while current_j >= 0 and map[current_i][current_j] in ["*", "-"]:
                        if map[current_i][current_j] == "*":
                            print(f"Node left at {current_i, current_j}")
                            self.nodeList[(i, j)].neighbors["LEFT"] = self.nodeList[(current_i, current_j)]
                            current_j = 0
                        current_j -= 1

    def show(self, display):
        for node in self.nodeList.values():
            node.show(display)