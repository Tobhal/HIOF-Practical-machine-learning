class Costumer:
    def __init__(self, i, x, y, d, q):
        self.i = int(i)
        self.x = int(x)         # Position
        self.y = int(y)         # Position
        self.duration = int(d)  # Service duration
        self.load = int(q)      # Load

        self.isBorderCostumer = False

        self.possibleDepots = []

    def addPossibleDepots(self, d):
        self.possibleDepots.append(d)

    def __repr__(self) -> str:
        return f'C{self.i}'

    def __str__(self) -> str:
        return f'Costumer {self.i}:\n\
    x, y: {self.x}, {self.y}\n\
    duration: {self.duration}\n\
    load: {self.load}'