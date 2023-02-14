from settings import settings
from textwrap import wrap
import os


def display_cube(cube_state):
    """Displays the cube's values line by line in a neat manner."""

    for stage in range(1, 4):  # 3 stages of displaying
        if stage in (1, 3):
            # set face index according to the stage
            if stage == 1:
                face = 0
            else:
                face = 5

            for row in range(3):
                v1, v2, v3 = cube_state[face][row]
                print(f"{v1:>8} {v2} {v3}")
        else:
            print()
            for row in range(3):
                row_display = ''
                for face in cube_state[1: 5]:
                    v1, v2, v3 = face[row]
                    row_display += f"{v1} {v2} {v3}  "
                print(row_display)
            print()


def add_empty_lists_to_indices_dictionary(*indices_dictionaries):
    """Adds 4 empty lists to each section of the indices dictionary."""
    for dictionary in indices_dictionaries:
        for key in dictionary.keys():
            dictionary[key] = [[] for x in range(4)]


def create_cube_copy(cube):
    """Returns a copy of the cube representation passed in."""
    return [[row[:] for row in face[:]] for face in cube]


def create_face_copy(face):
    return [[face[row][column] for column in range(3)] for row in range(3)]


def create_cube_representation(default_value):
    """Creates a list with a default value in a way that represents the cube."""
    faces, rows, columns = (6, 3, 3)
    return [[[default_value for column in range(columns)] for row in
             range(rows)] for face in range(faces)]


def order_colors(order):
    """Returns a ordered copy of the color details."""

    color_list = settings.color_details[:]  # creates the copy

    for index in range(len(order)):
        # loops through color list until all the values in the list order, equal the coresponding color details
        for color in color_list:
            if order[index] == color['color_reference']:
                order[
                    index] = color  # turns the color reference to the color details
                color_list.remove(color)  # removes that color
    return order


def get_dictionary_details(detail_dictionaries, reference_value=None,
                           return_value=None):
    """This function can be used to return specific details of a dictionary
    using a reference value (actual value we have) and a return value
    (key of the value we want)."""

    # if a reference value is not passed in, a list of all the values in the
    # list of dictionaries with the key return value is returned.
    if reference_value is None:
        return [details[return_value] for details in detail_dictionaries]
    else:
        for item in detail_dictionaries:
            if reference_value in item.values():
                # if a return value is not passed in, the dictionary
                # containing the reference value is returned.
                if return_value is None:
                    return item
                # if both the reference value and the return value are
                # passed in the specific value in the dictionary is returned.
                else:
                    return item[return_value]


def rename_text_file(folder_path, old_name, new_name):
    os.rename(folder_path + old_name, folder_path + new_name)


def write_state_to_text_file(cube_reference, file_path, *algorithms):
    file = open(file_path, "a")
    for algorithm in algorithms:
        file.write(f"Algorithm: {algorithm}\n")
    file.write("\n")
    for stage in range(1, 4):  # 3 stages of displaying
        if stage in (1, 3):
            # set face index according to the stage
            if stage == 1:
                face = 0
            else:
                face = 5

            for row in range(3):
                v1, v2, v3 = cube_reference[face][row]
                file.write(f"{v1:>8} {v2} {v3}\n")
        else:
            file.write("\n")
            for row in range(3):
                row_display = ''
                for face in cube_reference[1: 5]:
                    v1, v2, v3 = face[row]
                    row_display += f"{v1} {v2} {v3}  "
                file.write(f"{row_display}\n")
            file.write("\n")
    file.close()


def read_state_from_text_file(file_path):
    cube_representation = [[] for face in range(6)]
    algorithm_identifier = "Algorithm: "
    algorithms = []

    with open(file_path, "r") as algorithm_file:
        raw_state_from_text = [line.strip() for line in algorithm_file.readlines() if line.strip() != ""]

    while algorithm_identifier in raw_state_from_text[0]:
        algorithms.append(raw_state_from_text.pop(0).replace(algorithm_identifier, ""))

    section_1 = raw_state_from_text[3:-3]
    section_1 = [wrap(line, 6) for line in section_1]

    raw_state_from_text[3:-3] = []
    section_2 = raw_state_from_text

    for line_list in section_1:
        for face in range(1, 5):
            cube_representation[face].append(line_list[face - 1].split())

    cube_representation[0] = [face_row.split() for face_row in section_2[:3]]
    cube_representation[5] = [face_row.split() for face_row in section_2[-3:]]

    return cube_representation, algorithms


def get_file_list_from_folder(directory):
    file_list = [os.path.join(directory, file_name) for
                 file_name in os.listdir(directory) if
                 os.path.isfile(os.path.join(directory, file_name))]
    return file_list


def change_bottom_two_rows_on_cube(file_list, oll_indices):
    print(file_list)
    print(oll_indices)
    for file_directory in file_list:
        state, algorithm = read_state_from_text_file(file_directory)
        solved_state, solved = read_state_from_text_file("algorithms/solved")
        for face in range(6):
            for row in range(3):
                for column in range(3):
                    if [face, row, column] not in oll_indices:
                        state[face][row][column] = solved_state[face][row][column]
        write_state_to_text_file(state, algorithm)

