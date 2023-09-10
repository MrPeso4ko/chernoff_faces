import math

from chernoff_face.image import face
from chernoff_face.util.interval import Interval


def draw_dot(px: face.Face, x: int, y: int, dot_size: float = 5.):
    """Draws dot of size *dot_size* in center *x*, *y* in array *px* in-place
    :param px: Face object
    :param x: x
    :param y: y
    :param dot_size: size of dot. Default: 5"""
    for dx in range(int(-dot_size), int(dot_size)):
        for dy in range(int(-dot_size), int(dot_size)):
            if dx ** 2 + dy ** 2 <= dot_size ** 2:
                try:
                    px[x + dx][y + dy] = 0
                except IndexError:
                    pass
    return px


def draw_equation(px: face.Face, eq, boldness=5.):
    """Draws equation *eq* on face canvas *px*. Equation should be a mathematically-defined function which takes
    two arguments x, y and returns True if pont lies on figure and False otherwise"""
    for x in range(px.x_low, px.x_high):
        # t = time.time()
        for y in range(px.y_low, px.y_high):
            if eq(Interval.from_point(x + .5), Interval.from_point(y + .5)):
                draw_dot(px, px.ox + x, px.oy + y, boldness / 2)


def segment_eq(x1, y1, x2, y2):
    """Segment equation
    :return: eq(x, y) - function which defines segment with ends in (x1, y1) and (x2, y2)"""
    if x1 > x2:
        x1, y1, x2, y2 = x2, y2, x1, y1

    if y1 < y2:
        def eq(x, y):
            return x1 <= x <= x2 and -y1 >= y >= -y2 and (x - x1) * (y1 - y2) == (y + y1) * (x2 - x1)
    else:
        def eq(x, y):
            return x1 <= x <= x2 and -y1 <= y <= -y2 and (x - x1) * (y1 - y2) == (y + y1) * (x2 - x1)
    return eq


def ellipse_eq(a, b, c):
    """Ellipse equation
    :return: eq(x, y) - function which defines ellipse with parallel to coordinate axes semiaxes sqrt(*a*) and
        sqrt(*b*), displaced upwards by *c*"""

    def eq(x, y):
        return x ** 2 / a + (y - c) ** 2 / b == 1

    return eq


def rotate_x(x, y, angle):
    """rotates point *x*, *y* on angle *angle*
    :return: x coordinate of rotated point"""
    return x * math.cos(angle) - y * math.sin(angle)


def rotate_y(x, y, angle):
    """rotates point *x*, *y* on angle *angle*
    :return: y coordinate of rotated point"""
    return x * math.sin(angle) + y * math.cos(angle)


def slanted_ellipse_eq(slant, size, pos_x, pos_y, eccentricity):
    """Slanted ellipse equation
    :return: eq(x, y) - function which defines ellipse rotated by angle *slant* of defined *size* (major semiaxis)
        and *eccentricity*, with center in (*pos_x*, *pos_y*)"""

    def eq(x, y):
        return (rotate_x(x - pos_x, y + pos_y, slant) ** 2 /
                (size ** 2 - eccentricity ** 2 * size ** 2) +
                rotate_y(x - pos_x, y + pos_y, slant) ** 2 /
                size ** 2 == 1)  # разбить на более простые математические действия

    return eq


def circle_arc_eq(pos, radius, length):
    """Circle arc equation
    :return: eq(x, y) - function which defines circle arc with defined *radius* and *length*. With negative radius, arc
        is mirrored horizontally"""

    if radius >= 0:
        def eq(x, y):
            return y - (pos - radius) >= math.cos(length / (radius * 2)) * radius and x ** 2 + (
                    y - (pos - radius)) ** 2 == radius ** 2
    else:
        def eq(x, y):
            return y - (pos - radius) <= math.cos(length / (radius * 2)) * radius and x ** 2 + (
                    y - (pos - radius)) ** 2 == radius ** 2

    return eq
