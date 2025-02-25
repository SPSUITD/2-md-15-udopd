from src.gameobject import GameObject
from src.vector import Vector, zero_vector
from src.bombspecifications import BombSpecifications

class Player(GameObject):
    def __init__(self, sprite, name = "player", position = zero_vector(), rotation = 0.0, size = 1, speed = 0):
        super().__init__(sprite, name, position, rotation, size)
        self.speed = speed
        self.bomb_specifications = BombSpecifications(1, 100, 3)
        
    def move(self, v: Vector):
        self.sprite.center_x += v.x * self.speed
        self.sprite.center_y += v.y * self.speed