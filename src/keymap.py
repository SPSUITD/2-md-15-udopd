import arcade
from src.logger import Logger

class KeyMap:    
    def __init__(self, left = 'A', up = 'W', right = 'D', down = 'S'):
        if left != "" and up != "" and right != "" and down != "":
            if hasattr(arcade.key, left):
                self.left = getattr(arcade.key, left)
            if hasattr(arcade.key, up):
                self.up = getattr(arcade.key, up)
            if hasattr(arcade.key, right):
                self.right = getattr(arcade.key, right)
            if hasattr(arcade.key, down):
                self.down = getattr(arcade.key, down)
        #Logger().Message(f'init KeyMap[{self.left}, {self.up}, {self.right}, {self.down}]')
