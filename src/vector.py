import math

class Vector:
    x: float
    y: float

    def __init__(self, x = 0.0, y = 0.0):
        self.x = x
        self.y = y

    def lenght(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self):
        l = self.lenght()
        if l != 0:
            self.x /= l
            self.y /= l