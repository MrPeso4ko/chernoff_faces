import random

import chernoff_face

faces = []
for i in range(16):  # generate 16 random faces
    d = {}
    for key in chernoff_face.face_parameters:
        d[key] = random.random()
    face = chernoff_face.draw_face(d, caption=str(i))
    faces.append(face)
chernoff_face.draw_grid(faces, 2, 8, "random_faces.png")
