import arcade
import random

import src.config as cnf
from src.logger import Logger
from src.keymap import KeyMap
from src.config import SYMBOLS as symb
from src.playercontroller import PlayerController
from src.player import Player
from src.abstractobject import AbstractObject
from src.bombspecifications import BombSpecifications
from src.gameobject import GameObject
from src.bomb import Bomb
from src.vector import Vector, to_map_vector, to_global_vector, zero_vector, distance

class GameView(arcade.Window):
    def __init__(self):
        super().__init__(cnf.WINDOW_SIZE[0], cnf.WINDOW_SIZE[1], cnf.WINDOW_TITLE)
        self.background_color = arcade.csscolor.LIGHT_GREEN
        self.center_window()

    def setup(self):
        self.logger = Logger()

        self.map = None
        self.sprite_list = arcade.SpriteList()
        self.bombs = []
        self.blocks = []
        self.player_sprite = None
        self.explosion_list = []
        self.controllers = []
        self.__camera_setup__()
        self.__setup_abstract_objects__()
        self.__create_map__()
        
        self.__new_player__(keymap=KeyMap(
            left=cnf.PLAYER_1_KEYMAP.left,
            right=cnf.PLAYER_1_KEYMAP.right,
            up=cnf.PLAYER_1_KEYMAP.up,
            down=cnf.PLAYER_1_KEYMAP.down,
            spawn=cnf.PLAYER_1_KEYMAP.spawn
        ), 
                    name='player1',
                    texture_path=cnf.TEXTURES.PLAYER_1, 
                    position=to_global_vector(Vector(1, cnf.GRID_SIZE[1]-2)),
                    bomb_specifications = self.bomb)
        
        self.__new_player__(keymap=KeyMap(
            left=cnf.PLAYER_2_KEYMAP.left,
            right=cnf.PLAYER_2_KEYMAP.right,
            up=cnf.PLAYER_2_KEYMAP.up,
            down=cnf.PLAYER_2_KEYMAP.down,
            spawn=cnf.PLAYER_2_KEYMAP.spawn
        ), 
                    name='player2',
                    texture_path=cnf.TEXTURES.PLAYER_2, 
                    position=to_global_vector(Vector(cnf.GRID_SIZE[0]-2, 1)),
                    bomb_specifications = self.bomb)
    
    def __setup_abstract_objects__(self):
        self.bomb = BombSpecifications(
            cnf.BOMB_CONFIG.count,
            cnf.BOMB_CONFIG.lifetime,
            cnf.BOMB_CONFIG.size,
            cnf.TEXTURES.BOMB, 
            cnf.SYMBOLS.bomb)
        
        self.wall = AbstractObject(
            sprite_path=cnf.TEXTURES.WALL,
            name='wall',
            symbol=cnf.SYMBOLS.wall
            )
        
        self.block = AbstractObject(
            sprite_path=cnf.TEXTURES.BLOCK,
            name='block',
            symbol=cnf.SYMBOLS.block
            )
        
        self.explosion = AbstractObject(
            sprite_path=cnf.TEXTURES.EXPLOSION,
            name='explosion',
            symbol=cnf.SYMBOLS.empty
            )

    def __camera_setup__(self):
        self.camera = arcade.camera.Camera2D()
        self.camera.position = ((cnf.GRID_SIZE[0]-1)*cnf.SPRITE_SIZE/2, (cnf.GRID_SIZE[1]-1)*cnf.SPRITE_SIZE/2)

    def spawn(self, object: AbstractObject, pos: Vector, player: Player):
        if self.map[pos.x][pos.y] == symb.empty:
            new_go = GameObject(sprite=arcade.Sprite(object.sprite_path, cnf.SIZE),
                                    name=object.name,
                                    position=to_global_vector(pos))
            
            if isinstance(object, BombSpecifications):
                bomb = Bomb(new_go, object)
                player.bomb_list.append(bomb)
                bomb.parent = player
                self.bombs.append(bomb)
                new_go = bomb
            
            if object.name == 'block':
                self.blocks.append(new_go)
            
            self.sprite_list.append(new_go.sprite)
            self.map[pos.x][pos.y] = object.symbol
            self.logger.Message(f"{object.name} spawn at [{pos.x}, {pos.y}]")
            
        else:
            self.logger.Warning(f"invalid {object.name} spawn at [{pos.x}, {pos.y}]")
            
    def explose(self, bomb: Bomb):
        bomb.parent.bomb_list.remove(bomb)
        self.bombs.remove(bomb)
        bomb_map_position = to_map_vector(bomb.position)
        self.logger.Message(f"bomb explose at [{bomb_map_position.x}, {bomb_map_position.y}]")
        self.__spawn_explosion__(bomb_map_position, bomb.explosion_size)
        
        #ударная волна
        for b in self.bombs:
            temp_contr_pos = to_map_vector(b.position)
            in_radius = distance(bomb_map_position, temp_contr_pos) < bomb.explosion_size
            if in_radius:
                is_vis = self.is_visible(bomb_map_position, temp_contr_pos)
                if is_vis and b != bomb:
                    self.logger.Message(f"bomb at [{bomb_map_position.x}, {bomb_map_position.y}] " + 
                                        f"explose the bomb at [{temp_contr_pos.x}, {temp_contr_pos.y}]")
                    self.explose(b)

        #обработка попаданий по иным объектам  
        for c in self.controllers:
            temp_contr_pos = to_map_vector(c.player.position)
            in_radius = distance(bomb_map_position, temp_contr_pos) < bomb.explosion_size
            if in_radius:
                is_vis = self.is_visible(bomb_map_position, temp_contr_pos)
                if is_vis:
                    self.controllers.remove(c) #заглушка
                    self.logger.Message(f"bomb at [{bomb_map_position.x}, {bomb_map_position.y}] " + 
                                        f"kill the {c.player.name} at [{temp_contr_pos.x}, {temp_contr_pos.y}]")
   
        block_pos = []
        for bl in self.blocks:
            temp_contr_pos = to_map_vector(bl.position)
            in_radius = distance(bomb_map_position, temp_contr_pos) < bomb.explosion_size
            if in_radius:
                is_vis = self.is_visible(bomb_map_position, temp_contr_pos)
                if is_vis:
                    block_pos.append(bl)
                    self.logger.Message(f"bomb at [{bomb_map_position.x}, {bomb_map_position.y}] " + 
                                        f"remove the block at [{temp_contr_pos.x}, {temp_contr_pos.y}]")
                
        for bl in block_pos:
            temp = to_map_vector(bl.position)
            self.map[temp.x][temp.y] = cnf.SYMBOLS.empty
            self.blocks.remove(bl)
            self.sprite_list.remove(bl.sprite)

        self.map[bomb_map_position.x][bomb_map_position.y] = symb.empty
        self.sprite_list.remove(bomb.sprite)

    def __one_explosion__(self, pos: Vector):
        new_go = GameObject(sprite=arcade.Sprite(self.explosion.sprite_path, cnf.SIZE),
                            name=self.explosion.name,
                            position=to_global_vector(pos))
        new_go.lifetime = 20
        self.sprite_list.append(new_go.sprite)
        self.explosion_list.append(new_go)

    def __spawn_explosion__(self, pos: Vector, size: int):
        for x in range(0, size):
            if pos.x - x >= 0:
                if self.map[pos.x - x][pos.y] == cnf.SYMBOLS.wall:
                    break
                self.__one_explosion__(Vector(pos.x - x, pos.y))
                if self.map[pos.x - x][pos.y] == cnf.SYMBOLS.block:
                    break
        for x in range(1, size):
            if pos.x + x < len(self.map):
                if self.map[pos.x + x][pos.y] == cnf.SYMBOLS.wall:
                    break
                self.__one_explosion__(Vector(pos.x + x, pos.y))
                if self.map[pos.x + x][pos.y] == cnf.SYMBOLS.block:
                    break

        for y in range(0, size):
            if pos.y - y >= 0:
                if self.map[pos.x][pos.y - y] == cnf.SYMBOLS.wall:
                    break
                self.__one_explosion__(Vector(pos.x, pos.y - y))
                if self.map[pos.x][pos.y - y] == cnf.SYMBOLS.block:
                    break
        for y in range(1, size):
            if pos.y + y < len(self.map[0]):
                if self.map[pos.x][pos.y + y] == cnf.SYMBOLS.wall:
                    break
                self.__one_explosion__(Vector(pos.x, pos.y + y))
                if self.map[pos.x][pos.y + y] == cnf.SYMBOLS.block:
                    break
    
    def is_visible(self, v1: Vector, v2: Vector):
        map = self.map
        if v1.x != v2.x and v1.y != v2.y:
            return False
        if v1.x == v2.x:
            posx = v1.x
            if v1.y < v2.y:
                min, max = v1.y, v2.y
            else:
                min, max = v2.y, v1.y
            for posy in range(min+1, max):
                if map[posx][posy] != cnf.SYMBOLS.empty:
                    return False
        else:
            posy = v1.y
            if v1.x < v2.x:
                min, max = v1.x, v2.x
            else:
                min, max = v2.x, v1.x
            for posx in range(min+1, max):
                if map[posx][posy] != cnf.SYMBOLS.empty:
                    return False
        return True

    def __create_map__(self):
        width = cnf.GRID_SIZE[0]
        height = cnf.GRID_SIZE[1]
        self.map = [[symb.empty] * height for i in range(width)]

        for x in range(width):
            for y in range(height):
                if ((x == width-1 or x == 0 or y == 0 or y == height-1) or 
                    (x % 2 == 0 and y % 2 == 0)):
                    self.spawn(self.wall, Vector(x, y), None)
                else:
                    self.__spawn_box__(Vector(x, y))
        
        self.logger.Message(f"======= Map is created =======")

    def __spawn_box__(self, pos):
        safe_zone = (pos.x == 1 and pos.y == cnf.GRID_SIZE[1]-2 or #player1 safezone
            pos.x == 1 and pos.y == cnf.GRID_SIZE[1]-3 or
            pos.x == 1 and pos.y == cnf.GRID_SIZE[1]-4 or
            pos.x == 2 and pos.y == cnf.GRID_SIZE[1]-2 or
            pos.x == 3 and pos.y == cnf.GRID_SIZE[1]-2 or
            
            pos.x == cnf.GRID_SIZE[0]-2 and pos.y == 1 or #player2 safezone
            pos.x == cnf.GRID_SIZE[0]-3 and pos.y == 1 or
            pos.x == cnf.GRID_SIZE[0]-4 and pos.y == 1 or
            pos.x == cnf.GRID_SIZE[0]-2 and pos.y == 2 or
            pos.x == cnf.GRID_SIZE[0]-2 and pos.y == 3)

        if safe_zone:
            pass
        else:
            if random.randint(0, 10) < 9:
                self.spawn(self.block, pos, None)

    def __new_player__(self, texture_path = cnf.TEXTURES.PLAYER_1,
                    name = "player", 
                    position = zero_vector(), 
                    speed = 4, 
                    keymap = KeyMap(), 
                    bomb_specifications = None):
        if keymap.is_valid:
            player = Player(
                    sprite=arcade.Sprite(arcade.load_texture(texture_path), cnf.SIZE),
                    name=name,
                    position=position,
                    speed=speed,
                    bomb_specifications=bomb_specifications
                )
            controller = PlayerController(
                keymap=keymap,
                spawn_bomb_method=self.spawn,
                player=player,
                map=self.map
            )
            self.player_sprite = player.sprite
            self.sprite_list.append(player.sprite)
            self.controllers.append(controller)
        else:
            self.logger.Error(('Невалидная карта кнопок', '__new_player__', 60, '> Карта кнопок принимает код несуществующей кнопки'))

    def on_key_press(self, key, modifiers):
        for c in self.controllers:
            c.on_key_press(key)

    def on_key_release(self, key, modifiers):
        for c in self.controllers:
            c.on_key_release(key)
    
    def on_update(self, delta_time = 1/30):
        for e in self.explosion_list:
            e.lifetime -= 1
            if e.lifetime == 0:
                self.explosion_list.remove(e)
                self.sprite_list.remove(e.sprite)

        for b in self.bombs:
            if isinstance(b, Bomb):
                b.lifetime -= 1
                if b.lifetime == 0:
                    self.explose(b)
        for c in self.controllers:
            c.on_update()
            '''if isinstance(c, PlayerController):
                pos = to_map_vector(c.gameObject.position)
                self.logger.Message(f"Player position [{pos.x}, {pos.y}]")'''

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.sprite_list.draw()


def main():
    window = GameView()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()