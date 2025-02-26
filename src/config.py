SIZE = 0.5
ABSOLUTE_SIZE = 64
SPRITE_SIZE = ABSOLUTE_SIZE
GRID_SIZE = (17, 13)
WINDOW_SIZE = (GRID_SIZE[0]*SPRITE_SIZE, GRID_SIZE[1]*SPRITE_SIZE)
WINDOW_TITLE = "B0mberm@n"

class TEXTURES:
    PLAYER_1 = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
    PLAYER_2 = ":resources:images/animated_characters/robot/robot_idle.png"
    BOMB = ":resources:images/tiles/bomb.png"
    WALL = ":resources:images/tiles/brickGrey.png"
    BLOCK = ":resources:images/tiles/boxCrate_double.png"
    EXPLOSION = ":resources:images/tiles/lava.png"

class SYMBOLS:
    bomb = '@'
    wall = '#'
    empty = ' '
    block = '%'
    
class PLAYER_1_KEYMAP:
    left='A'
    right='D'
    up='W'
    down='S'
    spawn='SPACE'

class PLAYER_2_KEYMAP:
    left='LEFT'
    right='RIGHT'
    up='UP'
    down='DOWN'
    spawn='BACKSPACE'

class BOMB_CONFIG:
    count = 3 #max count of active bombs
    lifetime = 100 #ticks
    size = 3 #cells
