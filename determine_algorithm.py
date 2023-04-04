
def determine_cross_piece_details_from_state(self, state, from_file):
    indices = cube_coloring.edge_indices["bottom"] + cube_coloring.edge_indices["middle"] + cube_coloring.edge_indices["top"]

    edge_details = {"selected": [], "location": 0, "cross_color": state[5][1][1], "colors": []}
    if from_file:
        edge_details["selected"] = ["b", "w"]
    else:
        edge_details["selected"] = solve_cube.selected_cross_piece

    for tile_indices in indices:
        colors = []
        for face, row, column in tile_indices:
            colors.append(state[face][row][column])
        sorted_colors = colors[:]
        sorted_colors.sort()
        sorted_selected = edge_details["selected"][:]
        sorted_selected.sort()
        if sorted_colors == sorted_selected:
            edge_details["location"] = indices.index(tile_indices) + 1
            edge_details["colors"] = colors
    return edge_details

def compare_to_cross_algorithm_state(self, cube_reference, algorithm_state):
    algorithm_state_cross_piece_details = self.determine_cross_piece_details_from_state(
        algorithm_state, True)

    cube_reference_cross_piece_details = self.determine_cross_piece_details_from_state(
        cube_reference, False)

    alg_location = algorithm_state_cross_piece_details["location"]
    ref_location = cube_reference_cross_piece_details["location"]

    alg_cross_color = algorithm_state_cross_piece_details["cross_color"]
    ref_cross_color = cube_reference_cross_piece_details["cross_color"]

    alg_colors = algorithm_state_cross_piece_details["colors"]
    ref_colors = cube_reference_cross_piece_details["colors"]

    is_piece_oriented_the_same = alg_colors.index(alg_cross_color) == ref_colors.index(ref_cross_color)
    if ref_location == alg_location and is_piece_oriented_the_same:
        return True
    else:
        return False

def search_through_cross_algorithms(self, cube_reference):
    cross_file_list = get_file_list_from_folder("algorithms\\cross")

    for index in range(len(cross_file_list)):
        algorithm_state, algorithm = read_state_from_text_file(
            cross_file_list[index])
        if self.compare_to_cross_algorithm_state(cube_reference,
                                                 algorithm_state):
            return algorithm

    return "No algorithms found."

def determine_f2l_pair_details_from_state(self, state, from_file):
    f2l_pair_details = [
        {"name": "corner", "selected": [], "location": 0,
         "colors": [], "parity": None},
        {"name": "edge", "selected": [], "location": 0,
         "colors": [], "parity": None}]
    if from_file:
        f2l_pair_details[0]["selected"] = ["w", "b", "r"]
        f2l_pair_details[1]["selected"] = ["b", "r"]
    else:
        f2l_pair_details[0]["selected"] = [state[5][1][1]] + solve_cube.selected_f2l_pair
        f2l_pair_details[1]["selected"] = solve_cube.selected_f2l_pair

    corner_indices = cube_coloring.corner_indices["top"] + [[[5, 0, 2], [2, 2, 2], [3, 2, 0]]]
    edge_indices = cube_coloring.edge_indices["top"] + [[[2, 1, 2], [3, 1, 0]]]
    indices = [corner_indices, edge_indices]

    parity_calculators = [self.calculate_corner_orientation_parity, self.calculate_edge_orientation_parity]

    for index in range(2):
        piece = f2l_pair_details[index]
        for tile_indices in indices[index]:
            colors = []
            for face, row, column in tile_indices:
                colors.append(state[face][row][column])
            sorted_colors = colors[:]
            sorted_colors.sort()
            sorted_selected = piece["selected"][:]
            sorted_selected.sort()

            if sorted_colors == sorted_selected:
                piece["location"] = indices[index].index(tile_indices) + 1
                piece["colors"] = colors
                piece["parity"] = parity_calculators[index](piece["selected"], piece["colors"])
                break

    return f2l_pair_details

