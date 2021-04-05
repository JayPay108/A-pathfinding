import math

INFINITY = float('inf')
UNDEFINED = 0
UNVISITED = 1
OPEN = 2
CLOSED = 3


class Node:
    def __init__(self, nType, nodeNumber, status, costSoFar, estimatedHeuristic, estimatedTotal, previous, xLocation, yLocation, numPlotPos, namePlotPos, nodeLabel):
        self.nodeNumber = nodeNumber
        self.status = status
        self.costSoFar = costSoFar
        self.estimatedHeuristic = estimatedHeuristic
        self.estimatedTotal = estimatedTotal
        self.previous = previous
        self.xLocation = xLocation
        self.yLocation = yLocation

        # Not used by this program
        self.type = nType
        self.numPlotPos = numPlotPos
        self.namePlotPos = namePlotPos
        self.nodeLabel = nodeLabel

    # Calculating distance between two nodes using standard Euclidean distance formula
    def distanceFrom(self, node2):
        x1 = self.xLocation
        y1 = self.yLocation
        x2 = node2.xLocation
        y2 = node2.yLocation

        # Formula for calculating Euclidian Distance
        return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))


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

        self.nodes = [None]
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
            xLocation = float(row[7])
            yLocation = float(row[8])
            numPlotPos = int(row[9])
            namePlotPos = int(row[10])
            nodeLabel = row[11].replace('"', '').replace('\\n', '\n').strip()

            self.nodes.append(Node(nType, nodeNumber, status, costSoFar, estimatedHeuristic,
                            estimatedTotal, previous, xLocation, yLocation, numPlotPos, namePlotPos, nodeLabel))

        # Reading connections   
        connectionFile = open(connectionFileName, 'r')
        connectionFileRows = connectionFile.readlines()
        connectionFile.close()

        self.connections = [None]
        for row in connectionFileRows:
            if row[0] == '#':
                continue

            row = row.split(',')

            cType = row[0].replace('"', '').strip()
            connectionNumber = int(row[1])
            fromNode = int(row[2])
            toNode = int(row[3])
            cost = float(row[4])
            costPlotPosition = int(row[5])
            roadType = int(row[6])

            self.connections.append(Connection(cType, connectionNumber, fromNode, toNode, cost, costPlotPosition, roadType))

    def getConnections(self, currentNode):
        nodeConnections = []

        for connection in self.connections:
            if connection.fromNode == currentNode:
                nodeConnections.append(connection.connectionNumber)

        return nodeConnections

    def aStarFindLowest(self, openNodes):
        lowestTotal = INFINITY

        for nodeIndex in openNodes:
            node = self.nodes[nodeIndex]

            if node.estimatedTotal < lowestTotal:
                lowestTotal = node.estimatedTotal
                resultNodeIndex = nodeIndex

        return resultNodeIndex


    def aStarFindPath(self, first, last):
        first -= 1
        last -= 1

        for i in range(len(self.nodes)):
            self.nodes[i].status = UNVISITED
            self.nodes[i].costSoFar = INFINITY
            self.nodes[i].previous = UNDEFINED

        self.nodes[first].status = OPEN
        self.nodes[first].costSoFar = 0
        openNodes = [first]

        iteration = 0
        while len(openNodes) > 0:
            iteration += 1

            currentNodeIndex = self.aStarFindLowest(openNodes)

            if currentNodeIndex == last:
                pass #break

            currentConnections = self.getConnections(currentNodeIndex + 1)

            for connectionNumber in currentConnections:
                connection = self.connections[connectionNumber - 1]

                toNodeIndex = connection.toNode - 1
                toCost = self.nodes[currentNodeIndex].costSoFar + connection.cost

                if toCost < self.nodes[toNodeIndex].costSoFar:
                    self.nodes[toNodeIndex].status = OPEN
                    self.nodes[toNodeIndex].costSoFar = toCost
                    self.nodes[toNodeIndex].estimatedHeuristic = self.nodes[toNodeIndex].distanceFrom(self.nodes[last])
                    self.nodes[toNodeIndex].estimatedTotal = self.nodes[toNodeIndex].costSoFar + self.nodes[toNodeIndex].estimatedHeuristic
                    self.nodes[toNodeIndex].previous = currentNodeIndex
                    print(toNodeIndex + 1, self.nodes[toNodeIndex].previous + 1) # debug
                    
                    if toNodeIndex not in openNodes:
                        openNodes.append(toNodeIndex)
            
            self.nodes[currentNodeIndex].status = CLOSED
            openNodes.remove(currentNodeIndex)

    def retrievePath(self, first, last):
        first -= 1
        last -= 1

        path = []
        current = last

        while (current != first) and (current != UNDEFINED):
            path.append(current)
            current = self.nodes[current].previous

        if current == first:
            path.append(first)
            # Path found!

        else:
            path = []
            print('path not found') # debug
            # Path could not be found

        return path

graph = Graph("Nodes.txt", "Connections.txt") # TODO: Change these file names!
startNodeNumber = 10
endNodeNumber = 35
graph.aStarFindPath(startNodeNumber, endNodeNumber)
path = graph.retrievePath(startNodeNumber, endNodeNumber)

print('\n\n\n PATH \n------')
for i in path[::-1]:    
    print(i + 1)


print('-----')
connections = graph.getConnections(3)
print(connections)




