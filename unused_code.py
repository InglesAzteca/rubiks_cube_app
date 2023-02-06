def check_box_tile_coloring(self, check_box, add_remove):
    """Colors or removes color from the tiles in a section of the cube."""

    coloring_reference_copy = self.create_cube_copy(self.coloring_reference)
    # the cross only consists of the bottom edges of the cube.
    if check_box == 'cross':
        coloring_reference_copy = self.color_edge_tiles('bottom',
                                                        coloring_reference_copy,
                                                        add_remove)
    # f2l consists of the middle edges and the bottom corners.
    elif check_box == 'f2l':
        coloring_reference_copy = self.color_section(
            'f2l',
            coloring_reference_copy,
            add_remove)
    elif check_box == 'oll':
        coloring_reference_copy = self.color_oll_tiles(coloring_reference_copy,
                                                       add_remove)
    self.color_tiles(coloring_reference_copy)

    def color_edge_tiles(self, section, coloring_reference_copy, add_remove):
        """Colors or removes color from the edge tiles of a certain section
        (top/middle/bottom)."""

        # the edge consists of 2 tiles
        for tile_1, tile_2 in self.edge_indices[section]:
            # separates the tiles into their indecies (face index, row index, column index)
            face_1, row_1, column_1 = tile_1
            face_2, row_2, column_2 = tile_2

            # sets the color to the color of the centre tile
            if add_remove == 'add':
                color_1 = coloring_reference_copy[face_1][1][1]
                color_2 = coloring_reference_copy[face_2][1][1]

            # sets the color to a default value
            elif add_remove == 'remove':
                color_1, color_2 = 'd', 'd'

            coloring_reference_copy[face_1][row_1][column_1] = color_1
            coloring_reference_copy[face_2][row_2][column_2] = color_2

        return coloring_reference_copy

    def color_corner_tiles(self, section, coloring_reference_copy, add_remove):
        """Colors or removes color from the corner tiles of a certain section
        (top/bottom)."""

        # a corner consists of 3 tiles.
        for tile_1, tile_2, tile_3 in self.corner_indices[section]:
            # separates each tile into their indices (face index, row index, column index)
            face_1, row_1, column_1 = tile_1
            face_2, row_2, column_2 = tile_2
            face_3, row_3, column_3 = tile_3

            # sets the color to the color of the centre tile
            if add_remove == 'add':
                color_1 = coloring_reference_copy[face_1][1][1]
                color_2 = coloring_reference_copy[face_2][1][1]
                color_3 = coloring_reference_copy[face_3][1][1]

            # sets the color to a default value
            elif add_remove == 'remove':
                color_1, color_2, color_3 = 'd', 'd', 'd'

            coloring_reference_copy[face_1][row_1][column_1] = color_1
            coloring_reference_copy[face_2][row_2][column_2] = color_2
            coloring_reference_copy[face_3][row_3][column_3] = color_3

        return coloring_reference_copy

    def color_oll_tiles(self, coloring_reference_copy, add_remove):
        """Colors or removes color from the tiles on the upper face of the cube."""

        # sets color to the centre tile of the upper face.
        if add_remove == 'add':
            color = coloring_reference_copy[0][1][1]
        # sets color to a default value.
        elif add_remove == 'remove':
            color = 'd'

        for row in range(3):
            for column in range(3):
                # if it is not the centre tile (row 1, column 1) we color it.
                if row != 1 or column != 1:
                    coloring_reference_copy[0][row][column] = color

        return coloring_reference_copy

        # contains rotation details for each color if they were to be the start color
        rotation_details = {'yellow': ('X', 0),
                            'white': ('X', 2),
                            'green': ('X', 1, -1),
                            'blue': ('X', 1),
                            'orange': ('Z', 1, -1),
                            'red': ('Z', 1)
                            }
        coloring_reference_copy = self.create_cube_copy(self.coloring_reference)

        for key in rotation_details.keys():
            if key == start_color:
                # passes in the default color order and returns a list after the rotations have been performed
                color_order = self.cube_rotation(default_color_order,
                                                 *rotation_details[key])
                break

        # colors = self.order_colors(color_order) # returns a copy of the color details in order

        def color_tiles_according_to_check_box_states(self, required_states):
            """With a list of the check box states this function calls a function
            to color or remove color from a section of the cube."""

            # returns the check box's names that are used to identify what sections need to be colored.
            check_box_names = self.get_dictionary_details(
                self.check_box_details, return_value='name')

            coloring_reference_copy = self.create_cube_copy(
                self.coloring_reference)

            # are_colored = [self.is_cross_colored(), self.is_f2l_colored(), self.is_oll_colored()]

            for index in range(len(required_states)):
                # if the check box state is 0/off color is removed from the tiles.
                if required_states[index] == 0:
                    self.color_section(check_box_names[index],
                                       coloring_reference_copy, 'remove')

                # if the check box state is 1/on the tiles are colored.
                elif required_states[index] == 1:
                    self.color_section(check_box_names[index],
                                       coloring_reference_copy, 'add')


cube = [[['o', 'o', 'y'],
         ['b', 'y', 'o'],
         ['b', 'g', 'r']],

        [['b', 'w', 'w'],
         ['o', 'o', 'o'],
         ['b', 'w', 'w']],

        [['r', 'y', 'g'],
         ['w', 'b', 'r'],
         ['g', 'b', 'r']],

        [['y', 'b', 'g'],
         ['g', 'r', 'y'],
         ['g', 'y', 'b']],

        [['o', 'y', 'w'],
         ['b', 'g', 'g'],
         ['y', 'w', 'y']],

        [['o', 'r', 'w'],
         ['g', 'w', 'r'],
         ['o', 'r', 'r']]]

