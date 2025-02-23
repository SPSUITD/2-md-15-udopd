import arcade
from src.logger import Logger
from src.config import TEXTURES
from src.abstractobject import AbstractObject
from src.gameobject import GameObject
from src.player import Player
from src.spawner import Spawner
from src.vector import Vector
from src.keymap import KeyMap

SPRITE_SIZE = 32
WINDOW_WIDTH = 15*SPRITE_SIZE
WINDOW_HEIGHT = 13*SPRITE_SIZE
WINDOW_TITLE = "B0mberm@n"

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

        self.box = AbstractObject(
            sprite_path=TEXTURES.BOX,
            name='box',
            size=0.5
            )
        
        self.box1 = AbstractObject(
            sprite_path=TEXTURES.BOX1,
            name='box',
            size=0.5
            )
        
        self.__new__player__()
        self.__new__player__(name='player2', keymap=KeyMap('LEFT', 'UP', 'RIGHT', 'DOWN', 'BACKSPACE'), spawn_object=self.box1)
        
    def __camera_setup(self):
        self.camera = arcade.camera.Camera2D()
        self.camera.use()
        self.camera.position = (0, 0)
        self.game_objects.append(self.camera)

    def spawn(self, object: AbstractObject, position: Vector):
        new_go = GameObject(sprite=arcade.Sprite(object.sprite_path),
                            name=object.name,
                            size=object.size,
                            position=position)
        self.game_objects.append(new_go)
        self.sprite_list.append(new_go.sprite)

    def __new__player__(self, name = "player", position = Vector(0, 0), rotation = 0, size = 1, speed = 5, keymap = KeyMap(), spawn_object = None):
        player = Player(
            sprite=arcade.Sprite(arcade.load_texture(TEXTURES.PLAYER_TEXTURE)),
            name=name,
            size=size,
            rotation=rotation,
            position=position,
            speed=speed,
            keymap=keymap,
            spawner=Spawner(external_spawn=self.spawn, abstract_object=spawn_object) if spawn_object is not None else None
        )
        self.game_objects.append(player)
        self.sprite_list.append(player.sprite)
        self.controllers.append(player.controller)

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