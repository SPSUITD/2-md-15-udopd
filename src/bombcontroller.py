from src.controllable import Controllable
from src.bomb import Bomb

class BombController(Controllable):
    def __init__(self, bomb: Bomb, external_explose):
        self.gameObject = bomb
        self.__external_explose = external_explose

    def on_update(self):
        if isinstance(self.gameObject, Bomb):
            self.gameObject.lifetime -= 1
            if self.gameObject.lifetime == 0:
                if self.__external_explose is not None:
                    self.explose()
    
    def on_key_release(self, key):
        pass
    
    def on_key_press(self, key):
        pass

    def explose(self):
        self.__external_explose(self)