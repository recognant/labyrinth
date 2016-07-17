import pygame
import const
from actor import *
from vector import Vector2 as Vec2
from level import *
from spritesheet import *

class World(pygame.sprite.OrderedUpdates):

    __running = False
    __completed = False
    __camera = None
    __mapLayer = None
    __level = None

    __startPoint = (0, 0)
    __finishPoint = (0, 0)

    __arsenal = [Arsenal.CRATE, Arsenal.BOMB, Arsenal.CRATE, Arsenal.CRATE, Arsenal.CRATE, Arsenal.BOMB]

    def __init__(self):
        super(World, self).__init__()
        self.__loadResources()
        self.__walls = Layer(0)
        self.__way = Layer(1)
        self.__animations = Layer(2)

    def __loadResources(self):
        self.IMAGES_WIZARD = pygame.image.load("res/wizard_male.png")
        self.IMAGES_BLOCK = pygame.image.load("res/block_32x32.png")
        self.IMAGES_GRASS = pygame.image.load("res/grass_64x64.png")
        self.IMAGES_WATER = pygame.image.load("res/water_64x64.png")
        self.IMAGES_ARROW4 = pygame.image.load("res/arrow4_64x64.png")
        self.IMAGES_CRATE = pygame.image.load("res/crate_64x64.png")
        self.IMAGES_EXPLOSION = Spritesheet("res/explosion3.png").images_at(
            ((0,0,128,128),(128,0,128,128),(256,0,128,128),(384,0,128,128),
             (0,128,128,128),(128,128,128,128),(256,128,128,128),(384,128,128,128),
             (0,256,128,128),(128,256,128,128),(256,256,128,128),(384,256,128,128),
             (0,384,128,128),(128,384,128,128),(256,384,128,128),(384,384,128,128)), colorkey=(0,0,0))

    def create(self, level):
        if level.isDefective():
            raise Exception("Level is defective!")

        self.__level = level
        self.__boundaries = Vec2(level.dim[0], level.dim[1])
        
        self.__world = [[0 for j in range(self.__boundaries.y)] for i in range(self.__boundaries.x) ]
        self.__camera = Camera(self)

        for i in range(self.__boundaries.x):
            for j in range(self.__boundaries.y):
                if level.data[i][j] == "W":
                    actor = Block(self, i, j)
                    self.__walls.add(actor)
                    self.__world[i][j] = actor
                if level.data[i][j] == "0" or level.data[i][j] == "S" or level.data[i][j] == "E" or level.data[i][j] == "C":
                    actor = Free(self, i, j)
                    self.__way.add(actor)
                    self.__world[i][j] = actor
                if level.data[i][j] == "S":
                    self.__startPoint = Vec2(i, j)
                    self.player = Player(self, i, j)
                    self.add(self.player)
                if level.data[i][j] == "E":
                    self.__finishPoint = Vec2(i, j)
                if level.data[i][j] == "C":
                    self.__world[i][j].setCrate(True)

    def reset(self):
        if self.__level is not None:
            self.stop()
            self.destroy()
            self.create(self.__level)
            return True
        return False
        
    def render(self, display):
