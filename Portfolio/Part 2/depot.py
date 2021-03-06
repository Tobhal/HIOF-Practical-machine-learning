from vehicle import Vehicle

import random, copy

class Depot:
    m = 0
    n = 0

    def __init__(self, i, m, n, D, Q):
        self.i = int(i)
        self.m = int(m)
        self.n = int(n)
        self.D = int(D)
        self.Q = int(Q)

        self.x = 0
        self.y = 0

        self.vehicles = []
        self.costumers = []

        self.bestVehicles = []
        self.bestVehiclesDistance = 0

        self.color = (
            random.random(),
            random.random(),
            random.random()
        )

        for i in range(int(m)):
            self.vehicles.append(Vehicle(i, D, Q, self))

    def setPos(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def setBestVehiclesRoutes(self, vehiclesRoutes: list[Vehicle]):
        """
        Deep copy of the to sotore the depots best route, if the new route is better
        Also sets the self.bestVehicleDistance variable
        """
        # print('Copy | ', end='')
        self.bestVehicles = copy.copy(vehiclesRoutes)
        oldBest = self.bestVehiclesDistance
        
        # print('Calc: ', end='')
        self.bestVehiclesDistance = 0
        for v in vehiclesRoutes:
            # print(f'{v.id}, ', end='')
            self.bestVehiclesDistance += v.getDistance()

        # print(f'New best: {oldBest} -> {self.bestVehiclesDistance}')

    def addCostumer(self, c):
        self.costumers.append(c)

    def distrubuteVehiclesRandom(self):
        tmpCostumerArr = copy.copy(self.costumers)
        random.shuffle(tmpCostumerArr)

        # Run distortion multiple times to make sure all costumers are disturbed
        for _ in range(5):
            for vehicle in self.vehicles:
                if not len(tmpCostumerArr) == 0:
                    vehicle.fill(tmpCostumerArr)
                else:
                    break

        if len(tmpCostumerArr) > 0:
            raise Exception(f'D {self.i}: Not all costumers are given a route! {len(tmpCostumerArr)} left')

    def getLoad(self) -> int and int:
        tL = 0
        for c in self.costumers:
            tL += c.load

        return tL, tL / len(self.vehicles)

    def getTotalDistance(self) -> int:
        tD = 0
        for v in self.vehicles:
            tD += v.getDistance()

        return tD

    #
    # Ploting
    #
    def addDepotToPlot(self, ax):
        ax.scatter(self.x, self.y, color=self.color, zorder=2, marker='x')

    def addCostumerToPlot(self, ax):
        for costumer in self.costumers:
            if costumer.isBorderCostumer:
                ax.scatter(costumer.x, costumer.y, color=self.color, zorder=2, facecolors='none')
            else:
                ax.scatter(costumer.x, costumer.y, color=self.color, zorder=2)

    def addBestCostumersToPlot(self, ax):
        for vehicle in self.bestVehicles:
            for costumer in vehicle:
                if costumer.isBorderCostumer:
                    ax.scatter(costumer.x, costumer.y, color=self.color, zorder=2, facecolors='none')
                else:
                    ax.scatter(costumer.x, costumer.y, color=self.color, zorder=2)

    def addToPlot(self, ax):
        self.addDepotToPlot(ax)
        self.addCostumerToPlot(ax)

        for vehicle in self.vehicles:
            vehicle.addToPlot(ax)

    def addBestToPlot(self, ax):
        self.addDepotToPlot(ax)
        self.addCostumerToPlot(ax)

        for vehicle in self.bestVehicles:
            vehicle.addToPlot(ax)

    # 
    # Utility
    # 
    def __repr__(self) -> str:
        return f'D{self.i}: l={self.getLoad()} nC={len(self.costumers)} nV={len(self.vehicles)}'

    def __str__(self) -> str:
        vehiclesString = ''
        for vehicle in self.vehicles:
            vehiclesString += f'    Vehicle {vehicle.id}:\n\
      route {len(vehicle.getRouteID())}: {vehicle.getRoute()}\n\
      max duration: {vehicle.maxDuration}\n\
      max load: {vehicle.maxLoad}\n\
      current load: {vehicle.currentLoad}\n'

        costumerArr = []
        totalLoad = 0
        for costumer in self.costumers:
            costumerArr.append(costumer.i)
            totalLoad += costumer.load

        devidedLoad = totalLoad / len(self.vehicles)

        return f'Depot {self.i}:\n\
  x, y: {self.x}, {self.y}\n\
  m: {self.m}\n\
  n: {self.n}\n\
  D: {self.D}\n\
  Max Load: {self.Q}\n\
  Load: {totalLoad}, {devidedLoad}\n\
  Best Route: {self.bestVehicles}\n\
  Costumers: {costumerArr}\n\
  Vehicles:\n{vehiclesString}'