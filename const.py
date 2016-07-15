from vector import Vector2 as Vec2

class Constants():
    SCREEN_WIDTH = 600#1366
    SCREEN_HEIGHT = 400#768
    FPS = 30
    FIELD_SIZE = 64
    PLAYER_SPEED = 1

class Arsenal():
    BLOCK = 0
    CRATE = 1
    TURNER = 2
    BOMB = 3

class FieldType():
    BLOCK = 0
    FREE = 1
    TURNER = 2

class Direction():
    LEFT = Vec2(-1, 0)
    RIGHT = Vec2(1, 0)
    UP = Vec2(0, -1)
    DOWN = Vec2(0, 1)

class ItemType():
    CRATE = 0
    BOMB = 0

class Color():
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