def compare_to_f2l_algorithm_state(self, cube_reference, algorithm_state):
    algorithm_state_f2l_details = self.determine_f2l_pair_details_from_state(algorithm_state, True)

    cube_reference = cube_rotations.rotate_cube_to_required_location(cube_reference, solve_cube.selected_f2l_pair[0])

    cube_reference_f2l_details = self.determine_f2l_pair_details_from_state(cube_reference, False)
    print(cube_reference_f2l_details)
    print(algorithm_state_f2l_details)
    remove_from_dictionaries = ["selected", "colors"]
    for piece_index in range(2):
        for key in remove_from_dictionaries:
            del algorithm_state_f2l_details[piece_index][key]
            del cube_reference_f2l_details[piece_index][key]
    print(cube_reference_f2l_details)
    print(algorithm_state_f2l_details)

    if cube_reference_f2l_details == algorithm_state_f2l_details:
        return True
    else:
        return False

def search_through_f2l_algorithms(self, cube_reference):
    f2l_file_list = get_file_list_from_folder("algorithms\\f2l")

    cube_state, positioning_algorithm = self.position_f2l_pieces_correctly(cube_reference)
    print(positioning_algorithm)
    display_cube(cube_state)

    for index in range(len(f2l_file_list)):
        algorithm_state, algorithms = read_state_from_text_file(
            f2l_file_list[index])
        if self.compare_to_f2l_algorithm_state(cube_state,
                                               algorithm_state):
            algorithms = [f"{positioning_algorithm} {algorithm}" for algorithm in algorithms]
            return algorithms

    return "No algorithms found."

def move_corner_to_required_location(self, cube_state, corner_location):
    correct_location = [3, 6]
    wrong_top_location = [1, 2, 4]
    wrong_bottom_location = [5, 7, 8]

    algorithm = ""

    if corner_location not in correct_location:
        cube_rotations.set_cube_state(cube_state)
        if corner_location in wrong_top_location:
            rotation_details = [["U", 1, 2], ["U", 1, 1], ["U", -1, 1]]
            rotation_index = wrong_top_location.index(corner_location)

            cube_rotations.rotate_face(*rotation_details[rotation_index])
            algorithm = f"U{rotation_details[rotation_index][2]}".replace("1", "")
        else:
            rotation_details = ["L' U' L", "R' U2 R U", "L U2 L'"]
            rotation_index = wrong_bottom_location.index(corner_location)
            cube_rotations.perform_algorithm(rotation_details[rotation_index])
            algorithm = rotation_details[rotation_index]
        cube_state = cube_rotations.cube_state

    return cube_state, algorithm

def move_edge_to_top(self, cube_state, edge_location):
    correct_location = [1, 2, 3, 4, 7]
    wrong_middle_location = [5, 6, 8]

    algorithm = ""

    if edge_location not in correct_location:
        cube_rotations.set_cube_state(cube_state)

        rotation_details = ["L U' L' U", "L' U' L U", "R' U R'"]
        rotation_index = wrong_middle_location.index(edge_location)

        cube_rotations.perform_algorithm(
            rotation_details[rotation_index])
        algorithm = rotation_details[rotation_index]
        cube_state = cube_rotations.cube_state

    return cube_state, algorithm

def position_f2l_pieces_correctly(self, cube_state):
    selected_corner = [cube_state[5][1][1]] + solve_cube.selected_f2l_pair
    selected_edge = solve_cube.selected_f2l_pair

    corner_location = self.find_corner_location(cube_state, selected_corner)
    edge_location = self.find_edge_location(cube_state, selected_edge)

    cube_state, alg1 = self.move_corner_to_required_location(cube_state,
                                                             corner_location)
    cube_state, alg2 = self.move_edge_to_top(cube_state, edge_location)

    algorithm = f"{alg1} {alg2}"

    if corner_location == 6:
        new_edge_location = self.find_edge_location(cube_state, selected_edge)
        cube_state_copy = create_cube_copy(cube_state)
        cube_rotations.set_cube_state(cube_state_copy)

        for U_turn in range(3):
            face_color = cube_rotations.cube_state[new_edge_location][1][1]
            edge_color = cube_rotations.cube_state[new_edge_location][0][1]

            if edge_color == face_color:
                if U_turn == 0:
                    algorithm += ""
                elif U_turn == 1:
                    algorithm += "U"
                elif U_turn == 2:
                    algorithm += "U2"
                else:
                    algorithm += "U'"
                break
            else:
                cube_rotations.rotate_face("U")
                new_edge_location = self.find_edge_location(
                    cube_rotations.cube_state,
                    selected_edge)

    return cube_rotations.cube_state, algorithm

