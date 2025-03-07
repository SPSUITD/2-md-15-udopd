import arcade

import src.config as cnf
from src.keymap import KeyMap
from src.playercontroller import PlayerController
from src.vector import Vector
from client import Client

class ClientView(arcade.Window):
    controller: PlayerController
    
    def __init__(self):
        super().__init__(300, 200, 'Client')
        self.background_color = arcade.csscolor.BLACK
        self.direction = Vector(0, 0)

        self.controller = PlayerController(keymap=KeyMap(left=cnf.PLAYER_2_KEYMAP.left,
                      right=cnf.PLAYER_2_KEYMAP.right,
                      up=cnf.PLAYER_2_KEYMAP.up,
                      down=cnf.PLAYER_2_KEYMAP.down,
                      spawn=cnf.PLAYER_2_KEYMAP.spawn))

        self.client_setup()

    def client_setup(self):
        self.c = Client('127.0.0.1:5555')
        
    def on_key_press(self, key, modifiers):
        self.controller.on_key_press(key)
        self.c.on_key_press(key)

    def on_key_release(self, key, modifiers):
        self.controller.on_key_release(key)
        self.c.on_key_release(key)
    
    def on_update(self, deltatime):
        self.controller.on_update()

    def on_draw(self):
        self.clear()


def main():
    window = ClientView()
    arcade.run()

if __name__ == "__main__":
    main()