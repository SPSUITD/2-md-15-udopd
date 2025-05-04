from src.gameobject import GameObject
from src.bombspecifications import BombSpecifications
from src.player import Player
import math

class Bomb(GameObject):
    parent: Player
    lifetime: int
    explosion_size: int
    size: float
    time: int

    def __init__(self, go: GameObject, spec: BombSpecifications):
        self.time = 0
        super().__init__(go.sprite, go.name, go.position)
        self.lifetime = spec.lifetime
        self.explosion_size = spec.size
        self.scale = self.sprite.scale

    def update(self):
        self.lifetime -= 1
        self.time = (self.time+0.1) % 180
        self.size = 0.9 - math.cos(self.time)/10
        self.sprite.scale = (self.scale[0] * self.size, self.scale[1] * self.size)
