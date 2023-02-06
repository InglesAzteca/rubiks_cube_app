from settings import settings


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


def cube_rotation(cube_state, X_Y_Z, amount=1, prime=1):
    """Simulates a rotation of the cube."""

    # rotation coordinates
    X = [[0, 2], [2, 5], [5, 4]]
    Y = [[1, 2], [2, 3], [3, 4]]
    Z = [[0, 1], [1, 5], [5, 3]]

    if X_Y_Z == 'X':
        rotation = X
    elif X_Y_Z == 'Y':
        rotation = Y
    elif X_Y_Z == 'Z':
        rotation = Z

    for number_of_rotations in range(amount):
        # if prime equals -1 the values in the list are reversed
        for r in rotation[::prime]:
            r = r[::prime]
            cube_state[r[0]], cube_state[r[1]] = cube_state[r[1]], \
                                                 cube_state[r[0]]

    return cube_state


def create_cube_copy(cube):
    """Returns a copy of the cube representation passed in."""
    return [[row[:] for row in face[:]] for face in cube]


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