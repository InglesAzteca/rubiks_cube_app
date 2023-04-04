from coloring import CubeColoring
from solve_cube import SolveCube
from other_functions import create_cube_representation


class Model:
    def __init__(self):
        self.coloring_cube = CubeColoring(create_cube_representation("d"))
        self.solving_cube = None

        self.solving = False

        self.selected_color_reference = "d"

    def get_coloring_state(self):
        return self.coloring_cube.state

    def get_solving_state(self):
        return self.solving_cube.state

    def change_tile_reference(self, color_reference, face, row, column):
        self.coloring_cube.change_tile_color_reference(color_reference, face, row, column)

    def get_number_of_colors_on_cube(self):
        return self.coloring_cube.number_of_colors_on_cube

    def change_section_references_as_required(self, required_states, checkbox_names):
        self.coloring_cube.required_check_box_state_coloring(required_states, checkbox_names)

    def get_if_solving(self):
        return self.solving

    def is_cube_colored(self):
        return self.coloring_cube.is_cube_colored()

    def create_solving_cube(self):
        state = self.get_coloring_state()
        self.solving_cube = SolveCube(state)
        self.solving = True

    def is_selection_needed(self):
        return self.solving_cube.is_selection_needed()

    def set_selected_tile(self, face, row, column):
        self.solving_cube.set_selected_tile(face, row, column)

    def get_enable_list(self):
        return self.solving_cube.get_enable_list()

    def rotate_cube_due_to_selection(self):
        self.solving_cube.rotate_cube_due_to_selection()

    def solve_section(self):
        return self.solving_cube.solve_section()

    def format_suggested_algorithm_for_display(self, algorithms):
        return f"{algorithms[0].strip()} {algorithms[1][0].strip()}"
