import pygame
from color import *
import const
from vector import Vector2 as Vec2

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

class Entity(pygame.sprite.Sprite):

    _parent = None
    __selected = 0
    _active = True
    _x = 0
    _y = 0

    def __init__(self, parent, image = None, x=0, y=0, width=32, height=32):
        super(Entity, self).__init__()
        self._parent = parent
        if image is None:
            self.image = pygame.Surface([width, height])
            self.image.fill(Color.BLACK())
        else:
            self.image = image
            self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.normalize()
        self._x = x
        self._y = y

    def render(self, display):
        display.blit(self.image, self.rect)

    def parent(self):
        return self._parent

    def update(self, dt):
        self.rect.x, self.rect.y = self.screenX(), self.screenY() 

    def screenX(self):
        return self._x * const.FIELD_SIZE - self._parent.getCameraOffset()[0]

    def screenY(self):
        return self._y * const.FIELD_SIZE - self._parent.getCameraOffset()[1]

    def pos(self):
        return Vec2(self._x, self._y)

    def screenPos(self):
        return const.FIELD_SIZE * self.pos()

    def move(self, v):
        self.setPos(self.pos() - v)

    def setPos(self, v):
        self._x = v.x
        self._y = v.y
        self.rect.x, self.rect.y = self.screenX(), self.screenY()

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self.rect.width

    @property
    def height(self):
        return self.rect.height

    def size(self):
        return vec(self.rect.width, self.rect.height)
    
    def clicked(self, v):
        mX = v.x
        mY = v.y
        return self.screenX()<=mX<=self.screenX() + self.width and self.screenY()<=mY<=self.screenY() + self.height

    def select(self):
        if self.__selected == 0:
            self.__selected = 1
            self._select()

    def _select(self):
        self.image.set_alpha(0.5)

    def deselect(self):
        if self.__selected == 1:
            self.__selected = 0
            self._deselect()

    def _deselect(self):
        self.image.set_alpha(1.0)

    def selected(self):
        return self.__selected == 1

    def isActive(self):
        return self._active

    def setActive(self, active):
        self._active = active

    def destroy(self):
        self.kill()

class Field(Entity):

    _type = None

    def __init__(self, world, t, path, x, y):
        super(Field, self).__init__(world, path, x, y, const.FIELD_SIZE, const.FIELD_SIZE)
        self._type = t

    def getType(self):
        return self._type

    def isPassable(self):
        if self._type is None:
            return False
        return True

    def isWalkable(self):
        return False

class Actor(Entity):
    
    def __init__(self, world, path, x, y):
        super(Actor, self).__init__(world, path, x, y, const.FIELD_SIZE, const.FIELD_SIZE)

class Block(Field):

    def __init__(self, world, x, y):
        super(Block, self).__init__(world, FieldType.BLOCK, world.IMAGES_BLOCK, x, y)

    def isPassable(self):
        return False

class Free(Field):

    _crate = False
    _bomb = -1
    _dt = 0
    _item = None

    def __init__(self, world, x, y):
        super(Free, self).__init__(world, FieldType.FREE, world.IMAGES_GRASS, x, y)

    def hasCrate(self):
        return self._crate

    def setCrate(self, val):
        self._crate = val
        if self._crate:
            self.image = self._parent.IMAGES_CRATE
        else:
            self.image = self._parent.IMAGES_GRASS
        pygame.transform.scale(self.image, (self.width, self.height))

    def hasBomb(self):
        return self._bomb >= 0

    def setBomb(self, bomb):
        if isinstance(bomb, int):
            self._bomb = bomb

    def update(self, dt):
        super(Field, self).update(dt)
        self._dt = self._dt + dt
        if self._bomb < 0:
            self._dt = 0
        elif self._dt > 1:
            self._dt = self._dt - 1
            self._bomb = self._bomb - 1
        if -1 < self._bomb <= 0:
            self._bomb = -1
            self._parent.explode(self.pos())

    def hasItem(self):
        return self.hasCrate() or self.hasBomb()

    def isPassable(self):
        return not self.hasCrate()

    def isWalkable(self):
        return True

class Turner(Field):

    _direction = None

    def __init__(self, world, x, y, direction=None):
        super(Turner, self).__init__(world, FieldType.TURNER, world.IMAGES_ARROW4, x, y)
        self._direction = direction

    @property
    def direction(self):
        if self._direction is None:
            return Direction.RIGHT
        return self._direction

    def isPassable(self):
        return True

    def isWalkable(self):
        return True

class Player(Actor):

    _dt = 0
    _speed = const.PLAYER_SPEED
    direction = Direction.LEFT
    
    def __init__(self, world, x, y):
        super(Player, self).__init__(world, world.IMAGES_WIZARD, x, y)

    def update(self, dt):
        self._dt = self._dt + self._speed * dt
        if self._dt > 1:
            if self._parent.canMove(self.pos(), self.direction):
                self._parent.move(self.direction)
            else:
                right = Vec2(-self.direction.y, self.direction.x)
                left = -Vec2(-self.direction.y, self.direction.x)
                back = -Vec2(self.direction.x, self.direction.y)
                if self._parent.canMove(self.pos(), right):
                    self.direction = right
                elif self._parent.canMove(self.pos(), left):
                    self.direction = left
                elif self._parent.canMove(self.pos(), back):
                    self.direction = back
                self._parent.move(self.direction)
                    
            self._dt = self._dt - 1
        super(Player, self).update(dt)
