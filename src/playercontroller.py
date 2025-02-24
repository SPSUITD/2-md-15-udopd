from arcade import key as Key
from src.keymap import KeyMap
from src.player import Player
from src.vector import Vector
from src.spawner import Spawner

class PlayerController:
    spawner: Spawner
    keymap: KeyMap
    player: Player
    direction: Vector

    def __init__(self, keymap: KeyMap, player: Player, spawner = None):
        self.direction = Vector(0, 0)
        self.player = player
        self.keymap = keymap
        self.spawner = spawner

    def on_key_press(self, key: Key):
        match key:
            case self.keymap.up.key:
                self.keymap.up.is_pressed = True
                self.direction.y = 1
            case self.keymap.down.key:
                self.keymap.down.is_pressed = True
                self.direction.y = -1
            case self.keymap.left.key:
                self.keymap.left.is_pressed = True
                self.direction.x = -1
            case self.keymap.right.key:
                self.keymap.right.is_pressed = True
                self.direction.x = 1
            case self.keymap.spawn:
                if self.spawner is not None:
                    self.spawner.spawn(self.player.position)
        self.direction.normalize()

    def on_key_release(self, key: Key):
        match key:
            case self.keymap.up.key:
                self.keymap.up.is_pressed = False
                self.direction.y = -1 if self.keymap.down.is_pressed else 0
            case self.keymap.down.key:
                self.keymap.down.is_pressed = False
                self.direction.y = 1 if self.keymap.up.is_pressed else 0
            case self.keymap.left.key:
                self.keymap.left.is_pressed = False
                self.direction.x = 1 if self.keymap.right.is_pressed else 0
            case self.keymap.right.key:
                self.keymap.right.is_pressed = False
                self.direction.x = -1 if self.keymap.left.is_pressed else 0
        self.direction.normalize()

    def on_update(self):
        self.player.move(self.direction)