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
        self.iterations = min(iterations, 10000) # max iterations
        self.distance = distance # distance to extend towards the random node

        self.nearestNode = None # nearest node to the random node
        self.totalDistance = 0 # total distance of the path
        self.nearestDistance = 100000 # distance to the nearest node
        self.numWaypoints = 0 # number of waypoints
        self.waypoints = [] # list of waypoints

    def __repr__(self):
        return f"RRT({self.randomTree}, {self.goal}, {self.grid}, {self.iterations}, {self.distance})"

    # add the point to the nearest node and add goal when reached
    def addChild(self, x, y):
        if (x - self.goal.x)**2 + (y - self.goal.y)**2 <= self.distance**2:
            newNode2 = Node(x, y)
            self.nearestNode.children.append(newNode2)
            newNode2.parent = self.nearestNode

            newNode2.children.append(self.goal)
            self.goal.parent = newNode2

            self.waypoints.insert(0, np.array([x, y]))
            self.numWaypoints += 1
            self.totalDistance += np.linalg.norm(np.array([self.goal.x, self.goal.y]) - np.array([self.goal.parent.x, self.goal.parent.y]))

        else:
            if self.nearestNode.x == x and self.nearestNode.y == y:
                return
            newNode = Node(x, y)
            self.nearestNode.children.append(newNode)
            newNode.parent = self.nearestNode

    # get a random point in the grid
    def randomPoint(self, iter):
        if(iter % 10==0):
            z=random.randint(0,1)
            if(z==0):
                y=self.goal.y
                x= random.randint(0, self.grid.shape[1]-1)
                point=np.array([x,y])
            else:
                x=self.goal.x
                y= random.randint(0, self.grid.shape[0]-1)
                point=np.array([x,y])

        else:
             x = random.randint(0, self.grid.shape[1] - 1)
             y = random.randint(0, self.grid.shape[0] - 1)
             point = np.array([x, y])
            
        return point

    # steer a distance from the start point to the end point
    def steerToPoint(self, start, end):

        direction = self.unitVector(start, end)
        newEnd = np.array([start.x + self.distance*direction[0], start.y + self.distance*direction[1]]) # new end point along the direction of the random point

        #grid.shape[1] se refera la axa x!!!
        if (newEnd[0] < 0 or newEnd[0] >= self.grid.shape[1] or newEnd[1] < 0 or newEnd[1] >= self.grid.shape[0]):

            max_x = self.grid.shape[1] - 1
            max_y = self.grid.shape[0] - 1

            tx = float('inf')
            ty = float('inf')

            if direction[0] > 0:
                tx = (max_x - start.x) / direction[0]
            elif direction[0] < 0:
                tx = -start.x / direction[0]

            if direction[1] > 0:
                ty = (max_y - start.y) / direction[1]
            elif direction[1] < 0:
                ty = -start.y / direction[1]

            t = min(tx, ty, self.distance)
            newEnd = np.array([start.x + t * direction[0], start.y + t * direction[1]])
        
        obstaclePoint = self.isInObstacle(start, newEnd)
        distanceToObstacle = self.distanceEuclidian(start, obstaclePoint)
        distanceTraveled = min(self.distance, distanceToObstacle)
        
        finalPoint = np.array([start.x + direction[0] * distanceTraveled, start.y + direction[1] * distanceTraveled])

        return finalPoint

    # check if the obstacle is in the path
    def isInObstacle(self, start, end):
        vectorBetween = self.unitVector(start, end)
        testPoint = np.array([0.0, 0.0])
        pointBeforeObstacle = np.array([start.x + 0*vectorBetween[0], start.y + 0*vectorBetween[1]])
        for i in range(self.distance+1):
            testPoint[0] = start.x + i*vectorBetween[0]
            testPoint[1] = start.y + i*vectorBetween[1]
            if self.grid[min(np.int64(round(testPoint[1])),self.grid.shape[0]-1),min(np.int64(round(testPoint[0])),self.grid.shape[1]-1)] == 1:
                return pointBeforeObstacle
            pointBeforeObstacle = np.array([testPoint[0], testPoint[1]])
        return end

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

def random_seed():
    random.seed()
    min = 1
    max = 11
    return random.randint(min, max)

