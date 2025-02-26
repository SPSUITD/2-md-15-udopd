import math
import src.config as cnf

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

def to_map_vector(global_vector: Vector):
    size = cnf.SPRITE_SIZE
    return Vector(round(global_vector.x / size), round(global_vector.y / size))

def to_global_vector(map_vector: Vector):
    size = cnf.SPRITE_SIZE
    return Vector(map_vector.x * size, map_vector.y * size)

def zero_vector():
    return Vector(0, 0)

def distance(v1: Vector, v2: Vector):
    return math.sqrt((v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2)