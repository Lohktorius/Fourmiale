import pants
import math
import csv
import time
from datetime import timedelta
import networkx as nx
import matplotlib.pyplot as plt

### Variables
nodesArray = []
numberOfPubsToLookAt = int(20)

### Graph initialisation
G = nx.Graph()
plt.style.use('ggplot')

### Functions definition

def nodesArrayFillUp ( easting, northing ):
    easting = float(easting)
    northing = float(northing)
    nodesArray.append((easting, northing))

# Fitness function chosen : cartesian distance
def distance (x,y):
        # entre deux points a et b : racine carré de ((xa - ya) au carré + (xb- yb) au carré)
    return math.sqrt(pow(x[1]-y[1],2) + pow(x[0]-y[0],2))

def runACO(nodes, numberOfPubsToLookAt):
    world = pants.World(nodes, distance)

    solver_setting_report_format = "\n".join([
        "Solver settings:",
        "limit={w.limit}",
        "rho={w.rho}, Q={w.q}",
        "alpha={w.alpha}, beta={w.beta}",
        "elite={w.elite}"
        ])

    print(solver_setting_report_format.format(w=solver))
    
    columns = "{!s:<25}\t{:<25}"
    divider = "-" * (25 + 25)
    header = columns.format("Time Elapsed", "Distance")
    columns = columns.replace('<', '>', 1)
    
    print()
    print(header)
    print(divider)
    
    fastest = None
    start_time = time.time()
    for i, ant in enumerate(solver.solutions(world)):
        fastest = ant
        fastest_time = timedelta(seconds=(time.time() - start_time))
        print(columns.format(fastest_time, ant.distance))
    total_time = timedelta(seconds=(time.time() - start_time))
    
    print(divider)
    print("Best solution:")
    for i, n in zip(fastest.visited, fastest.tour):
        print("  {:>8} = {}".format(i, n))
    
    print("Solution length: {}".format(fastest.distance))
    print('Shortest way between the first ' + str(numberOfPubsToLookAt) + ' English Pubs (easting/northings) :')
    print(fastest.distance)
    print("Found at {} out of {} seconds.".format(fastest_time, total_time))

### Datas Retrieval from the csv file
with open('open_pubs.csv') as csvfile:
    file = csv.DictReader(csvfile)
    for row in file:
        nodesArrayFillUp(row['easting'], row['northing'])

# Limit of the dataset for testing and to respect memory limit
nodesArray = nodesArray[0:numberOfPubsToLookAt]
G.add_nodes_from(nodesArray)

### Solver and World Instanciation
world = pants.World(nodesArray, distance)
solver = pants.Solver()

### Solution definition
solution = solver.solve(world)


##### Solution #####
runACO(nodesArray, numberOfPubsToLookAt)

###  Display Graph
nx.draw_networkx(G)
plt.show()