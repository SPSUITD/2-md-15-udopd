import arcade
import random

import src.config as cnf
from src.explosiongroup import ExplosionGroup
from src.logger import Logger
from src.keymap import KeyMap
from src.config import SYMBOLS as symb
from src.playercontroller import PlayerController
from src.player import Player
from src.abstractobject import AbstractObject
from src.bombspecifications import BombSpecifications, clone
from src.gameobject import GameObject
from src.bomb import Bomb
from src.vector import Vector, to_map_vector, to_global_vector, zero_vector, distance
from server import Server
from client import Client

class GameView(arcade.Window):
    def __init__(self, host_ip = ''):
        name = ''
        if host_ip != '':
            name = f"_host ({host_ip})"

        super().__init__(cnf.WINDOW_SIZE[0]+cnf.GUI_SIZE[0]*cnf.SPRITE_SIZE, cnf.WINDOW_SIZE[1]+cnf.GUI_SIZE[1]*cnf.SPRITE_SIZE, cnf.WINDOW_TITLE+name)
        self.background_color = arcade.csscolor.LIGHT_GREEN
        self.center_window()
        self.host_ip = host_ip

    def setup(self, count):
        self.logger = Logger()

        self.map = None
        self.sprite_list = arcade.SpriteList()
        self.bombs = []
        self.blocks = []
        self.buffs = []
        self.player_sprite = None
        self.explosion_list = []
        self.controllers = []
        
        self.clients = []
        self.servers = []
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
                    position=to_global_vector(Vector(cnf.PLAYER_POS[0][0], cnf.PLAYER_POS[0][1])),
                    bomb_specifications = self.bomb)
        
        if count == 0:
            self.setup_pvp_game()
        else:
            self.setup_localgame(count-1)
    
    def setup_pvp_game(self):
        self.__new_player__(keymap=KeyMap(
            left=cnf.PLAYER_2_KEYMAP.left,
            right=cnf.PLAYER_2_KEYMAP.right,
            up=cnf.PLAYER_2_KEYMAP.up,
            down=cnf.PLAYER_2_KEYMAP.down,
            spawn=cnf.PLAYER_2_KEYMAP.spawn
        ), 
                    name='player1',
                    texture_path=cnf.TEXTURES.PLAYER_2, 
                    position=to_global_vector(Vector(cnf.PLAYER_POS[1][0], cnf.PLAYER_POS[1][1])),
                    bomb_specifications = self.bomb)
            
    def setup_localgame(self, count):
        for i in range(count):
            self.servers.append(Server(self.host_ip+":555"+str(i), cnf.SERVER_DELTATIME))
        
        for i in range(count):
            self.__new_player__(keymap=KeyMap(
                left=cnf.PLAYER_1_KEYMAP.left,
                right=cnf.PLAYER_1_KEYMAP.right,
                up=cnf.PLAYER_1_KEYMAP.up,
                down=cnf.PLAYER_1_KEYMAP.down,
                spawn=cnf.PLAYER_1_KEYMAP.spawn
            ), 
                        name='player'+str(i+2),
                        texture_path=cnf.TEXTURES.PLAYER_2, 
                        position=to_global_vector(Vector(cnf.PLAYER_POS[i+1][0], cnf.PLAYER_POS[i+1][1])),
                        bomb_specifications = self.bomb,
                        source=self.servers[i],
                        connect_method=self.connect_client)

    def connect_client(self, ip):
        #self.logger.Message(f'{ip}_client successfully connected')
        self.clients.append(Client(ip+":5555"))

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
        
        self.add_bomb = AbstractObject(
            sprite_path=cnf.TEXTURES.ADD_BOMB,
            symbol=cnf.SYMBOLS.add_bomb,
            name='add_bomb'
            )
        
        self.add_explosion_size = AbstractObject(
            sprite_path=cnf.TEXTURES.ADD_EXPLOSION_SIZE,
            symbol=cnf.SYMBOLS.add_explosion_size,
            name='add_explosion_size'
            )

    def __camera_setup__(self):
        self.camera = arcade.camera.Camera2D()
        self.camera.position = ((cnf.WINDOW_SIZE[0]-cnf.SPRITE_SIZE)/2, (cnf.WINDOW_SIZE[1]+(cnf.GUI_SIZE[1]-1)*cnf.SPRITE_SIZE)/2)

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

            if  object.name == 'add_bomb' or object.name == 'add_explosion_size':
                new_go.lifetime = cnf.BUFF_LIFETIME
                self.buffs.append(new_go)
            
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
        explose_list = []
        for b in self.bombs:
            temp_contr_pos = to_map_vector(b.position)
            in_radius = distance(bomb_map_position, temp_contr_pos) < bomb.explosion_size
            if in_radius:
                is_vis = self.is_visible(bomb_map_position, temp_contr_pos)
                if is_vis and b != bomb:
                    self.logger.Message(f"bomb at [{bomb_map_position.x}, {bomb_map_position.y}] " + 
                                        f"explose the bomb at [{temp_contr_pos.x}, {temp_contr_pos.y}]")
                    explose_list.append(b)

        #обработка попаданий по иным объектам
        players = []
        for c in self.controllers:
            temp_contr_pos = to_map_vector(c.player.position)
            in_radius = distance(bomb_map_position, temp_contr_pos) < bomb.explosion_size
            if in_radius:
                is_vis = self.is_visible(bomb_map_position, temp_contr_pos)
                if is_vis:
                    players.append(c)
                    self.logger.Message(f"bomb at [{bomb_map_position.x}, {bomb_map_position.y}] " + 
                                        f"kill the {c.player.name} at [{temp_contr_pos.x}, {temp_contr_pos.y}]")
   
        buff_pos = []
        for buff in self.buffs:
            temp_contr_pos = to_map_vector(buff.position)
            in_radius = distance(bomb_map_position, temp_contr_pos) < bomb.explosion_size
            if in_radius:
                is_vis = self.is_visible(bomb_map_position, temp_contr_pos)
                if is_vis:
                    buff_pos.append(buff)
                    self.logger.Message(f"bomb at [{bomb_map_position.x}, {bomb_map_position.y}] " + 
                                        f"remove the buff at [{temp_contr_pos.x}, {temp_contr_pos.y}]")

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
        
        for p in players:
            if p.player.sprite in self.sprite_list:
                self.sprite_list.remove(p.player.sprite)
            self.controllers.remove(p) #заглушка
        for b in explose_list:
            self.explose(b)
        for buff in buff_pos:
            temp = to_map_vector(buff.position)
            if buff in buff_pos:
                self.buffs.remove(buff)
                self.map[temp.x][temp.y] = cnf.SYMBOLS.empty
            if buff.sprite in self.sprite_list:
                self.sprite_list.remove(buff.sprite)
        for bl in block_pos:
            temp = to_map_vector(bl.position)
            #проверка на случай, если несколько бомб с разных сторон взорвут один и тот же блок
            if bl in self.blocks:
                self.blocks.remove(bl)
                self.map[temp.x][temp.y] = cnf.SYMBOLS.empty
                self.__buff_spawn__(temp)
            if bl.sprite in self.sprite_list:
                self.sprite_list.remove(bl.sprite)
        

        self.map[bomb_map_position.x][bomb_map_position.y] = symb.empty
        self.sprite_list.remove(bomb.sprite)

    def __one_explosion__(self, pos: Vector, explosion_group: ExplosionGroup):
        new_go = GameObject(sprite=arcade.Sprite(self.explosion.sprite_path, cnf.SIZE),
                            name=self.explosion.name,
                            position=to_global_vector(pos))
        new_go.lifetime = 20
        explosion_group.sprite_list.append(new_go.sprite)
        #self.explosion_list.append(new_go)

    def __spawn_explosion__(self, pos: Vector, size: int):
        explosion_group = ExplosionGroup(20)
        for x in range(0, size):
            if pos.x - x >= 0:
                if self.map[pos.x - x][pos.y] == cnf.SYMBOLS.wall:
                    break
                self.__one_explosion__(Vector(pos.x - x, pos.y), explosion_group)
                if (self.map[pos.x - x][pos.y] == cnf.SYMBOLS.block or 
                    self.map[pos.x - x][pos.y] == cnf.SYMBOLS.add_bomb or
                    self.map[pos.x - x][pos.y] == cnf.SYMBOLS.add_explosion_size):
                    break
        for x in range(1, size):
            if pos.x + x < len(self.map):
                if self.map[pos.x + x][pos.y] == cnf.SYMBOLS.wall:
                    break
                self.__one_explosion__(Vector(pos.x + x, pos.y), explosion_group)
                if (self.map[pos.x + x][pos.y] == cnf.SYMBOLS.block or 
                    self.map[pos.x + x][pos.y] == cnf.SYMBOLS.add_bomb or
                    self.map[pos.x + x][pos.y] == cnf.SYMBOLS.add_explosion_size):
                    break
        for y in range(0, size):
            if pos.y - y >= 0:
                if self.map[pos.x][pos.y - y] == cnf.SYMBOLS.wall:
                    break
                self.__one_explosion__(Vector(pos.x, pos.y - y), explosion_group)
                if (self.map[pos.x][pos.y - y] == cnf.SYMBOLS.block or 
                    self.map[pos.x][pos.y - y] == cnf.SYMBOLS.add_bomb or
                    self.map[pos.x][pos.y - y] == cnf.SYMBOLS.add_explosion_size):
                    break
        for y in range(1, size):
            if pos.y + y < len(self.map[0]):
                if self.map[pos.x][pos.y + y] == cnf.SYMBOLS.wall:
                    break
                self.__one_explosion__(Vector(pos.x, pos.y + y), explosion_group)
                if (self.map[pos.x][pos.y + y] == cnf.SYMBOLS.block or 
                    self.map[pos.x][pos.y + y] == cnf.SYMBOLS.add_bomb or
                    self.map[pos.x][pos.y + y] == cnf.SYMBOLS.add_explosion_size):
                    break
        self.explosion_list.append(explosion_group)
    
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

    def __buff_spawn__(self, pos: Vector):
        if (random.randint(0, 100) / 100) < cnf.BUFF_PROBABILITY:
            if random.randint(0, 10) < 5:
                self.spawn(self.add_bomb, pos, None)
            else:
                self.spawn(self.add_explosion_size, pos, None)
    
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
            pos.x == cnf.GRID_SIZE[0]-2 and pos.y == 3 or
            
            pos.x == 1 and pos.y == 1 or #player3 safezone
            pos.x == 1 and pos.y == 2 or
            pos.x == 1 and pos.y == 3 or
            pos.x == 2 and pos.y == 1 or
            pos.x == 3 and pos.y == 1 or
            
            pos.x == cnf.GRID_SIZE[0]-2 and pos.y == cnf.GRID_SIZE[1]-2 or #player4 safezone
            pos.x == cnf.GRID_SIZE[0]-3 and pos.y == cnf.GRID_SIZE[1]-2 or
            pos.x == cnf.GRID_SIZE[0]-4 and pos.y == cnf.GRID_SIZE[1]-2 or
            pos.x == cnf.GRID_SIZE[0]-2 and pos.y == cnf.GRID_SIZE[1]-3 or
            pos.x == cnf.GRID_SIZE[0]-2 and pos.y == cnf.GRID_SIZE[1]-4)

        if safe_zone:
            pass
        else:
            if random.randint(0, 10) < 9:
                self.spawn(self.block, pos, None)

    def __new_player__(self, texture_path = cnf.TEXTURES.PLAYER_1,
                    name = "player", 
                    position = zero_vector(), 
                    speed = cnf.PLAYER_SPEED, 
                    keymap = KeyMap(), 
                    bomb_specifications = BombSpecifications,
                    source: Server = None,
                    connect_method = None):
        if keymap.is_valid:
            player = Player(
                    sprite=arcade.Sprite(arcade.load_texture(texture_path), cnf.SIZE),
                    name=name,
                    position=position,
                    speed=speed,
                    bomb_specifications=clone(bomb_specifications)
                )
            controller = PlayerController(
                keymap=keymap,
                spawn_bomb_method=self.spawn,
                player=player,
                map=self.map,
                rm_buff=self.remove_buff,
                source=source,
                connect_method=connect_method
            )
            self.player_sprite = player.sprite
            self.sprite_list.append(player.sprite)
            self.controllers.append(controller)
        else:
            self.logger.Error(('Невалидная карта кнопок', '__new_player__', 60, '> Карта кнопок принимает код несуществующей кнопки'))

    def on_key_press(self, key, modifiers):
        for c in self.controllers:
            if c.source is None:
                c.on_key_press(key)

    def on_key_release(self, key, modifiers):
        for c in self.controllers:
            if c.source is None:
                c.on_key_release(key)
    
    def remove_buff(self, buff_pos: Vector):
        for b in self.buffs:
            buff_map_pos = to_map_vector(b.position)
            if buff_map_pos.x == buff_pos.x and buff_map_pos.y == buff_pos.y: 
                self.map[buff_map_pos.x][buff_map_pos.y] = cnf.SYMBOLS.empty
                self.sprite_list.remove(b.sprite)
                self.buffs.remove(b)
                return

    def on_update(self, delta_time = 1/30):
        if self.explosion_list is not None:
            for g in self.explosion_list:
                g.lifetime -= 1
                if g.lifetime == 0:
                    self.explosion_list.remove(g)

        for b in self.bombs:
            if isinstance(b, Bomb):
                b.lifetime -= 1
                if b.lifetime == 0:
                    self.explose(b)

        for b in self.buffs:
            b.lifetime -= 1
            if b.lifetime == 0:
                self.remove_buff(to_map_vector(b.position))

        for c in self.controllers:
            c.on_update()
            if c.source is not None:
                c.server_update()
                
        for c in self.clients:
            players = [[(i.player.position.x, i.player.position.y), i.player.name] for i in self.controllers]

            explosions = []
            for i in self.explosion_list:
                for e in i.sprite_list:
                    explosions.append((e.center_x, e.center_y))

            #explosions = [[(i.position.x, i.position.y)] for i in self.explosion_list]
            data = {
                "map": self.map,
                "players": players,
                "eplosions": explosions,
            }
            c.push(data)

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.sprite_list.draw()
        for g in self.explosion_list:
            g.sprite_list.draw()


def start_game(host_api='', count=0):
    window = GameView(host_api)
    window.setup(count)
    arcade.run()