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
    """
    This function uses for loops to obtain a cube reference from the 3D list of
    tile instances.

    :param cube_tile_instances: A 3D list containing the button/tile instances
    of the visual cube representation.
    :return: Returns a 3D containing references to the colors on the button
    instances.
    """
    # creates a 3D list with the default value "d"
    cube_reference = create_cube_representation("d")

    for face_index in range(6):
        for row_index in range(3):
            for column_index in range(3):
                # ensures that the tiles have been created
                if cube_tile_instances[face_index][row_index][column_index] is not None:

                    tile_instance = cube_tile_instances[face_index][row_index][column_index]
                    # we use .cget() to get the hex color value of the tile
                    color = tile_instance.cget("fg_color")

                    # we get the color reference using the hex color value
                    color_reference = get_dictionary_details(settings.color_details, color, "color_reference")
                    # change the value in the cube_reference to the color
                    # reference obtained from the tile instance
                    cube_reference[face_index][row_index][column_index] = color_reference
    return cube_reference


class CubeColoring(Cube):
    """
    This class is used to color a cube state by changing colour references. It
    contains methods to do so in different ways and tracks the number of colors
    on the cube.
    """
    def __init__(self, state):
        """Initialize parent attributes, then initialize child attributes."""
        super().__init__(state)

        self.number_of_colors_on_cube = {"r": 0, "b": 0, "y": 0, "o": 0, "g": 0,
                                         "w": 0}

    def handle_number_of_colors_on_cube(self, current_color, new_color):
        """
        This method is in charge of validating and changing the dictionary
        containing the number of colors on the cube.
        :param current_color: This is the color reference of current color of
        the tile.
        :param new_color: This is the color reference of the color we want to
        color the tile.
        :return: This function returns True or false depending if the conditions
        are met."""
        if current_color != new_color:
            # if the new color is not "d" we are coloring
            if new_color != "d":
                if self.number_of_colors_on_cube[new_color] < 9:
                    self.number_of_colors_on_cube[new_color] += 1

                    if current_color != "d":
                        self.number_of_colors_on_cube[current_color] -= 1
                    return True
                else:
                    return False
            # if the new color is "d" we are removing a color
            else:
                self.number_of_colors_on_cube[current_color] -= 1
                return True
        else:
            return False

    def change_tile_color_reference(self, new_color, face_index, row_index, column_index):
        """
        Changes the color reference of a specific tile by indexing it on the
        cube state.

        :param new_color: The color reference of the color the tile is being
        changed to.
        :param face_index: The index of the face on the cube. (0 - 5)
        :param row_index: The index of the row on the face. (0 - 2)
        :param column_index: The index of the column on the face. (0 - 2)
        """
        is_centre = (row_index == 1) and (column_index == 1)

        current_color = self.state[face_index][row_index][column_index]
        if not is_centre:
            if self.handle_number_of_colors_on_cube(current_color, new_color):
                self.state[face_index][row_index][column_index] = new_color

    def required_check_box_state_coloring(self, required_states, checkbox_names):
        """
        Uses the required states and checkbox names to call the method that
        changes the section colors on the cube.

        :param required_states: A list of states that the checkboxes are
        required to be in. eg. [1, 1, 0]
        :param checkbox_names: A list containing the names of the checkboxes.
        """
        # a list representing which sections are colored
        are_colored = [self.is_cross_solved(),
                       self.is_f2l_solved(),
                       self.is_oll_solved()]

        for index in range(3):
            if required_states[index] == 0 and are_colored[index]:
                self.change_section_colors(checkbox_names[index], "remove")
            elif required_states[index] == 1 and not are_colored[index]:
                self.change_section_colors(checkbox_names[index], "add")

    def change_section_colors(self, section, add_remove):
        """
        Changes the color references of a specific section on the cube.
        :param section: The section being colored or discolored.
        :param add_remove: A string that is either add or remove.
        """
        # dictionary containing the indices to all sections.
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

            is_centre = (row == 1) and (column == 1)
            if not is_centre:
                if self.handle_number_of_colors_on_cube(self.state[face][row][column], new_color):
                    self.state[face][row][column] = new_color

    def remove_color_if_number_of_colors_greater_than_nine(self, section_indices):
        """
        This method removes the color from the cube if the number of colors is
        greater than nine. This happens due to section coloring.
        :param section_indices: Contains indices of the section.
        """
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
                            is_in_indices = [face, row, column] \
                                in section_indices

                            if color == palette_color and not is_in_indices:
                                self.state[face][row][column] = "d"
                                color_count -= 1
                                flag = color_count > 9

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

    def reset_state_to_default(self):
        """Changes all the color references on the cube to the default value."""
        for face in range(6):
            for row in range(3):
                for column in range(3):
                    self.state[face][row][column] = "d"

    def reset_number_of_colors_on_cube(self):
        """Changes all the color number to zero."""
        for color_reference in self.number_of_colors_on_cube.keys():
            self.number_of_colors_on_cube[color_reference] = 0
