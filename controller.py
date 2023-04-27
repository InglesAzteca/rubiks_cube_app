from other_functions import get_dictionary_details


class Controller:
    """
    A class that represents the brain of my application, interacts with the view
    and model. This is the 'Controller' part of my MVC model.
    """

    def __init__(self, model, view):
        """Initialize the attributes of the controller."""

        # instances of the model and view
        self.model = model
        self.view = view

        # =============== binding coloring section from view ===================
        self.bind_palette_buttons_to_controller()

        self.bind_cube_representation_to_controller()

        self.bind_start_color_menu()

        self.bind_checkboxes()

        self.bind_solve_button()

        self.bind_reset_state_button()

    def bind_palette_buttons_to_controller(self):
        """
        Gets the palette button instances and binds them to the method in the
        controller (set_selected_color).
        """
        # gets palette instances
        palette_buttons = get_dictionary_details(
            self.view.color_palette.palette_details, return_value="button")

        for button in palette_buttons:
            # uses lambda to pass the button instance as an argument
            button.configure(
                command=lambda button=button: self.set_selected_color(button))

    def bind_cube_representation_to_controller(self):
        """
        Gets all the instances of the cube tiles and binds them to the method in
        the controller (tile_event).
        """
        # 3D list of tile instances
        tile_instances = self.view.cube_representation.cube_tile_instances

        for face_index in range(6):
            for row_index in range(3):
                for column_index in range(3):
                    # uses indices to reference a tile instance
                    tile = tile_instances[face_index][row_index][column_index]
                    # uses lambda to pass the indices as arguments
                    tile.configure(command=lambda
                                   face=face_index,
                                   row=row_index,
                                   column=column_index:
                                   self.tile_event(face, row, column))

    def bind_start_color_menu(self):
        """
        Binds the menu instance to the method in the controller (menu_event).
        """
        self.view.input_assistors.menu_instance.configure(
            command=self.menu_event)

    def bind_checkboxes(self):
        """
        Binds the checkboxes to the method in the controller (checkbox_event).
        """
        # list of dictionaries containing checkbox details
        checkbox_details = self.view.input_assistors.checkbox_details

        for checkbox_index in range(len(checkbox_details)):
            checkbox = checkbox_details[checkbox_index]["check_box"]
            variable = checkbox_details[checkbox_index]["variable"]
            required_states = checkbox_details[checkbox_index][
                "required_states"]

            # uses lambda to pass the variable and required states as arguments
            checkbox.configure(command=lambda variable=variable,
                                              required_states=required_states: self.checkbox_event(
                variable, required_states))

    def bind_solve_button(self):
        """Bind the solve button instance to the controller method
        (solve_button_event)."""
        self.view.solve_and_current_algorithm_display.solve_button.configure(
            command=self.solve_button_event)

    def bind_reset_state_button(self):
        """Binds the reset state button to the controller."""
        button = self.view.algorithm_display_and_state_reset.reset_state_button
        button.configure(command=self.reset_state_event)

    def get_palette_color(self, button):
        """Returns the hex color value from the button instance passed in."""
        return button.cget("fg_color")

    def set_selected_color(self, button):
        """Using the a button instance this method gets the buttons hex color
        value and updates the color on the selected color label."""
        selected_color = self.get_palette_color(button)
        self.view.input_assistors.update_selected_color(selected_color)

    def get_palette_details(self):
        """Returns a list of dictionaries containing details to of the color
        palette buttons."""
        return self.view.color_palette.palette_details

    def call_enable_color_palette(self):
        """This methods gets the palette details and respective references and
        uses the references to enable the color palette buttons."""
        palette_details = self.get_palette_details()
        palette_references = get_dictionary_details(palette_details,
                                                    return_value="color_reference")

        self.view.color_palette.enable_or_disable_palette_buttons(
            palette_references, "normal")

    def call_disable_color_palette(self):
        """This methods gets the palette details and respective references and
        uses the references to disable the color palette buttons."""
        palette_details = self.get_palette_details()
        palette_references = get_dictionary_details(palette_details,
                                                    return_value="color_reference")

        self.view.color_palette.enable_or_disable_palette_buttons(
            palette_references, "disabled")

    def get_checkbox_details(self):
        """
        Returns a list of dictionaries containing details of each checkbox.
        """
        return self.view.input_assistors.checkbox_details

    def call_enable_checkboxes(self):
        """This methods enables all checkboxes."""
        self.view.input_assistors.enable_or_disable_checkboxes("enable")

    def call_disable_checkboxes(self):
        """This methods disables all checkboxes."""
        self.view.input_assistors.enable_or_disable_checkboxes("disable")

    def call_enable_solve_button(self):
        """This method enables the solve button."""
        self.view.solve_and_current_algorithm_display.enable_or_disable_solve_button("normal", "Solve")

    def call_disable_solve_button(self):
        """This method disables the solve button."""
        self.view.solve_and_current_algorithm_display.enable_or_disable_solve_button("disabled",
                                                                   "Solve")

    def call_enable_start_color_menu(self):
        """This method enables the start color option menu."""
        self.view.input_assistors.enable_of_disable_start_color_menu("noraml")

    def call_disable_start_color_menu(self):
        """This method disables the start color option menu."""
        self.view.input_assistors.enable_of_disable_start_color_menu("disabled")

    def call_color_centre_tiles(self):
        """Colors the centre tiles of the cube for coloring"""
        self.model.coloring_cube.color_centre_tiles()

    def call_change_tile_reference(self, face, row, column):
        """This changes the color reference of a specific tile on the coloring
        cube using the tile indices."""
        color = self.view.get_selected_color_reference()
        self.model.change_tile_reference(color, face, row, column)

    def call_update_colors_from_coloring(self):
        """This method updates the colors on the cube representation by getting
        the state from the cube for coloring."""
        state = self.model.get_coloring_state()
        self.view.update_tile_colors(state)

    def call_update_palette_variables(self):
        """Updates the numbers on the palette using the number of colors on the
        coloring cube."""
        self.view.update_palette_variables(
            self.model.get_number_of_colors_on_cube())

    def handle_checkbox_event(self, required_state):
        """
        This methods uses a list of requires states to change the color
        references on th coloring cube. It then updates the cube visualization,
        the states of the checkboxes and the variables on the palette buttons.
        """
        checkbox_details = self.get_checkbox_details()
        # uses get_dictionary_details to get a list of check box names
        checkbox_names = get_dictionary_details(checkbox_details,
                                                return_value="name")

        self.model.change_section_references_as_required(required_state,
                                                         checkbox_names)

        cube_state = self.model.get_coloring_state()
        self.view.update_tile_colors(cube_state)

        self.view.update_checkbox_states(required_state)

        self.call_update_palette_variables()

    def menu_event(self, start_color):
        """
        This method is called when the start color option menu is selected.
        It enables the color palette and checkboxes and colors the centre tiles.
        It then disables the option menu.
        (start_color is not used because the current system only solves from
        white.)
        """
        self.call_enable_color_palette()
        self.call_enable_checkboxes()

        self.call_color_centre_tiles()
        self.call_update_colors_from_coloring()
        self.call_update_palette_variables()

        self.call_disable_start_color_menu()

    def tile_event(self, face_index, row_index, column_index):
        """
        This method is called when a tile on the cube representation in pressed.
        It called other method to color the coloring cube until it is fully
        colored. It then disables the color palette and checkboxes.
        If a selection is needed it will then set the selected color when
        called.

        :param face_index: int value between 0-5 that represent the face
        :param row_index: int value between 0-2 that represent the row
        :param column_index: int value between 0-2 that represent the column

        These parameters are used to reference a specific location on the cube.
        """
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
                    self.view.disable_tiles_for_selection_using_enable_list(
                        enable_list)
                else:
                    self.call_enable_solve_button()
        else:
            if self.model.is_selection_needed():
                self.model.set_selected_tile(face_index, row_index,
                                             column_index)

                self.model.rotate_cube_due_to_selection()

                state = self.model.get_solving_state()
                self.view.update_tile_colors(state)

                enable_list = self.model.get_enable_list()
                self.view.disable_tiles_for_selection_using_enable_list(
                    enable_list)

                self.call_enable_solve_button()

    def checkbox_event(self, variable, required_states):
        """
        This method is called when a checkbox is called. It calls the
        handle_checkbox_event which deal with the coloring and state updates.

        :param variable: is the variable of the checkbox pressed
        :param required_states: is a 2D list containing required states for all
        checkboxes.
        """
        # gets a binary value from the variable
        state = variable.get()
        # uses the state to get a specific set of required states
        required_state = required_states[state]
        self.handle_checkbox_event(required_state)

    def solve_button_event(self):
        """
        This method is called when the solve button is pressed. It gets, formats
        and displays an algorithm for a specific section.
        It also updates the colors on the cube visualization after the section
        has been solved and disables tiles if a further selection is needed.
        """
        try:
            current_section = self.model.solving_cube.current_section
            algorithm = self.model.solve_section()
            algorithm = self.model.format_suggested_algorithm_for_display(algorithm)
            self.view.update_algorithm_display(f"{current_section.upper()}: {algorithm}")

            state = self.model.get_solving_state()
            self.view.update_tile_colors(state)

            self.view.enable_all_tiles()
            if self.model.is_selection_needed():
                enable_list = self.model.get_enable_list()
                self.view.disable_tiles_for_selection_using_enable_list(enable_list)

                self.call_disable_solve_button()

            if self.model.solving_cube.is_cube_solved():
                self.call_disable_solve_button()
        except:
            self.reset_state_event()
            self.view.solve_and_current_algorithm_display.change_algorithm("Invalid State.")
            self.call_disable_solve_button()

    def reset_state_event(self):
        """This method is called when the reset button is pressed."""
        self.model.reset_coloring()
        self.model.solving = False

        state = self.model.get_coloring_state()
        self.view.update_tile_colors(state)
        self.view.update_palette_variables(
            self.model.get_number_of_colors_on_cube())

        self.view.clear_algorithm_displays()

        self.call_enable_start_color_menu()
