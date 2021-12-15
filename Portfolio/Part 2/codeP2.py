# from skopt import gp_minimize
# from sko.GA import GA

from math import sqrt
from typing import Dict
import matplotlib.pyplot as plt

# Importing supporting classes for storing data
from costumer import Costumer
from vehicle import Vehicle
from depot import Depot

import sys, random, copy
import traceback, logging   # Error catching

depots = []

costumers = []
costumersDistribute = []
costumersSwappable = []

totalVehicles = 0

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
xMax = 0
xMin = 0
yMax = 0
yMin = 0

borderLineThreshold = 0.5

# Crossover setting
crossoverRate = 0.8
crossoverChangeCostumers = 2

# Dist to store the lowest distance and its generation (generation: distance)
shortestDistance = dict()

parensToKeep = 20

showProgress = True

iterations = (1, 1000)

def updateMinMax(x, y):
    global xMax, xMin, yMax, yMin
    x = int(x)
    y = int(y)

    xMax = x if x > xMax else xMax
    xMin = x if x < xMin else xMin
    yMax = y if y > yMax else yMax
    yMin = y if y < yMin else yMin

def parseFile(fileName):
    global totalVehicles

    with open(f'DataFiles/{fileName}.txt') as file:

        # Parse first line
        m, n, t = file.readline().split()

        totalVehicles = int(m) * int(t)

        # Set up depots
        for i in range(int(t)):
            D, Q = file.readline().split()
            depots.append(Depot(i, m, n, D, Q))

        # Set up costumers        
        for _ in range(int(n)):
            line = file.readline().split()
            x = line[1]
            y = line[2]

            updateMinMax(x, y)

            costumers.append(Costumer(line[0], x, y, line[3], line[4]))
            costumersDistribute.append(Costumer(line[0], x, y, line[3], line[4]))

        for depot in depots:
            line = file.readline().split()
            x = line[1]
            y = line[2]

            updateMinMax(x, y)

            depot.setPos(x, y)

    file.close()

def readSolutionFile(fileName):
    fileName = fileName if fileName > 10 else f'0{fileName}'
    with open(f'SolutionFiles/p{fileName}.txt') as file:
        return file.readline().removesuffix('\n')

# 
# Utils
# 
def calcDistance(ax, ay, bx, by):
    xDistance = abs(ax - bx)
    yDistance = abs(ay - by)

    return sqrt((xDistance**2) + (yDistance**2))

def getDepotFromID(depotID: int) -> Depot:
    global depots

    for depot in depots:
        if depot.i == depotID:
            return depot

    return None

#
# GA algorithm
#
def GA():
    global costumersDistribute, depots, shortestDistance, iterations

    # NOTE: Can change edge costumers to another depot randomly?

    initialLengths = []

    # 2. Random distribution
    distrobuteCostumersToDepot(costumersDistribute, depots)
    for depot in depots:
        depot.distrubuteVehiclesRandom()
        depot.setBestVehiclesRoutes(depot.vehicles)
        initialLengths.append((copy.deepcopy(depot.getTotalDistance())))

    # print(initialLengths)
    # print(depots)

    # 3. Evaluate the fitness
    ## Sort the shortest distance first, unless it is 0 then last
    ## Because that vehicle is not contributing to the total delivering
    bestVehicle, totalDistance = evaluateFitness(depots)
    shortestDistance[0] = totalDistance

    # for vehicle in allVehicles:
        # print(f'D={vehicle.depot.i} V={vehicle.id}: Distance={vehicle.getDistance()}')

    # 4. while not termination condition
    for t in range(iterations[0], iterations[1]):
        # 5. Select parents
        ## Work on each depot, because using adding parents to another depot is longer.
        ## TODO: select parents from a depot and only work with costumers in that depot. Can try to change the edge costumers to the other depot for possible better result
        for depot in depots:
            # p = Process(target=doGA, args=(t, depot))
            # proc.append(p)
            doGA(t, depot)

            if showProgress:
                progress = (t-iterations[0])/((iterations[1]-1)-iterations[0]) * 100
                sys.stdout.write(f'\rProgress: {round(progress,1)}%')
                sys.stdout.flush()

    if showProgress:
        print()

        # for p in proc:
        #     p.start()

        # for p in proc:
        #     p.join()

        # print('------')
        # parents = []
        # for _ in range(totalVehicles):
        #     parents.append(selectParents(bestVehicle))

        # 6. Apply crossover
        # offspring = applyCrossover(parents)

        # 7. Apply mutation
        # offspring = applyMutation(offspring)

        # allVehicles = evaluateFitness(offspring)

    # for i in range(len(initialLengths)):
    #     print(initialLengths[i])
    #     print(depots[i].bestVehiclesDistance)
    #     print()

