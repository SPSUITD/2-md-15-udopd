from arcade import SpriteList

class ExplosionGroup:
    lifetime: int
    sprite_list: SpriteList

    def __init__(self, lifetime):
        self.sprite_list = SpriteList()
        self.lifetime = lifetime