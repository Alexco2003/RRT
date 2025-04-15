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
        self.grid = grid # grid of the environment; x,y on the grid = grid[y,x]
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
        if (x - self.goal.x)**2 + (y - self.goal.y)**2 <= self.distance**2:
            self.nearestNode.children.append(self.goal)
            self.goal.parent = self.nearestNode
        else:
            newNode = Node(x, y)
            self.nearestNode.children.append(newNode)
            newNode.parent = self.nearestNode

    # get a random point in the grid
    def randomPoint(self):
        x = random.randint(0, self.grid.shape[1] - 1)
        y = random.randint(0, self.grid.shape[0] - 1)
        point = np.array([x, y])
        return point

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
        vectorBetween = self.unitVector(start, end)
        testPoint = np.array([0.0, 0.0])
        for i in range(self.distance):
            testPoint[0] = start.x + i*vectorBetween[0]
            testPoint[1] = start.y + i*vectorBetween[1]
            if self.grid[min(np.int64(round(testPoint[1])),899),min(np.int64(round(testPoint[0])),1799)] == 1:
                return True
        return False

    # find unit vector between a node and an end point
    def unitVector(self, start, end):
         #calculam directia in care vrem sa ne miscam in functie de coordonatele nodului start si coord. punctului la care vrem sa ajungem end
        direction=np.array([end[0]-start.x,end[1]-start.y]) 
        norm=np.linalg.norm(direction) #calculam lungimea sau modulul vectorului dir. (ex: norm=sqrt(a^2+b^2)), pentru a mentine distanta in directia end
        if norm ==0: #daca norma unui punct e 0 inseamna ca nu are directie deci punctul de start este egal cu punctul de final si de asemenea n avem voie sa impartim la 0 in NumPy
            return np.array([0.0,0.0])
        return direction/norm #impartim ca sa obtinem un vector unitar=de lungime 1, dar cu aceeasi directie (ar trebui sa fie de ex: [0.2342.0.6544])

    # find the nearest node from a given unconnected point (Euclidian distance)
    def findNearestNode(self, root, point):
        if root is None:
            return
        minDistance = self.distanceEuclidian(root, point)
        if minDistance < self.nearestDistance:
            self.nearestDistance = minDistance
            self.nearestNode = root

        for child in root.children:
            self.findNearestNode(child, point)



    # find euclidian distance between a node and a point
    def distanceEuclidian(self, node, point):
        dist = np.sqrt((node.x - point[0])**2 + (node.y - point[1])**2)
        return dist

    # check if the goal has been reached
    def goalFound(self, point):
        distance_to_goal=self.distanceEuclidian(self.goal,point) #calculeaza distanta dintr point si nodul goal
        return distance_to_goal<=self.distance #daca distanta este mai mica sau egala cu self.distance atunci consideram ca a atins scopul


    # reset the nearest node and distance
    def resetNearestValues(self):
        self.nearestNode = None
        self.nearestDistance = 10000

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
        #self.totalDistance += self.distance
        #Daca suntem aproape de goal distanta poate fii mai mica deci cea de jos ar fii mai precisa
        self.totalDistance += np.linalg.norm(np.array([goal.x, goal.y]) - np.array([goal.parent.x, goal.parent.y]))

        self.retraceRRTPath(goal.parent)


# Load the grid, set start and goal <x, y> positions, number of iterations, step size
grid = np.load('test_images/test.npy')
print(grid.shape)
start = np.array([100.0, 100.0])
goal = np.array([1700.0,750.0])
numIterations = 500
stepSize = 200
goalRegion = plt.Circle((goal[0], goal[1]), stepSize, color='b', fill=False)

fig = plt.figure("RRT Algorithm")
plt.imshow(grid, cmap='binary')
plt.plot(start[0], start[1], 'ro')
plt.plot(goal[0], goal[1], 'bo')
ax = fig.gca()
ax.add_patch(goalRegion)
plt.xlabel('X-axis $(m)$')
plt.ylabel('Y-axis $(m)$')

rrt=RRT(start,goal,grid,numIterations,stepSize)

for i in range(rrt.iterations):
    rrt.resetNearestValues()
    print("Iteration: ",i)

    point=rrt.randomPoint()
    rrt.findNearestNode(rrt.randomTree,point)
    newPoint=rrt.steerToPoint(rrt.nearestNode,point)
    obstacle=rrt.isInObstacle(rrt.nearestNode,newPoint)

    if(obstacle==False):
        rrt.addChild(newPoint[0],newPoint[1])
        plt.pause(0.10)
        plt.plot([rrt.nearestNode.x,newPoint[0]],[rrt.nearestNode.y,newPoint[1]],'go',linestyle="--")

        if(rrt.goalFound(newPoint)):
            rrt.addChild(goal[0],goal[1])
            print("Goal found")
            break

rrt.retraceRRTPath(rrt.goal)
rrt.waypoints.insert(0,start)
print("Number of waypoints: ", rrt.numWaypoints)
print("Path Distance: ", rrt.totalDistance)
print("Waypoints: ",rrt.waypoints)

for i in range(len(rrt.waypoints)-1):
    plt.plot([rrt.waypoints[i][0],rrt.waypoints[i+1][0]],[rrt.waypoints[i][1],rrt.waypoints[i+1][1]],'ro',linestyle="--")
    plt.pause(0.10)

plt.show()




