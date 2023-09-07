import math

import chernoff_face.image.canvas
from chernoff_face.util import geometry, functions


def _ellipse_numbers(x1, y1, x2, y2, e):
    """numbers for *geometry.ellipse_eq* function which draw an ellipse passing through two points and eccentricity *e*
    :returns: three numbers *a*, *b*, *c*"""
    d = (x1 ** 2 * (2 * (e + 1) * (y1 - y2) ** 2 - 2 * x2 ** 2) + ((e + 1) * (y1 - y2) ** 2 + x2 ** 2) ** 2 + x1 ** 4)
    a = d / (4 * (e + 1) * (y1 - y2) ** 2)
    b = d / (4 * (e + 1) ** 2 * (y1 - y2) ** 2)
    c = ((e + 1) * (y1 ** 2 - y2 ** 2) + x1 ** 2 - x2 ** 2) / (2 * (e + 1) * (y1 - y2))
    return a, b, c


def draw_face(params):
    canvas = chernoff_face.image.canvas.Canvas(-125, 125, -125, 125)
    ux = lx = 0
    uy = params[2]
    ly = -params[2]
    px = params[0]
    py = 0

    px, py = geometry.rotate_x(px, py, params[1]), geometry.rotate_y(px, py, params[1])

    a1, b1, c1 = _ellipse_numbers(px, py, ux, uy, params[4])
    a2, b2, c2 = _ellipse_numbers(px, py, lx, ly, params[3])

    face_eq = functions.composite_or(lambda x, y: y > py and geometry.ellipse_eq(a1, b1, c1)(x, y),
                                     lambda x, y: y < py and geometry.ellipse_eq(a2, b2, c2)(x, y))

    face_eq = functions.composite_or(face_eq, geometry.segment_eq(0, params[5], 0, -params[5]))

    # if params[7] ==

    face_eq = functions.composite_or(face_eq, geometry.circle_arc_eq(params[6], 150 * 1 / params[7], params[8]))

    face_eq = functions.composite_or(face_eq, geometry.slanted_ellipse_eq(-params[11], params[13], params[10],
                                                                          params[9], params[12]),
                                     geometry.slanted_ellipse_eq(params[11], params[13], -params[10], params[9],
                                                                 params[12]))

    face_eq = functions.composite_or(face_eq,
                                     geometry.slanted_ellipse_eq(0, 2, -params[10] + params[14] * math.sin(params[11]),
                                                                 params[9] - params[14] * math.cos(params[11]), 0),
                                     geometry.slanted_ellipse_eq(0, 2, params[10] - params[14] * math.sin(params[11]),
                                                                 params[9] - params[14] * math.cos(params[11]), 0))

    face_eq = functions.composite_or(face_eq,
                                     geometry.segment_eq(params[10] - params[17] / 2 * math.cos(params[16]),
                                                         params[9] + params[15] - params[17] / 2 * math.sin(params[16]),
                                                         params[10] + params[17] / 2 * math.cos(params[16]),
                                                         params[9] + params[15] + params[17] / 2 * math.sin(
                                                             params[16])),
                                     geometry.segment_eq(-params[10] - params[17] / 2 * math.cos(params[16]),
                                                         params[9] + params[15] + params[17] / 2 * math.sin(params[16]),
                                                         -params[10] + params[17] / 2 * math.cos(params[16]),
                                                         params[9] + params[15] - params[17] / 2 * math.sin(
                                                             params[16])))

    geometry.draw_equation(canvas, face_eq, 2)
    canvas.to_image()
