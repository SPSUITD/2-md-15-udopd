class AbstractObject:
    def __init__(self, sprite_path: str, size: float, name: str):
        self.sprite_path = sprite_path
        self.size = size
        self.name = name