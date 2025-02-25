from src.abstractobject import AbstractObject
from src.player import Player
from src.logger import Logger

class Spawner:
    bomb_list: list

    def __init__(self, external_spawn, abstract_object: AbstractObject):
        self.__external_spawn = external_spawn
        self.__abstract_object = abstract_object
        self.bomb_list = list()

    def spawn(self, player: Player):
        if len(self.bomb_list) < player.bomb_specifications.count:
            if self.__abstract_object is not None:
                self.__external_spawn(self.__abstract_object, player.position, player.bomb_specifications, self.bomb_list)
        else:
            Logger().Warning(f"invalid bomb spawn (max number ({player.bomb_specifications.count}) of bomb already on map)")