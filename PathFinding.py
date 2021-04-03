import math

# Simple vector class, this is missing alot of methods a normal vector
# object should have but it has what is needed for this assignment
class Vector:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y  # Z in this sense

    def normalize(self):    # Normalize to unit vector
        magnitude = self.length()
        self.x /= magnitude
        self.y /= magnitude

    def length(self):   # Returns the vector's magnitude
        return math.sqrt(math.pow(self[0], 2) + math.pow(self[1], 2))

    def dot(self, vector2): # Will preform dot product on a second vector
        return (self.x * vector2.x) + (self.y * vector2.y)

    # Operator overloading
    def __add__(self, vector2):
        return Vector(self[0] + vector2[0], self[1] + vector2[1])

    def __sub__(self, vector2):
        return Vector(self[0] - vector2[0], self[1] - vector2[1])

    def __mul__(self, scalar):
        return Vector(self[0] * scalar, self[1] * scalar)

    def __truediv__(self, scalar):
        return Vector(self[0] / scalar, self[1] / scalar)

    def __getitem__(self, key): # Bracket overloading
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        return None

class Node:
    def __init__(self, nType, nodeNumber, status, costSoFar, estimatedHeuristic, estimatedTotal, previous, location, numPlotPos, namePlotPos, nodeLabel):
        self.nodeNumber = nodeNumber
        self.status = status
        self.costSoFar = costSoFar
        self.estimatedHeuristic = estimatedHeuristic
        self.estimatedTotal = estimatedTotal
        self.previous = previous
        self.location = location

        # Not used by this program
        self.type = nType
        self.numPlotPos = numPlotPos
        self.namePlotPos = namePlotPos
        self.nodeLabel = nodeLabel

    # Calculating distance between two nodes using standard Euclidean distance formula
    def distanceFrom(self, node2):
        return math.sqrt(math.pow(node2.location.x - self.location.x, 2) + math.pow(node2.location.y - self.location.y, 2))


class Connection:
    def __init__(self, cType, connectionNumber, fromNode, toNode, cost, costPlotPosition, roadType):
        self.connectionNumber = connectionNumber
        self.fromNode = fromNode
        self.toNode = toNode
        self.cost = cost

        # Not used by this program
        self.cType = cType
        self.costPlotPosition = costPlotPosition
        self.roadType = roadType

class Graph:
    # Will build graph data structure from given files
    def __init__(self, nodeFileName, connectionFileName):
        nodeFile = open(nodeFileName, 'r')
        nodeFileRows = nodeFile.readlines()
        nodeFile.close()

        self.nodes = []
        for row in nodeFileRows:
            if row[0] == '#':
                continue

            row = row.split(',')

            nType = row[0].replace('"', '').strip()
            nodeNumber = int(row[1])
            status = int(row[2])
            costSoFar = float(row[3])
            estimatedHeuristic = float(row[4])
            estimatedTotal = float(row[5])
            previous = float(row[6])
            location = Vector(float(row[7]), float(row[8]))
            numPlotPos = int(row[9])
            namePlotPos = int(row[10])
            nodeLabel = row[11].replace('"', '').replace('\\n', '\n').strip()

            self.nodes.append(Node(nType, nodeNumber, status, costSoFar, estimatedHeuristic,
                            estimatedTotal, previous, location, numPlotPos, namePlotPos, nodeLabel))

        # Reading connections   
        connectionFile = open(connectionFileName, 'r')
        connectionFileRows = connectionFile.readlines()
        connectionFile.close()

        self.connections = []
        for row in connectionFileRows:
            if row[0] == '#':
                continue

            row = row.split(',')

            cType = row[0].replace('"').strip()
            connectionNumber = int(row[1])
            fromNode = int(row[2])
            toNode = int(row[3])
            cost = float(row[4])
            costPlotPosition = int(row[5])
            roadType = int(row[6])

            self.connections.append(Connection(cType, connectionNumber, fromNode, toNode, cost, costPlotPosition, roadType))
