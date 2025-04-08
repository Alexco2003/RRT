import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.pyplot import rcParams
np.set_printoptions(precision=3, suppress=True)
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
plt.rcParams['font.size'] = 22

class Node:
    def __init__(self, x, y):
        self.x = x # x coordinate
        self.y = y # y coordinate
        self.children = [] # list of children nodes
        self.parent = None # parent node

    def __repr__(self):
        return f"Node({self.x}, {self.y})"

class RRT:
    def __init__(self, start, goal, grid, iterations, distance):
        self.randomTree = Node(start[0], start[1]) # root of the tree
        self.goal = Node(goal[0], goal[1]) # goal node
        self.grid = grid # grid of the environment
        self.iterations = min(iterations, 300) # max iterations
        self.distance = distance # distance to extend towards the random node

        self.nearestNode = None # nearest node to the random node
        self.totalDistance = 0 # total distance of the path
        self.nearestDistance = 10000 # distance to the nearest node
        self.numWaypoints = 0 # number of waypoints
        self.waypoints = [] # list of waypoints

    def __repr__(self):
        return f"RRT({self.randomTree}, {self.goal}, {self.grid}, {self.iterations}, {self.distance})"





