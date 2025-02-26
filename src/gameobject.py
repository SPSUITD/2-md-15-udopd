from src.vector import Vector, zero_vector

class GameObject():
    name: str
    position: Vector
    sprite: None

    def __init__(self, sprite, name = "gameObject", position = zero_vector()):
        self.name = name
        self.sprite = sprite
        self.position = position

    @property
    def position(self):
        return Vector(self.sprite.center_x, self.sprite.center_y)
    
    @position.setter
    def position(self, position: Vector):
        self.sprite.center_x = position.x
        self.sprite.center_y = position.y