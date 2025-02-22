from src.vector import Vector
from src.logger import Logger

class GameObject:
    name: str

    def __init__(self, sprite, name = "gameObject", position = Vector(0, 0), rotation = 0.0, size = 1):
        self.name = name
        self.sprite = sprite
        self.sprite.angle = rotation
        self.sprite.height *= size
        self.sprite.width *= size
        self.sprite.center_x = position.x
        self.sprite.center_y = position.y

    def move(self, v: Vector, speed: float):
        self.sprite.center_x += v.x * speed
        self.sprite.center_y += v.y * speed

    def rotate(self, a: float):
        self.sprite.angle += a

    def __del__(self):
        class_name = self.__class__.__name__
        #Logger().Message(f'{class_name} уничтожен')