from coloring import CubeColoring
from solve_cube import SolveCube
from other_functions import create_cube_representation


class Model:
    """
    A class that represents the data and algorithms of my application. This is
    the 'Model' part of my MVC model.
    """
    def __init__(self):
        """Initialize the attributes of my class."""

        self.coloring_cube = CubeColoring(create_cube_representation("d"))
        self.solving_cube = None

        self.solving = False

        self.selected_color_reference = "d"

    def get_coloring_state(self):
        """Returns the state of the class that is used for coloring."""
        return self.coloring_cube.state

    def get_solving_state(self):
        """Returns the state of the class that is used for solving."""
        return self.solving_cube.state

    def change_tile_reference(self, color_reference, face, row, column):
        """Changes the color reference of a tile in the coloring cube."""
        self.coloring_cube.change_tile_color_reference(color_reference, face, row, column)

    def get_number_of_colors_on_cube(self):
        """Returns a dictionary containing the amount of each color on the
        coloring cube."""
        return self.coloring_cube.number_of_colors_on_cube

    def change_section_references_as_required(self, required_states, checkbox_names):
        """Changes the color references of different sections using a list of
        required states."""
        self.coloring_cube.required_check_box_state_coloring(required_states, checkbox_names)

    def get_if_solving(self):
        """Returns the attribute solving which represents if the application is
        currently solving a state or not."""
        return self.solving

    def is_cube_colored(self):
        """
        Returns a boolean value depending if the cube has been fully colored.
        """
        return self.coloring_cube.is_cube_colored()

    def create_solving_cube(self):
        """
        Creates and stores an instance of the class SolveCube in the attribute
        solving cube. The state passed in is the state of the coloring cube.

        The attribute solving is also set to true.
        """
        state = self.get_coloring_state()
        self.solving_cube = SolveCube(state)
        self.solving = True

    def is_selection_needed(self):
        """Checks if a selection is needed for the current stage."""
        return self.solving_cube.is_selection_needed()

    def set_selected_tile(self, face, row, column):
        """Sets a selected tile by setting the index of that tile."""
        self.solving_cube.set_selected_tile(face, row, column)

    def get_enable_list(self):
        """Returns a list of tile indices that can be selected."""
        return self.solving_cube.get_enable_list()

    def rotate_cube_due_to_selection(self):
        """Rotates the solve cube according to a selection."""
        self.solving_cube.rotate_cube_due_to_selection()

    def solve_section(self):
        """Calls the solve section method that returns an algorithm that has
        solved the current section."""
        return self.solving_cube.solve_section()

    def format_suggested_algorithm_for_display(self, algorithms):
        """
        Returns a formatted string that contains a positioning algorithm and the
        suggested algorithm, ready to display for the user.
        """
        return f"{algorithms[0].strip()} {algorithms[1][0].strip()}".strip()

    def reset_coloring(self):
        """Resets the coloring cube state and resets the number of colors on the
        cube."""
        self.coloring_cube.reset_state_to_default()
        self.coloring_cube.reset_number_of_colors_on_cube()


