# from skopt import gp_minimize
# from sko.GA import GA

from math import sqrt
from typing import Dict
import matplotlib.pyplot as plt
from matplotlib import cm

import numpy as np
import pandas as pd

# Importing supporting classes for storing data
from costumer import Costumer
from vehicle import Vehicle
from depot import Depot

import sys
import random

depots = []

costumers = []
costumersDistribute = []
costumersSwappable = []

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
xMax = 0
xMin = 0
yMax = 0
yMin = 0

borderLineThreshold = 0.5

shortestDistance = []

def updateMinMax(x, y):
    global xMax, xMin, yMax, yMin
    x = int(x)
    y = int(y)

    xMax = x if x > xMax else xMax
    xMin = x if x < xMin else xMin
    yMax = y if y > yMax else yMax
    yMin = y if y < yMin else yMin

def parseFile(fileName):
    with open(f'DataFiles/{fileName}.txt') as file:

        # Parse first line
        m, n, t = file.readline().split()

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

# 
# Utils
# 
def calcDistance(ax, ay, bx, by):
    xDistance = abs(ax - bx)
    yDistance = abs(ay - by)

    return sqrt((xDistance**2) + (yDistance**2))

#
# GA algorithm
#
def GA():
    global costumersDistribute, depots

    # 2. Random distribution
    distrobuteCostumersToDepot(costumersDistribute, depots)
    for depot in depots:
        depot.distrubuteVehiclesRandom()

    # 3. Evaluate the fitness
    ## Sort the shortest distance first, unless it is 0 then last
    allVehicles, totalDistance = evaluateFitness(depots)
    print(totalDistance)

    # for vehicle in allVehicles:
    #     print(f'D={vehicle.depot.i} V={vehicle.id}: Distance={vehicle.getDistance()}')

    # 4. while not termination condition
    # t = 1
    # while (1 < 20):
    #     # 5. Select parents
    #     # parents = selectParents(allVehicles)

    #     # 6. Apply crossover
    #     # offspring = applyCrossover(parents)

    #     # 7. Apply mutation
    #     # offspring = applyMutation(offspring)

    #     # allVehicles = evaluateFitness(offspring)
    #     pass
    # pass    

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
        costumer.addPossibleDepots(shortestDepot.i)

        for key, val in depotsDistance.items():
            if (val - shortestDistance) / shortestDistance < borderLineThreshold and key != shortestDepot.i:
                costumer.addPossibleDepots(key)
                costumer.isBorderCostumer = True
                isBorderCostumer = True

        if isBorderCostumer:
            costumersSwappable.append(costumer)

def evaluateFitness(depots: list[Depot]) -> list[Vehicle]:
    allVehicles = []
    totalDistance = 0
    
    for depot in depots:
        for vehicle in depot.vehicles:
            allVehicles.append(vehicle)
            totalDistance += vehicle.getDistance()

    return sorted(allVehicles, key=lambda x: x.getDistance()), totalDistance

def selectParents(routes: list[Vehicle]) -> list[Vehicle]:
    pass

def applyCrossover(parents: list[Vehicle]) -> list[Vehicle]:
    pass

def applyMutation(offspring: list[Vehicle]) -> list[Vehicle]:
    pass

# 
# Test things
#
def testThing(fileNum):
    global depots, costumers, costumersDistribute, fig, ax, xMax, xMin, yMax, yMin, borderLineThreshold
    depots = []

    costumers = []
    costumersDistribute = []
    costumersSwappable = []

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    xMax = 0
    xMin = 0
    yMax = 0
    yMin = 0

    borderLineThreshold = 0.5

    shortestDistance = [] 

    num = fileNum if fileNum > 10 else f'0{fileNum}'

    parseFile(f'p{num}')

    padding = 5
    ax.set_xlim(xMin - padding, xMax + padding)
    ax.set_ylim(yMin - padding, yMax + padding)

    # Run the GA algorithm
    GA()

    for depot in depots:
        # print(depot)
        depot.addToPlot(ax)

    plt.show()

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

    parseFile(f'p01')

    padding = 5
    ax.set_xlim(xMin - padding, xMax + padding)
    ax.set_ylim(yMin - padding, yMax + padding)

    # Run the GA algorithm
    GA()

    for depot in depots:
        # print(depot)
        depot.addToPlot(ax)

    plt.show()

"""
FIX: Not able to distrobute costumers correctly: [4, 6, 7, 10, 11]
TODO: Refactor x,y to vec2?
"""