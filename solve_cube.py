from cube import Cube
from other_functions import get_file_list_from_folder, read_state_from_text_file


class SolveCube(Cube):
    def __init__(self, state):
        super().__init__(state)

        self.cross = self.is_cross_solved()
        self.f2l = self.is_f2l_solved()
        self.oll = self.is_oll_solved()
        self.pll = self.is_pll_solved()

        self.selection_needed = False

        self.selected_tile = []

        self.current_section = "cross"

    def solve_cross(self):
        algorithm = self.search_through_cross_algorithms()
        if algorithm != "No algorithms found.":
            self.perform_algorithm(algorithm)
            self.update_current_section()
        return "", algorithm

    def determine_cross_piece_details_from_state(self, state, from_file):
        indices = self.edge_indices["bottom"] + \
                  self.edge_indices["middle"] + \
                  self.edge_indices["top"]

        edge_details = {"selected": [], "location": 0,
                        "cross_color": state[5][1][1], "colors": []}
        if from_file:
            edge_details["selected"] = ["b", "w"]
        else:
            edge_details["selected"] = [self.state[2][1][1], "w"]

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

    def compare_to_cross_algorithm_state(self, algorithm_state):
        algorithm_state_cross_piece_details = self.determine_cross_piece_details_from_state(
            algorithm_state, True)

        cube_reference_cross_piece_details = self.determine_cross_piece_details_from_state(
            self.state, False)

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

    def search_through_cross_algorithms(self):
        cross_file_list = get_file_list_from_folder("algorithms\\cross")

        for index in range(len(cross_file_list)):
            algorithm_state, algorithm = read_state_from_text_file(
                cross_file_list[index])
            if self.compare_to_cross_algorithm_state(algorithm_state):
                return algorithm

        return "No algorithms found."

    def solve_f2l(self):
        positioning_algorithm, algorithms = self.search_through_f2l_algorithms()
        if algorithms != "No algorithm found.":
            self.perform_algorithm(algorithms)
            self.update_current_section()
        return positioning_algorithm, algorithms

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
            f2l_pair_details[0]["selected"] = ["w", self.state[2][1][1], self.state[3][1][1]]
            f2l_pair_details[1]["selected"] = [self.state[2][1][1], self.state[3][1][1]]

        corner_indices = self.corner_indices["top"] + [[[5, 0, 2], [2, 2, 2], [3, 2, 0]]]
        edge_indices = self.edge_indices["top"] + [[[2, 1, 2], [3, 1, 0]]]
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

    def compare_to_f2l_algorithm_state(self, algorithm_state):
        algorithm_state_f2l_details = self.determine_f2l_pair_details_from_state(algorithm_state, True)

        cube_reference_f2l_details = self.determine_f2l_pair_details_from_state(self.state, False)

        remove_from_dictionaries = ["selected", "colors"]
        for piece_index in range(2):
            for key in remove_from_dictionaries:
                del algorithm_state_f2l_details[piece_index][key]
                del cube_reference_f2l_details[piece_index][key]

        if cube_reference_f2l_details == algorithm_state_f2l_details:
            return True
        else:
            return False

    def search_through_f2l_algorithms(self):
        f2l_file_list = get_file_list_from_folder("algorithms\\f2l")

        positioning_algorithm = self.position_f2l_pieces_correctly()

        for index in range(len(f2l_file_list)):
            algorithm_state, algorithms = read_state_from_text_file(
                f2l_file_list[index])
            if self.compare_to_f2l_algorithm_state(algorithm_state):
                return positioning_algorithm, algorithms

        return "No algorithms found."

    def move_corner_to_required_location(self, corner_location):
        correct_location = [3, 6]
        wrong_top_location = [1, 2, 4]
        wrong_bottom_location = [5, 7, 8]

        algorithm = ""

        if corner_location not in correct_location:
            if corner_location in wrong_top_location:
                rotation_details = [["U", 1, 2], ["U", 1, 1], ["U", -1, 1]]
                rotation_index = wrong_top_location.index(corner_location)

                self.rotate_face(*rotation_details[rotation_index])
                algorithm = f"U{rotation_details[rotation_index][2]}".replace("1", "")
            else:
                rotation_details = ["L' U' L", "R' U2 R U'", "L U2 L'"]
                rotation_index = wrong_bottom_location.index(corner_location)
                self.perform_algorithm([rotation_details[rotation_index]])
                algorithm = rotation_details[rotation_index]

        return algorithm

    def move_edge_to_top(self, edge_location):
        correct_location = [1, 2, 3, 4, 7]
        wrong_middle_location = [5, 6, 8]

        algorithm = ""

        if edge_location not in correct_location:

            rotation_details = ["L U' L' U", "L' U' L U", "R' U R'"]
            rotation_index = wrong_middle_location.index(edge_location)

            self.perform_algorithm([rotation_details[rotation_index]])
            algorithm = rotation_details[rotation_index]

        return algorithm

    def position_f2l_pieces_correctly(self):
        selected_corner = ["w", self.state[2][1][1], self.state[3][1][1]]
        selected_edge = [self.state[2][1][1], self.state[3][1][1]]

        corner_location = self.find_corner_location(selected_corner)
        alg1 = self.move_corner_to_required_location(corner_location)


        edge_location = self.find_edge_location(selected_edge)
        alg2 = self.move_edge_to_top(edge_location)

        algorithm = f"{alg1} {alg2}"
        algorithm = algorithm.strip()

        if corner_location == 6:
            new_edge_location = self.find_edge_location(selected_edge)
            edge_color = self.state[new_edge_location][0][1]

            required_location = self.find_face_index(edge_color)

            location_difference = new_edge_location - required_location

            alg3 = ""
            if location_difference != 0:
                alg3 += " U"
                if abs(location_difference) == 2:
                    alg3 += "2"
                elif location_difference < 0:
                    alg3 += "'"

            self.perform_algorithm([alg3])
            algorithm += alg3

        return algorithm

    def find_face_index(self, color_reference):
        for face_index in range(6):
            if color_reference == self.state[face_index][1][1]:
                return face_index

    def find_corner_location(self, selected_corner):
            corner_indices = self.corner_indices["top"] + self.corner_indices["bottom"]

            for index in range(len(corner_indices)):
                corner_colors = []
                for tile in corner_indices[index]:
                    face, row, column = tile
                    corner_colors.append(self.state[face][row][column])

                sorted_colors = corner_colors[:]
                sorted_colors.sort()

                sorted_selected_colors = selected_corner[:]
                sorted_selected_colors.sort()

                if sorted_colors == sorted_selected_colors:
                    return index + 1

    def find_edge_location(self, selected_edge):
            edge_indices = self.edge_indices["top"] + \
                             self.edge_indices["middle"]
            for index in range(len(edge_indices)):
                edge_colors = []
                for tile in edge_indices[index]:
                    face, row, column = tile
                    edge_colors.append(self.state[face][row][column])

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

    def solve_oll(self):
        positioning_algorithm, algorithms = self.search_through_oll_algorithms()
        if algorithms != "No algorithm found.":
            self.perform_algorithm([positioning_algorithm])
            self.perform_algorithm(algorithms)
            self.update_current_section()
        return positioning_algorithm, algorithms

    def calculate_oll_parities(self, state):
        corners = self.corner_indices["top"][:]
        edges = self.edge_indices["top"][:]
        edges.reverse()
        
        corner_parities = []
        edge_parities = []

        for piece_index in range(4):
            corner_piece = corners[piece_index]
            edge_piece = edges[piece_index]

            corner_colors = []
            for face, row, column in corner_piece:
                color = state[face][row][column]
                corner_colors.append(color)

            edge_colors = []
            for face, row, column in edge_piece:
                color = state[face][row][column]

                edge_colors.append(color)

            edge_colors.reverse()

            corner_parity = corner_colors.index("y")
            edge_parity = edge_colors.index("y")

            corner_parities.append(corner_parity)
            edge_parities.append(edge_parity)
        return corner_parities, edge_parities

    def compare_to_oll_algorithm_state(self, algorithm_state):
        algorithm_parities = self.calculate_oll_parities(algorithm_state)
        parities = self.calculate_oll_parities(self.state)

        if parities == algorithm_parities:
            return True, ""
        else:
            positioning_algorithm = ""
            for u_turn in range(3):
                # simulate a rotation in the clockwise direction
                corner_parities, edge_parities = parities

                corner_parities.insert(0, corner_parities.pop())
                edge_parities.insert(0, edge_parities.pop())

                positioning_algorithm += "U"

                if parities == algorithm_parities:
                    number_of_turns = positioning_algorithm.count("U")
                    if number_of_turns == 3:
                        positioning_algorithm = "U'"
                    elif number_of_turns == 2:
                        positioning_algorithm = "U2"
                    return True, positioning_algorithm

            return False, ""

    def search_through_oll_algorithms(self):
        oll_file_list = get_file_list_from_folder("algorithms\\oll")

        for index in range(len(oll_file_list)):
            algorithm_state, algorithms = read_state_from_text_file(oll_file_list[index])
            same_state, positioning_algorithm = self.compare_to_oll_algorithm_state(algorithm_state)
            if same_state:
                return positioning_algorithm, algorithms

        return "No algorithms found."

    def solve_pll(self):
        positioning_algorithm, algorithms = self.search_through_pll_algorithms()
        if algorithms != "No algorithm found.":
            self.perform_algorithm([positioning_algorithm])
            self.perform_algorithm(algorithms)
            self.update_current_section()
        return positioning_algorithm, algorithms

    def calculate_pll_color_order(self, state):

        pll_color_list = [state[face][row][column] for
                              face, row, column in self.pll_indices]

        r = [r for r in range(len(pll_color_list)) if pll_color_list[r] == "r"]
        g = [g for g in range(len(pll_color_list)) if pll_color_list[g] == "g"]
        o = [o for o in range(len(pll_color_list)) if pll_color_list[o] == "o"]
        b = [b for b in range(len(pll_color_list)) if pll_color_list[b] == "b"]

        color_order = [r, g, o, b]

        return color_order

    def compare_to_pll_algorithm_state(self, algorithm_state):
        # needs to be modified to give cube rotations and u turns
        # also to work with different start colors
        # try implement with other algorithms

        algorithm_color_order = self.calculate_pll_color_order(algorithm_state)
        color_order = self.calculate_pll_color_order(self.state)
        positioning_algorithm = ""
        for u_turn in range(5):
            if color_order == algorithm_color_order:

                number_of_turns = positioning_algorithm.count("U")
                if number_of_turns == 3:
                    positioning_algorithm = "U'"
                elif number_of_turns == 2:
                    positioning_algorithm = "U2"

                return True, positioning_algorithm
            else:
                for index in range(1, 4):
                    if color_order[index] == algorithm_color_order[0]:
                        shifted_color_order = color_order[:]
                        for shift in range(index):
                            shifted_color_order.append(shifted_color_order.pop(0))

                        if shifted_color_order == algorithm_color_order:

                            number_of_turns = positioning_algorithm.count("U")
                            if number_of_turns == 3:
                                positioning_algorithm = "U'"
                            elif number_of_turns == 2:
                                positioning_algorithm = "U2"

                            return True, positioning_algorithm
                positioning_algorithm += "U"

            color_order = [[(index - 3) % 12 for index in color_indices] for color_indices in color_order]
            for order in color_order:
                order.sort()


        return False, ""

    def search_through_pll_algorithms(self):
        pll_file_list = get_file_list_from_folder("algorithms\\pll")

        for index in range(len(pll_file_list)):
            algorithm_state, algorithms = read_state_from_text_file(pll_file_list[index])
            is_same, positioning_algorithm = self.compare_to_pll_algorithm_state(algorithm_state)
            if is_same:
                return positioning_algorithm, algorithms

        return "No algorithms found."
    
    def solve_section(self):
        self.update_current_section()
        if self.current_section == "cross":
            algorithm = self.solve_cross()

        elif self.current_section == "f2l":
            algorithm = self.solve_f2l()

        elif self.current_section == "oll":
            algorithm = self.solve_oll()

        elif self.current_section == "pll":
            algorithm = self.solve_pll()
        else:
            algorithm = self.last_rotations()
        self.update_current_section()
        return algorithm

    def last_rotations(self):
        last_algorithm = ""
        while self.is_pll_solved() and not self.is_cube_solved():
            self.U_turn()
            last_algorithm += "U"

        number_of_u_turns = last_algorithm.count("U")

        if number_of_u_turns == 3:
            last_algorithm = "U'"
        elif number_of_u_turns == 2:
            last_algorithm = "U2"

        return "", [last_algorithm]



    def update_current_section(self):
        self.cross = self.is_cross_solved()
        self.f2l = self.is_f2l_solved()
        self.oll = self.is_oll_solved()
        self.pll = self.is_pll_solved()

        if self.cross:
            if self.f2l:
                if self.oll:
                    if self.pll:
                        self.current_section = "solved"
                        return
                    self.current_section = "pll"
                    self.selection_needed = False
                    return
                self.current_section = "oll"
                self.selection_needed = False
                return
            self.current_section = "f2l"
            self.selection_needed = True
        else:
            self.current_section = "cross"
            self.selection_needed = True

    def search_for_unsolved_cross_pieces(self):
        unsolved_cross_pieces = self.edge_indices["bottom"][:]
        for index in range(4):
            tile_1, tile_2 = self.edge_indices["bottom"][index]

            face_1, row_1, column_1 = tile_1
            actual_color_1 = self.state[face_1][row_1][column_1]
            required_color_1 = self.state[face_1][1][1]

            face_2, row_2, column_2 = tile_2
            actual_color_2 = self.state[face_2][row_2][column_2]
            required_color_2 = self.state[face_2][1][1]

            if actual_color_1 == required_color_1 and actual_color_2 == required_color_2:
                unsolved_cross_pieces.remove(self.edge_indices["bottom"][index])
        return unsolved_cross_pieces

    def search_for_unsolved_f2l_pairs(self):
        f2l_edges = self.edge_indices["middle"][:]
        f2l_edges.append(f2l_edges.pop(0))
        f2l_corners = self.corner_indices["bottom"][:]

        unsolved_f2l_edges = f2l_edges[:]
        unsolved_f2l_corners = f2l_corners[:]

        for index in range(4):
            f2l_pair_indices = f2l_edges[index] + f2l_corners[index]
            for face, row, column in f2l_pair_indices:
                actual_color = self.state[face][row][column]
                solved_color = self.state[face][1][1]

                if actual_color == solved_color:
                    is_f2l_pair_solved = True
                else:
                    is_f2l_pair_solved = False
                    break

            if is_f2l_pair_solved:
                unsolved_f2l_edges.remove(f2l_edges[index])
                unsolved_f2l_corners.remove(f2l_corners[index])

        return unsolved_f2l_edges, unsolved_f2l_corners

    def is_selection_needed(self):
        self.update_current_section()
        if self.current_section == "cross":
            self.selection_needed = True
        elif self.current_section == "f2l":
            self.selection_needed = True
        return self.selection_needed

    def get_cross_enable_list(self):
        unsolved_cross_pieces = self.search_for_unsolved_cross_pieces()
        enable_list = [indices for pieces in unsolved_cross_pieces for indices in pieces]
        return enable_list

    def get_f2l_enable_list(self):
        unsolved_f2l_pairs = self.search_for_unsolved_f2l_pairs()
        enable_list = [indices for pieces in unsolved_f2l_pairs for piece in pieces for indices in piece]
        return enable_list

    def get_enable_list(self):
        self.update_current_section()
        if self.current_section == "cross":
            enable_list = self.get_cross_enable_list()
        elif self.current_section == "f2l":
            enable_list = self.get_f2l_enable_list()
        else:
            enable_list = []

        return enable_list

    def set_selected_tile(self, face, row, column):
        self.selected_tile = [face, row, column]

    def rotate_cube_due_to_selection(self):
        face_index = self.get_face_index_from_selected()
        centre_color = self.state[face_index][1][1]

        self.rotate_cube_to_required_location(centre_color)

    def get_face_index_from_selected(self):
        if self.selected_tile in self.cross_indices:
            for piece in self.edge_indices["bottom"]:
                if self.selected_tile in piece:
                    return piece[0][0]
        elif self.selected_tile in self.f2l_indices:
            for piece in self.edge_indices["middle"]:
                if self.selected_tile in piece:
                    return piece[0][0]
            for piece in self.corner_indices["bottom"]:
                if self.selected_tile in piece:
                    return piece[1][0]




cube_state = [[["y", "y", "y"], ["y", "y", "y"], ["y", "y", "y"]],
              [["r", "b", "g"], ["r", "r", "r"], ["r", "r", "r"]],
              [["o", "o", "r"], ["g", "g", "g"], ["g", "g", "g"]],
              [["g", "r", "o"], ["o", "o", "o"], ["o", "o", "o"]],
              [["b", "g", "b"], ["b", "b", "b"], ["b", "b", "b"]],
              [["w", "w", "w"], ["w", "w", "w"], ["w", "w", "w"]]]

# cs = SolveCube(cube_state)
# print(cs.search_through_pll_algorithms())


