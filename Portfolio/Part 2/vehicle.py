from costumer import Costumer
import math, random

class Vehicle:
    def __init__(self, id, maxDuration, maxLoad, depot):
        self.id = id

        self.maxDuration = maxDuration
        self.currentDuration = 0

        self.maxLoad = maxLoad
        self.currentLoad = 0

        self.route = []
        self.depot = depot

        self.color = (
            random.random(),
            random.random(),
            random.random()
        )

    def fill(self, costumers: list[Costumer]):
        for costumer in costumers:
            if self.canAddCostumer(costumer):
                self.addCostumer(costumer)
                costumers.remove(costumer)
            else:
                continue

    def addCostumer(self, costumer: Costumer) -> bool:
        if not costumer in self.route:
            self.route.append(costumer)
            self.currentLoad += costumer.load

    def canAddCostumer(self, costumer: Costumer) -> bool:
        return costumer.load < (int(self.maxLoad) - int(self.currentLoad))

    def addRoute(self, route: list[Costumer]) -> bool:
        if self.getLoadOfRoute(route) < self.maxLoad and len(route) < self.maxDuration:
            self.route = route
            return True
        else:
            return False

    def getLoadOfRoute(route: list[Costumer]) -> int:
        totLoad = 0
        for c in route:
            totLoad += c.load

        return totLoad

    def getRouteID(self) -> list[int]:
        return [c.i for c in self.route]

    def getRoute(self) -> list:
        retRoute = [[c.x, c.y] for c in self.route]

        retRoute.insert(0, [self.depot.x, self.depot.y])
        retRoute.append([self.depot.x, self.depot.y])

        return retRoute

    def getDistance(self) -> int:
        calcRoute = self.getRoute()
        totalDistance = 0

        for i in range(1, len(self.route)):
            prevRoute = self.route[i - 1]
            thisRoute = self.route[i]

            xDistance = abs(prevRoute.x - thisRoute.x)
            yDistance = abs(prevRoute.y - thisRoute.y)
            
            totalDistance += math.sqrt((xDistance**2) + (yDistance**2))

        # for place in calcRoute:
        #     totalDistance += math.sqrt(place[0]**2 + place[1]**2)

        return totalDistance
        
    def addToPlot(self, ax):
        x, y = [], []

        for route in self.getRoute():
            x.append(route[0])
            y.append(route[1])

        ax.plot(x, y, color=self.color, zorder=1)

    def __str__(self):
        return f'Vehicle {self.id}:\n\
    route: {self.route}\n\
    max duration: {self.maxDuration}\n\
    max load: {self.maxLoad}\n\
    depot ID: {self.depot.i}'