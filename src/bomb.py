from src.gameobject import GameObject
from src.vector import zero_vector

class Bomb(GameObject):    
    def __init__(self, sprite, name = "bomb", position = zero_vector(), rotation = 0.0, size = 1, lifetime = 300, explosion_size = 3):
        super().__init__(sprite, name, position, rotation, size)
        self.lifetime = lifetime
        self.size = explosion_size
