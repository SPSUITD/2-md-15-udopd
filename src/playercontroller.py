import src.config as cnf

from src.vector import Vector, zero_vector, to_global_vector, to_map_vector, distance
from src.logger import Logger
from src.player import Player
from src.keymap import KeyMap

class PlayerController():
    keymap: KeyMap
    direction: Vector
    player: Player
    map: None

    def __init__(self, keymap, player, spawn_bomb_method, map: list[list[str]] = None):
        self.direction = zero_vector()
        self.spawn_bomb_method = spawn_bomb_method
        self.player = player
        self.keymap = keymap

        self.map = map

    def on_key_press(self, key):
        match key:
            case self.keymap.up.key:
                self.keymap.up.is_pressed = True
            case self.keymap.down.key:
                self.keymap.down.is_pressed = True
            case self.keymap.left.key:
                self.keymap.left.is_pressed = True
            case self.keymap.right.key:
                self.keymap.right.is_pressed = True
            case self.keymap.spawn:
                self.spawn()

    def on_key_release(self, key):
        match key:
            case self.keymap.up.key:
                self.keymap.up.is_pressed = False
            case self.keymap.down.key:
                self.keymap.down.is_pressed = False
            case self.keymap.left.key:
                self.keymap.left.is_pressed = False
            case self.keymap.right.key:
                self.keymap.right.is_pressed = False
                
    def key_update(self):
        if self.keymap.up.is_pressed:
            self.direction.y = 0 if self.keymap.down.is_pressed else 1
        else:
            self.direction.y = -1 if self.keymap.down.is_pressed else 0
        if self.keymap.down.is_pressed:
            self.direction.y = 0 if self.keymap.up.is_pressed else -1
        else:
            self.direction.y = 1 if self.keymap.up.is_pressed else 0
        if self.keymap.left.is_pressed:
            self.direction.x = 0 if self.keymap.right.is_pressed else -1
        else:
            self.direction.x = 1 if self.keymap.right.is_pressed else 0
        if self.keymap.right.is_pressed:
            self.direction.x = 0 if self.keymap.left.is_pressed else 1
        else:
            self.direction.x = -1 if self.keymap.left.is_pressed else 0

    def on_update(self):
        self.key_update()

        new_pos = Vector(self.player.sprite.center_x + self.direction.x * self.player.speed, 
                         self.player.sprite.center_y + self.direction.y * self.player.speed)
        self.rewrite_direction(new_pos)
        self.direction.normalize()
        self.player.move(self.direction)

    def spawn(self):
        max_count = self.player.bomb_specifications.count
        if len(self.player.bomb_list) < max_count:
            self.spawn_bomb_method(self.player.bomb_specifications, to_map_vector(self.player.position), self.player)
        else:
            Logger().Warning(f"invalid bomb spawn (max number ({max_count}) of bomb already on map)")

    def rewrite_direction(self, next_pos: Vector):
        if self.direction.x != 0 or self.direction.y != 0:
            map_next_pos = to_map_vector(next_pos)

            if self.direction.x != 0:
                dirx = int(self.direction.x)
                symb = self.map[map_next_pos.x + dirx][map_next_pos.y]
                if symb != cnf.SYMBOLS.empty:
                    if distance(to_global_vector(Vector(map_next_pos.x + dirx, map_next_pos.y)), next_pos) < cnf.SPRITE_SIZE*0.9:
                        self.direction.x = 0
                        
            if self.direction.y != 0:
                diry = int(self.direction.y)
                symb = self.map[map_next_pos.x][map_next_pos.y+diry]
                if symb != cnf.SYMBOLS.empty:
                    if distance(to_global_vector(Vector(map_next_pos.x, map_next_pos.y+diry)), next_pos) < cnf.SPRITE_SIZE*0.9:
                        self.direction.y = 0