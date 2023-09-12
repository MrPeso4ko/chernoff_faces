import math

from chernoff_face.image import face
from chernoff_face.util import geometry, functions


def _ellipse_numbers(x1, y1, x2, y2, e):
    """numbers for *geometry.ellipse_eq* function which draw an ellipse passing through two points and eccentricity *e*
    :returns: three numbers *a*, *b*, *c*"""
    d = (x1 ** 2 * (2 * (e + 1) * (y1 - y2) ** 2 - 2 * x2 ** 2) + ((e + 1) * (y1 - y2) ** 2 + x2 ** 2) ** 2 + x1 ** 4)
    a = d / (4 * (e + 1) * (y1 - y2) ** 2)
    b = d / (4 * (e + 1) ** 2 * (y1 - y2) ** 2)
    c = ((e + 1) * (y1 ** 2 - y2 ** 2) + x1 ** 2 - x2 ** 2) / (2 * (e + 1) * (y1 - y2))
    return a, b, c


face_parameters = [
    "radius_to_corner",
    "angle_to_corner",
    "vertical_size",
    "upper_part_eccentricity",
    "lower_part_eccentricity",
    "nose_length",
    "mouth_vertical_pos",
    "mouth_curvature",
    "mouth_length",
    "eyes_vertical_pos",
    "eyes_horizontal_pos",
    "eyes_slant",
    "eyes_eccentricity",
    "eyes_size",
    "pupils_position",
    "eyebrows_vertical_pos",
    "eyebrows_slant",
    "eyebrows_size"
]

_params_indexes = {
    "radius_to_corner": 0,
    "angle_to_corner": 1,
    "vertical_size": 2,
    "upper_part_eccentricity": 3,
    "lower_part_eccentricity": 4,
    "nose_length": 5,
    "mouth_vertical_pos": 6,
    "mouth_curvature": 7,
    "mouth_length": 8,
    "eyes_vertical_pos": 9,
    "eyes_horizontal_pos": 10,
    "eyes_slant": 11,
    "eyes_eccentricity": 12,
    "eyes_size": 13,
    "pupils_position": 14,
    "eyebrows_vertical_pos": 15,
    "eyebrows_slant": 16,
    "eyebrows_size": 17,
}

_params_ranges = {
    "radius_to_corner": (70, 90),
    "angle_to_corner": (-0.7, 0.7),
    "vertical_size": (90, 120),
    "upper_part_eccentricity": (-0.5, 1.5),
    "lower_part_eccentricity": (-0.5, 1.5),
    "nose_length": (5, 20),
    "mouth_vertical_pos": (30, 70),
    "mouth_curvature": (-5, 5),
    "mouth_length": (10, 100),
    "eyes_vertical_pos": (35, 75),
    "eyes_horizontal_pos": (5, 25),
    "eyes_slant": (1, 2),
    "eyes_eccentricity": (0.1, 0.9),
    "eyes_size": (10, 30),
    "pupils_position": (-10, 10),
    "eyebrows_vertical_pos": (7, 20),
    "eyebrows_slant": (-0.5, 1),
    "eyebrows_size": (10, 30),
}


def _calculate_param(key: str, val: float) -> float:
    """calculates parameter in range (0, 1) to real range"""
    low = _params_ranges[key][0]
    high = _params_ranges[key][1]
    return low + (high - low) * val


def _prepare_params(parameters: dict) -> list[float]:
    params = [0] * 18
    for key in _params_indexes:
        if key in parameters:
            if 0 <= parameters[key] <= 1:
                val = parameters[key]
            else:
                raise ValueError("parameter {} is out of (0,1) range".format(key))
        else:
            val = 0.5
        params[_params_indexes[key]] = _calculate_param(key, val)
    return params


