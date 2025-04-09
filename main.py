import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.pyplot import rcParams
np.set_printoptions(precision=3, suppress=True)
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
plt.rcParams['font.size'] = 12

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

    # add the point to the nearest node and add goal when reached
    def addChild(self, x, y):
        pass

    # get a random point in the grid
    def randomPoint(self):
        pass

    # steer a distance from the start point to the end point
    def steerToPoint(self, start, end):
        offset = self.distance * self.unitVector(start, end)
        point = np.array([start.x + offset[0], start.y + offset[1]])
        
        #grid.shape[1] se refera la axa x!!!
        if point[0] < 0 or point[0] >= self.grid.shape[1] or point[1] < 0 or point[1] >= self.grid.shape[0]:
            return np.array([start.x, start.y])
        
        if not self.isInObstacle(start, point):
            return point
        else:
            return np.array([start.x, start.y])
        

    # check if the obstacle is in the path
    def isInObstacle(self, start, end):
        pass

    # find unit vector between two points
    def unitVector(self, start, end):
        pass

    # find the nearest node from a given unconnected point (Euclidian distance)
    def findNearestNode(self, root, point):
        pass

    # find euclidian distance between a node and a point
    def distance(self, node, point):
        dist = np.sqrt((node.x - point[0])**2 + (node.y - point[1])**2)
        return dist

    # check if the goal has been reached
    def goalFound(self, point):
        pass

    # reset the nearest node and distance
    def resetNearestValues(self):
        pass

    # trace the path from goal to start
    def retraceRRTPath(self, goal):
        if goal is None or goal.parent is None:
            return

        #end recursion when goal node reaches the start node
        if goal.x == self.randomTree.x and goal.y ==self.randomTree.y:
            return
        
        self.numWaypoints += 1
        currentPoint = np.array([goal.x, goal.y])
        self.waypoints.insert(0, currentPoint)
        self.totalDistance += self.distance
        #Daca suntem aproape de goal distanta poate fii mai mica deci cea de jos ar fii mai precisa
        #self.totalDistance += np.linalg.norm(np.array([goal.x, goal.y]) - np.array([goal.parent.x, goal.parent.y]))

        self.retraceRRTPath(goal.parent)


# Load the grid, set start and goal <x, y> positions, number of iterations, step size
grid = np.load('test_images/test.npy')
start = np.array([100.0, 100.0])
goal = np.array([1700.0,750.0])
numIterations = 200
stepSize = 50
goalRegion = plt.Circle((goal[0], goal[1]), stepSize, color='b', fill=False)

fig = plt.figure("RRT Algorithm")
plt.imshow(grid, cmap='binary')
plt.plot(start[0], start[1], 'ro')
plt.plot(goal[0], goal[1], 'bo')
ax = fig.gca()
ax.add_patch(goalRegion)
plt.xlabel('X-axis $(m)$')
plt.ylabel('Y-axis $(m)$')
plt.show()


