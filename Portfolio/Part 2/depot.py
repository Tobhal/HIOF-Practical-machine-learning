from vehicle import Vehicle

class Depot:
    m = 0
    n = 0

    def __init__(self, i, m, n, D, Q):
        self.i = int(i) + 1
        self.m = int(m)
        self.n = int(n)
        self.D = int(D)
        self.Q = int(Q)

        self.x = 0
        self.y = 0

        self.vehicles = []

        for i in range(int(m)):
            self.vehicles.append(Vehicle(i, D, Q, self))

    def setPos(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        vehiclesString = ''
        for vehicle in self.vehicles:
            vehiclesString += f'    Vehicle {vehicle.id + 1}:\n\
      route {len(vehicle.getRouteID())}: {vehicle.getRoute()}\n\
      max duration: {vehicle.maxDuration}\n\
      max load: {vehicle.maxLoad}\n\
      current load: {vehicle.currentLoad}\n'

        return f'Depot {self.i}:\n\
  x, y: {self.x}, {self.y}\n\
  m: {self.m}\n\
  n: {self.n}\n\
  D: {self.D}\n\
  Q: {self.Q}\n\
  Vehicles:\n{vehiclesString}'