def draw_face(parameters: dict = None, caption: str = "") -> face.Face:
    """
    :param parameters: dictionary of face parameters
    :param caption: face caption (will be written above the face)

    takes dictionary of face patameters and returns Face object

    each value should be in (0, 1) interval. if parameter is not present, it defaults to 0.5

    allowed keys (they can also be found in face_parameters constant):

    *radius_to_corner*: radius from center to face corner (intersection point of two ellipses)  
    
    *angle_to_corner*: angle from OX to face corner

    *vertical_size*: vertical size of face

    *upper_part_eccentricity*: upper part of face eccentricity

    *lower_part_eccentricity*: lower part of face eccentricity

    *nose_length*: nose length

    *mouth_vertical_pos*: mouth vertical pos

    *mouth_curvature*: mouth curvature

    *mouth_length*: length of mouth arc

    *eyes_vertical_pos*: eyes vertical position

    *eyes_horizontal_pos*: eyes horizontal position

    *eyes_slant*: eyes slant

    *eyes_eccentricity*: eyes eccentricity

    *eyes_size*: eyes size

    *pupils_position*: pupils position

    *eyebrows_vertical_pos*: eyebrows vertical position

    *eyebrows_slant*: eyebrows slant

    *eyebrows_size*: eyebrows size

    :return: Face object, which afterward can be moved to an image"""
    if parameters is None:
        parameters = {}
    params = _prepare_params(parameters)
    face_canvas = face.Face(caption)
    ux = lx = 0
    uy = params[2]
    ly = -params[2]
    px = params[0]
    py = 0

    px, py = geometry.rotate_x(px, py, params[1]), geometry.rotate_y(px, py, params[1])

    a1, b1, c1 = _ellipse_numbers(px, py, ux, uy, params[4])
    a2, b2, c2 = _ellipse_numbers(px, py, lx, ly, params[3])

    face_eq = [
        # lower face
        lambda x, y: y > py and geometry.ellipse_eq(a1, b1, c1)(x, y),
        # upper face
        lambda x, y: y < py and geometry.ellipse_eq(a2, b2, c2)(x, y),
        # nose
        geometry.segment_eq(0, params[5], 0, -params[5]),
        # right eye
        geometry.slanted_ellipse_eq(-params[11], params[13], params[13] + params[10],
                                    params[9], -10 * params[12] / (-10 * params[12] - 1)),
        # left eye
        geometry.slanted_ellipse_eq(params[11], params[13], - params[13] - params[10],
                                    params[9], -10 * params[12] / (-10 * params[12] - 1)),
        # right pupil
        geometry.slanted_ellipse_eq(0, 2, params[13] + params[10] + geometry.rotate_x(0, -params[14], -params[11]),
                                    params[9] + geometry.rotate_y(0, -params[14], -params[11]), 0),
        # left pupil
        geometry.slanted_ellipse_eq(0, 2, -params[13] - params[10] + geometry.rotate_x(0, -params[14], params[11]),
                                    params[9] + geometry.rotate_y(0, -params[14], params[11]), 0),
        # left eyebrow
        geometry.segment_eq(params[10] - geometry.rotate_x(params[17] / 2, 0, params[16]),
                            params[9] + params[15] - geometry.rotate_y(params[17] / 2, 0, params[16]),
                            params[10] + geometry.rotate_x(params[17] / 2, 0, params[16]),
                            params[9] + params[15] + geometry.rotate_y(params[17] / 2, 0, params[16])),
        # right eyebrow
        geometry.segment_eq(-params[10] - params[17] / 2 * math.cos(params[16]),
                            params[9] + params[15] + geometry.rotate_y(params[17] / 2, 0, params[16]),
                            -params[10] + params[17] / 2 * math.cos(params[16]),
                            params[9] + params[15] - geometry.rotate_y(params[17] / 2, 0, params[16]))]

    if -0.7 <= params[7] <= 0.7:
        face_eq.append(geometry.segment_eq(-params[8] / 2, -params[6], params[8] / 2, -params[6]))
    else:
        face_eq.append(geometry.circle_arc_eq(params[6], 150 / params[7], params[8]))

    geometry.draw_equation(face_canvas, functions.composite_or(*face_eq), 2)
    return face_canvas
