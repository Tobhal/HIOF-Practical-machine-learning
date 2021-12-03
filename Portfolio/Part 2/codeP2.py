# from skopt import gp_minimize
from sko.GA import GA

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import os

# Class to store the depots
class Depot:
    def __init__(self, i, m, n, D, Q):
        self.i = int(i) + 1
        self.m = int(m)
        self.n = int(n)
        self.D = int(D)
        self.Q = int(Q)

        self.x = 0
        self.y = 0

    def setPos(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return f'Depot {self.i}\n\
    x, y: {self.x}, {self.y}\n\
    m: {self.m}\n\
    n: {self.n}\n\
    D: {self.D}\n\
    Q: {self.Q}'

# Class to store the costumer
class Costumer:
    def __init__(self, i, x, y, d, q):
        self.i = int(i)
        self.x = int(x)
        self.y = int(y)
        self.d = int(d)
        self.q = int(q)

    def __str__(self):
        return f'Costumer {self.i}\n\
    x, y: {self.x}, {self.y}\n\
    d: {self.d}\n\
    q: {self.q}'

depots = []
costumers = []

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
xMax = 0
xMin = 0
yMax = 0
yMin = 0

def updateMinMax(x, y):
    global xMax, xMin, yMax, yMin
    x = int(x)
    y = int(y)

    xMax = x if x > xMax else xMax
    xMin = x if x < xMin else xMin
    yMax = y if y > yMax else yMax
    yMin = y if y < yMin else yMin


def plotList(list: list, name: str, color: str):
    global ax

    for el in list:
        ax.scatter(el.x, el.y, color=color)

def parseFile(fileName):
    with open(f'DataFiles\\{fileName}.txt') as file:

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

        for depot in depots:
            line = file.readline().split()
            x = line[1]
            y = line[2]

            updateMinMax(x, y)

            depot.setPos(x, y)

    file.close()
            


if __name__ == '__main__':
    parseFile('p01')

    padding = 5
    ax.set_xlim(xMin - padding, xMax + padding)
    ax.set_ylim(yMin - padding, yMax + padding)

    plotList(depots, 'Depots', 'r')
    plotList(costumers, 'Costumers', 'g')

    plt.show()