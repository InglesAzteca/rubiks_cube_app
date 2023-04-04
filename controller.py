from other_functions import get_dictionary_details

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # =============== binding coloring section from view ===================
        # bind the controller to the palette buttons
        self.bind_palette_buttons_to_controller()
        # bind tiles
        self.bind_cube_representation_to_controller()

        self.bind_start_color_menu()

        self.bind_checkboxes()

        self.bind_solve_button()

    def bind_palette_buttons_to_controller(self):
        palette_buttons = get_dictionary_details(
            self.view.color_palette.palette_details, return_value="button")
        for button in palette_buttons:
            button.configure(
                command=lambda button=button: self.set_selected_color(button))

    def bind_cube_representation_to_controller(self):
        tile_instances = self.view.cube_representation.cube_tile_instances

        for face_index in range(6):
            for row_index in range(3):
                for column_index in range(3):
                    tile = tile_instances[face_index][row_index][column_index]
                    tile.configure(command=lambda face=face_index, row=row_index, column=column_index: self.tile_event(face, row, column))

    def bind_start_color_menu(self):
        self.view.input_assistors.menu_instance.configure(command=self.menu_event)

    def bind_checkboxes(self):
        checkbox_details = self.view.input_assistors.checkbox_details

        for checkbox_index in range(len(checkbox_details)):
            checkbox = checkbox_details[checkbox_index]["check_box"]
            variable = checkbox_details[checkbox_index]["variable"]
            required_states = checkbox_details[checkbox_index]["required_states"]
            checkbox.configure(command=lambda variable=variable,
                               required_states=required_states: self.checkbox_event(variable, required_states))

    def bind_solve_button(self):
        self.view.algorithm_display.solve_button.configure(command=self.solve_button_event)

    def get_palette_color(self, button):
        return button.cget("fg_color")

    def set_selected_color(self, button):
        selected_color = self.get_palette_color(button)
        self.view.input_assistors.update_selected_color(selected_color)

    def get_palette_details(self):
        return self.view.color_palette.palette_details

    def call_enable_color_palette(self):
        palette_details = self.get_palette_details()
        palette_references = get_dictionary_details(palette_details,
                                                    return_value="color_reference")

        self.view.color_palette.enable_or_disable_palette_buttons(
            palette_references, "normal")

    def call_disable_color_palette(self):
        palette_details = self.get_palette_details()
        palette_references = get_dictionary_details(palette_details,
                                                    return_value="color_reference")

        self.view.color_palette.enable_or_disable_palette_buttons(
            palette_references, "disabled")

    def get_checkbox_details(self):
        return self.view.input_assistors.checkbox_details

    def call_enable_checkboxes(self):
        self.view.input_assistors.enable_or_disable_checkboxes("enable")

    def call_disable_checkboxes(self):
        self.view.input_assistors.enable_or_disable_checkboxes("disable")

    def call_enable_solve_button(self):
        self.view.algorithm_display.enable_or_disable_solve_button("normal", "Solve")

    def call_disable_solve_button(self):
        self.view.algorithm_display.enable_or_disable_solve_button("disabled", "Solve")

    def call_enable_start_color_menu(self):
        self.view.input_assistors.enable_of_disable_start_color_menu("noraml")

    def call_disable_start_color_menu(self):
        self.view.input_assistors.enable_of_disable_start_color_menu("disabled")

    def call_color_centre_tiles(self):
        self.model.coloring_cube.color_centre_tiles()

    def call_change_tile_reference(self, face, row, column):
        color = self.view.get_selected_color_reference()
        self.model.change_tile_reference(color, face, row, column)

    def call_update_colors_from_coloring(self):
        state = self.get_state_from_coloring()
        self.view.update_tile_colors(state)

    def get_state_from_coloring(self):
        return self.model.coloring_cube.state

    def call_update_palette_variables(self):
        self.view.update_palette_variables(self.model.get_number_of_colors_on_cube())

    def handle_checkbox_event(self, required_state):
        checkbox_details = self.get_checkbox_details()
        checkbox_names = get_dictionary_details(checkbox_details,
                                                return_value="name")

        self.model.change_section_references_as_required(required_state,
                                                         checkbox_names)
        cube_state = self.get_state_from_coloring()
        self.view.update_tile_colors(cube_state)
        # changes the check box states to their required state
        self.view.update_checkbox_states(required_state)

        self.call_update_palette_variables()

    def menu_event(self, start_color):
        self.call_enable_color_palette()
        self.call_enable_checkboxes()

        self.call_color_centre_tiles()
        self.call_update_colors_from_coloring()
        self.call_update_palette_variables()

        self.call_disable_start_color_menu()

    def tile_event(self, face_index, row_index, column_index):
        if not self.model.get_if_solving():
            self.call_change_tile_reference(face_index, row_index, column_index)
            self.call_update_colors_from_coloring()
            self.call_update_palette_variables()

            if self.model.is_cube_colored():
                self.call_disable_color_palette()
                self.call_disable_checkboxes()

                self.model.create_solving_cube()
                if self.model.is_selection_needed():
                    enable_list = self.model.get_enable_list()
                    self.view.disable_tiles_for_selection_using_enable_list(enable_list)
                else:
                    self.call_enable_solve_button()
        else:
            if self.model.is_selection_needed():
                self.model.set_selected_tile(face_index, row_index, column_index)

                self.model.rotate_cube_due_to_selection()

                state = self.model.get_solving_state()
                self.view.update_tile_colors(state)

                enable_list = self.model.get_enable_list()
                self.view.disable_tiles_for_selection_using_enable_list(enable_list)

                self.call_enable_solve_button()

    def checkbox_event(self, variable, required_states):
        state = variable.get()
        required_state = required_states[state]
        self.handle_checkbox_event(required_state)

    def solve_button_event(self):
        algorithm = self.model.solve_section()
        algorithm = self.model.format_suggested_algorithm_for_display(algorithm)
        self.view.update_algorithm_display(algorithm)

        state = self.model.get_solving_state()
        self.view.update_tile_colors(state)

        self.view.enable_all_tiles()
        if self.model.is_selection_needed():
            enable_list = self.model.get_enable_list()
            self.view.disable_tiles_for_selection_using_enable_list(enable_list)

            self.call_disable_solve_button()
