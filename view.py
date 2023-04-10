import customtkinter

from color_palette import ColorPaletteFrame
from input_assistors import InputAssistiveFunctionsFrame
from visual_cube_representation import CubeRepresentationFrame
from solve_and_current_algorithm_display import SolveAndCurrentAlgorithmDisplayFrame
from algorithm_display_and_state_reset import AlgorithmDisplayAndStateResetFrame

from other_functions import get_dictionary_details, settings


class View(customtkinter.CTkTabview):
    """
    A class that represents the UI of my application. This is the 'View' part of
    my MVC model.
    """
    def __init__(self, master, **kwargs):
        """
        Initialize parent attributes.
        Then initialize the attributes of the child class View.
        """
        super().__init__(master, **kwargs)

        # creating tabs

        self.add("Solving")
        self.add("Timing")
        self.add("Progress")

        # ============== adding frames to the Coloring tab ==================
        self.input_assistors = InputAssistiveFunctionsFrame(master=self.tab("Solving"),
                                                            corner_radius=0)
        self.input_assistors.grid(row=0, column=0, sticky='nswe', rowspan=3)

        self.color_palette = ColorPaletteFrame(master=self.tab("Solving"))
        self.color_palette.grid(row=0, column=1, padx=20, pady=10)

        self.cube_representation = CubeRepresentationFrame(master=self.tab("Solving"))
        self.cube_representation.grid(row=1, column=1, padx=20, pady=10)

        self.solve_and_current_algorithm_display = SolveAndCurrentAlgorithmDisplayFrame(master=self.tab("Solving"))
        self.solve_and_current_algorithm_display.grid(row=2, column=1, padx=10, pady=10)

        self.algorithm_display_and_state_reset = AlgorithmDisplayAndStateResetFrame(master=self.tab("Solving"))
        self.algorithm_display_and_state_reset.grid(row=0, column=2, rowspan=3 ,padx=20, pady=10, sticky="nsew")

    def get_selected_color_reference(self):
        """Returns the color reference of the selected color."""
        selected_color = self.input_assistors.selected_color_label.cget("fg_color")
        selected_color_reference = get_dictionary_details(settings.color_details,
                                                          selected_color,
                                                          "color_reference")
        return selected_color_reference

    def update_tile_colors(self, state):
        """Uses the state to update the cube representation accordingly."""
        self.cube_representation.update_tile_colors(state)

    def update_palette_variables(self, dictionary_of_number_of_colors):
        """
        Uses a dictionary containing the amount of each color on the cube, to
        update the variables on the color palette buttons.
        """
        self.color_palette.update_palette_variables(dictionary_of_number_of_colors)

    def update_checkbox_states(self, required_states):
        """Uses a list of required states to update the checkbox states."""
        self.input_assistors.change_checkbox_states(required_states)

    def disable_tiles_for_selection_using_enable_list(self, enable_list):
        """
        Uses a list of tile indices to disable tiles on the cube representation
        for tile selection.
        """
        self.cube_representation.disable_tiles_not_in_list(enable_list)

    def enable_all_tiles(self):
        """Enables all tiles on the cube representation."""
        self.cube_representation.enable_or_disable_all_tiles("normal")

    def update_algorithm_display(self, algorithm):
        """Updates the algorithm on the label that displays algorithms."""
        self.solve_and_current_algorithm_display.change_algorithm(algorithm)

        self.algorithm_display_and_state_reset.add_algorithm_to_display(algorithm)

    def clear_algorithm_displays(self):
        """Clears the algorithm on the display."""
        self.algorithm_display_and_state_reset.clear_algorithm_display()
        self.solve_and_current_algorithm_display.change_algorithm("")
