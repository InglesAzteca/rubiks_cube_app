import customtkinter
from color_palette import ColorPaletteFrame
from input_assistors import InputAssistiveFunctionsFrame
from visual_cube_representation import CubeRepresentationFrame
from algorithm_display import AlgorithmDisplayFrame

from other_functions import get_dictionary_details, settings


class View(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Coloring")
        self.add("Timing")
        self.add("Progress")

        # add widgets on tab Coloring
        self.input_assistors = InputAssistiveFunctionsFrame(master=self.tab("Coloring"),
                                                            corner_radius=0)
        self.input_assistors.grid(row=0, column=0, sticky='nswe', rowspan=3)

        self.color_palette = ColorPaletteFrame(master=self.tab("Coloring"))
        self.color_palette.grid(row=0, column=1, padx=20, pady=10)

        self.cube_representation = CubeRepresentationFrame(master=self.tab("Coloring"))
        self.cube_representation.grid(row=1, column=1, padx=20, pady=10)

        self.algorithm_display = AlgorithmDisplayFrame(master=self.tab("Coloring"))
        self.algorithm_display.grid(row=2, column=1, padx=20, pady=10)

    def get_selected_color_reference(self):
        selected_color = self.input_assistors.selected_color_label.cget("fg_color")
        selected_color_reference = get_dictionary_details(settings.color_details,
                                                          selected_color, "color_reference")

        return selected_color_reference

    def update_tile_colors(self, state):
        self.cube_representation.update_tile_colors(state)

    def update_palette_variables(self, dictionary_of_number_of_colors):
        self.color_palette.update_palette_variables(dictionary_of_number_of_colors)

    def update_checkbox_states(self, required_states):
        self.input_assistors.change_checkbox_states(required_states)

    def disable_tiles_for_selection_using_enable_list(self, enable_list):
        self.cube_representation.disable_tiles_not_in_list(enable_list)

    def enable_all_tiles(self):
        self.cube_representation.enable_or_disable_all_tiles("normal")

    def update_algorithm_display(self, algorithm):
        self.algorithm_display.change_algorithm(algorithm)