##        for i in range(self.__boundaries.x):
##            for j in range(self.__boundaries.y):
##                self.__world[i][j].render(display)
        self.__way.render(display)
        self.__walls.render(display)
        super(World, self).draw(display)
        self.__animations.render(display)

    def update(self, dt):
        if not self.__running or self.__completed:
            return

        self.__way.update(dt)
        self.__walls.update(dt)
        self.player.update(dt)
        super(World, self).update(dt)
        self.__animations.update(dt)
        #self.__camera.pan(self.player.screenPos())

    def start(self):
        self.__running = True

    def stop(self):
        self.__running = False

    def canMove(self, p, d):
        i, j = (p.x + d.x) % self.__boundaries.x, (p.y + d.y) % self.__boundaries.y
        dx, dy = d
        passable = self.__world[i][j].isPassable()
        if not passable:
            k = max(self.__boundaries.x, self.__boundaries.y)
            while self.__world[i][j].isWalkable() and not self.__world[i][j].isPassable() and k > 0:
                i, j = (i + dx) % self.__boundaries.x, (j + dy) % self.__boundaries.y
                k = k - 1
            return self.__world[i][j].isWalkable() and self.__world[i][j].isPassable()
        return passable

    def move(self, d):
        i, j = self.player.pos()
        i, j = (i + d.x) % self.__boundaries.x, (j + d.y) % self.__boundaries.y
        self.player.setPos(Vec2(i, j))
        dx, dy = d
        if self.__world[i][j].getType() == FieldType.FREE and self.__world[i][j].hasCrate():
            field = self.__world[i][j]
            while self.__world[i][j].isWalkable() and not self.__world[i][j].isPassable() and self.__world[i][j].hasCrate():
                i, j = (i + dx) % self.__boundaries.x, (j + dy) % self.__boundaries.y
            field.setCrate(False)
            if self.__world[i][j].isWalkable() and self.__world[i][j].isPassable():
                if self.__world[i][j].getType() == FieldType.FREE:
                    self.__world[i][j].setCrate(True)
                    
        if self.player.pos() == self.__finishPoint:
            self.__completed = True
        i, j = self.player.pos()
        if self.__world[i][j].getType() == FieldType.TURNER:
            self.player.direction = self.__world[i][j].direction

    def explode(self, p):
        self.__animations.add(Animation(self, self.IMAGES_EXPLOSION, p.x-0.5, p.y-0.5, 2 * Constants.FIELD_SIZE, 2 * Constants.FIELD_SIZE))
        self.explode_((p.x + Direction.LEFT.x) % self.__boundaries.x, (p.y + Direction.LEFT.y) % self.__boundaries.y)
        self.explode_((p.x + Direction.RIGHT.x) % self.__boundaries.x, (p.y + Direction.RIGHT.y) % self.__boundaries.y)
        self.explode_((p.x + Direction.UP.x) % self.__boundaries.x, (p.y + Direction.UP.y) % self.__boundaries.y)
        self.explode_((p.x + Direction.DOWN.x) % self.__boundaries.x, (p.y + Direction.DOWN.y) % self.__boundaries.y)

    def explode_(self, i, j):
        self.__animations.add(Animation(self, self.IMAGES_EXPLOSION, i, j))
        if self.__world[i][j].getType() == FieldType.BLOCK:
            self.__world[i][j].destroy()
            actor = Free(self, i, j)
            self.__way.add(actor)
            self.__world[i][j] = actor
        if self.__world[i][j].getType() == FieldType.FREE and self.__world[i][j].hasCrate():
            self.__world[i][j].setCrate(False)

    def replaceField(self, i, j, ftype = None):
        if ftype is not None:
            pass

    def destroy(self):
        self.stop()
        self.__world = None
        self.__walls.destroy()
        self.__way.destroy()
        self.empty()

    def getCameraOffset(self):
        if self.__camera is None:
            return (0, 0)
        return self.__camera.offset

    def getWorldBoundaries(self):
        if self.__boundaries is None:
            return (0, 0)
        return Vec2(self.__boundaries.x * Constants.FIELD_SIZE, self.__boundaries.y * Constants.FIELD_SIZE)

    def getCamera(self):
        return self.__camera

    def completed(self):
        return self.__completed == True

    def click(self, mX, mY):
        offX, offY = self.getCamera().offset
        x, y = mX + offX, mY + offY
        i, j = int(x / Constants.FIELD_SIZE), int(y / Constants.FIELD_SIZE)
        #print i,j
        if self.__world[i][j].getType() == FieldType.FREE and len(self.__arsenal) > 0:
            arsenal = self.__arsenal.pop(0)
            if arsenal == Arsenal.BLOCK:
                self.__world[i][j].destroy()
                actor = Block(self, i, j)
                self.__walls.add(actor)
                self.__world[i][j] = actor
            elif arsenal == Arsenal.CRATE:
                self.__world[i][j].setCrate(True)
            elif arsenal == Arsenal.BOMB:
                self.__world[i][j].setBomb(5)
            #print self.__arsenal
            #actor = Block(self, i, j, const.FIELD_SIZE, const.FIELD_SIZE)
            #self.__walls.add(actor)
            #self.__world[i][j] = 0
            #self.__world[i][j] = Turner(self, i, j, Direction.RIGHT)

class Camera():

    offset = (0, 0)
    size = (Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)

    def __init__(self, world, offset=(0, 0)):
        if hasattr(offset, "__getitem__") and len(offset) == 2:
            self.offset = (offset[0], offset[1])
        if isinstance(world, World):
            self.__world = world

    def pan(self, p):
        if hasattr(p, "__getitem__") and len(p) == 2:
            x, y = (p[0] - self.size[0] / 2, p[1] - self.size[1] / 2)
            boundaries = self.__world.getWorldBoundaries()
            if x < 0:
                x = 0
            if x + self.size[0] > boundaries[0]:
                x = boundaries[0] - self.size[0]
            if y < 0:
                y = 0
            if y + self.size[1] > boundaries[1]:
                y = boundaries[1] - self.size[1]
            self.offset = (x, y)

    def move(self, p):
        if hasattr(p, "__getitem__") and len(p) == 2:
            x, y = self.offset[0] + p[0], self.offset[1] + p[1]
            boundaries = self.__world.getWorldBoundaries() 
            if x < 0:
                x = 0
            if x + self.size[0] > boundaries[0]:
                x = boundaries[0] - self.size[0]
            if y < 0:
                y = 0
            if y + self.size[1] > boundaries[1]:
                y = boundaries[1] - self.size[1]
            if boundaries[0] < self.size[0]:
                x = 0
            if boundaries[1] < self.size[1]:
                y = 0
            self.offset = (x, y)

    def reset(self):
        self.offset = (0, 0)

class Layer(pygame.sprite.OrderedUpdates):
    
    __hidden = 0
    __id = -1

    def __init__(self, _id = -1):
        super(Layer, self).__init__()
        self.__id = _id

    def update(self, dt):
        super(Layer, self).update(dt)

    def render(self, display):
        if not self.__hidden:
            super(Layer, self).draw(display)
    
    def hide(self):
        self.__hidden = 1

    def show(self):
        self.__hidden = 0

    def isHidden(self):
        return self.__hidden == 1

    def getId(self):
        return self.__id

    def destroy(self):
        self.empty()

