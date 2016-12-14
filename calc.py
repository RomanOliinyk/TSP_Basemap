# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from xlrd import open_workbook, cellname
import os

# Creating Node class to fill them with data from
class Node():
    def __init__(self, ID, name, lng, lat, distance):
        self.id = ID
        self.name = str(name)
        self.lng = lng
        self.lat = lat
        self.distance = distance
        self.taken = None
        self.cluster = None

    def __str__( self ):
        output = str( self.id )
        return output

    def __repr__(self):
        return str(self)


# Length between two Nodes
# node == currentNode; element2 == ID of Node 2
def length(node, element2):
	return node.distance[element2]

# Total distance
def totalDistance(nodes, solution):
    objective = length(solution[-1], solution[0].id)
    for index in range(0, len(solution)-1):
        objective += length(solution[index], solution[index+1].id)
    #print ('TOTAL DISTANCE: {}'.format(objective))
    return (objective/1000) # return in kilometers

# Function to open Excel sheet and create Nodes to work with
def readingExcelSheet(filename):
    nodes = []

    book = open_workbook(filename)
    sheet = book.sheet_by_index(0)

    for row in range(sheet.nrows):
        name = sheet.row_values(row)[0]
        lng = sheet.row_values(row)[1]
        lat = sheet.row_values(row)[2]
        distance = sheet.row_values(row)[3:]
        nodes.append(Node(row, name, lng, lat, distance))
    return nodes

# Drawing map with matplotlib basemap module
def drawingMap(nodes, filename):
    # creatin mapBase to work with only for Europe zone
    mapBase = Basemap(projection = 'gall', resolution = 'h', llcrnrlat = 32,
        urcrnrlat = 64, llcrnrlon = -20, urcrnrlon = 40)
    # drawing countries
    mapBase.drawcountries(linewidth = 1, linestyle = 'solid', color = 'k',
        antialiased = 1, ax = None, zorder = None)
    # giving it a nice look using NASA's satalite images
    mapBase.bluemarble()

    # lists of longitudes and latitudes
    lons = []
    lats = []
    lngLine = []
    latLine = []

    # plot destinations using coordinates from Nodes
    for item in nodes:
        lons.append(item.lng)
        lats.append(item.lat)

    x,y = mapBase(lons, lats)
    #print (lons)
    #print (lngLine)
    #print (lats)
    #print (latLine)
    mapBase.plot(x, y, 'bo', markersize = 18)

    # Connecting coordinates with lines
    mapBase.plot(x, y, color='r', linewidth=3)

    # Finishing the circle
    lngLine.append(nodes[-1].lng)
    lngLine.append(nodes[0].lng)
    latLine.append(nodes[-1].lat)
    latLine.append(nodes[0].lat)
    x,y = mapBase(lngLine, latLine)
    mapBase.plot(x, y, color='r', linewidth = 3)

    # shows the map if needed before saving
    #plt.show()

    # saving to png file
    plt.savefig(filename)

    # reseting plot
    plt.clf()

# Solving TSP Algorithms
# Greedy Algorithm-------------------------------------------------------------
def greedyAlgorithm(nodes):
    print ('Creating Greedy Solution')

    freeNodes = nodes[:]
    solution = []
    comparedNode = freeNodes[0]
    freeNodes.remove(comparedNode)
    solution.append(comparedNode)
    while len(freeNodes) > 0:
        print(len(freeNodes))
        min_l = None
        min_n = None
        for currentNode in freeNodes:
            l = length(currentNode, int(comparedNode.id))
            if min_l is None:
                min_l = l
                min_n = currentNode
            elif l < min_l:
                min_l = l
                min_n = currentNode
        solution.append(min_n)
        freeNodes.remove(min_n)
        n = min_n

    print ('Total distance: ' + str(totalDistance(nodes, solution)))
    print ('Greedy solution: ' + str(solution))
    return solution
#------------------------------------------------------------------------------
#2-opt optimization algorigthm-------------------------------------------------
#
#    Before 2opt             After 2opt
#       Y   Z                    Y   Z
#       O   O----->              O-->O---->
#      / \  ^                     \
#     /   \ |                      \
#    /     \|                       \
# ->O       O              ->O------>O
#   C       X                C       X
#
# In a 2opt optimization step we consider two nodes, Y and X.  (Between Y
# and X there might be many more nodes, but they don't matter.) We also
# consider the node C following Y and the node Z following X. i
#
# For the optimization we see replacing the edges CY and XZ with the edges CX
# and YZ reduces the length of the path  C -> Z.  For this we only need to
# look at |CY|, |XZ|, |CX| and |YZ|.   |YX| is the same in both
# configurations.
#
# If there is a length reduction we swap the edges AND reverse the direction
# of the edges between Y and X.
#
# In the following function we compute the amount of reduction in length
# (gain) for all combinations of nodes (X,Y) and do the swap for the
# combination that gave the best gain.

# we take greedyAlgorithm solution to 2-opt optimize
def optimize2optAlgorithm(nodes, solution, numberOfNodes):
    best = 0
    bestMove = None
    for ci in range(0, numberOfNodes):
        for xi in range(0, numberOfNodes):
            yi = (ci + 1) % numberOfNodes # C is the node before Y
            zi = (xi + 1) % numberOfNodes # Z is the node after X

            c = solution[ ci ]
            y = solution[ yi ]
            x = solution[ xi ]
            z = solution[ zi ]
            # Getting the distance between nodes
            cy = length(c, y.id)
            xz = length(x, z.id)
            cx = length(c, x.id)
            yz = length(y, z.id)

            # Only makes sence if all nodes are distinct
            if xi != ci and xi != yi and ci != zi:
                # What will be the reduction in length
                gain = (cy + xz) - (cx + yz)
                # Check if it is the best so far
                if gain > best:
                    bestMove = (ci,yi,xi,zi)
                    best = gain

    print ('Best move: {}, Best gain: {}'.format(bestMove, best))
    if bestMove is not None:
        (ci,yi,xi,zi) = bestMove

        # Creating an empty solution
        newSolution = list(range(0, numberOfNodes))
        # In the new solution C is the first node.
        # this we only need two copy loops instead of three
        newSolution[0] = solution[ci]

        n = 1
        # Copy all nodes between X and Y including X and Y
        # in revers direction to the new solution
        while xi != yi:
            newSolution[n] = solution[xi]
            n += 1
            xi = (xi-1)%numberOfNodes
        newSolution[n] = solution[yi]

        n += 1
        # Copy al lthe nodes between Z and C in normal direction
        while zi != ci:
            newSolution[n] = solution[zi]
            n += 1
            zi = (zi+1)%numberOfNodes
        return (True, newSolution)
    else:
        return(False, solution)

def twoOptAlgorithm(nodes, numberOfNodes):
    # Artificial solution to work around with
    solution = [n for n in nodes]
    go = True
    # Optimizing the solution with 2-opt algorithm untill no further
    # optimization is possible
    while go:
        (go, solution) = optimize2optAlgorithm(nodes, solution, numberOfNodes)
    totalDistance2Opt = totalDistance(nodes, solution)
    print ('2-opt Optimization Solution ' + str(solution))
    print ('2-opt Optimization Total Distance: {}'.format(totalDistance2Opt))
    return solution
#------------------------------------------------------------------------------

# changing dir to 'Results' to read excel table
os.chdir('Results')

nodes = readingExcelSheet('queryTable.xls')
greedySolution = greedyAlgorithm(nodes)

twoOpt = twoOptAlgorithm(nodes)

drawingMap(greedySolution, 'greedySolution.png')
drawingMap(twoOpt, 'twoOptSolution.png')
