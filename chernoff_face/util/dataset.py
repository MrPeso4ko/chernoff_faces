def map_parameters_to_dataset(parameters: list, dataset: list) -> list[dict]:
    """maps every column of dataset to given face parameters. returns list of dicts,
    each one can be then used in draw_face

    each column will be mapped to every parameter in its list, for example:
    example:
    *[["angle_to_corner", "lower_part_eccentricity"],
    ["eyes_horizontal_pos", "eyes_size"],
    ["mouth_curvature"],
    ["radius_to_corner"]]* will be used to map 4-column dataset.
    first column will be copied to "angle_to_corner " and "lower_part_eccentricity" face parameters,
    second column - "eyes_horizontal_pos" and "eyes_size" parameters in dict and so on.
    every other parameters will be set to default.

    :param parameters: list of lists of column parameters.
    :param dataset: dataset. number of columns should be equal to len(parameters)
    """
    res = []
    for data_line in dataset:
        data_line_mapped = {}
        for i in range(len(parameters)):
            for param in parameters[i]:
                data_line_mapped[param] = data_line[i]
        res.append(data_line_mapped)
    return res
