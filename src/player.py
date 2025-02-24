from src.gameobject import GameObject
from src.vector import Vector

class Player(GameObject):
    def __init__(self, sprite, name = "gameObject", position = Vector(0, 0), rotation = 0.0, size = 1, speed = 0):
        GameObject.__init__(self, sprite, name, position, rotation, size)
        self.speed = speed
        
    def move(self, v: Vector):
        self.sprite.center_x += v.x * self.speed
        self.sprite.center_y += v.y * self.speed