import threading
import src.config as cnf

from src.vector import Vector, zero_vector, to_global_vector, to_map_vector
from src.logger import Logger
from src.player import Player
from src.keymap import KeyMap
from server import Server

class PlayerController:
    keymap: KeyMap
    direction: Vector
    player: Player
    map: None
    rm_buff: None

    def __init__(self, keymap, player = None, spawn_bomb_method = None, map: list[list[str]] = None, rm_buff = None, online: bool = False):
        self.direction = zero_vector()
        self.spawn_bomb_method = spawn_bomb_method
        self.player = player
        self.keymap = keymap
        self.rm_buff = rm_buff
        self.map = map
        self.online = online    
        if online:
            self.server_setup()        

    def server_setup(self):
        self.s = Server('127.0.0.1:5555')
        threading.Thread(target=self.s.run, daemon=True).start()
            
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
                if self.player is not None:
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
        if self.online:
            data = self.s.get_client_input()
            self.parse_keymap(data)
            #Logger().Message(f'direction: {self.direction.x} {self.direction.y}')
        self.key_update()
        if self.map is not None:
            self.collision()
        self.direction.normalize()
        if self.player is not None:
            self.player.move(self.direction)

    def parse_keymap(self, data):
        if data is not None:
            if data['action'] == 'press':
                self.on_key_press(data['key'])
            else:
                self.on_key_release(data['key'])

    def spawn(self):
        max_count = self.player.bomb_specifications.count
        if self.spawn_bomb_method is not None and len(self.player.bomb_list) < max_count:
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
                if next_cell == cnf.SYMBOLS.empty or next_cell == cnf.SYMBOLS.add_explosion_size or next_cell == cnf.SYMBOLS.add_bomb:
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
                if next_cell == cnf.SYMBOLS.empty or next_cell == cnf.SYMBOLS.add_explosion_size or next_cell == cnf.SYMBOLS.add_bomb:
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

            #подбор баффов
            cell = self.map[player_map_pos.x][player_map_pos.y]
            if cell == cnf.SYMBOLS.add_bomb:
                Logger().Message(f"{self.player.name} upgrade the max bomb count, received in [{player_map_pos.x} {player_map_pos.y}]")
                self.player.bomb_specifications.count += 1
                self.rm_buff(player_map_pos)
            if cell == cnf.SYMBOLS.add_explosion_size:
                Logger().Message(f"{self.player.name} upgrade the bomb explosion size, received in [{player_map_pos.x} {player_map_pos.y}]")
                self.player.bomb_specifications.size += 1
                self.rm_buff(player_map_pos)
            