def find_corner_location(self, cube_state, selected_corner):
    corner_indices = cube_coloring.corner_indices["top"] + cube_coloring.corner_indices["bottom"]
    for index in range(len(corner_indices)):
        corner_colors = []
        for tile in corner_indices[index]:
            face, row, column = tile
            corner_colors.append(cube_state[face][row][column])

        sorted_colors = corner_colors[:]
        sorted_colors.sort()

        sorted_selected_colors = selected_corner[:]
        sorted_selected_colors.sort()

        if sorted_colors == sorted_selected_colors:
            return index + 1

def find_edge_location(self, cube_state, selected_edge):
    edge_indices = cube_coloring.edge_indices["top"] + \
                     cube_coloring.edge_indices["middle"]
    for index in range(len(edge_indices)):
        edge_colors = []
        for tile in edge_indices[index]:
            face, row, column = tile
            edge_colors.append(cube_state[face][row][column])

        sorted_colors = edge_colors[:]
        sorted_colors.sort()

        sorted_selected_colors = selected_edge[:]
        sorted_selected_colors.sort()

        if sorted_colors == sorted_selected_colors:
            return index + 1

def calculate_corner_orientation_parity(self, selected_corner_colors, corner_colors):
    relative_color = selected_corner_colors[0]
    for index in range(3):
        if relative_color == corner_colors[index]:
            return index

def calculate_edge_orientation_parity(self, selected_edge_colors, edge_colors):
    relative_color = selected_edge_colors[0]
    for index in range(3):
        if relative_color == edge_colors[index]:
            return index

def calculate_oll_color_order(self, state):
    oll_color_list = [state[face][row][column] for
                      face, row, column in cube_coloring.oll_indices]

    color_order = [y for y in range(len(oll_color_list)) if oll_color_list[y] == "y"]

    return color_order

def compare_to_oll_algorithm_state(self, cube_reference, algorithm_state):
    algorithm_color_order = self.calculate_oll_color_order(algorithm_state)

    for u_turn in range(3):
        color_order = self.calculate_oll_color_order(cube_reference)

        if color_order == algorithm_color_order:
            return True
        else:
            cube_rotations.set_cube_state(cube_reference)
            cube_rotations.rotate_face("U")
            cube_reference = cube_rotations.cube_state
    return False

def search_through_oll_algorithms(self, cube_reference):
    oll_file_list = get_file_list_from_folder("algorithms\\oll")

    for index in range(len(oll_file_list)):
        algorithm_state, algorithm = read_state_from_text_file(oll_file_list[index])
        if self.compare_to_oll_algorithm_state(cube_reference,
                                               algorithm_state):
            return algorithm

    return "No algorithms found."

def calculate_pll_color_order(self, state):
    pll_color_list = [state[face][row][column] for
                      face, row, column in cube_coloring.pll_indices]

    r = [r for r in range(len(pll_color_list)) if pll_color_list[r] == "r"]
    g = [g for g in range(len(pll_color_list)) if pll_color_list[g] == "g"]
    o = [o for o in range(len(pll_color_list)) if pll_color_list[o] == "o"]
    b = [b for b in range(len(pll_color_list)) if pll_color_list[b] == "b"]

    color_order = [r, g, o, b]

    return color_order

def compare_to_pll_algorithm_state(self, cube_reference, algorithm_state):
    # needs to be modified to give cube rotations and u turns
    # also to work with different start colors
    # try implement with other algorithms

    algorithm_color_order = self.calculate_pll_color_order(algorithm_state)

    for u_turn in range(3):
        color_order = self.calculate_pll_color_order(cube_reference)

        if color_order == algorithm_color_order:
            return True
        else:
            for index in range(1, 4):
                if color_order[index] == algorithm_color_order[0]:
                    for shift in range(index):
                        color_order.append(color_order.pop(0))

                    if color_order == algorithm_color_order:
                        return True

            cube_rotations.set_cube_state(cube_reference)
            cube_rotations.rotate_face("U")
            cube_reference = cube_rotations.cube_state
    return False

def search_through_pll_algorithms(self, cube_reference):
    pll_file_list = get_file_list_from_folder("algorithms\\pll")

    for index in range(len(pll_file_list)):
        algorithm_state, algorithm = read_state_from_text_file(pll_file_list[index])
        if self.compare_to_pll_algorithm_state(cube_reference, algorithm_state):
            return algorithm

    return "No algorithms found."