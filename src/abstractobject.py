class AbstractObject:
    sprite_path: str
    sprite_size: float
    name: str
    symbol: str    

    def __init__(self, sprite_path: str, name: str, sprite_size = 0.5, symbol: str = ' '):
        self.sprite_path = sprite_path
        self.sprite_size = sprite_size
        self.name = name
        self.symbol = symbol