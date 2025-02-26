from src.gameobject import GameObject
from src.bombspecifications import BombSpecifications
from src.player import Player

class Bomb(GameObject):
    parent: Player
    lifetime: int
    explosion_size: int

    def __init__(self, go: GameObject, spec: BombSpecifications):
        super().__init__(go.sprite, go.name, go.position)
        self.lifetime = spec.lifetime
        self.explosion_size = spec.size
