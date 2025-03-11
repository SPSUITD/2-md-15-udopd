import arcade
import sys

import src.config as cnf
from src.keymap import KeyMap
from src.playercontroller import PlayerController
from src.vector import Vector, to_global_vector
from client import Client
from server import Server

class ClientView(arcade.Window):
    controller: PlayerController
    
    def __init__(self, ip):
        super().__init__(cnf.WINDOW_SIZE[0]+cnf.GUI_SIZE[0]*cnf.SPRITE_SIZE, cnf.WINDOW_SIZE[1]+cnf.GUI_SIZE[1]*cnf.SPRITE_SIZE, cnf.WINDOW_TITLE+'_client_'+ip)
        self.background_color = arcade.csscolor.LIGHT_GREEN
        self.center_window()
        self.direction = Vector(0, 0)
        self.sprite_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.map = []
        self.players = []
        self.eplosions = []

        self.controller = PlayerController(keymap=KeyMap(left=cnf.PLAYER_1_KEYMAP.left,
                      right=cnf.PLAYER_1_KEYMAP.right,
                      up=cnf.PLAYER_1_KEYMAP.up,
                      down=cnf.PLAYER_1_KEYMAP.down,
                      spawn=cnf.PLAYER_1_KEYMAP.spawn))
        
        self.camera = arcade.camera.Camera2D()
        self.camera.position = ((cnf.WINDOW_SIZE[0]-cnf.SPRITE_SIZE)/2, (cnf.WINDOW_SIZE[1]+(cnf.GUI_SIZE[1]-1)*cnf.SPRITE_SIZE)/2)

        self.draw_walls()
        self.client_setup(ip)
        self.server_setup(ip+'1')

    def client_setup(self, ip):
        self.client = Client(ip)

    def server_setup(self, ip):
        self.server = Server(ip, cnf.SERVER_DELTATIME)
        
    def on_key_press(self, key, modifiers):
        self.controller.on_key_press(key)
        if key == self.controller.keymap.spawn:
            data = {
                'action': 'spawn'
            }
            self.client.push(data)
        else:
            self.push_direction()

    def on_key_release(self, key, modifiers):
        self.controller.on_key_release(key)
        self.push_direction()
        
    def on_update(self, deltatime):
        self.controller.on_update()
        data = self.server.get_data()
        if data is not None and 'map' in data:
            self.map = data['map']
            self.players = data['players']
            self.eplosions = data['eplosions']
        
    def on_draw(self):
        self.clear()
        self.draw_map()
        self.sprite_list.draw()
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
        self.client.push(data)

    def draw_map(self):            
        if self.map is not None and len(self.map) != 0:
            self.sprite_list.clear()

            if self.players is not None and len(self.players) != 0:
                for x in self.players:
                    sprite_path = cnf.TEXTURES.PLAYER_1 if x[1] == 'player1' else cnf.TEXTURES.PLAYER_2
                    self.sprite_list.append(arcade.Sprite(sprite_path, 
                                                                cnf.SIZE,
                                                                x[0][0],
                                                                x[0][1]))
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
                                sprite_path = cnf.TEXTURES.BOMB
                        if sprite_path is not None:
                            self.sprite_list.append(arcade.Sprite(sprite_path, 
                                                            cnf.SIZE,
                                                            pos.x,
                                                            pos.y))
            
            if self.eplosions is not None and len(self.eplosions) != 0:
                for e in self.eplosions:
                    self.sprite_list.append(arcade.Sprite(cnf.TEXTURES.EXPLOSION, 
                                                                cnf.SIZE,
                                                                e[0],
                                                                e[1]))
    
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


def main(port):
    ClientView(ip='127.0.0.1:'+port)
    arcade.run()

if __name__ == "__main__":
    main(sys.argv[1])