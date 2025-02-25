import arcade

from src.logger import Logger
import src.config as cnf
from src.config import SYMBOLS as symb, BOMB_CONFIG as bc
from src.playercontroller import PlayerController, KeyMap, Spawner, AbstractObject, GameObject, Player, BombSpecifications
from src.bomb import Bomb
from src.vector import Vector, to_map_vector, to_global_vector, zero_vector, distance
from src.bombcontroller import BombController

class GameView(arcade.Window):
    def __init__(self):
        super().__init__(cnf.WINDOW_SIZE.x, cnf.WINDOW_SIZE.y, cnf.WINDOW_TITLE)
        self.background_color = arcade.csscolor.LIGHT_GREEN
        self.center_window()

    def setup(self):
        self.logger = Logger()

        self.map = None
        self.sprite_list = arcade.SpriteList()
        self.controllers = []
        self.__camera_setup__()
        self.__setup_abstract_objects__()
        self.__create_map__()
        self.__new_player__(keymap=cnf.PLAYER_1_KEYMAP, 
                            spawn_object=self.bomb, 
                            size=0.5, #заглушка, так как исходные текстуры персонажей бОльшего размера, чем тайлы
                            texture_path=cnf.TEXTURES.PLAYER_1, 
                            position=to_global_vector(Vector(1, cnf.GRID_SIZE.y-2)))
        
        '''self.__new_player__(keymap=cnf.PLAYER_2_KEYMAP, 
                            spawn_object=self.bomb, 
                            size=0.5, #заглушка, так как исходные текстуры персонажей бОльшего размера, чем тайлы
                            texture_path=cnf.TEXTURES.PLAYER_2,
                            position=to_global_vector(Vector(cnf.GRID_SIZE.x-2, 1)))'''
    
    def __setup_abstract_objects__(self):
        self.bomb = AbstractObject(
            sprite_path=cnf.TEXTURES.BOMB,
            name='bomb',
            size=0.5
            )
        
        self.wall = AbstractObject(
            sprite_path=cnf.TEXTURES.WALL,
            name='wall',
            size=0.5
            )
        
        self.block = AbstractObject(
            sprite_path=cnf.TEXTURES.BLOCK,
            name='block',
            size=0.5
            )

    def __camera_setup__(self):
        self.camera = arcade.camera.Camera2D()
        self.camera.position = ((cnf.GRID_SIZE.x-1)*cnf.SPRITE_SIZE/2, (cnf.GRID_SIZE.y-1)*cnf.SPRITE_SIZE/2)

    def spawn(self, object: AbstractObject, position: Vector, bomb_specification: BombSpecifications = None, bomb_list: list = None):
        map_pos = to_map_vector(position)
        if self.map[map_pos.x][map_pos.y] == symb.empty:

            if object.name == 'bomb':
                new_go = Bomb(sprite=arcade.Sprite(object.sprite_path, cnf.SIZE),
                              name=object.name,
                              size=object.size,
                              position=to_global_vector(map_pos),
                              lifetime=bomb_specification.lifetime,
                              explosion_size=bomb_specification.size,
                              lst=bomb_list)
                self.controllers.append(BombController(new_go, self.explose))
                self.map[map_pos.x][map_pos.y] = symb.bomb
                bomb_list.append(new_go)
            else:
                new_go = GameObject(sprite=arcade.Sprite(object.sprite_path, cnf.SIZE),
                                    name=object.name,
                                    size=object.size,
                                    position=to_global_vector(map_pos))
                self.map[map_pos.x][map_pos.y] = symb.wall

            self.sprite_list.append(new_go.sprite)
            self.logger.Message(f"{object.name} spawn at [{map_pos.x}, {map_pos.y}]")
        else:
            self.logger.Warning(f"invalid spawn {object.name} at [{map_pos.x}, {map_pos.y}]")

    def explose(self, bomb_controller: BombController):
        if isinstance(bomb_controller.gameObject, Bomb):
            if bomb_controller.gameObject in bomb_controller.gameObject.parent_list:
                bomb_controller.gameObject.parent_list.remove(bomb_controller.gameObject)

        self.controllers.remove(bomb_controller)
        bomb_map_position = to_map_vector(bomb_controller.gameObject.position)
        self.logger.Message(f"bomb explose at [{bomb_map_position.x}, {bomb_map_position.y}]")

        for c in self.controllers:
            temp_contr_pos = to_map_vector(c.gameObject.position)
            is_vis = self.is_visible(bomb_map_position, temp_contr_pos)
            in_radius = distance(bomb_map_position, temp_contr_pos) < bomb_controller.gameObject.explosion_size
            if (is_vis and in_radius):
                if isinstance(c, BombController):
                        self.logger.Message(f"bomb at [{bomb_map_position.x}, {bomb_map_position.y}] " + 
                                            f"find the bomb at [{temp_contr_pos.x}, {temp_contr_pos.y}]")
                        c.explose()
                elif isinstance(c, PlayerController):
                    self.controllers.remove(c) #заглушка
                    self.logger.Message(f"bomb at [{bomb_map_position.x}, {bomb_map_position.y}] " + 
                                        f"kill the {c.gameObject.name} at [{temp_contr_pos.x}, {temp_contr_pos.y}]")
                    

        self.map[bomb_map_position.x][bomb_map_position.y] = symb.empty
        self.sprite_list.remove(bomb_controller.gameObject.sprite)
    
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
        width = cnf.GRID_SIZE.x
        height = cnf.GRID_SIZE.y
        self.map = [[symb.empty] * height for i in range(width)]

        for x in range(width):
            for y in range(height):
                if ((x == width-1 or x == 0 or y == 0 or y == height-1) or 
                    (x % 2 == 0 and y % 2 == 0)):
                    self.spawn(self.wall, to_global_vector(Vector(x, y)))
        
        self.logger.Message(f"====Map is created====")

    def __new_player__(self, texture_path = cnf.TEXTURES.PLAYER_1,
                    name = "player", 
                    position = zero_vector(), 
                    rotation = 0, 
                    size = 1, 
                    speed = 4, 
                    keymap = KeyMap(), 
                    spawn_object = None):
        if keymap.is_valid:
            bc = cnf.BOMB_CONFIG
            player = Player(
                    sprite=arcade.Sprite(arcade.load_texture(texture_path), cnf.SIZE),
                    name=name,
                    size=size,
                    rotation=rotation,
                    position=position,
                    speed=speed*cnf.SIZE,
                    bomb_specifications=BombSpecifications(bc.count, bc.lifetime, bc.explosion_size)
                )
            controller = PlayerController(
                keymap=keymap,
                spawner=Spawner(external_spawn=self.spawn, abstract_object=spawn_object) if spawn_object is not None else None,
                player=player
            )
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