import chernoff_face
from PIL import Image

dataset_file = open("dataset.csv")
countries = []  # read data from file
dataset = []
for line in dataset_file:
    line = line.split(',')
    countries.append(line[0])
    dataset.append(list(map(float, line[1:5])))

# data normalization
maximums = list(dataset[0])
minimums = list(dataset[0])

for data_line in dataset[1:]:
    for i in range(4):
        maximums[i] = max(maximums[i], data_line[i])
        minimums[i] = min(minimums[i], data_line[i])

for data_line in dataset:
    for i in range(4):
        data_line[i] = (data_line[i] - minimums[i]) / (maximums[i] - minimums[i])

face_parameters = chernoff_face.map_parameters_to_dataset([
    ["-eyes_slant", "eyebrows_slant"],
    ["-mouth_curvature"],
    ["upper_face_eccentricity", "eyes_size"],
    ["-radius_to_corner", "-lower_part_eccentricity"]], dataset)
faces = []
for country, parameters in zip(countries, face_parameters):
    faces.append(chernoff_face.draw_face(caption=country, parameters=parameters))

chernoff_face.draw_grid(faces, 3, 5, "covid.png")

map = Image.open("world_map.png")  # manually position some faces on world map
map = map.convert(mode='1', dither=Image.Dither.NONE).resize((map.width * 3, map.height * 3))
faces[0].draw_on_image((570, 770), map)
faces[1].draw_on_image((1147, 1395), map)
faces[2].draw_on_image((2693, 354), map)
faces[9].draw_on_image((3107, 1735), map)
faces[13].draw_on_image((2875, 850), map)
faces[5].draw_on_image((2273, 1682), map)
faces[11].draw_on_image((3437, 766), map)
faces[12].draw_on_image((2540, 1317), map)
faces[10].draw_on_image((3217, 1140), map)
faces[8].draw_on_image((1976, 1763), map)

map.save("world_map_with_face.png")
