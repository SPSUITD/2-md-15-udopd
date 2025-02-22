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

        self.game_objects = list()
        self.sprite_list = arcade.SpriteList()
        self.controllers = list()
        self.__camera_setup()
        
        self.player = self.__player_setup()
        self.player.controller = Controller(speed=5,
                                            keymap=KeyMap(),
                                            game_object=self.player)
        self.controllers.append(self.player.controller)
        
        self.player1 = self.__player_setup(position=Vector(-40, 40))
        self.player1.controller = Controller(speed=3,
                                            keymap=KeyMap('LEFT', 'UP', 'RIGHT', 'DOWN'),
                                            game_object=self.player1)
        self.controllers.append(self.player1.controller)
        
    def __camera_setup(self):
        self.camera = arcade.camera.Camera2D()
        self.camera.use()
        self.camera.position = (0, 0)
        self.game_objects.append(self.camera)

    def __player_setup(self, name = "player", position = Vector(0, 0), rotation = 0, size = 1):
        player = GameObject(
            sprite=arcade.Sprite(arcade.load_texture(TEXTURES.PLAYER_TEXTURE)),
            name=name,
            size=size,
            rotation=rotation,
            position=position
        )
        self.game_objects.append(player)
        self.sprite_list.append(player.sprite)
        return player

    def on_key_press(self, key, modifiers):
        for c in self.controllers:
            c.on_key_press(key)

    def on_key_release(self, key, modifiers):
        for c in self.controllers:
            c.on_key_release(key)
    
    def on_update(self, delta_time = 1/30):
        for c in self.controllers:
            c.on_update()

    def on_draw(self):
        #if hasattr(self, 'logger'):
            #self.logger.Message("draw frame")
        self.clear()
        self.camera.use()
        self.sprite_list.draw()


def main():
    window = GameView()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()