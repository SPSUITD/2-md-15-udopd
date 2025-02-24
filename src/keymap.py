import arcade

class KeyMap:
    class Button:
        key: arcade.key
        is_pressed: bool

        def __init__(self, key):
            self.is_pressed = False
            self.key = key

    def __init__(self, left = 'A', up = 'W', right = 'D', down = 'S', spawn = 'SPACE'):
        if left != "" and up != "" and right != "" and down != "":
            if hasattr(arcade.key, left):
                self.left = self.Button(getattr(arcade.key, left))
            if hasattr(arcade.key, up):
                self.up = self.Button(getattr(arcade.key, up))
            if hasattr(arcade.key, right):
                self.right = self.Button(getattr(arcade.key, right))
            if hasattr(arcade.key, down):
                self.down = self.Button(getattr(arcade.key, down))

        if spawn is not None:
            if hasattr(arcade.key, spawn):
                self.spawn = getattr(arcade.key, spawn)