# Load the grid, set start and goal <x, y> positions, number of iterations, step size
while True:
    print()
    print("Select a number between 1 and 11 to load a grid. ")
    print("Choose 0 for a random grid.")
    print("Enter your number: ")
    gridNumber = int(input())
    if gridNumber >= 1 and gridNumber <= 11:
        grid = np.load(f'test_images/test{gridNumber}.npy')
        break
    elif gridNumber == 0:
        gridNumber = random_seed()
        grid = np.load(f'test_images/test{gridNumber}.npy')
        break
    else:
        print("Please enter a valid number!")

def setup(start, goal, numIterations, stepSize):
    start = start
    goal = goal
    numIterations = numIterations
    stepSize = stepSize

    goalRegion = plt.Circle((goal[0], goal[1]), stepSize, color='b', fill=False)
    fig = plt.figure("RRT Algorithm")
    plt.imshow(grid, cmap='binary')
    plt.plot(start[0], start[1], 'ro')
    plt.plot(goal[0], goal[1], 'bo')
    ax = fig.gca()
    ax.add_patch(goalRegion)
    plt.xlabel('X-axis $(m)$')
    plt.ylabel('Y-axis $(m)$')

    return start, goal, numIterations, stepSize

if gridNumber == 1:
    start, goal, numIterations, stepSize = setup([120.0, 650.0], [1435.0, 410.0], 100, 200)
if gridNumber == 2:
    start, goal, numIterations, stepSize = setup([567.0, 475.0], [1511.0, 292.0], 2000, 40)
if gridNumber == 3:
    start, goal, numIterations, stepSize = setup([16.0, 8.0], [1592.0, 754.0], 200, 175)
if gridNumber == 4:
    start, goal, numIterations, stepSize = setup([1555.0, 62.0], [297.0, 516.0], 750, 130)
if gridNumber == 5:
    start, goal, numIterations, stepSize = setup([135.0, 108.0], [1418.0, 101.0], 500, 100)
if gridNumber == 6:
    start, goal, numIterations, stepSize = setup([614.0, 634.0], [1186.0, 89.0], 1000, 50)
if gridNumber == 7:
    start, goal, numIterations, stepSize = setup([74.0, 655.0], [1396.0, 122.0], 750, 75)
if gridNumber == 8:
    start, goal, numIterations, stepSize = setup([454.0, 66.0], [150.0, 724.0], 1500, 80)
if gridNumber == 9:
    start, goal, numIterations, stepSize = setup([1521.0, 708.0], [44.0, 682.0], 1000, 40)
if gridNumber == 10:
    start, goal, numIterations, stepSize = setup([602.0, 553.0], [711.0, 57.0], 3000, 120)
if gridNumber == 11:
    start, goal, numIterations, stepSize = setup([37.0, 98.0], [1551.0, 687.0], 9999, 50)

print()
# print(grid.shape)
rrt=RRT(start, goal, grid, numIterations, stepSize)

for i in range(rrt.iterations):
    rrt.resetNearestValues()
    print("Iteration: ",i)

    point=rrt.randomPoint(i)
    # If we want to see how the random point gets generated
    # temp_plot, = plt.plot(point[0], point[1], 'o', color='orange', linestyle="--")
    # plt.pause(2)
    # temp_plot.remove()
    rrt.findNearestNode(rrt.randomTree,point)
    newPoint=rrt.steerToPoint(rrt.nearestNode,point)

    rrt.addChild(newPoint[0],newPoint[1])
    plt.pause(0.10)
    # colors = ['g', 'b', 'm']
    # color_index = i % 3  # Determine the color based on the iteration
    plt.plot([rrt.nearestNode.x, newPoint[0]], [rrt.nearestNode.y, newPoint[1]], 'go', linestyle="--")

    if(rrt.goalFound(newPoint)):
        print("Goal found!")
        break

rrt.retraceRRTPath(rrt.goal)
rrt.waypoints.insert(0,start)
print("Number of waypoints: ", rrt.numWaypoints)
print("Path Distance: ", rrt.totalDistance)
#print("Waypoints: ",rrt.waypoints)

for i in range(len(rrt.waypoints)-1):
    plt.plot([rrt.waypoints[i][0],rrt.waypoints[i+1][0]],[rrt.waypoints[i][1],rrt.waypoints[i+1][1]],'ro',linestyle="--")
    plt.pause(0.10)

plt.show()



