from src.gameobject import GameObject
from src.vector import Vector
from src.playercontroller import PlayerController

class Player(GameObject):
    controller: PlayerController

    def __init__(self, sprite, name = "gameObject", position = Vector(0, 0), rotation = 0.0, size = 1, speed = 0, keymap = None, spawner = None):
        GameObject.__init__(self, sprite, name, position, rotation, size)
        self.controller = PlayerController(speed, keymap, super(), spawner)