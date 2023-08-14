import math

from PIL import Image

sz = 130

x_low = -sz
x_high = sz
y_low = -sz
y_high = sz


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


def draw_dot(x: int, y: int, dot_size=5.):
    global px
    for dx in range(int(-dot_size), int(dot_size)):
        for dy in range(int(-dot_size), int(dot_size)):
            if dx ** 2 + dy ** 2 <= dot_size ** 2:
                px[x + dx][y + dy] = 0


def draw_equation(eq, boldness=5):
    global ox, oy
    for x in range(x_low, x_high):
        for y in range(y_low, y_high):
            if eq(Interval.from_point(x + .5), Interval.from_point(y + .5)):
                draw_dot(ox + x, oy + y, boldness / 2)


def segment_eq(x1, y1, x2, y2):
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1

    def eq(x, y):
        return x1 <= x <= x2 and -y1 >= y >= -y2 and (x - x1) * (y1 - y2) == (y + y1) * (x2 - x1)

    return eq


def ellipse_eq(a, b, c):
    def eq(x, y):
        return x ** 2 / a + (y - c) ** 2 / b == 1

    return eq


def slanted_ellipse_eq(slant, size, pos_x, pos_y, eccentricity):
    def eq(x, y):  # a ** 2 - e ** 2 * a ** 2 = b ** 2
        return (((x - pos_x) * math.cos(slant) - (y + pos_y) * math.sin(slant)) ** 2 /
                (size ** 2 - eccentricity ** 2 * size ** 2) +
                ((x - pos_x) * math.sin(slant) + (y + pos_y) * math.cos(slant)) ** 2 /
                size ** 2 == 1)

    return eq


def _composite_two_or(func1, func2):
    def or_func(x, y):
        return func1(x, y) or func2(x, y)

    return or_func


def composite_or(*funcs):
    def res(x, y):
        return False

    for func in funcs:
        res = _composite_two_or(res, func)
    return res


def circle_arc_eq(pos, radius, length):
    if radius >= 0:
        def eq(x, y):
            return y - (pos - radius) >= math.cos(length / (radius * 2)) * radius and x ** 2 + (
                    y - (pos - radius)) ** 2 == radius ** 2
    else:
        def eq(x, y):
            return y - (pos - radius) <= math.cos(length / (radius * 2)) * radius and x ** 2 + (
                    y - (pos - radius)) ** 2 == radius ** 2

    return eq


def draw_face(params):
    ux = lx = 0
    uy = params[2]
    ly = -params[2]
    px = params[0]
    py = 0
    px, py = px * math.cos(params[1]) - py * math.sin(params[1]), px * math.sin(params[1]) + py * math.cos(params[1])
    a1 = (px ** 2 * (2 * (params[4] + 1) * (py - uy) ** 2 - 2 * ux ** 2) + (
            (params[4] + 1) * (py - uy) ** 2 + ux ** 2) ** 2 + px ** 4) / (4 * (params[4] + 1) * (py - uy) ** 2)
    b1 = (px ** 2 * (2 * (params[4] + 1) * (py - uy) ** 2 - 2 * ux ** 2) + (
            (params[4] + 1) * (py - uy) ** 2 + ux ** 2) ** 2 + px ** 4) / (
                 4 * (params[4] + 1) ** 2 * (py - uy) ** 2)
    c1 = ((params[4] + 1) * (py ** 2 - uy ** 2) + px ** 2 - ux ** 2) / (2 * (params[4] + 1) * (py - uy))
    a2 = (px ** 2 * (2 * (params[3] + 1) * (py - ly) ** 2 - 2 * lx ** 2) + (
            (params[3] + 1) * (py - ly) ** 2 + lx ** 2) ** 2 + px ** 4) / (4 * (params[3] + 1) * (py - ly) ** 2)
    b2 = (px ** 2 * (2 * (params[3] + 1) * (py - ly) ** 2 - 2 * lx ** 2) + (
            (params[3] + 1) * (py - ly) ** 2 + lx ** 2) ** 2 + px ** 4) / (4 * (params[3] + 1) ** 2 * (
            py - ly) ** 2)
    c2 = ((params[3] + 1) * (py ** 2 - ly ** 2) + px ** 2 - lx ** 2) / (2 * (params[3] + 1) * (py - ly))

    face_eq = composite_or(lambda x, y: y > py and ellipse_eq(a1, b1, c1)(x, y),
                           lambda x, y: y < py and ellipse_eq(a2, b2, c2)(x, y))

    face_eq = composite_or(face_eq, segment_eq(0, params[5], 0, -params[5]))

    face_eq = composite_or(face_eq, circle_arc_eq(params[6], 150 * 1 / params[7], params[8]))

    face_eq = composite_or(face_eq, slanted_ellipse_eq(-params[11], params[13], params[10],
                                                       params[9], params[12]),
                           slanted_ellipse_eq(params[11], params[13], -params[10], params[9], params[12]))

    face_eq = composite_or(face_eq, slanted_ellipse_eq(0, 2, -params[10] + params[14] * math.sin(params[11]),
                                                       params[9] - params[14] * math.cos(params[11]), 0),
                           slanted_ellipse_eq(0, 2, params[10] - params[14] * math.sin(params[11]),
                                              params[9] - params[14] * math.cos(params[11]), 0))

    face_eq = composite_or(face_eq,
                           segment_eq(params[10] - params[17] / 2, params[9] + params[15], params[10] + params[17] / 2,
                                      params[9] + params[15]),
                           segment_eq(-params[10] - params[17] / 2, params[9] + params[15], -params[10] + params[17] / 2,
                                      params[9] + params[15])
                           )

    draw_equation(face_eq, 2)


px = [[]]
ox = oy = 0


def main():
    global ox, oy, px
    img = Image.new("1", (x_high - x_low, y_high - y_low), "white")

    px = [[1] * (y_high - y_low) for i in range(x_high - x_low)]

    pixels = img.load()
    ox, oy = -x_low, -y_low

    params = [0.5] * 18

    params[0] = 80  # radius from center to face corner (intersection point of two ellipses)
    params[1] = -0.6  # angle from OX to face corner
    params[2] = 100  # vertical size of face
    params[3] = 0.4  # upper part of face eccentricity
    params[4] = 0.2  # lower part of face eccentricity

    params[5] = 10  # nose length

    params[6] = 60  # mouth vertical pos
    params[7] = -3  # mouth curvature
    params[8] = 30  # length of mouth arc

    params[9] = 55  # eyes vertical pos
    params[10] = 30  # eyes horisontal pos
    params[11] = 3  # eyes slant
    params[12] = 0.8  # eyes eccentricity
    params[13] = 10  # eyes size

    params[14] = -2  # pupils position

    params[15] = 15  # eyebrows vertical position
    params[16] = 1  # eyebrows slant
    params[17] = 11  # eyebrows size

    draw_face(params)

    for x in range(x_high - x_low):
        for y in range(y_high - y_low):
            pixels[x, y] = px[x][y]
    img.save("face.png", "png")


if __name__ == '__main__':
    main()
