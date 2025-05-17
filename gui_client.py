import arcade
import time
import math
import src.config as cnf

from src.bomb import Bomb
from src.keymap import KeyMap
from src.playercontroller import PlayerController
from src.vector import Vector, to_global_vector
from client import Client
from server import Server

class ClientView(arcade.Window):
    controller: PlayerController
    
    def __init__(self, server, client):
        super().__init__(cnf.WINDOW_SIZE[0], cnf.WINDOW_SIZE[1], cnf.WINDOW_TITLE+'_client')
        self.background_color = arcade.csscolor.LIGHT_GREEN
        self.center_window()
        self.direction = Vector(0, 0)
        self.map_list = arcade.SpriteList()
        self.bombs = arcade.SpriteList()
        self.players_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.current_state = None
        self.current_data = ''
        self.map = ''
        self.spawn = False

        self.controller = PlayerController(keymap=KeyMap(left=cnf.PLAYER_1_KEYMAP.left,
                      right=cnf.PLAYER_1_KEYMAP.right,
                      up=cnf.PLAYER_1_KEYMAP.up,
                      down=cnf.PLAYER_1_KEYMAP.down,
                      spawn=cnf.PLAYER_1_KEYMAP.spawn))
        
        self.camera = arcade.camera.Camera2D()
        self.camera.position = ((cnf.WINDOW_SIZE[0]-cnf.SPRITE_SIZE)/2, (cnf.WINDOW_SIZE[1]-cnf.SPRITE_SIZE)/2)

        self.server = server
        self.client = client
        self.draw_walls()
        
    def on_key_press(self, key, modifiers):
        self.controller.on_key_press(key)
        if key == self.controller.keymap.spawn and not self.spawn:
            self.spawn = True
            self.client.push({'action': 'spawn'})
        else:
            self.push_direction()

    def on_key_release(self, key, modifiers):
        if key == self.controller.keymap.spawn:
            self.spawn = False
        self.controller.on_key_release(key) 
        self.push_direction()
        
    def on_update(self, deltatime):
        self.controller.on_update()
        data = self.server.get_data()

        rem_bombs = []
        for b in self.bombs:
            b.lifetime += 1
            b.scale = cnf.SIZE* (0.9 - math.cos((b.lifetime / 10) % 180)/10)
            if b.lifetime >= cnf.BOMB_CONFIG.lifetime:
                rem_bombs.append(b)

        for rb in rem_bombs:
            self.bombs.remove(rb)
        
        if self.current_data != str(data):
            if 'map' in data and self.map != data['map']:
                self.map = data['map']
                self.draw_map()
            if 'players' in data:
                self.draw_players(data['players'])
            if 'explosions' in data:
                if data['explosions'] != 'None':
                    self.draw_explosions(data['explosions'])
                else:
                    self.explosions_list.clear()
            self.current_data = str(data)
        
    def on_draw(self):
        self.clear()
        self.players_list.draw()
        self.map_list.draw()
        self.bombs.draw()
        self.explosions_list.draw()
        self.wall_list.draw()
        self.camera.use()

    def push_direction(self):
        km = self.controller.keymap
        data = {
            'action': 'direction',
            'up': km.up.is_pressed,
            'down': km.down.is_pressed,
            'left': km.left.is_pressed,
            'right': km.right.is_pressed,
        }
        if self.current_state != data:
            self.current_state = data
            self.client.push(data)

    def draw_players(self, players):
        self.players_list.clear()
        for x in players:
            match x[1]:
                case "player1":
                    sprite_path = cnf.TEXTURES.PLAYER_1
                case _:
                    sprite_path = cnf.TEXTURES.PLAYER_2
            self.players_list.append(arcade.Sprite(sprite_path, 
                                                    cnf.SIZE,
                                                    x[0][0],
                                                    x[0][1]))
            
    def draw_explosions(self, explosions):
        rem_bombs = []
        
        for e in explosions:
            self.explosions_list.append(arcade.Sprite(cnf.TEXTURES.EXPLOSION, 
                                                    cnf.SIZE,
                                                    e[0],
                                                    e[1]))
            if self.bombs_contains(e[0], e[1]):
                for b in self.bombs:
                    if b.center_x == e[0] and b.center_y == e[1]:
                        rem_bombs.append(b)
                        break
        
        for rb in rem_bombs:
            if rb in self.bombs:
                self.bombs.remove(rb)

    def draw_map(self):
        self.map_list.clear()
        width = cnf.GRID_SIZE[0]
        height = cnf.GRID_SIZE[1]

        for x in range(width):
            for y in range(height):
                if not ((x == width-1 or x == 0 or y == 0 or y == height-1) or 
                    (x % 2 == 0 and y % 2 == 0)):
                    s = self.map[x][y]
                    pos = to_global_vector(Vector(x, y))
                    sprite_path = None
                    match s:
                        case cnf.SYMBOLS.block:
                            sprite_path = cnf.TEXTURES.BLOCK
                        case cnf.SYMBOLS.add_bomb:
                            sprite_path = cnf.TEXTURES.ADD_BOMB
                        case cnf.SYMBOLS.add_explosion_size:
                            sprite_path = cnf.TEXTURES.ADD_EXPLOSION_SIZE
                        case cnf.SYMBOLS.bomb:
                            temp = arcade.Sprite(cnf.TEXTURES.BOMB, 
                                                        cnf.SIZE,
                                                        pos.x,
                                                        pos.y)
                            if not self.bombs_contains(pos.x, pos.y):
                                temp.lifetime = 0
                                self.bombs.append(temp)
                    if sprite_path is not None and sprite_path is not cnf.TEXTURES.BOMB:
                        self.map_list.append(arcade.Sprite(sprite_path, 
                                                        cnf.SIZE,
                                                        pos.x,
                                                        pos.y))
    
    def bombs_contains(self, bomb_x, bomb_y):
        for b in self.bombs:
            if b.center_x == bomb_x and b.center_y == bomb_y:
                return True
        return False

    def draw_walls(self):
        width = cnf.GRID_SIZE[0]
        height = cnf.GRID_SIZE[1]

        for x in range(width):
            for y in range(height):
                if ((x == width-1 or x == 0 or y == 0 or y == height-1) or 
                    (x % 2 == 0 and y % 2 == 0)):
                    pos = to_global_vector(Vector(x, y))
                    self.wall_list.append(arcade.Sprite(cnf.TEXTURES.WALL, 
                                                          cnf.SIZE,
                                                          pos.x,
                                                          pos.y))

def start_game(host_ip, my_ip):
    client = Client(host_ip)
    my_ip += ":5555"
    client.push({
            'connect': my_ip,
            })
    server = Server(my_ip)
    while not ('game_size' in server.get_data()):
        time.sleep(0.1)
    
    size = server.get_data()['game_size']
    cnf.SIZE = size
    cnf.SPRITE_SIZE = 128*size
    cnf.PLAYER_SPEED = 8*size
    cnf.WINDOW_SIZE = (cnf.GRID_SIZE[0]*cnf.SPRITE_SIZE, 
                       (cnf.GRID_SIZE[1])*cnf.SPRITE_SIZE)
        
    ClientView(server, client)
    arcade.run()
    