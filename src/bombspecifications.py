from src.abstractobject import AbstractObject

class BombSpecifications(AbstractObject):
    def __init__(self, count: int, lifetime: int, size: int, sprite_path: str, symbol: str):
        super().__init__(sprite_path=sprite_path, name='bomb', symbol=symbol)
        self.count = count
        self.lifetime = lifetime
        self.size = size

def clone(self: BombSpecifications):
    return BombSpecifications(self.count, self.lifetime, self.size, self.sprite_path, self.symbol)