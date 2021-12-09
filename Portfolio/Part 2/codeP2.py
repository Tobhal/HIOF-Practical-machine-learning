# from skopt import gp_minimize
# from sko.GA import GA

import matplotlib.pyplot as plt
from matplotlib import cm

import numpy as np
import pandas as pd

# Importing supporting classes for storing data
from costumer import Costumer
from vehicle import Vehicle
from depot import Depot

import os
import random

depots = []
costumers = []
costumersDistribute = []

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
xMax = 0
xMin = 0
yMax = 0
yMin = 0

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)

def updateMinMax(x, y):
    global xMax, xMin, yMax, yMin
    x = int(x)
    y = int(y)

    xMax = x if x > xMax else xMax
    xMin = x if x < xMin else xMin
    yMax = y if y > yMax else yMax
    yMin = y if y < yMin else yMin

def distrubeCostumersRandomly(costumers: list[Costumer], depots: Depot) -> bool:
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

def fillVehicle(costumers: list[Costumer], vehicle: Vehicle):
    for costumer in costumers:
        if vehicle.canAddCostumer(costumer):
            vehicle.addCostumer(costumer)
            costumers.remove(costumer)
        else:
            return

def plotList(list: list, name: str, color: str):
    global ax

    for el in list:
        ax.scatter(el.x, el.y, color=color, zorder=2)

def plotRoute(list: list, name: str, color: str):
    global ax

    x = []
    y = []

    for el in list:
        x.append(el[0])
        y.append(el[1])

    ax.plot(x, y, color=color, zorder=1)


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

if __name__ == '__main__':
    # Parse the data file. Just specify the file name without the extention
    parseFile('p01')

    padding = 5
    ax.set_xlim(xMin - padding, xMax + padding)
    ax.set_ylim(yMin - padding, yMax + padding)

    distrubeCostumersRandomly(costumersDistribute, depots)

    plotList(depots, 'Depots', 'r')
    plotList(costumers, 'Costumers', 'g')
    
    colors = cm.rainbow(np.linspace(0, 1, 10))

    for depot in depots:
        print(depot)

        # Set a random color for the route for the depot
        color = (
            random.random(),
            random.random(),
            random.random()
        )

        for vehicle in depot.vehicles:            
            plotRoute(vehicle.getRoute(), 'Route', color=color)

    plt.show()
