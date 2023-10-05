import random

import chernoff_face

faces = []
for i in range(15):  # generate 15 random faces
    d = {}
    for key in chernoff_face.face_parameters:
        d[key] = random.random()
    face = chernoff_face.draw_face(d, caption=str(i + 1))
    faces.append(face)
chernoff_face.draw_grid(faces, 3, 5, "random_faces.png")
