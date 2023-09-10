from PIL import Image

from chernoff_face.image import face

_face_width = face.Face.x_high - face.Face.x_low
_face_height = face.Face.y_high - face.Face.y_low


def draw_grid(faces: list[face.Face], x: int, y: int, filename: str):
    img = Image.new("1", (_face_width * x, _face_height * y), "white")
    i = 0
    j = 0
    for face in faces:
        face.draw_on_image((i * _face_width, j * _face_height), img)
        j += 1
        if j == y:
            j = 0
            i += 1
        if i == x:
            break
    img.save(filename)