corners = {'top': [[[0, 0, 0], [1, 0, 0], [4, 0, 2]],
                   [[0, 0, 2], [4, 0, 0], [3, 0, 2]],
                   [[0, 2, 2], [3, 0, 0], [2, 0, 2]],
                   [[0, 2, 0], [2, 0, 0], [1, 0, 2]]],

           'bottom': [[[5, 0, 0], [1, 2, 2], [2, 2, 0]],
                      [[5, 0, 2], [2, 2, 2], [3, 2, 0]],
                      [[5, 2, 2], [3, 2, 2], [4, 2, 0]],
                      [[5, 2, 0], [4, 2, 2], [1, 2, 0]]]}

edges = {'top': [[[1, 0, 1], [0, 1, 0]],
                 [[2, 0, 1], [0, 2, 1]],
                 [[3, 0, 1], [0, 1, 2]],
                 [[4, 0, 1], [0, 0, 1]]],

         'middle': [[[1, 1, 0], [4, 1, 2]],
                    [[1, 1, 2], [2, 1, 0]],
                    [[2, 1, 2], [3, 1, 0]],
                    [[3, 1, 2], [4, 1, 0]]],

         'bottom': [[[1, 2, 1], [5, 1, 0]],
                    [[2, 2, 1], [5, 0, 1]],
                    [[3, 2, 1], [5, 1, 2]],
                    [[4, 2, 1], [5, 2, 1]]]}


def calculate_corner_parity():
    top_face_color = cube[0][1][1]
    bottom_face_color = cube[5][1][1]
    correctly_orientated = 0
    clockwise = 0
    anti_clockwise = 0

    c = [corner[0] for section in [corners["top"], corners["bottom"]] for corner in section]
    cw = [corner[1] for section in [corners["top"], corners["bottom"]] for corner in section]
    acw = [corner[2] for section in [corners["top"], corners["bottom"]] for corner in section]

    corner_indices = []

    all_corner_indices = [index for section in [corners["top"], corners["bottom"]] for corner in section for index in corner]
    for face in range(6):
        for row in range(3):
            for column in range(3):
                is_corner = [face, row, column] in all_corner_indices
                if is_corner and top_face_color in cube[face][row][column]:
                    corner_indices.append([face, row, column])

                if is_corner and bottom_face_color in cube[face][row][column]:
                    corner_indices.append([face, row, column])

    for face, row, column in corner_indices[:]:
        if face in (0, 5):
            correctly_orientated += 1
            corner_indices.remove([face, row, column])


    for index in corner_indices[:]:
        if index in cw:
            clockwise += 1
        elif index in acw:
            anti_clockwise += 1

    corner_parity = (clockwise + anti_clockwise * 2) % 3


def calculate_edge_parity():
    correct = 0
    wrong = 0

    color_pairs = [["w", "y"], ["b", "g"], ["o", "r"]]

    all_edge_indices = [edge for section in [edges["top"], edges["middle"], edges["bottom"]] for edge in section]

    for edge1, edge2 in all_edge_indices[:]:
        face1, row1, column1 = edge1
        face2, row2, column2 = edge2

        tile_color = cube[face1][row1][column1]
        centre_color = cube[face1][1][1]

        actual_color_pair = [tile_color, centre_color]
        actual_color_pair.sort()

        correct_color_pair = None
        for color_pair in color_pairs:
            if tile_color in color_pair:
                print(color_pair)
                correct_color_pair = color_pair
                break
        print(actual_color_pair, correct_color_pair)
        if tile_color == centre_color or actual_color_pair == correct_color_pair:
            correct += 1
            wrong += 1

    print(correct)
    print(wrong)


def determine_edge_parity():
    correct = 0
    wrong = 0

    color_pairs = [["w", "y"], ["b", "g"], ["o", "r"]]

    all_edge_indices = [edge for section in
                        [edges["top"], edges["middle"], edges["bottom"]] for
                        edge in section]

def handling_check_box_states_with_tile_event(self, indices):
    face, row, column = indices
    indices_list = [self.cross_indices, self.f2l_indices, self.oll_indices]
    states = get_dictionary_details(checkboxes.checkbox_details,
                                    return_value="variable")
    required_states = get_dictionary_details(checkboxes.checkbox_details,
                                             return_value="required_states")

    current_tile_color = self.coloring_reference[face][row][column]
    selected_color = color_palette.selected_color

    is_same_color = selected_color == current_tile_color

    if not is_same_color:
        for index in range(3):
            if indices in indices_list[index] and states[index].get() == 1:
                checkboxes.change_checkbox_states(required_states[index][0])
                break

def get_section_indices_required_states_and_name(self, indices):
        indices_list = [self.cross_indices, self.f2l_indices, self.oll_indices]
        required_states = get_dictionary_details(checkboxes.checkbox_details,
                                                 return_value="required_states")
        section_names = get_dictionary_details(checkboxes.checkbox_details,
                                               return_value="name")
        for index in range(3):
            section_indices = indices_list[index]
            if indices in section_indices:
                return section_indices, required_states[index], section_names[index]