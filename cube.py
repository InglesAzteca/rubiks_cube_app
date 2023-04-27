from other_functions import create_face_copy, create_cube_copy


class CubeDetails:
    """
    This class contains methods and attributes that create and store grouped
    cube indices and cube rotation details along with a list of possible moves.
    """
    def __init__(self):
        """Initialize class attributes."""
        self.possible_moves = list("xyzULFRBDMESulfrbd")
        self.x_rotation_details = {"face_coordinates": [[0, 2], [2, 5], [5, 4]],
                                   "affected_faces": [[1, 3, 4, 5], [0, 1, 3, 4]],
                                   "direction": [[-1, 1, 1, 1], [1, 1, -1, 1]],
                                   "amount": [[1, 1, 2, 2], [2, 1, 1, 2]]}
        self.y_rotation_details = {"face_coordinates": [[1, 2], [2, 3], [3, 4]],
                                   "affected_faces": [[0, 5], [0, 5]],
                                   "direction": [[1, -1], [-1, 1]],
                                   "amount": [[1, 1], [1, 1]]}
        self.z_rotation_details = {"face_coordinates": [[0, 1], [1, 5], [5, 3]],
                                   "affected_faces": [[0, 1, 2, 3, 4, 5],
                                                     [0, 1, 2, 3, 4, 5]],
                                   "direction": [[1, 1, 1, 1, -1, 1],
                                                 [-1, -1, -1, -1, 1, -1]],
                                   "face_rotation_amount": [[1, 1, 1, 1, 1, 1],
                                                            [1, 1, 1, 1, 1, 1]]}

        self.corner_indices = {'top': None, 'bottom': None}
        self.edge_indices = {'top': None, 'middle': None, 'bottom': None}
        self.cross_indices = []
        self.f2l_indices = []
        self.oll_indices = []
        self.pll_indices = []

        # Adds indices to the attributes above by calling methods in the class
        self.add_indices()

    def add_empty_lists_to_indices_dictionary(self, *dictionaries):
        """Adds 4 empty lists to each section of the indices dictionary."""
        for dictionary in dictionaries:
            for key in dictionary.keys():
                dictionary[key] = [[] for x in range(4)]

    def create_edge_indices(self):
        """Creates the indices for each edge on the cube using modulus to create
        a specific index sequence."""

        # top edge indices sequences
        # -----sequence 1------sequence 2-----
        #       1 0 1           0 1 0
        #       2 0 1           0 2 1
        #       3 0 1           0 1 2
        #       4 0 1           0 0 1

        # middle edge indices sequences
        # -----sequence 3------sequence 4-----
        #       4 1 2           1 1 0
        #       1 1 2           2 1 0
        #       2 1 2           3 1 0
        #       3 1 2           4 1 0

        # bottom edge indices sequences
        # -----sequence 6------sequence 6-----
        #       1 2 1           5 1 0
        #       2 2 1           5 0 1
        #       3 2 1           5 1 2
        #       4 2 1           5 2 1

        for index in range(4):
            self.edge_indices['top'][index].append([index + 1, 0, 1])  # creates sequence 1
            self.edge_indices['top'][index].append([0, 5 % (index + 2), 5 % (index + 1)])  # creates sequence 2

            self.edge_indices['middle'][index].append([abs(index + (4 % (4 + index)) - 4), 1,2])  # creates sequence 3
            self.edge_indices['middle'][index].append([index + 1, 1, 0])  # creates sequence 4

            self.edge_indices['bottom'][index].append([index + 1, 2, 1])  # creates sequence 5
            self.edge_indices['bottom'][index].append([5, abs(index - 1), 5 % (index + 1)])  # creates sequence 6

    def create_corner_indices(self):
        """Creates the indices for each corner on the cube using modulus to
        create a specific index sequence."""

        # top corner indices sequences
        # -----sequence 1------sequence 2------sequence 3-----
        #       0 0 0           1 0 0           4 0 2
        #       0 0 2           4 0 0           3 0 2
        #       0 2 2           3 0 0           2 0 2
        #       0 2 0           2 0 0           1 0 2

        # bottom corner indices sequences
        # -----sequence 4------sequence 5------sequence 6-----
        #       5 0 0           1 2 2           2 2 0
        #       5 0 2           2 2 2           3 2 0
        #       5 2 2           3 2 2           4 2 0
        #       5 2 0           4 2 2           1 2 0

        for index in range(4):
            self.corner_indices['top'][index].append([0, 2 % (index + 1), 2 * (index ** 2) % 3])  # creates sequence 1
            self.corner_indices['top'][index].append([(5 - index) % (4 + index), 0, 0])  # creates sequence 2
            self.corner_indices['top'][index].append([4 - index, 0, 2])  # creates sequence 3

            self.corner_indices['bottom'][index].append([5, 2 % (index + 1), 2 * (index ** 2) % 3])  # creates sequence 4
            self.corner_indices['bottom'][index].append([index + 1, 2, 2])  # creates sequence 5
            self.corner_indices['bottom'][index].append([(index + 2) % (7 - index), 2, 0])  # creates sequence 6

    def create_cross_indices(self):
        """
        Returns a list of indices of the tiles in the cross section of the cube.
        """
        centre_tile = [5, 1, 1]
        cross_indices = [index for edge in self.edge_indices["bottom"] for index
                         in edge]
        cross_indices.append(centre_tile)
        return cross_indices

    def create_f2l_indices(self):
        """
        Returns a list of indices of the tiles in the F2L section of the cube.
        """
        centre_tiles = [[face, 1, 1] for face in range(1, 5)]
        bottom_corner = [index for corner in self.corner_indices["bottom"] for
                         index in corner]
        middle_edge = [index for edge in self.edge_indices["middle"] for index
                       in edge]

        indices = [bottom_corner, middle_edge, centre_tiles]
        return [cord for section in indices for cord in section]

    def create_oll_indices(self):
        """
        Returns a list of indices of the tiles in the OLL section of the cube.
        """
        face = 0
        top_face_indices = [[face, row, column] for row in range(3) for column in
                       range(3)]
        return top_face_indices + self.pll_indices

    def create_pll_indices(self):
        """
        Returns a list of indices of the tiles in the PLL section of the cube.
        """
        row = 0
        return [[face, row, column] for face in range(1, 5) for column in range(3)]

    def add_indices(self):
        """Adds all indices to the attributes."""
        self.add_empty_lists_to_indices_dictionary(self.corner_indices,
                                                   self.edge_indices)
        self.create_edge_indices()
        self.create_corner_indices()

        self.cross_indices = self.create_cross_indices()
        self.f2l_indices = self.create_f2l_indices()
        self.oll_indices = self.create_oll_indices()
        self.pll_indices = self.create_pll_indices()


