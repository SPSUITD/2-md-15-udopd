from src.vector import Vector

class GameObject:
    name: str
    size: float

    def __init__(self, sprite, name = "gameObject", position = Vector(0, 0), rotation = 0.0, size = 1):
        self.name = name
        self.size = size
        self.sprite = sprite
        self.sprite.angle = rotation
        self.sprite.height *= size
        self.sprite.width *= size
        self.set_position(position)

    def move(self, v: Vector, speed: float):
        self.sprite.center_x += v.x * speed
        self.sprite.center_y += v.y * speed

    def set_position(self, position: Vector):
        self.sprite.center_x = position.x
        self.sprite.center_y = position.y

    def get_position(self):
        return Vector(self.sprite.center_x, self.sprite.center_y)

    def rotate(self, a: float):
        self.sprite.angle += a