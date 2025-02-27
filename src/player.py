from src.gameobject import GameObject
from src.vector import Vector
from src.bombspecifications import BombSpecifications

class Player(GameObject):
    speed: float
    bomb_list: list
    bomb_specifications: BombSpecifications

    def __init__(self, sprite, name = "player", position = None, speed = 0, bomb_specifications: BombSpecifications = None):
        super().__init__(sprite, name, position)
        self.bomb_list = []
        self.speed = speed
        self.bomb_specifications = bomb_specifications

    def move(self, v: Vector):
        self.sprite.center_x += v.x * self.speed
        self.sprite.center_y += v.y * self.speed
        self.position.x += v.x * self.speed
        self.position.y += v.y * self.speed