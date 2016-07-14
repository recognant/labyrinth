class Level():

    data = None
    dim = (0, 0)
    _defective = False

    def __init__(self, path):
        with open(path, 'r') as f:
            content = f.readlines()
        f.closed

        try:
            x, y, self.data = self._parse(content)
            self.dim = (x, y)
            self._defective = False
        except:
            self._defective = True

    def _parse(self, level):
        header = level.pop(0)
        x, y = self._parseDimension(header)

        data = [["0" for j in range(y)] for i in range(x)]

        i = j = 0
        while len(level) > 0:
            i = 0
            line = level.pop(0)
            for l in line:
                c = ord(l)
                if 47 < c < 58 or 96 < c < 123 or 64 < c < 91:
                    data[i][j] = l.upper()
                    i = i + 1
            j = j + 1

        return x, y, data

    def _parseDimension(self, line):
        x = ""
        y = ""
        cur = x
        for l in line:
            c = ord(l)
            if 47 < c < 58:
                cur = cur + str(l)
            elif c == 32:
                x = cur
                cur = y
            elif c == 10:
                y = cur
        return int(x), int(y)

    def isDefective(self):
        return self._defective


#l=Level("level1.txt")
#print l.data
