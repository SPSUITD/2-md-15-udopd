from src.keymap import KeyMap
from src.gameobject import GameObject
from src.vector import Vector
from src.logger import Logger

class Controller:
    keymap: KeyMap
    game_object: GameObject
    direction: Vector
    speed: float
    class Keys:
        left: bool
        right: bool
        up: bool
        down: bool

        def __init__(self):
            self.left = False
            self.right = False
            self.up = False
            self.down = False

    def __init__(self, speed, keymap, game_object):
        self.direction = Vector(0, 0)
        self.game_object = game_object
        self.speed = speed
        self.keymap = keymap
        self.move_keys = self.Keys()

    def on_key_press(self, key):
        match key:
            case self.keymap.up:
                self.move_keys.up = True
                self.direction.y = 1
            case self.keymap.down:
                self.move_keys.down = True
                self.direction.y = -1
            case self.keymap.left:
                self.move_keys.left = True
                self.direction.x = -1
            case self.keymap.right:
                self.move_keys.right = True
                self.direction.x = 1
        self.direction.normalize()

    def on_key_release(self, key):
        match key:
            case self.keymap.up:
                self.move_keys.up = False
                self.direction.y = -1 if self.move_keys.down else 0
            case self.keymap.down:
                self.move_keys.down = False
                self.direction.y = 1 if self.move_keys.up else 0
            case self.keymap.left:
                self.move_keys.left = False
                self.direction.x = 1 if self.move_keys.right else 0
            case self.keymap.right:
                self.move_keys.right = False
                self.direction.x = -1 if self.move_keys.left else 0
        self.direction.normalize()

    def on_update(self):
        self.game_object.move(self.direction, self.speed)
        #Logger().Message(f'dir: [{self.direction.x}, {self.direction.y}]')