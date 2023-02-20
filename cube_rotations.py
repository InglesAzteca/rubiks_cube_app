from other_functions import create_cube_copy, create_face_copy


class CubeRotations:
    def __init__(self, cube_reference, edge_indices, corner_indices):
        self.cube_state = cube_reference
        self.edge_indices = edge_indices
        self.corner_indices = corner_indices

    def set_cube_state(self, cube_state):
        self.cube_state = cube_state

    def simulate_cube_rotation_with_list_of_centres(self, list_of_centres, x_y_z, prime=1, amount=1):
        if x_y_z == 'x':
            face_coordinates = [[0, 2], [2, 5], [5, 4]]
        elif x_y_z == 'y':
            face_coordinates = [[1, 2], [2, 3], [3, 4]]
        elif x_y_z == 'z':
            face_coordinates = [[0, 1], [1, 5], [5, 3]]

        for number_of_rotations in range(amount):
            # if prime equals -1 the values in the list are reversed
            for r in face_coordinates[::prime]:
                r = r[::prime]
                list_of_centres[r[0]], list_of_centres[r[1]] = list_of_centres[r[1]], list_of_centres[r[0]]
        return list_of_centres

    def rotate_cube(self, x_y_z, prime=1, amount=1):
        """Simulates a rotation of the cube."""
        cube_state_copy = create_cube_copy(self.cube_state)

        x_rotation_details = {"face_coordinates": [[0, 2], [2, 5], [5, 4]],
                              "affected_faces": [[1, 3, 4, 5], [0, 1, 3, 4]],
                              "direction": [[-1, 1, 1, 1], [1, 1, -1, 1]],
                              "amount": [[1, 1, 2, 2], [2, 1, 1, 2]]}
        y_rotation_details = {"face_coordinates": [[1, 2], [2, 3], [3, 4]],
                              "affected_faces": [[0, 5], [0, 5]],
                              "direction": [[1, -1], [-1, 1]],
                              "amount": [[1, 1], [1, 1]]}
        z_rotation_details = {"face_coordinates": [[0, 1], [1, 5], [5, 3]],
                              "affected_faces": [[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]],
                              "direction": [[1, 1, 1, 1, -1, 1], [-1, -1, -1, -1, 1, -1]],
                              "face_rotation_amount": [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]}
        if x_y_z == 'x':
            rotation_details = x_rotation_details
        elif x_y_z == 'y':
            rotation_details = y_rotation_details
        elif x_y_z == 'z':
            rotation_details = z_rotation_details

        face_coordinates, affected_faces, direction, face_rotation_amount = rotation_details.values()

        for number_of_rotations in range(amount):
            # if prime equals -1 the values in the list are reversed
            for r in face_coordinates[::prime]:
                r = r[::prime]
                cube_state_copy[r[0]], cube_state_copy[r[1]] = cube_state_copy[r[1]], cube_state_copy[r[0]]

            self.set_cube_state(cube_state_copy)

            if prime == 1:
                prime_index = 0
            elif prime == -1:
                prime_index = 1

            for index in range(len(affected_faces[prime_index])):
                self.rotate_tiles_on_face(affected_faces[prime_index][index], direction[prime_index][index], face_rotation_amount[prime_index][index])

    def rotate_tiles_on_face(self, face_index, direction=1, amount=1):
        for number_of_rotations in range(amount):
            face_copy = create_face_copy(self.cube_state[face_index])

            face_corner_indices = [[row, column] for row in range(3) for column in range(3) if row != 1 and column != 1]
            face_corner_indices.append(face_corner_indices.pop(-2))

            face_edge_indices = [[row, column] for row in range(3) for column in range(3) if (row != 1 and column == 1) or (row == 1 and column != 1)]
            face_edge_indices.append(face_edge_indices.pop(1))

            shifted_face_corner_indices = face_corner_indices[:]
            shifted_face_edge_indices = face_edge_indices[:]

            if direction == 1:
                shifted_face_corner_indices.insert(0, shifted_face_corner_indices.pop())
                shifted_face_edge_indices.insert(0, shifted_face_edge_indices.pop())
            elif direction == -1:
                shifted_face_corner_indices.append(shifted_face_corner_indices.pop(0))
                shifted_face_edge_indices.append(shifted_face_edge_indices.pop(0))

            for index in range(4):
                corner_row, corner_column = face_corner_indices[index]
                edge_row, edge_column = face_edge_indices[index]

                shifted_corner_row, shifted_corner_column = shifted_face_corner_indices[index]
                shifted_edge_row, shifted_edge_column = shifted_face_edge_indices[index]

                face_copy[corner_row][corner_column] = self.cube_state[face_index][shifted_corner_row][shifted_corner_column]
                face_copy[edge_row][edge_column] = self.cube_state[face_index][shifted_edge_row][shifted_edge_column]

            self.cube_state[face_index] = create_face_copy(face_copy)

    def U_turn(self, prime, amount):
        cube_state_copy = create_cube_copy(self.cube_state)

        top_corners = self.corner_indices["top"][:]
        top_edges = self.edge_indices["top"][:]

        for number_of_rotations in range(amount):
            if prime == 1:
                top_corners.append(top_corners.pop(0))
                top_edges.insert(0, top_edges.pop())
            elif prime == -1:
                top_corners.insert(0, top_corners.pop())
                top_edges.append(top_edges.pop(0))

            for piece in range(4):
                for tile_index in range(3):
                    color_index = self.corner_indices["top"][piece][tile_index]
                    new_color_index = top_corners[piece][tile_index]

                    face_1, row_1, column_1 = color_index
                    face_2, row_2, column_2 = new_color_index

                    cube_state_copy[face_2][row_2][column_2] = \
                        self.cube_state[face_1][row_1][column_1]

                for tile_index in range(2):
                    color_index = self.edge_indices["top"][piece][tile_index]
                    new_color_index = top_edges[piece][tile_index]

                    face_1, row_1, column_1 = color_index
                    face_2, row_2, column_2 = new_color_index

                    cube_state_copy[face_2][row_2][column_2] = \
                        self.cube_state[face_1][row_1][column_1]

        self.set_cube_state(cube_state_copy)

    def rotate_face(self, notation, prime=1, amount=1):
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
            self.rotate_face("L", -prime, amount)
            self.rotate_face("R", prime, amount)
        elif notation == "E":
            self.rotate_cube("y", -prime, amount)
            self.rotate_face("U", prime, amount)
            self.rotate_face("D", -prime, amount)
        elif notation == "S":
            self.rotate_cube("z", prime, amount)
            self.rotate_face("F", -prime, amount)
            self.rotate_face("B", prime, amount)
        elif notation == "u":
            self.rotate_cube("y", prime, amount)
            self.rotate_face("D", prime, amount)
        elif notation == "l":
            self.rotate_cube("x", -prime, amount)
            self.rotate_face("R", prime, amount)
        elif notation == "f":
            self.rotate_cube("z", prime, amount)
            self.rotate_face("B", prime, amount)
        elif notation == "r":
            self.rotate_cube("x", prime, amount)
            self.rotate_face("L", prime, amount)
        elif notation == "b":
            self.rotate_cube("z", -prime, amount)
            self.rotate_face("F", prime)
        elif notation == "d":
            self.rotate_cube("y", -prime, amount)
            self.rotate_face("U", prime, amount)

    def perform_algorithm(self, algorithm):
        algorithm = algorithm[0]
        remove = ["(", ")", "[", "]"]
        cube_rotation_notations = ["x", "y", "z"]

        for character in remove:
            algorithm = algorithm.replace(character, "")

        algorithm = algorithm.split()

        for notation in algorithm:
            prime = 1
            amount = 1
            if "'" in notation:
                prime = -1
                notation = notation.strip("'")
            if "2" in notation:
                amount = 2
                notation = notation.strip("2")

            if notation in cube_rotation_notations:
                self.rotate_cube(notation, prime, amount)
            else:
                self.rotate_face(notation, prime, amount)

    def rotate_cube_to_required_location(self, cube_reference, selected):
        centre_colors = [cube_reference[face_index][1][1] for face_index in range(1, 5)]
        color_1_index = centre_colors.index(selected)

        number_of_rotations = [3, 0, 1, 2]
        self.set_cube_state(cube_reference)
        self.rotate_cube("y", amount=number_of_rotations[color_1_index])
        cube_reference = self.cube_state

        return cube_reference










