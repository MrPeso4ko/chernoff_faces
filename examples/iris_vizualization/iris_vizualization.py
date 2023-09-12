# visualisation of Fischer Iris dataset
import random

import chernoff_face

with open("iris.data") as data_file:
    data = []
    titles = []
    for line in data_file:
        data_line = line.strip().split(",")
        data.append([float(x) for x in data_line[:-1]])  # convert all values from string to float
        titles.append(data_line[-1])

mins = list(data[0])
maxs = list(data[0])

for i in range(len(data)):  # calculate minimum and maximum for each value in dataset
    data_line = data[i]
    for j in range(len(data_line)):
        mins[j] = min(mins[j], data_line[j])
        maxs[j] = max(maxs[j], data_line[j])
sums = {}
counts = {}

for title in set(titles):
    sums[title] = [0] * len(data[0])
    counts[title] = [0] * len(data[0])

for i in range(len(data)):  # normalize data, find averages and draw faces. might take a while
    data_line = data[i]
    for j in range(len(data_line)):
        data_line[j] = (data_line[j] - mins[j]) / (maxs[j] - mins[j])
        sums[titles[i]][j] += data_line[j]
        counts[titles[i]][j] += 1

parameters = [["lower_part_eccentricity"],
              ["eyes_horizontal_pos", "eyes_size", "eyes_slant"],
              ["mouth_curvature", "mouth_length", "angle_to_corner"],
              ["radius_to_corner", "upper_part_eccentricity"]]
mapped_data = chernoff_face.map_parameters_to_dataset(parameters, data)  # map normalized data to dicts

faces = []

for i in range(len(mapped_data)):
    faces.append(chernoff_face.draw_face(mapped_data[i], "{} - {}".format(titles[i], i + 1)))

random.shuffle(faces)  # shuffle the data
for i in range(0, len(faces), 25):  # draw all faces on 5x5 grids
    chernoff_face.draw_grid(faces[i: i + 25], 5, 5, "irises - {}.png".format(i // 25 + 1))

# draw averages for every cluster
avg_faces = []
for title in sums:
    avg = [sums[title][i] / counts[title][i] for i in range(len(sums[title]))]
    mapped_avg = chernoff_face.map_parameters_to_dataset(parameters, [avg])
    avg_faces.append(chernoff_face.draw_face(mapped_avg[0], title))
chernoff_face.draw_grid(avg_faces, 1, 3, "average_faces.png")
