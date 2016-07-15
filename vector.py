class Vector2(list):

    def __init__(self, x = 0, y = 0, *args, **kwargs):
        super(Vector2, self).__init__(*args, **kwargs)
        super(Vector2, self).append(x)
        super(Vector2, self).append(y)

    @property
    def x(self):
        return super(Vector2, self).__getitem__(0)

    @property
    def y(self):
        return super(Vector2, self).__getitem__(1)

    def append(self, item):
        pass

    # v1 + v2
    def __add__(self, v):
        return Vector2(self.x + v.x, self.y + v.y)

    # v1 - v2
    def __sub__(self, v):
        return Vector2(self.x - v.x, self.y - v.y)

    # v2 - v1
    def __rsub__(self, v):
        return Vector2(v.x - self.x, v.y - self.y)

    # v1[i]
    def __getitem__(self, i):
        if 0<=i<2:
            return super(Vector2, self).__getitem__(i)
        else:
            raise Exception("Index out of bounds!")

    # v1 * v2
    def __mul__(self, v):
        return self.x * v.x + self.y + v.y

    # k * v1
    def __rmul__(self, k):
        return Vector2(k * self.x, k * self.y)

    # len(v1)
    def __len__(self):
        return 2

    # -v1
    def __neg__(self):
        return -1 * Vector2(self.x, self.y)

    # +v1
    def __pos__(self):
        return Vector2(self.x, self.y)

    # v1 == v2
    def __eq__(self, v):
        return self.x == v.x and self.y == v.y

    # v1 != v2
    def __ne__(self, v):
        return not self == v

    # str(v1)
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    # v1 | v2
    def __or__(self, v):
        return self * v == 0

    # abs(v1)
    def __abs__(self):
        return Vector2(abs(self._x), abs(self._y))

    # ~v1
    def __inv__(self):
        return Vector2(self._y, self._x)
