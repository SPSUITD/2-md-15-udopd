from src.abstractobject import AbstractObject
from src.bombspecifications import BombSpecifications

class Spawner:
    def __init__(self, external_spawn, abstract_object: AbstractObject):
        self.__external_spawn = external_spawn
        self.__abstract_object = abstract_object

    def spawn(self, position, specifications):
        if self.__abstract_object is not None:
            self.__external_spawn(self.__abstract_object, position, specifications)