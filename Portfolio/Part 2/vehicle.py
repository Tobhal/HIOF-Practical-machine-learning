from costumer import Costumer
import math, random, copy, sys

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

    def addCostumerIndex(self, costumer: Costumer, index: int) -> None:
        if not costumer in self.route:
            self.route.insert(index, costumer)
            self.currentLoad += costumer.load

    def removeCostumer(self, costumer: Costumer) -> None:
        if costumer in self.route:
            self.currentLoad -= costumer.load
            self.route.remove(costumer)

    def addCostumerOptimal(self, costumer: Costumer) -> bool:
        """
        Add costumer to the optimal place in the route

        return:
            True: if the costumer is added
            False: if the costumer is not added
        """
        # print('Adding optimal:', costumer.i)
        if not costumer in self.route and self.canAddCostumer(costumer):
            testRoute = copy.copy(self.route)
            bestRoute = testRoute
            bestRouteDistance = sys.maxsize

            # NOTE: add -1 to len(testRoute) if things do not work?
            for i in range(0, len(testRoute) + 1):
                tmpRoute = copy.copy(testRoute)
                tmpRoute.insert(i, costumer)
                tmpDistance = Vehicle.calcDistance(Vehicle.genFullRoute(tmpRoute, self.depot.x, self.depot.y))

                # print('     ', tmpRoute, tmpDistance)

                if bestRouteDistance > tmpDistance:
                    bestRoute = tmpRoute
                    bestRouteDistance = tmpDistance
                    # print('Best:', bestRoute, bestRouteDistance)

            # set the route to the best route, remove first and last element
            # NOTE: can add [1:-1] if the first and last element is the depot
            # print(self.route)
            # print(bestRoute)
            self.route = bestRoute
            return True

        return False

    def canAddCostumer(self, costumer: Costumer) -> bool:
        return costumer.load < (int(self.maxLoad) - int(self.currentLoad))

    def addRoute(self, route: list[Costumer]) -> bool:
        if self.getLoadOfRoute(route) < self.maxLoad and len(route) < self.maxDuration:
            self.route = route
            return True
        else:
            return False

    def getLoad(self) -> int:
        totLoad = 0
        for c in self.route:
            totLoad += c.load

        return totLoad

    def getLoadOfRoute(route: list[Costumer]) -> int:
        totLoad = 0
        for c in route:
            totLoad += c.load

        return totLoad

    def getRouteID(self) -> list[int]:
        return [c.i for c in self.route]
    
    def getFullRouteID(self) -> list[int]:
        retRoute = [c.i for c in self.route]
        retRoute.insert(0, 0)
        retRoute.append(0)
        
        return retRoute

    def getRoute(self) -> list:
        return Vehicle.genFullRoute(self.route, self.depot.x, self.depot.y)

    @staticmethod
    def genFullRoute(route: list, depotX: int, depotY: int) -> list:
        retRoute = [[c.x, c.y] for c in route]
        retRoute.insert(0, [depotX, depotY])
        retRoute.append([depotX, depotY])

        return retRoute

    def getDistance(self) -> int:
        return Vehicle.calcDistance(self.getRoute())

    @staticmethod
    def calcDistance(route: list) -> int:
        calcRoute = route
        totalDistance = 0

        for i in range(1, len(calcRoute)):
            prevRoute = calcRoute[i - 1]
            thisRoute = calcRoute[i]

            xDistance = abs(prevRoute[0] - thisRoute[0])
            yDistance = abs(prevRoute[1] - thisRoute[1])
            
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

    # def __repr__(self) -> str:
    #     return f'V{self.id}: D={self.depot.i} R={len(self.route)}'

    def __str__(self) -> str:
        return f'Vehicle {self.id}:\n\
    route: {self.route}\n\
    max duration: {self.maxDuration}\n\
    load: {self.getLoad()}/{self.maxLoad}\n\
    depot ID: {self.depot.i}'