def doGA(t: int, depot: Depot):
    # print('Fitness | ', end='')
    bestDepotVehicle, totalDepotDistance = evaluateDepotFitness(depot.vehicles)
    # print(f'{t:2}: {depot.i:2} - {totalDepotDistance}')

    parents = []

    # print('Parents | ', end='')
    for _ in range(int((len(depot.vehicles) - (len(depot.vehicles) % 2)) / 2)):
        p = selectParents(bestDepotVehicle)
        parents.append(p)
        bestDepotVehicle.remove(p[0])
        bestDepotVehicle.remove(p[1])

    # offspring = applyCrossover(parents)
    # print('Crossover | ', end='')
    applyCrossover2(parents)

    # Apply mutation

    # print(depot.getTotalDistance())
    # Set best solution
    if depot.bestVehiclesDistance > depot.getTotalDistance():
        depot.setBestVehiclesRoutes(depot.vehicles)

def distrubeCostumersRandomly(costumers: list[Costumer], depots: list[Depot]) -> bool:
    random.shuffle(costumers)

    # Store all vehicles in one list
    vehicles = []
    for i in range(depots[0].m):
        for depot in depots:
            vehicles.append(depot.vehicles[i])

    for vehicle in vehicles:
        if not len(costumers) == 0:
            vehicle.fill(costumers)
        else:
            break

    if len(costumers) > 0:
        raise Exception(f'Not all costumers are given a route! {len(costumers)} left')

    # for depot in depots:
    #     print(depot)

def distrobuteCostumersToDepot(costumers: list[Costumer], depots:list[Depot]) -> bool:
    """
    Calclate the closes depot to a costumer and add that costumer to that depot
    """
    for costumer in costumers:
        isBorderCostumer = False
        depotsDistance = dict()

        shortestDistance = sys.maxsize
        shortestDepot = depots[0]

        for depot in depots:
            distance = calcDistance(costumer.x, costumer.y, depot.x, depot.y)
            depotsDistance[depot.i] = distance
            if distance < shortestDistance:
                shortestDistance = distance
                shortestDepot = depot

        shortestDepot.addCostumer(costumer)
        costumer.addPossibleDepots(getDepotFromID(shortestDepot.i))

        for key, val in depotsDistance.items():
            if (val - shortestDistance) / shortestDistance < borderLineThreshold and key != shortestDepot.i:
                costumer.addPossibleDepots(getDepotFromID(key))
                costumer.isBorderCostumer = True
                isBorderCostumer = True

        if isBorderCostumer:
            costumersSwappable.append(costumer)

def evaluateFitness(depots: list[Depot]) -> list[Vehicle] and int:
    allVehicles = []
    totalDistance = 0
    
    for depot in depots:
        for vehicle in depot.vehicles:
            allVehicles.append(vehicle)
            totalDistance += vehicle.getDistance()

    return sorted(allVehicles, key=lambda v: v.getDistance() if v.getDistance() != 0 else sys.maxsize), totalDistance

def evaluateDepotFitness(vehicles: list[Vehicle]) -> list[Vehicle]:
    totalDistance = 0
    for vehicle in vehicles:
        totalDistance += vehicle.getDistance()

    return sorted(vehicles, key=lambda v: v.getDistance() if v.getDistance() != 0 else sys.maxsize), totalDistance

# Select parents functions
def selectParents(routes: list[Vehicle]) -> tuple[Vehicle, Vehicle]:
    """
    Selecting parens using a form of turnament
    """
    routesIsEven = len(routes) % 2 == 0
    routeLen = len(routes)

    compIndex = [i for i in range(len(routes))]
    random.shuffle(compIndex)

    if routeLen == 2 or routeLen == 3:
        # Just return the 2 routes as parents. We cant do much with them
        return (routes[compIndex[0]], routes[compIndex[1]])
    elif routeLen >= 4:
        winner1, looser1 = runTurnament(routes[compIndex[0]], routes[compIndex[1]], 0.8)
        winner2, looser2 = runTurnament(routes[compIndex[2]], routes[compIndex[3]], 0.8)
        return (winner1, winner2)

    # parent1 = runTurnament(routes[0], routes[1], 0.8)
    # parent2 = runTurnament(routes[2], routes[3], 0.8)

    # return (parent1, parent2)

