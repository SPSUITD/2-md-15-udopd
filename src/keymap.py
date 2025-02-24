from arcade import key as Key

class KeyMap:
    is_valid: bool

    class Button:
        key: Key
        is_pressed: bool

        def __init__(self, key):
            self.is_pressed = False
            self.key = getattr(Key, key)

    def __init__(self, left = 'A', up = 'W', right = 'D', down = 'S', spawn = None):
        if hasattr(Key, left) and hasattr(Key, up) and hasattr(Key, right) and hasattr(Key, down):
            self.is_valid = True
            self.left = self.Button(left)
            self.up = self.Button(up)
            self.right = self.Button(right)
            self.down = self.Button(down)

            if spawn is not None:
                if hasattr(Key, spawn):
                    self.spawn = getattr(Key, spawn)
                else:
                    self.is_valid = False  
            else:
                self.spawn = None
        else:
            self.is_valid = False        
