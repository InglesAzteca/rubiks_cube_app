import tkinter
import customtkinter

from coloring import *
from solve_cube import SolveCube

from other_functions import *


class TabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Solving")
        self.add("Timing")
        self.add("Progress")

        # add widgets on tabs
        


class RubiksApp(customtkinter.CTk):
    WIDTH = settings.width
    HEIGHT = settings.height

    color_label_details = {'color_reference': 'd', 'label': None}

    palette_details = [
        {'name': 'red_button', 'color_reference': 'r', 'button': None,
         'variable': None},
        {'name': 'blue_button', 'color_reference': 'b', 'button': None,
         'variable': None},
        {'name': 'yellow_button', 'color_reference': 'y', 'button': None,
         'variable': None},
        {'name': 'orange_button', 'color_reference': 'o', 'button': None,
         'variable': None},
        {'name': 'green_button', 'color_reference': 'g', 'button': None,
         'variable': None},
        {'name': 'white_button', 'color_reference': 'w', 'button': None,
         'variable': None},
        {'name': 'remove_button', 'color_reference': 'd', 'button': None,
         'variable': None}
    ]
    selected_color = None

    menu_variable = None
    menu_instance = None
    start_color = None

    checkbox_details = [
        {'name': 'cross', 'check_box': None, 'text': 'Cross',
         'variable': None,
         'required_states': [[0, 0, 0], [1, 0, 0]]},
        {'name': 'f2l', 'check_box': None, 'text': 'F2L  ',
         'variable': None,
         'required_states': [[1, 0, 0], [1, 1, 0]]},
        {'name': 'oll', 'check_box': None, 'text': 'OLL  ',
         'variable': None,
         'required_states': [[1, 1, 0], [1, 1, 1]]}
    ]

    face_frames = {
        'white_face': None,
        'orange_face': None,
        'green_face': None,
        'red_face': None,
        'blue_face': None,
        'yellow_face': None
    }
    cube_tile_instances = create_cube_representation(None)
    cube_coloring = CubeColoring(get_cube_reference_from_tile_instances(cube_tile_instances))

    solve_button = None

    label = None

    solving = False

    coloring = True

    selection_needed = False

    solve_cube = None

    def __init__(self):
        super().__init__()

        self.title(settings.title)
        self.geometry(f"{RubiksApp.WIDTH}x{RubiksApp.HEIGHT}")

        # =========== create frames ===================

        self.left_frame = customtkinter.CTkFrame(master=self,
                                                 width=128,
                                                 corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky='nswe', rowspan=3)

        self.color_palette_frame = customtkinter.CTkFrame(master=self)
        self.color_palette_frame.grid(row=0,
                                      column=1,
                                      sticky='nswe',
                                      padx=16,
                                      pady=16)

        self.cube_frame = customtkinter.CTkFrame(master=self)
        self.cube_frame.grid(row=1, column=1, sticky='nswe', padx=16, pady=16)

        self.solve_frame = customtkinter.CTkFrame(master=self)
        self.solve_frame.grid(row=2, column=1, sticky='nswe', padx=16, pady=16)

        # ================ left frame ===================

        self.create_selected_color_label(self.left_frame)

        self.create_option_menu(self.left_frame)

        self.create_checkboxes(self.left_frame)

        # self.create_label_frame(self.left_frame)
        # self.create_selected_cross_label(selected_cross_piece_label.label_frame)
        #
        # self.create_label_frame(self.left_frame)
        # self.create_selected_f2l_label(selected_f2l_piece_label.label_frame)

        # =============== color palette frame ==============

        # add buttons for color palette argument = list of dictionaries
        self.create_buttons(self.color_palette_frame)

        # ============== cube frame ========================

        # add cube face frames
        self.create_face_frames(self.cube_frame)

        # add tiles/buttons to each face
        self.create_and_add_tiles()

        # ============ solve frame =============================

        self.create_solve_button(self.solve_frame)
        self.enable_or_disable_solve_button("disabled")
        self.create_algorithm_display_label(self.solve_frame)

    def create_selected_color_label(self, frame):
        light_color = get_dictionary_details(settings.color_details, 'd',
                                             'light_color')
        label = customtkinter.CTkLabel(
            master=frame,
            width=146,
            height=32,
            corner_radius=6,
            text="Selected Color",
            fg_color=light_color)
        label.grid(row=0, column=0, padx=16, pady=16)

        self.color_label_details["label"] = label

    def update_selected_color(self, color_reference):
        color = get_dictionary_details(settings.color_details, color_reference,
                                       "light_color")
        self.color_label_details["label"].configure(fg_color=color)

    def create_buttons(self, frame):
        """Creates and adds buttons to the color_palette_frame according to the
        amount of items in the parameter colors (In this case 6). This must be a
        list of dictionaries containing the main color and the hover color."""
        row = 0
        column = 0
        index = 0

        ordered_colors = order_colors(list("rbyogwd"))

        for color in ordered_colors:
            variable = tkinter.StringVar()  # create a string variable

            if color["color_name"] != "default":
                variable.set('9')  # set the variable to 9
            else:
                variable.set("Remove")
            # adds the variable to the dictionary containing the buttons details
            self.palette_details[index]['variable'] = variable

            button = customtkinter.CTkButton(master=frame,
                                             width=110,
                                             height=20,
                                             textvariable=variable,
                                             fg_color=color['dark_color'],
                                             hover_color=color['dark_color'],
                                             state="disabled",
                                             command=lambda
                                                 button=self.palette_details[
                                                     index]: self.palette_event(
                                                 button))
            button.grid(row=row, column=column, pady=6, padx=6)
            # adds the button instance to the dictionary containing the buttons details
            self.palette_details[index]['button'] = button

            index += 1
            column += 1

    def palette_event(self, button):
        """Stores the current selected button."""
        self.selected_color = button["color_reference"]
        self.update_selected_color(self.selected_color)

    def enable_or_disable_palette_buttons(self, button_references, normal_disabled):
        """Sets the state of each color palette button to normal/chlickable and
        sets the color to the main color."""
        # gets the button instances from the color palette button's details
        palette_buttons = [
            get_dictionary_details(self.palette_details, button_reference, 'button')
            for button_reference in button_references]
        for button in palette_buttons:
            color_reference = get_dictionary_details(self.palette_details,
                                                     button,
                                                     'color_reference')
            if normal_disabled == "normal":
                light_or_dark = "light_color"
            elif normal_disabled == "disabled":
                light_or_dark = 'dark_color'

            fg_color = get_dictionary_details(settings.color_details,
                                              color_reference,
                                              light_or_dark)
            button.configure(state=normal_disabled, fg_color=fg_color)

    def update_palette_variables(self):
        variables = get_dictionary_details(self.palette_details[:6], return_value="variable")
        palette_references = get_dictionary_details(self.palette_details[:6], return_value="color_reference")

        for index in range(len(variables)):
            palette_reference = palette_references[index]
            variable_number = 9 - self.cube_coloring.number_of_colors_on_cube[palette_reference]
            variables[index].set(str(variable_number))

            if variable_number > 0:
                self.enable_or_disable_palette_buttons(palette_reference, "normal")
            elif variable_number == 0:
                self.enable_or_disable_palette_buttons(palette_reference, "disabled")
                # if self.cube_coloring.number_of_colors_on_cube[self.selected_color] == 9:
                #     self.selected_color = "d"
                #     self.update_selected_color(self.selected_color)

    def create_option_menu(self, frame):
        self.menu_variable = customtkinter.StringVar(
            value="Start From")  # set initial value
        self.menu_instance = customtkinter.CTkOptionMenu(
            master=frame,
            values=["White", "Yellow", "Green", "Blue", "Orange", "Red"],
            command=self.menu_callback,
            variable=self.menu_variable)
        self.menu_instance.grid(row=1, column=0, padx=16, pady=16)

    def menu_callback(self, start_color):
        """This function is called when the start color has been selected."""

        # enables the buttons if the start color hasn't been selected previously
        if self.start_color is None:
            palette_references = get_dictionary_details(
                self.palette_details, return_value="color_reference")
            self.enable_or_disable_palette_buttons(palette_references,
                                                            "normal")
            self.enable_or_disable_checkboxes("enable")

            self.cube_coloring.change_centre_tile_colors()
            color_tiles(self.cube_tile_instances, self.cube_coloring.state)

            self.update_palette_variables()

            self.start_color = "w"

    def create_checkboxes(self, frame):
        """Creates check boxes using a list of dictionaries that contains the
        check box details."""

        row = 2
        for index in range(
                len(self.checkbox_details)):  # the number of loops depend on the length of the list
            check_box = self.checkbox_details[index]

            check_box['variable'] = tkinter.IntVar()  # add an integer variable
            # add an check box instance
            check_box['check_box'] = customtkinter.CTkCheckBox(
                master=frame,
                text=check_box['text'],
                state=tkinter.DISABLED,
                command=lambda variable=check_box['variable'],
                               required_states=check_box['required_states']:
                self.checkbox_event(variable, required_states),
                variable=check_box['variable'],
                onvalue=1,
                offvalue=0)
            check_box['check_box'].grid(row=row, column=0, padx=20, pady=10)
            row += 1

    def checkbox_event(self, variable, required_states):
        """Calls a coloring function and a function that changes the check box
        states, when any of the check boxes is clicked."""

        state = variable.get()

        checkbox_names = get_dictionary_details(self.checkbox_details,
                                                return_value="name")
        self.cube_coloring.required_check_box_state_coloring(required_states[state], checkbox_names)
        color_tiles(self.cube_tile_instances, self.cube_coloring.state)
        self.update_palette_variables()
        # changes the check box states to their required state
        self.change_checkbox_states(required_states[state])

    def enable_or_disable_checkboxes(self, enable_disable):
        """Sets the state of each toggle button to normal/chlickable."""
        for check_box in self.checkbox_details:
            if enable_disable == "enable":
                check_box['check_box'].configure(state=tkinter.NORMAL)
            elif enable_disable == "disable":
                check_box['check_box'].configure(state=tkinter.DISABLED)

    def change_checkbox_states(self, required_states):
        """Changes the state of the check boxes according to a list of required
        states and returns the required states list which is the current states
        after the for loop has ended."""

        # returns a list of the check boxes variables.
        check_box_variables = get_dictionary_details(
            self.checkbox_details, return_value='variable')
        # creates a list of binary values representing the current states
        current_states = [variable.get() for variable in check_box_variables]

        # returns the check box instances
        check_boxes = get_dictionary_details(self.checkbox_details,
                                             return_value='check_box')

        for index in range(len(current_states)):
            current, required = current_states[index], required_states[index]
            if current != required:
                # if the check box state is 0/off it is set to 1/on
                if current == 0:
                    check_boxes[index].select()
                # if the check box state is 1/on it is set to 0/off
                elif current == 1:
                    check_boxes[index].deselect()

    def create_face_frames(self, frame):
        """Creates the layout of the cube faces using frames."""

        cube_layout = [
            ['space', 'frame', 'space', 'space'],
            ['frame'] * 4,
            ['space', 'frame', 'space', 'space']
        ]
        face_keys = list(
            self.face_frames.keys())  # creates a list of the keys in cube_face_frames
        face_index = 0

        for row in range(3):
            for column in range(4):
                if cube_layout[row][column] == 'frame':
                    face = customtkinter.CTkFrame(master=frame)
                    face.grid(row=row, column=column)
                    # adds the frame instance to the dictionary using the cube_face_keys list and the face_index
                    self.face_frames[face_keys[face_index]] = face
                    face_index += 1

    def create_and_add_tiles(self):
        """Adds the tiles/buttons to each face frame."""
        size = 52
        face_index = 0

        default_color = get_dictionary_details(settings.color_details, 'd')
        # loops through the instances of the face frames
        for face in self.face_frames.values():
            for row in range(3):
                for column in range(3):
                    tile = customtkinter.CTkButton(
                        master=face,
                        text='',
                        fg_color=default_color["light_color"],
                        hover_color=default_color["dark_color"],
                        width=size,
                        height=size,
                        command=lambda face_index=face_index, row=row,
                                       column=column: self.button_event(
                            face_index, row, column))
                    tile.grid(row=row, column=column, padx=4, pady=4)
                    # Adds the button instance to the list representing the cube
                    self.cube_tile_instances[face_index][row][column] = tile

            face_index += 1

    def enable_or_disable_all_tiles(self, normal_disabled):
        for face in range(6):
            for row in range(3):
                for column in range(3):
                    self.enable_or_disable_tile(face, row, column, normal_disabled)

    def enable_or_disable_tile(self, face_index, row_index, column_index, normal_disabled):
        # gets the button instances from the color palette button's details
        button = self.cube_tile_instances[face_index][row_index][column_index]
        tile_color = button.cget("fg_color")

        if normal_disabled == "normal":
            light_or_dark = "light_color"
        elif normal_disabled == "disabled":
            light_or_dark = 'dark_color'

        fg_color = get_dictionary_details(settings.color_details,
                                          tile_color,
                                          light_or_dark)
        button.configure(state=normal_disabled, fg_color=fg_color)

    def button_event(self, face_index, row_index, column_index):
        """Colors an individual tiles according to the arguments passed in."""

        if self.coloring:
            self.cube_coloring.change_tile_color_reference(self.selected_color,
                                                           face_index,
                                                           row_index,
                                                           column_index)
            color_tiles(self.cube_tile_instances, self.cube_coloring.state)
            self.update_palette_variables()
            if self.cube_coloring.is_cube_colored():
                self.enable_or_disable_palette_buttons(get_dictionary_details(self.palette_details, return_value="color_reference"), "disabled")
                self.enable_or_disable_checkboxes("disable")
                self.coloring = False
                self.initiate_solving()
        else:
            if self.solve_cube.selection_needed:
                self.solve_cube.set_selected_tile(face_index, row_index, column_index)
                self.solve_cube.rotate_cube_due_to_selection()
                color_tiles(self.cube_tile_instances, self.solve_cube.state)
                self.disable_tiles_not_in_list()
                self.enable_or_disable_solve_button("normal")

    def create_solve_button(self, frame):
        default_color = get_dictionary_details(settings.color_details, 'd')

        self.solve_button = customtkinter.CTkButton(
            master=frame,
            width=146,
            height=32,
            text='Solve',
            fg_color=default_color["dark_color"],
            hover_color=default_color["dark_color"],
            state="disabled",
            command=self.solve_event)
        self.solve_button.grid(row=0, column=0, padx=16, pady=16)

    def solve_event(self):
        self.solve_cube.solve_section()

        color_tiles(self.cube_tile_instances, self.solve_cube.state)
        self.enable_or_disable_all_tiles("normal")
        print(self.solve_cube.current_section)
        if self.solve_cube.selection_needed:
            self.disable_tiles_not_in_list()
            self.enable_or_disable_solve_button("disabled")

    def enable_or_disable_solve_button(self, normal_disabled):
        if normal_disabled == "normal":
            light_or_dark = "light_color"
            # new_text = self.get_stage_text()
        elif normal_disabled == "disabled":
            light_or_dark = 'dark_color'
            new_text = "Solve"

        fg_color = get_dictionary_details(settings.color_details, "d",
                                          light_or_dark)
        self.solve_button.configure(state=normal_disabled, fg_color=fg_color,
                                    text="Solve")

    def create_algorithm_display_label(self, frame):
        self.label = customtkinter.CTkLabel(
            master=frame,
            height=32,
            width=650,
            corner_radius=6,
            fg_color='#2b9ced',
            text="")
        self.label.grid(row=0, column=2, padx=16, pady=16)

    def change_algorithm(self, algorithm):
        self.label.configure(text=algorithm)

    def initiate_solving(self):
        self.solving = True
        self.solve_cube = SolveCube(self.cube_coloring.state)

        self.solve_cube.update_current_section()

        if self.solve_cube.selection_needed:
            self.disable_tiles_not_in_list()

    def disable_tiles_not_in_list(self):
        self.enable_or_disable_all_tiles("disabled")
        enable_list = self.solve_cube.get_enable_list()

        for face, row, column in enable_list:
            self.enable_or_disable_tile(face, row, column, "normal")


if __name__ == "__main__":
    app = RubiksApp()
    app.mainloop()
