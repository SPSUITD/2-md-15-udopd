SIZE = 0.4
SPRITE_SIZE = 64*2*SIZE
GRID_SIZE = (17, 13)
WINDOW_SIZE = (GRID_SIZE[0]*SPRITE_SIZE, GRID_SIZE[1]*SPRITE_SIZE)
WINDOW_TITLE = "B0mberm@n"

PLAYER_SPEED = 4*2*SIZE
BUFF_LIFETIME = 500
BUFF_PROBABILITY = 0.2

class TEXTURES:
    PLAYER_1 = ":resources:images/animated_characters/male_person/malePerson_idle.png"
    PLAYER_2 = ":resources:images/animated_characters/robot/robot_idle.png"
    BOMB = ":resources:images/tiles/bomb.png"
    WALL = ":resources:images/tiles/brickGrey.png"
    BLOCK = ":resources:images/tiles/boxCrate_double.png"
    EXPLOSION = ":resources:images/tiles/lava.png"
    ADD_BOMB = ":resources:images/items/coinSilver_test.png"
    ADD_EXPLOSION_SIZE = ":resources:images/items/gold_1.png"

class SYMBOLS:
    bomb = '@'
    wall = '#'
    empty = ' '
    block = '%'
    add_bomb = '+@'
    add_explosion_size = '+B'
    
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
    count = 1 #max count of active bombs
    lifetime = 150 #ticks
    size = 2 #cells
