SIZE = 0.3
SPRITE_SIZE = 128*SIZE
GRID_SIZE = (17, 13)
WINDOW_SIZE = (GRID_SIZE[0]*SPRITE_SIZE, (GRID_SIZE[1])*SPRITE_SIZE)
WINDOW_TITLE = "B0mberm@n"

SCREEN_DELAY = 100
PLAYER_SPEED = 8*SIZE
BUFF_LIFETIME = 500
BUFF_PROBABILITY = 0.2

PLAYER_POS = [(1, GRID_SIZE[1]-2),
              (GRID_SIZE[0]-2, 1),
              (1, 1),
              (GRID_SIZE[0]-2, GRID_SIZE[1]-2)]

class TEXTURES:
    PLAYER_1 = "sprites/character1.png"
    PLAYER_2 = "sprites/character2.png"
    BOMB = "sprites/bomb.png"
    WALL = "sprites/wall.png"
    BLOCK = "sprites/block.png"
    EXPLOSION = "sprites/explosion.png"
    ADD_BOMB = "sprites/buffBomb.png"
    ADD_EXPLOSION_SIZE = "sprites/buffPower.png"
    WIN2 = "sprites/2win.png"
    WIN1 = "sprites/1win.png"
    YOU_WIN = "sprites/youwin.png"
    YOU_LOSE = "sprites/youlose.png"

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
    count = 1
    lifetime = 150
    size = 2
    