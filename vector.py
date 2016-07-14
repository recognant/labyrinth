class Vector2(list):

    def __init__(self, x = 0, y = 0, *args, **kwargs):
        super(Vector2, self).__init__(*args, **kwargs)
        self.append(x)
        self.append(y)

    @property
    def x(self):
        return super(Vector2, self).__getitem__(0)

    @property
    def y(self):
        return super(Vector2, self).__getitem__(1)

    def __add__(self, v):
        return Vector2(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return Vector2(self.x - v.x, self.y - v.y)

    def __rsub__(self, v):
        return Vector2(v.x - self.x, v.y - self.y)

    def __getitem__(self, i):
        if 0<=i<2:
            return super(Vector2, self).__getitem__(i)
        else:
            raise Exception("Index out of bounds!")
        
    def __mul__(self, v):
        return self.x * v.x + self.y + v.y

    def __rmul__(self, k):
        return Vector2(k * self.x, k * self.y)

    def __len__(self):
        return 2

    def __neg__(self):
        return -1 * Vector2(self.x, self.y)

    def __pos__(self):
        return Vector2(self.x, self.y)

    def __eq__(self, v):
        return self.x == v.x and self.y == v.y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __mod__(self, i):
        return Vector2(self.x % i, self.y % i)

    def __div__(self, i):
        return Vector2(self.x / i, self.y / i)