def runTurnament(parent1: Vehicle, parent2: Vehicle, bias: int) -> Vehicle and Vehicle:
    """
    Run a turnament where parent 1 and parent 2 is compeating.
        Return:
        Winner, looser
    """
    if random.uniform(0, 1) < bias:
        if parent2.getDistance() < parent1.getDistance():
            return parent2, parent1
    else:
        if random.uniform(0, 1) < 0.5:
             return parent2, parent1
    return parent1, parent2

# Crossover functions
def applyCrossover(parents: list[tuple[Vehicle, Vehicle]]) -> list[Vehicle]:
    """
    Applying crossover using Gant Tour Best Cost Crossover (GTBCX)
    """
    global crossoverRate, crossoverChangeCostumers
    
    retList = []
    print(parents)

    for parent1, parent2 in parents:
        # Random if not to run crossover
        if random.uniform(0, 1) > crossoverRate:
            retList.append((parent1, parent2))

        print()

        # Try to select costumers to crossover for some iterations, if noting works then, just leave them...
        for _ in range(5):
            # Select 2 costumers if available
            p1ChangeCostumers, p1ChangeCostumersIndex = selectRandomCostumer(parent1)
            p2ChangeCostumers, p2ChangeCostumersIndex = selectRandomCostumer(parent2)

            if canAddCostumersToRoute(p1ChangeCostumers, parent2) and canAddCostumersToRoute(p2ChangeCostumers, parent1):
                # Both parent have the space to take in the costumers, so the crossover can work
                # NOTE: sometimes the costumer can't be added
                print('Can add Costumer')
                print('P2:')
                print(parent2)
                for costumer in p1ChangeCostumers:
                    status = parent2.addCostumerOptimal(costumer)

                    if not status:
                        print('error adding costumer')
                print(parent2)

                print('P1:')
                print(parent1)
                for costumer in p2ChangeCostumers:
                    status = parent1.addCostumerOptimal(costumer)

                    if not status:
                        print('error adding costumer')
                print(parent1)
                retList.append((parent1, parent2))
                break
            else:
                # Add back costumers
                for i in range(len(p1ChangeCostumers)):
                    parent1.addCostumerIndex(p1ChangeCostumers[i], p1ChangeCostumersIndex[i])
                
                for i in range(len(p2ChangeCostumers)):
                    parent2.addCostumerIndex(p2ChangeCostumers[i], p2ChangeCostumersIndex[i])
        else:
            # Failed to apply crossover to the parents, so just return them in the same state
            print('Failed to add costumer')
            retList.append((parent1, parent2))

    return retList

def applyCrossover2(parents: list[tuple[Vehicle, Vehicle]]) -> None:
    """
    # Apply crossover directly to the parents. Using a deepcopy of the parents for calculations, then apply directly to parents if things works
    """
    global crossoverRate, crossoverChangeCostumers

    # workingParents = copy.deepcopy(parents)
    # print(parents)
    # print(workingParents)
    # print()

    for p1, p2 in parents:
        
        if random.uniform(0, 1) > crossoverRate:
            # Random chance of not doing anything to the parents, so do nothing
            continue

        for _ in range(5):
            # print('P1:', p1.route)
            # print('P2:', p2.route)

            p1CC, p1CCI = selectRandomCostumer(p1)
            p2CC, p2CCI = selectRandomCostumer(p2)

            canAdd1 = canAddCostumersToRoute(p1CC, p2)
            canAdd2 = canAddCostumersToRoute(p2CC, p1)

            if canAdd1 and canAdd2:
                for c in p1CC:
                    status = p2.addCostumerOptimal(c)
                    # print('Adding', c.i, 'to', p2.id)
                    # print(status)
                
                for c in p2CC:
                    status = p1.addCostumerOptimal(c)
                #     print('Adding', c.i, 'to', p1.id)
                #     print(status)

                # print('P1:', p1.route)
                # print(p1CC)
                # print('P2:', p2.route)
                # print(p2CC)

            else:
                for i in range(len(p1CC)):
                    p1.addCostumerIndex(p1CC[i], p1CCI[i])

                for i in range(len(p2CC)):
                    p2.addCostumerIndex(p2CC[i], p2CCI[i])

                # print('P1:', p1.route)
                # print('P2:', p2.route)   



            # print()

        # print()



