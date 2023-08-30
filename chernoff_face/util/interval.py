class Interval:
    def __init__(self, a, b):
        if a < b:
            self.a = a
            self.b = b
        else:
            self.a = b
            self.b = a

    @classmethod
    def from_point(cls, x, eps=1):
        return cls(x - eps, x + eps)

    @classmethod
    def from_interval(cls, s):
        return Interval(s.a, s.b)

    def __add__(self, other):
        if isinstance(other, Interval):
            return Interval(self.a + other.a, self.b + other.b)
        return Interval(self.a + other, self.b + other)

    def __sub__(self, other):
        if isinstance(other, Interval):
            return Interval(self.a - other.a, self.b - other.b)
        return Interval(self.a - other, self.b - other)

    def __mul__(self, other):
        if isinstance(other, Interval):
            return Interval(self.a * other.a, self.b * other.b)
        return Interval(self.a * other, self.b * other)

    def __pow__(self, power, modulo=None):
        if power % 2 == 0 and self.a < 0 < self.b:
            return Interval(0, max(self.a ** power, self.b ** power))
        else:
            a, b = self.a ** power, self.b ** power
            if a > b:
                a, b = b, a
            return Interval(a, b)

    def __truediv__(self, other):
        return Interval(self.a / other, self.b / other)

    def __eq__(self, other):
        if isinstance(other, Interval):
            x = Interval.from_interval(self)
            y = Interval.from_interval(other)
            if x.a > y.a:
                x, y = y, x
            return y.a <= x.b
        return self.a <= other <= self.b

    def __gt__(self, other):
        if isinstance(other, Interval):
            return self.a + self.b > other.a + other.b
        return (self.a + self.b) > 2 * other

    def __lt__(self, other):
        if isinstance(other, Interval):
            return self.a + self.b < other.a + other.b
        return (self.a + self.b) < 2 * other

    def __ge__(self, other):
        if isinstance(other, Interval):
            return self.b >= other.a
        return self.b >= other

    def __le__(self, other):
        if isinstance(other, Interval):
            return self.a <= other.b
        return self.a <= other

    def __ne__(self, other):
        return not self == other
