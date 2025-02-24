from src.controller import Controllable
from src.bomb import Bomb

class BombController(Controllable):
    bomb: Bomb

    def __init__(self, bomb: Bomb, external_explose):
        self.bomb = bomb
        self.__external_explose = external_explose

    def on_update(self):
        self.bomb.lifetime -= 1
        if self.bomb.lifetime == 0:
           if self.__external_explose is not None:
                self.__external_explose(self.bomb)
                del self
    
    def on_key_release(self, key):
        pass
    
    def on_key_press(self, key):
        pass