from costumer import Costumer

class Vehicle:
    def __init__(self, id, maxDuration, maxLoad, depot):
        self.id = id
        self.maxDuration = maxDuration
        self.maxLoad = maxLoad

        self.route = []
        self.currentDuration = 0
        self.currentLoad = 0

        self.depot = depot

    def fill(self, costumers: list[Costumer]):
        for costumer in costumers:
            if self.canAddCostumer(costumer):
                self.addCostumer(costumer)
                costumers.remove(costumer)
            else:
                continue

    def addCostumer(self, costumer: Costumer) -> bool:
        if not costumer in self.route:
            if costumer.load < (int(self.maxLoad) - int(self.currentLoad)):
                self.route.append(costumer)
                self.currentLoad += costumer.load
                # print(self.id, self.currentLoad)
                return True
            else:
                return False

    def canAddCostumer(self, costumer: Costumer) -> bool:
        if costumer.load < (int(self.maxLoad) - int(self.currentLoad)):
            return True
        else:
            return False

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



    def __str__(self):
        return f'Vehicle {self.id}:\n\
    route: {self.route}\n\
    max duration: {self.maxDuration}\n\
    max load: {self.maxLoad}\n\
    depot ID: {self.depot.i}'