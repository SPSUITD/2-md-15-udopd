import src.vector as V
from src.logger import Logger
from src.player import Player
from src.keymap import KeyMap

class PlayerController():
    keymap: KeyMap
    direction: V.Vector
    player: Player

    def __init__(self, keymap, player, spawn_bomb_method):
        self.direction = V.zero_vector()
        self.spawn_bomb_method = spawn_bomb_method
        self.player = player
        self.keymap = keymap

    def on_key_press(self, key):
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
                self.spawn()
        self.direction.normalize()

    def on_key_release(self, key):
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

    def spawn(self):
        max_count = self.player.bomb_specifications.count
        if len(self.player.bomb_list) < max_count:
            self.spawn_bomb_method(self.player.bomb_specifications, V.to_map_vector(self.player.position), self.player)
        else:
            Logger().Warning(f"invalid bomb spawn (max number ({max_count}) of bomb already on map)")