class Cube(CubeDetails):
    """
    This class models a 3 by 3 rubik's cube by simulating rotations, performing
    algorithms and updating the state accordingly.
    """
    def __init__(self, state):
        """Initialize parent attributes then initialize child attributes."""
        super().__init__()
        self.state = state
        self.moves = ""

    def is_cross_solved(self):
        """Returns True if the cross section is solved and False if its not."""
        for indices in self.cross_indices:
            face, row, column = indices
            centre_color = self.state[face][1][1]
            if self.state[face][row][column] != centre_color:
                return False
        return True

    def is_f2l_solved(self):
        """Returns True if the F2L section is solved and False if its not."""
        # loops through the indices
        for face, row, column in self.f2l_indices:
            centre_color = self.state[face][1][1]
            # compares tiles to the centre tile color
            if self.state[face][row][column] != centre_color:
                return False
        return True

    def is_oll_solved(self):
        """Returns True if the OLL section is solved and False if its not."""
        # loops through the first face (face_index = 0)
        for row in self.state[0]:
            # in a set there are not repeated values
            if not len(set(row)) == 1:
                return False
        return True

    def is_pll_solved(self):
        """Returns True if the PLL section is solved and False if its not."""
        for face in self.state:
            for row in face:
                if not len(set(row)) == 1:
                    return False
        return True

    def is_cube_solved(self):
        """Returns True if the cube is solved and False if its not."""
        for face in range(6):
            for row in range(3):
                for column in range(3):
                    # compares tiles on the cube to the centre tile of that face
                    if self.state[face][row][column] != self.state[face][1][1]:
                        return False
        return True

    def add_move_to_moves(self, notation):
        """Add the moves performed to the attribute that stores the moves."""
        if notation in self.possible_moves:
            self.moves.join(notation)

    def rotate_cube(self, x_y_z, prime=1, amount=1):
        """Simulates a rotation of the cube."""
        self.add_move_to_moves(x_y_z)

        if x_y_z == 'x':
            rotation_details = self.x_rotation_details
        elif x_y_z == 'y':
            rotation_details = self.y_rotation_details
        elif x_y_z == 'z':
            rotation_details = self.z_rotation_details

        face_coordinates, affected_faces, directions, face_rotation_amount = rotation_details.values()

        # moves faces around
        for number_of_rotations in range(amount):
            # if prime equals -1 the values in the list are reversed
            for face_indices in face_coordinates[::prime]:
                # if prime equals -1 the pair of face indices are reversed
                face_indices = face_indices[::prime]

                self.state[face_indices[0]], self.state[face_indices[1]] = \
                    self.state[face_indices[1]], self.state[face_indices[0]]

            if prime == 1:
                prime_index = 0
            elif prime == -1:
                prime_index = 1

            # rotates tiles on faces that need tile rotations (affected faces)
            for index in range(len(affected_faces[prime_index])):
                face = affected_faces[prime_index][index]
                direction = directions[prime_index][index]
                rotation_amount = face_rotation_amount[prime_index][index]

                self.rotate_tiles_on_face(face, direction, rotation_amount)

    def perform_move(self, notation, prime=1, amount=1):
        """
        This method performs any move on the cube using self.U_turn,
        self.rotate_cube, notation, prime and amount.

        :param notation: A string value representing a move on the cube.
        :param prime: The direction of rotation.
        (clockwise: prime = 1, anti-clockwise: prime = -1)
        :param amount: The number of rotations.
        """
        self.add_move_to_moves(notation)

        if notation == "U":
            self.U_turn(prime, amount)

        elif notation == "L":
            self.rotate_cube("z")
            self.U_turn(prime, amount)
            self.rotate_cube("z", -1)

        elif notation == "F":
            self.rotate_cube("x")
            self.U_turn(prime, amount)
            self.rotate_cube("x", -1)

        elif notation == "R":
            self.rotate_cube("z", -1)
            self.U_turn(prime, amount)
            self.rotate_cube("z")

        elif notation == "B":
            self.rotate_cube("x", -1)
            self.U_turn(prime, amount)
            self.rotate_cube("x")

        elif notation == "D":
            self.rotate_cube("x", amount=2)
            self.U_turn(prime, amount)
            self.rotate_cube("x", amount=2)

        elif notation == "M":
            self.rotate_cube("x", -prime, amount)
            self.perform_move("L", -prime, amount)
            self.perform_move("R", prime, amount)

        elif notation == "E":
            self.rotate_cube("y", -prime, amount)
            self.perform_move("U", prime, amount)
            self.perform_move("D", -prime, amount)

        elif notation == "S":
            self.rotate_cube("z", prime, amount)
            self.perform_move("F", -prime, amount)
            self.perform_move("B", prime, amount)

        elif notation == "u":
            self.rotate_cube("y", prime, amount)
            self.perform_move("D", prime, amount)

        elif notation == "l":
            self.rotate_cube("x", -prime, amount)
            self.perform_move("R", prime, amount)

        elif notation == "f":
            self.rotate_cube("z", prime, amount)
            self.perform_move("B", prime, amount)

        elif notation == "r":
            self.rotate_cube("x", prime, amount)
            self.perform_move("L", prime, amount)

        elif notation == "b":
            self.rotate_cube("z", -prime, amount)
            self.perform_move("F", prime)

        elif notation == "d":
            self.rotate_cube("y", -prime, amount)
            self.perform_move("U", prime, amount)

    def U_turn(self, prime=1, amount=1):
        """
        This method simulates a U rotation on the cube.

        :param prime: Prime refers to the direction of rotation so either
        clockwise (prime = 1) or anti-clockwise (prime = -1).
        :param amount: Is the number of rotations.
        """
        # The layer being turned is the top layer of the cube
        # The top layer consists of 4 corners and 4 edges and the centre
        top_corners = self.corner_indices["top"][:]
        top_edges = self.edge_indices["top"][:]

        cube_copy = create_cube_copy(self.state)

        for number_of_rotations in range(amount):
            # if the tiles are being rotated clockwise
            # the first corner becomes the last
            # the last edge becomes the first
            if prime == 1:
                top_corners.append(top_corners.pop(0))
                top_edges.insert(0, top_edges.pop())
            # if the tiles are being rotated anti-clockwise
            # the last corner becomes the first
            # the first edge becomes the last
            elif prime == -1:
                top_corners.insert(0, top_corners.pop())
                top_edges.append(top_edges.pop(0))

            for piece in range(4):
                # using the cube copy to move corner tiles around
                for tile_index in range(3):
                    color_index = self.corner_indices["top"][piece][tile_index]
                    new_color_index = top_corners[piece][tile_index]

                    face_1, row_1, column_1 = color_index
                    face_2, row_2, column_2 = new_color_index

                    cube_copy[face_2][row_2][column_2] = self.state[face_1][row_1][column_1]

                # using the cube copy to move edge tiles around
                for tile_index in range(2):
                    color_index = self.edge_indices["top"][piece][tile_index]
                    new_color_index = top_edges[piece][tile_index]

                    face_1, row_1, column_1 = color_index
                    face_2, row_2, column_2 = new_color_index

                    cube_copy[face_2][row_2][column_2] = self.state[face_1][row_1][column_1]

        # after we have moved the pieces on the cube_copy
        # we change the state to the cube_copy
        self.state = cube_copy

    def rotate_tiles_on_face(self, face_index, direction=1, amount=1):
        """
        This method rotates the tiles on a specific face (face_index) in a
        certain direction (direction) for a number of rotations (amount).

        :param face_index: Is the index of the face we want to rotate the tiles.
        :param direction: Is the direction we want to rotate the tiles around
        the centre tile (clockwise = 1, anti-clockwise = -1).
        :param amount: Is the number of rotations we want to perform.
        """
        for number_of_rotations in range(amount):
            face = create_face_copy(self.state[face_index])

            # we split the face indices into corner and edge indices
            face_corner_indices = [[row, column] for row in range(3) for column in range(3)
                                   if row != 1 and column != 1]
            # rearrange the face_corner_indices to a specific order
            face_corner_indices.append(face_corner_indices.pop(-2))

            face_edge_indices = [[row, column] for row in range(3) for column in range(3)
                                 if (row != 1 and column == 1) or (row == 1 and column != 1)]
            # rearrange the face_edge_indices to a specific order
            face_edge_indices.append(face_edge_indices.pop(1))

            # we create a copies that we will shift
            shifted_face_corner_indices = face_corner_indices[:]
            shifted_face_edge_indices = face_edge_indices[:]

            # if the tiles are being rotated clockwise
            # the last tile will move to the first position
            if direction == 1:
                shifted_face_corner_indices.insert(0, shifted_face_corner_indices.pop())
                shifted_face_edge_indices.insert(0, shifted_face_edge_indices.pop())
            # if the tiles are being rotated anti-clockwise
            # the first tile will move to the last position
            elif direction == -1:
                shifted_face_corner_indices.append(shifted_face_corner_indices.pop(0))
                shifted_face_edge_indices.append(shifted_face_edge_indices.pop(0))

            for index in range(4):
                corner_row, corner_column = face_corner_indices[index]
                edge_row, edge_column = face_edge_indices[index]

                shifted_corner_row, shifted_corner_column = shifted_face_corner_indices[index]
                shifted_edge_row, shifted_edge_column = shifted_face_edge_indices[index]

                # shifted indices are used to change the values on the face copy
                face[corner_row][corner_column] = self.state[face_index][shifted_corner_row][shifted_corner_column]
                face[edge_row][edge_column] = self.state[face_index][shifted_edge_row][shifted_edge_column]

            # finally the cube face is set to the face with shifted tiles
            self.state[face_index] = face

    def perform_algorithm(self, algorithm):
        """
        This method performs an algorithm by removing unnecessary notation and
        obtaining prime and amount values.

        :param algorithm: Is a list of algorithms that result in the same final
        state.
        """
        algorithm = algorithm[0]

        remove = ["(", ")", "[", "]"]
        cube_rotation_notations = ["x", "y", "z"]

        # removes unnecessary notation
        for character in remove:
            algorithm = algorithm.replace(character, "")

        # turns the string into a list
        algorithm = algorithm.split()

        # loops through the algorithm an performs moves individually in order
        for notation in algorithm:
            prime = 1
            amount = 1
            if "'" in notation:
                prime = -1
                notation = notation.strip("'")
            if "2" in notation:
                amount = 2
                notation = notation.strip("2")

            # performs a move
            if notation in cube_rotation_notations:
                self.rotate_cube(notation, prime, amount)
            else:
                self.perform_move(notation, prime, amount)

    def rotate_cube_to_required_location(self, selected):
        """
        Rotated the cube to a required location where an algorithm can be
        performed from, using a selected color.

        :param selected: A color reference of a face that has been selected.
        """
        # gets centre tile references where face_index is between 1 and 4
        centre_colors = [self.state[face_index][1][1] for face_index in range(1, 5)]
        # gets the index of that face in the centre tile references
        color_index = centre_colors.index(selected)

        # the amount of rotations depends on the location
        # each value refers to the amount of rotations at a specific location
        number_of_rotations = [3, 0, 1, 2]
        self.rotate_cube("y", amount=number_of_rotations[color_index])

