from other_functions import get_dictionary_details, settings, \
    create_cube_representation
from cube import Cube


def color_tiles(cube_tile_instances, cube_reference):
    """Uses a modified copy of the cube coloring reference list, colors the
    tiles and then updates the coloring reference to the values in the copy
    which is the current state."""

    current_cube_reference = get_cube_reference_from_tile_instances(
        cube_tile_instances)

    for face in range(6):
        for row in range(3):
            for column in range(3):
                current_color = current_cube_reference[face][row][column]
                new_color = cube_reference[face][row][column]
                # colors a tile only if the value has been modified
                if current_color != new_color:
                    color = get_dictionary_details(settings.color_details,
                                                   new_color)

                    light_color = color['light_color']
                    dark_color = color['dark_color']

                    # updates the color
                    cube_tile_instances[face][row][column].configure(
                        fg_color=light_color,
                        hover_color=dark_color)


def get_cube_reference_from_tile_instances(cube_tile_instances):
    cube_reference = create_cube_representation("d")

    for face_index in range(6):
        for row_index in range(3):
            for column_index in range(3):
                if cube_tile_instances[face_index][row_index][column_index] is not None:
                    tile_instance = cube_tile_instances[face_index][row_index][
                        column_index]
                    color = tile_instance.cget("fg_color")
                    color_reference = get_dictionary_details(
                        settings.color_details, color, "color_reference")
                    cube_reference[face_index][row_index][
                        column_index] = color_reference

    return cube_reference


class CubeColoring(Cube):
    def __init__(self, state):
        super().__init__(state)

        self.number_of_colors_on_cube = {"r": 0, "b": 0, "y": 0, "o": 0, "g": 0,
                                         "w": 0}

    def handle_number_of_colors_on_cube(self, current_color, new_color):
        if current_color != new_color:
            if new_color != "d":
                if self.number_of_colors_on_cube[new_color] < 9:
                    self.number_of_colors_on_cube[new_color] += 1

                    if current_color != "d":
                        self.number_of_colors_on_cube[current_color] -= 1
                    return True
                else:
                    return False
            else:
                self.number_of_colors_on_cube[current_color] -= 1
                return True
        else:
            return False

    def change_tile_color_reference(self, new_color, face_index,
                                    row_index, column_index):

        is_centre = (row_index == 1) and (column_index == 1)

        current_color = self.state[face_index][row_index][column_index]
        if not is_centre:
            if self.handle_number_of_colors_on_cube(current_color, new_color):
                self.state[face_index][row_index][column_index] = new_color

    def required_check_box_state_coloring(self, required_states, checkbox_names):
        are_colored = [self.is_cross_solved(),
                       self.is_f2l_solved(),
                       self.is_oll_solved()]

        for index in range(3):
            if required_states[index] == 0 and are_colored[index]:
                add_remove = "remove"
                self.change_section_colors(checkbox_names[index], add_remove)
            elif required_states[index] == 1:
                add_remove = "add"
                self.change_section_colors(checkbox_names[index], add_remove)

    def change_section_colors(self, section, add_remove):
        section_dictionary = {"cross": self.cross_indices,
                              "f2l": self.f2l_indices,
                              "oll": [oll_index for
                                      oll_index in self.oll_indices if
                                      oll_index not in self.pll_indices]}

        for face, row, column in section_dictionary[section]:
            if add_remove == "remove":
                new_color = "d"
            elif add_remove == "add":
                new_color = self.state[face][1][1]

            is_centre = row == 1 and column == 1
            if not is_centre:
                if self.handle_number_of_colors_on_cube(self.state[face][row][column], new_color):
                    self.state[face][row][column] = new_color


    def remove_color_if_number_of_colors_greater_than_nine(self,
                                                           section_indices):
        color_references = get_dictionary_details(settings.color_details[:6],
                                                  return_value="color_reference")

        for palette_color in color_references:
            color_count = self.number_of_colors_on_cube[palette_color]
            flag = color_count > 9
            if flag:
                for face in range(6):
                    for row in range(3):
                        for column in range(3):
                            color = self.state[face][row][column]
                            is_in_indices = [face, row,
                                             column] in section_indices
                            if color == palette_color and not is_in_indices:
                                self.state[face][row][column] = "d"
                                color_count -= 1
                                flag = color_count > 9
                            if not flag:
                                break
                        if not flag:
                            break
                    if not flag:
                        break

            self.number_of_colors_on_cube[palette_color] = color_count
    def color_centre_tiles(self):
        """Colors the centre tile of each face relative to the rotation details.
        """
        default_color_order = list('yrgobw')  # sets a default order of colors
        for face_index in range(6):
            self.state[face_index][1][1] = default_color_order[face_index]
            self.number_of_colors_on_cube[default_color_order[face_index]] += 1

    def is_cube_colored(self):
        """Depending if the coloring reference list contains the value d
        (which represents the default color), true (if d is not in the list) or
        false (if d is in the list) is returned."""

        for face in self.state:
            for row in face:
                if 'd' in row:
                    return False
        return True
