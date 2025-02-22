import arcade
from src.logger import Logger
from src.config import _ as TEXTURES
from src.gameobject import GameObject
from src.vector import Vector
from src.keymap import KeyMap
from src.controller import Controller

SPRITE_SIZE = 64
WINDOW_WIDTH = 15*SPRITE_SIZE
WINDOW_HEIGHT = 13*SPRITE_SIZE
WINDOW_TITLE = "Bomberman"

class GameView(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        self.background_color = arcade.csscolor.LIGHT_GREEN

    def setup(self):
        self.logger = Logger()
        self.camera = arcade.camera.Camera2D()
        self.camera.use()
        self.camera.position = (0, 0)

        self.game_objects = list()

        self.player = self.__player_init__()
        self.game_objects.append(self.player)
        self.game_objects.append(self.camera)
        self.player_controller = Controller(speed=5, 
                                       keymap=KeyMap(), 
                                       game_object=self.player)
        
    def on_key_press(self, key, modifiers):
        self.player_controller.on_key_press(key)

    def on_key_release(self, key, modifiers):
        self.player_controller.on_key_release(key)
    
    def on_update(self, delta_time = 30):
        self.player_controller.on_update()

    def __player_init__(self):
        player = GameObject(
            sprite=arcade.Sprite(arcade.load_texture(TEXTURES.PLAYER_TEXTURE)),
            name="player",
            position=Vector(0, 0),
            rotation=0
        )
        return player


    def on_draw(self):
        #if hasattr(self, 'logger'):
            #self.logger.Message("draw frame")

        self.clear()
        self.camera.use()
        
        arcade.draw_sprite(self.player.sprite)


def main():
    window = GameView()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()