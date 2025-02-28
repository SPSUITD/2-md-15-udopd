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
        self.collision()
        self.direction.normalize()
        self.player.move(self.direction)

    def spawn(self):
        max_count = self.player.bomb_specifications.count
        if len(self.player.bomb_list) < max_count:
            self.spawn_bomb_method(self.player.bomb_specifications, to_map_vector(self.player.position), self.player)
        else:
            Logger().Warning(f"invalid bomb spawn from {self.player.name} (max number ({max_count}) of bomb already on map)")

    def collision(self):
        if self.direction.x != 0 or self.direction.y != 0:
            player_map_pos = to_map_vector(self.player.position)

            #горизонтальное движение
            if self.direction.x != 0:
                next_pos = Vector(player_map_pos.x + self.direction.x, player_map_pos.y)
                next_cell = self.map[next_pos.x][next_pos.y]
                if next_cell == cnf.SYMBOLS.empty:
                    next_glob_pos = to_global_vector(next_pos)
                    if abs(to_global_vector(player_map_pos).y - self.player.position.y) > 5:
                        self.direction.y = int(abs(to_global_vector(player_map_pos).y - self.player.position.y) / (to_global_vector(player_map_pos).y - self.player.position.y))
                    else:
                        self.direction.y = 0
                        self.player.set_position(Vector(self.player.position.x, to_global_vector(player_map_pos).y))
                else:
                    next_glob_pos = to_global_vector(player_map_pos)

                if abs(next_glob_pos.x - self.player.position.x) > 5:
                    self.direction.x = abs(next_glob_pos.x - self.player.position.x) / (next_glob_pos.x - self.player.position.x)
                else:
                    self.direction.x = 0
                    self.player.set_position(Vector(next_glob_pos.x, self.player.position.y))
            
            #вертикальное движение
            if self.direction.y != 0:
                next_pos = Vector(player_map_pos.x, player_map_pos.y + self.direction.y)
                next_cell = self.map[next_pos.x][next_pos.y]
                if next_cell == cnf.SYMBOLS.empty:
                    next_glob_pos = to_global_vector(next_pos)
                    if abs(to_global_vector(player_map_pos).x - self.player.position.x) > 5:
                        self.direction.x = int(abs(to_global_vector(player_map_pos).x - self.player.position.x) / (to_global_vector(player_map_pos).x - self.player.position.x))
                    else:
                        self.direction.x = 0
                        self.player.set_position(Vector(to_global_vector(player_map_pos).x, self.player.position.y))
                else:
                    next_glob_pos = to_global_vector(player_map_pos)

                if abs(next_glob_pos.y - self.player.position.y) > 5:
                    self.direction.y = abs(next_glob_pos.y - self.player.position.y) / (next_glob_pos.y - self.player.position.y)
                else:
                    self.direction.y = 0
                    self.player.set_position(Vector(self.player.position.x, next_glob_pos.y))
