from PIL import Image

from chernoff_face.image.face import Face

_face_width = Face.x_high - Face.x_low
_face_height = Face.y_high - Face.y_low


def draw_grid(faces: list[Face], x: int, y: int, filename: str):
    img = Image.new("1", (_face_width * y, _face_height * x), "white")
    i = 0
    j = 0
    for face in faces:
        face.draw_on_image((i * _face_width, j * _face_height), img)
        i += 1
        if i == y:
            i = 0
            j += 1
        if j == x:
            break
    img.save(filename)