def canAddCostumersToRoute(costumersToAdd: list[Costumer], vehicle: Vehicle) -> bool:
    costumersWeight = 0

    for costumer in costumersToAdd:
        costumersWeight += costumer.load

    return costumersWeight < (int(vehicle.maxLoad) - int(vehicle.currentLoad))
    
def selectRandomCostumer(parent: Vehicle) -> list[Vehicle] and list[int]:
    """
    Select random costumers to be used in crossover.

    Return a list of costumers and the index they was removed from.
        To be able to add them back if the crossover don't work for the costumers 

    TODO: Decide what happend when a vehicle only have 1 costumer in its route
    """
    global crossoverChangeCostumers

    selectedCostumers = []
    selectedCostumersIndex = []

    if len(parent.route) > crossoverChangeCostumers:
        for _ in range(crossoverChangeCostumers):
            # Select random costumer
            i = random.randrange(0, len(parent.route))
            costumer = parent.route[i]

            selectedCostumers.append(costumer)
            selectedCostumersIndex.append(i)
            parent.removeCostumer(costumer)

    elif len(parent.route) != 0:
        for _ in range(random.randrange(len(parent.route))):
            # Select random costumer
            i = random.randrange(0, len(parent.route))
            costumer = parent.route[i]

            selectedCostumers.append(costumer)
            selectedCostumersIndex.append(i)
            parent.removeCostumer(costumer)

    return selectedCostumers, selectedCostumersIndex


# Mutation functions
def applyMutation(offspring: list[Vehicle]) -> list[Vehicle]:
    pass


#
# Print solution
#
def calcSolution():
    totalCost = 0
    bestRoutes = []
    for depot in depots:
        totalCost += depot.getTotalDistance()
        
        for vehicle in depot.bestVehicles:
            bestRoutes.append([depot.i + 1, vehicle.id + 1, round(vehicle.getDistance(), 2), vehicle.getLoad(), vehicle.getFullRouteID()])

    return totalCost, bestRoutes

def checkWithSolution():
    """
    Run true all files and calculate for each. Then print the calculated cost with the solution cost
    """
    for i in range(1, 23):
        try:
            cost = testThing(i)
            solutionCost = readSolutionFile(i)
            print(f'Cost = {round(cost, 2)} | Solution = {solutionCost}')
        except Exception as e:
            # logging.error(traceback.format_exc())
            print(f'Error with file: {i}')

# 
# Test things
#
def testThing(fileNum):
    global depots, costumers, costumersDistribute, fig, ax, xMax, xMin, yMax, yMin, borderLineThreshold
    depots = []

    costumers = []
    costumersDistribute = []

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    xMax = 0
    xMin = 0
    yMax = 0
    yMin = 0

    borderLineThreshold = 0.5

    num = fileNum if fileNum > 10 else f'0{fileNum}'

    parseFile(f'p{num}')

    padding = 5
    ax.set_xlim(xMin - padding, xMax + padding)
    ax.set_ylim(yMin - padding, yMax + padding)

    # Run the GA algorithm
    GA()

    totalCost, bestRoutes = calcSolution()

    return totalCost
    # for depot in depots:
    #     # print(depot)
    #     depot.addToPlot(ax)

    # plt.show()

def testForErrors():
    errorIndex = dict()

    for i in range(1, 23):
        for l in range(5):
            try:
                testThing(i)
            except:
                if not i in errorIndex:
                    errorIndex[i] = 1
                else:
                    errorIndex[i] += 1

    if len(errorIndex) > 0:
        print(f'Errors on the index: ')
        for key, val in errorIndex.items():
            print(f'  {key:2}: {val}')

if __name__ == '__main__':
    # testThing(1)
    # testForErrors()


    checkWithSolution()
    """
    parseFile(f'p03')

    padding = 5
    ax.set_xlim(xMin - padding, xMax + padding)
    ax.set_ylim(yMin - padding, yMax + padding)

    # Run the GA algorithm
    GA()

    totalCost, bestRoutes = calcSolution()
    print(totalCost)

    for route in bestRoutes:
        print(route)

    for depot in depots:
        # print(depot)
        # depot.addToPlot(ax)
        depot.addBestToPlot(ax)

    # plt.show()

    """

"""
FIX: Not able to distrobute costumers correctly: [4, 6, 7, 10, 11]
TODO: Refactor x,y to vec2? call it coord
"""