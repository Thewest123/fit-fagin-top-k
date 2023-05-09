class Mouse:
    def __init__(self):
        self.name = None
        self.weight = None
        self.accuracy = None
        self.dpi = None
        self.price = None

    def assign(self, name, weight, accuracy, dpi, price):
        self.name = name
        self.weight = weight
        self.accuracy = accuracy
        self.dpi = dpi
        self.price = price
