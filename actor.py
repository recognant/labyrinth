import pygame
from const import *
from vector import Vector2 as Vec2
import random

class Way(list):

    LEFT = self(Direction.LEFT, Direction.LEFT)
    RIGHT = self(Direction.RIGHT, Direction.RIGHT)
    UP = self(Direction.UP, Direction.UP)
    DOWN = self(Direction.DOWN, Direction.DOWN)

    def __init__(self, d_in = 0, d_out = 0, *args, **kwargs):
        super(Way, self).__init__(*args, **kwargs)
        super(Way, self).append(d_in)
        super(Way, self).append(d_out)

    def append(self, item):
        pass

    @property
    def In(self):
        return super(Way, self).__getitem__(0)

    @property
    def Out(self):
        return super(Way, self).__getitem__(1)

    def find(self, d):
        if d == self.In:
            return self.Out
        return None

    def __getitem__(self, i):
        if 0<=i<2:
            return super(Vector2, self).__getitem__(i)
        else:
            raise Exception("Index out of bounds!")

class Ways(list):
    
    def __init__(self, ways, *args, **kwargs):
        super(Ways, self).__init__(*args, **kwargs)
        self.extend(ways)

    def find(self, d):
        ways = list()
        for _,way in enumerate(self):
            v = way.find(d)
            if v is not None:
                ways = ways + v
        return random.choice(ways)

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
            self.image.fill(Color.BLACK)
        else:
            self.image = pygame.transform.scale(image, (width, height))
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
        return self._x * Constants.FIELD_SIZE - self._parent.getCameraOffset()[0]

    def screenY(self):
        return self._y * Constants.FIELD_SIZE - self._parent.getCameraOffset()[1]

    def pos(self):
        return Vec2(self._x, self._y)

    def screenPos(self):
        return Constants.FIELD_SIZE * self.pos()

    def move(self, v):
        self.setPos(self.pos() + v)

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
        return self.screenX() <= v.x <= self.screenX() + self.width and self.screenY() <= v.y <= self.screenY() + self.height

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

class Animation(Entity):

    _images = None
    _dt = 0
    _cur = 0
    _duration = 1
    _speed = 1
    _frames = 0

    def __init__(self, world, images, x=0, y=0, width=32, height=32, duration=1):
        super(Animation, self).__init__(world, images[0], x, y, max(width, Constants.FIELD_SIZE), max(height, Constants.FIELD_SIZE))
        self._images = images
        self._duration = duration
        self._frames = len(images)
        self._speed = max(float(self._frames) / duration, 1.0)

    def update(self, dt):
        super(Animation, self).update(dt)
        self._dt = self._dt + self._speed * dt
        if self._dt >= 1:
            self._dt = self._dt - 1
            self._cur = self._cur + 1
            if self._cur < len(self._images):
                self.image = pygame.transform.scale(self._images[self._cur], self.rect.size)
            else:
                self.destroy()

class Field(Entity):

    _type = None

    def __init__(self, world, t, path, x, y):
        super(Field, self).__init__(world, path, x, y, Constants.FIELD_SIZE, Constants.FIELD_SIZE)
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
        super(Actor, self).__init__(world, path, x, y, Constants.FIELD_SIZE, Constants.FIELD_SIZE)

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
        elif self._dt >= 1:
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

class Crossing(Field):

    _ways = None

    def __init__(self, world, x, y, ways):
        super(CROSSING, self).__init__(world, FieldType.CROSSING, world.IMAGES_ARROW4, x, y)
        self._ways = ways

    def find(self, d):
        way = self._ways.find(d)
        if way is None:
            return d
        return way

    def isPassable(self):
        return True

    def isWalkable(self):
        return True

class Turner(Field):

    _d = None

    def __init__(self, world, x, y, direction=None):
        super(Turner, self).__init__(world, FieldType.TURNER, world.IMAGES_ARROW4, x, y)
        self._d = direction

    def direction(self, d):
        if self._d is None:
            return d
        return self._d

    def isPassable(self):
        return True

    def isWalkable(self):
        return True

class DualTurner(Turner):

    _d2 = None

    def __init__(self, world, x, y, directions=None):
        if len(directions) < 2:
            raise Exception()

        super(DualTurner, self).__init__(world, x, y, directions[0])
        self._d2 = directions[1]

    def direction(self, d):
        if d | self._d or d | self._d2:
            return random.choice((self._d, self._d2))
        if d == self._d or d | self._d:
            return self._d
        return self._d2

class TripleTurner(DualTurner):

    _d3 = None

    def __init__(self, world, x, y, directions=None):
        if len(directions) < 3:
            raise Exception()

        super(DualTurner, self).__init__(world, x, y, (directions[0], directions[1]))
        self._d3 = directions[2]

    def direction(self, d):
        if d == self._d:
            return self._d
        if d == self._d2:
            return self._d2
        if d == self._d3:
            return self._d3
        return random.choice((~d, -(~d)))

class Player(Actor):

    _dt = 0
    _speed = Constants.PLAYER_SPEED
    direction = Direction.LEFT
    
    def __init__(self, world, x, y):
        super(Player, self).__init__(world, world.IMAGES_WIZARD, x, y)

    def update(self, dt):
        self._dt = self._dt + self._speed * dt
        if self._dt >= 1:
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
