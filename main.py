import tkinter
import customtkinter

from selected_color_label import SelectedColorLabel
from algorithm_display import AlgorithmDisplay
from cube_rotations import CubeRotations
from selected_pieces import SelectedCrossPieceColor, SelectedF2LPieceColors

from other_functions import *


class ColorPalette:
    def __init__(self):
        self.ordered_colors = order_colors(list("rbyogwd"))
        self.palette_details = [
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
        self.selected_color = None

    def create_buttons(self, frame):
        """Creates and adds buttons to the color_palette_frame according to the
        amount of items in the parameter colors (In this case 6). This must be a
        list of dictionaries containing the main color and the hover color."""
        row = 0
        column = 0
        index = 0

        for color in self.ordered_colors:
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
                                             command=lambda button=self.palette_details[
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
        selected_color_label.update_color(self.selected_color)

    def enable_or_disable_palette_buttons(self, button_references, normal_disabled):
        """Sets the state of each color palette button to normal/chlickable and
        sets the color to the main color."""
        # gets the button instances from the color palette button's details
        palette_buttons = [get_dictionary_details(self.palette_details, button_reference, 'button') for button_reference in button_references]
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

    def change_variable_by(self, button_references, amount):
        variables = [get_dictionary_details(self.palette_details, button_reference, "variable") for button_reference in button_references]
        for index in range(len(button_references)):
            reference = button_references[index]

            variable = variables[index]
            new_variable = int(variable.get()) + amount
            variable.set(str(new_variable))

            if new_variable > 0:
                self.enable_or_disable_palette_buttons(reference, "normal")
            elif new_variable == 0:
                self.enable_or_disable_palette_buttons(reference, "disabled")
                self.selected_color = "d"

                selected_color_label.update_color(self.selected_color)


class CheckBoxes:
    def __init__(self):
        self.checkbox_details = [
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

    def create_checkboxes(self, frame):
        """Creates check boxes using a list of dictionaries that contains the
        check box details."""

        row = 2
        for index in range(len(self.checkbox_details)):  # the number of loops depend on the length of the list
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
        # returns 0 or 1 (represents the state: 0 = off, 1 = on)
        state = variable.get()

        # colors sections on the cube using a list of states
        cube_coloring.required_check_box_state_coloring(required_states[state])

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


class StartColorOptionMenu:
    def __init__(self):
        super().__init__()
        self.menu_variable = None
        self.menu_instance = None
        self.start_color = None

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
            palette_references = get_dictionary_details(color_palette.palette_details, return_value="color_reference")
            color_palette.enable_or_disable_palette_buttons(palette_references, "normal")
            checkboxes.enable_or_disable_checkboxes("enable")

        self.start_color = start_color.lower()
        # uses the start color to color the centre tiles in specific order.
        cube_coloring.color_centre_tiles(self.start_color)

        # returns a list of all the check box's variables
        check_box_variables = get_dictionary_details(
            checkboxes.checkbox_details, return_value='variable')
        # creates a list of the states (0/1) of the check boxes
        current_states = [variable.get() for variable in
                          check_box_variables]

        # uses the current states to color sections of the cube
        cube_coloring.required_check_box_state_coloring(current_states)


class CubeColoring:
    def __init__(self):
        self.coloring = True
        self.selection_needed = False
        self.face_frames = {
            'white_face': None,
            'orange_face': None,
            'green_face': None,
            'red_face': None,
            'blue_face': None,
            'yellow_face': None
        }
        self.cube_buttons = create_cube_representation(None)
        self.cube_reference = create_cube_representation("d")

        self.edge_indices = {'top': None, 'middle': None, 'bottom': None}
        self.corner_indices = {'top': None, 'bottom': None}
        add_empty_lists_to_indices_dictionary(self.edge_indices,
                                              self.corner_indices)
        self.create_edge_indices()
        self.create_corner_indices()

        self.pll_indices = self.create_pll_indices()
        self.oll_indices = self.create_oll_indices()
        self.f2l_indices = self.create_f2l_indices()
        self.cross_indices = self.create_cross_indices()

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
                    self.cube_buttons[face_index][row][column] = tile

            face_index += 1

    def enable_or_disable_all_tiles(self, normal_disabled):
        for face in range(6):
            for row in range(3):
                for column in range(3):
                    self.enable_or_disable_tile(face, row, column, normal_disabled)

    def enable_or_disable_tile(self, face_index, row_index, column_index, normal_disabled):
        # gets the button instances from the color palette button's details
        button = self.cube_buttons[face_index][row_index][column_index]
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
            cube_reference_copy = create_cube_copy(self.cube_reference)
            is_centre_tile = (row_index == 1) and (column_index == 1)

            # ensures a color has been selected and that it is not the centre tile.
            if not is_centre_tile:
                cube_reference_copy[face_index][row_index][
                    column_index] = color_palette.selected_color

                will_affect = self.will_tile_coloring_affect_checkboxes(cube_reference_copy)
                if will_affect != "Not affected":
                    checkboxes.change_checkbox_states(will_affect)

                self.color_tiles(cube_reference_copy)
        else:
            if self.selection_needed:
                solve_cube.set_selected_piece(face_index, row_index, column_index)


    def color_tiles(self, copy_of_cube_reference):
        """Uses a modified copy of the cube coloring reference list, colors the
        tiles and then updates the coloring reference to the values in the copy
        which is the current state."""

        for face in range(6):
            for row in range(3):
                for column in range(3):
                    current_color = self.cube_reference[face][row][column]
                    new_color = copy_of_cube_reference[face][row][column]
                    # colors a tile only if the value has been modified
                    if current_color != new_color:

                        if current_color != "d" or new_color == "d":
                            color_palette.change_variable_by(current_color, 1)
                        if new_color != "d":
                            color_palette.change_variable_by(new_color, -1)

                        color = get_dictionary_details(settings.color_details, new_color)

                        light_color = color['light_color']
                        dark_color = color['dark_color']

                        # updates the color
                        self.cube_buttons[face][row][column].configure(
                            fg_color=light_color,
                            hover_color=dark_color)

        self.cube_reference = copy_of_cube_reference  # updates the coloring reference

        if self.is_cube_colored(self.cube_reference):
            self.coloring = False
            self.selection_needed = solve_cube.disable_tiles_if_required()
            if not self.selection_needed:
                solve.enable_or_disable_solve_button("normal")
        else:
            self.coloring = True
            solve.enable_or_disable_solve_button("disabled")

    def color_section(self, section, cube_reference_copy, add_remove):
        section_dictionary = {"cross": self.cross_indices,
                              "f2l": self.f2l_indices,
                              "oll": [oll_index for
                                      oll_index in self.oll_indices if
                                      oll_index not in self.pll_indices]}

        for face, row, column in section_dictionary[section]:
            if add_remove == "remove":
                color = "d"
            elif add_remove == "add":
                color = cube_reference_copy[face][1][1]

            is_centre_tile = row == 1 and column == 1

            if not is_centre_tile:
                cube_reference_copy[face][row][column] = color

        self.color_tiles(cube_reference_copy)

        self.remove_color_due_to_negative_variable(section_dictionary[section])

    def color_centre_tiles(self, start_color):
        """Colors the centre tile of each face relative to the rotation details.
        """
        cube_reference_copy = create_cube_copy(self.cube_reference)

        default_color_order = list('wogrby')  # sets a default order of colors
        for face_index in range(6):
            color_reference = default_color_order[face_index]
            cube_reference_copy[face_index][1][1] = color_reference

        # contains rotation details for each color if they were the start color
        rotation_details = {'yellow': ('x', 1, 0),
                            'white': ('x', 1, 2),
                            'green': ('x', -1, 1),
                            'blue': ('x', 1, 1),
                            'orange': ('z', -1, 1),
                            'red': ('z', 1, 1)
                            }

        for key in rotation_details.keys():
            if key == start_color:
                color_order = cube_rotations.simulate_cube_rotation_with_list_of_centres(default_color_order, *rotation_details[key])
                break

        for face_index in range(6):
            # adds the color reference to the centre of each face
            cube_reference_copy[face_index][1][1] = color_order[face_index]

        # passes in the coloring reference copy then colors the tiles
        self.color_tiles(cube_reference_copy)

    def get_centre_tile_colors(self, cube_reference):
        """Returns a list of all the centre tile color reference."""
        return [face[1][1] for face in cube_reference]

    def remove_color_due_to_negative_variable(self, section_indices):
        color_references = get_dictionary_details(
            color_palette.palette_details[:6], return_value="color_reference")
        cube_reference_copy = create_cube_copy(self.cube_reference)

        for palette_color in color_references:
            variable_value = int(get_dictionary_details(
                color_palette.palette_details[:6], palette_color,
                "variable").get())
            flag = variable_value < 0
            if flag:
                for face in range(6):
                    for row in range(3):
                        for column in range(3):
                            color = cube_reference_copy[face][row][column]
                            is_in_indices = [face, row,
                                             column] in section_indices
                            if color == palette_color and not is_in_indices:
                                cube_reference_copy[face][row][column] = "d"
                                variable_value += 1
                                flag = variable_value < 0
                            if not flag:
                                break
                        if not flag:
                            break
                    if not flag:
                        break

        self.color_tiles(cube_reference_copy)

    def will_tile_coloring_affect_checkboxes(self, cube_reference_copy):
        are_colored_before = [self.is_cross_solved(self.cube_reference), self.is_f2l_solved(self.cube_reference),
                              self.is_oll_solved(self.cube_reference)]
        are_colored_after = [self.is_cross_solved(cube_reference_copy), self.is_f2l_solved(cube_reference_copy),
                             self.is_oll_solved(cube_reference_copy)]
        if are_colored_before == are_colored_after:
            return "Not affected"
        else:
            for index in range(3):
                section_names = get_dictionary_details(
                    checkboxes.checkbox_details,
                    return_value="name")
                section_name = section_names[index]

                required_states = get_dictionary_details(
                    checkboxes.checkbox_details, section_name,
                    "required_states")

                is_colored_after = are_colored_after[index]

                if not is_colored_after:
                    return required_states[0]

            return required_states[1]

    def required_check_box_state_coloring(self, required_states):
        check_box_names = get_dictionary_details(checkboxes.checkbox_details,
                                                 return_value="name")
        are_colored = [self.is_cross_solved(self.cube_reference),
                       self.is_f2l_solved(self.cube_reference),
                       self.is_oll_solved(self.cube_reference)]

        for index in range(3):
            cube_reference_copy = create_cube_copy(self.cube_reference)
            if required_states[index] == 0 and are_colored[index]:
                add_remove = "remove"
                self.color_section(check_box_names[index],
                                   cube_reference_copy, add_remove)
            elif required_states[index] == 1:
                add_remove = "add"
                self.color_section(check_box_names[index],
                                   cube_reference_copy, add_remove)

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
        #       1 1 0           4 1 2
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
            self.edge_indices['top'][index].append(
                [index + 1, 0, 1])  # creates sequence 1
            self.edge_indices['top'][index].append(
                [0, 5 % (index + 2), 5 % (index + 1)])  # creates sequence 2

            self.edge_indices['middle'][index].append(
                [(index - 1) % (index + 1) + 1, 1,
                 2 % (index + 2)])  # creates sequence 3
            self.edge_indices['middle'][index].append([4 - ((3 - index) % 3), 1,
                                                       abs(2 % (
                                                                   index + 2) - 2)])  # creates sequence 4

            self.edge_indices['bottom'][index].append(
                [index + 1, 2, 1])  # creates sequence 5
            self.edge_indices['bottom'][index].append(
                [5, abs(index - 1), 5 % (index + 1)])  # creates sequence 6

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
            self.corner_indices['top'][index].append([0, 2 % (index + 1), 2 * (
                        index ** 2) % 3])  # creates sequence 1
            self.corner_indices['top'][index].append(
                [(5 - index) % (4 + index), 0, 0])  # creates sequence 2
            self.corner_indices['top'][index].append(
                [4 - index, 0, 2])  # creates sequence 3

            self.corner_indices['bottom'][index].append([5, 2 % (index + 1),
                                                         2 * (
                                                                     index ** 2) % 3])  # creates sequence 4
            self.corner_indices['bottom'][index].append(
                [index + 1, 2, 2])  # creates sequence 5
            self.corner_indices['bottom'][index].append(
                [(index + 2) % (7 - index), 2, 0])  # creates sequence 6

    def create_cross_indices(self):
        centre_tile = [5, 1, 1]
        cross_indices = [index for edge in self.edge_indices["bottom"] for index
                         in edge]
        cross_indices.append(centre_tile)

        return cross_indices

    def create_f2l_indices(self):
        centre_tiles = [[face, 1, 1] for face in range(1, 5)]
        bottom_corner = [index for corner in self.corner_indices["bottom"] for
                         index in corner]
        middle_edge = [index for edge in self.edge_indices["middle"] for index
                       in edge]

        indices = [bottom_corner, middle_edge, centre_tiles]
        f2l_indices = [cord for section in indices for cord in section]

        return f2l_indices

    def create_oll_indices(self):
        face = 0
        top_face_indices = [[face, row, column] for row in range(3) for column in
                       range(3)]
        oll_indices = top_face_indices + self.pll_indices
        return oll_indices

    def create_pll_indices(self):
        row = 0
        pll_indices = [[face, row, column] for face in range(1, 5) for column in range(3)]

        return pll_indices

    def is_cross_solved(self, cube_reference):
        for indices in self.cross_indices:
            face, row, column = indices
            centre_color = cube_reference[face][1][1]
            if cube_reference[face][row][column] != centre_color:
                return False
        return True

    def is_f2l_solved(self, cube_reference):
        for indices in self.f2l_indices:
            face, row, column = indices
            centre_color = cube_reference[face][1][1]
            if cube_reference[face][row][column] != centre_color:
                return False
        return True

    def is_oll_solved(self, cube_reference):
        for row in cube_reference[0]:
            output = len(set(row)) == 1
            if not output:
                return output
        return output

    def is_pll_solved(self, cube_reference):
        for face in cube_reference:
            for row in face:
                output = len(set(row)) == 1
                if not output:
                    return output
        return output

    def is_cube_colored(self, cube_reference):
        """Depending if the coloring reference list contains the value d
        (which represents the default color), true (if d is not in the list) or
        false (if d is in the list) is returned."""

        for face in cube_reference:
            for row in face:
                if 'd' in row:
                    return False
        return True


class SolveButton:
    def __init__(self):
        self.solve_button = None

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
        solve_cube.solve_section()

    def enable_or_disable_solve_button(self, normal_disabled):
        if normal_disabled == "normal":
            light_or_dark = "light_color"
            new_text = self.get_stage_text()
        elif normal_disabled == "disabled":
            light_or_dark = 'dark_color'
            new_text = "Solve"

        fg_color = get_dictionary_details(settings.color_details,  "d", light_or_dark)
        self.solve_button.configure(state=normal_disabled, fg_color=fg_color, text=new_text)

    def get_stage_text(self):
        stage_names = ["Cross", "F2L", "OLL", "PLL"]
        variables = get_dictionary_details(checkboxes.checkbox_details, return_value="variable")
        states = [variable.get() for variable in variables]

        for index in range(3):
            if states[2 - index] == 1:
                text = "Solve " + stage_names[(2 - index) + 1].upper()
                return text
        return f"Solve {stage_names[0]}"


class DetermineAlgorithm:
    def __init__(self):
        pass

    def determine_cross_piece_details_from_state(self, state, from_file):
        indices = cube_coloring.edge_indices["bottom"] + cube_coloring.edge_indices["middle"] + cube_coloring.edge_indices["top"]

        edge_details = {"selected": [], "location": 0, "cross_color": state[5][1][1], "colors": []}
        if from_file:
            edge_details["selected"] = ["b", "w"]
        else:
            edge_details["selected"] = solve_cube.selected_cross_piece

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

    def compare_to_cross_algorithm_state(self, cube_reference, algorithm_state):
        algorithm_state_cross_piece_details = self.determine_cross_piece_details_from_state(
            algorithm_state, True)

        cube_reference_cross_piece_details = self.determine_cross_piece_details_from_state(
            cube_reference, False)

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

    def search_through_cross_algorithms(self, cube_reference):
        cross_file_list = get_file_list_from_folder("algorithms\\cross")

        for index in range(len(cross_file_list)):
            algorithm_state, algorithm = read_state_from_text_file(
                cross_file_list[index])
            if self.compare_to_cross_algorithm_state(cube_reference,
                                                     algorithm_state):
                return algorithm

        return "No algorithms found."

    def determine_f2l_pair_details_from_state(self, state, from_file):
        f2l_pair_details = [
            {"name": "corner", "selected": [], "location": 0,
             "colors": []},
            {"name": "edge", "selected": [], "location": 0,
             "colors": []}]
        if from_file:
            f2l_pair_details[0]["selected"] = ["w", "b", "r"]
            f2l_pair_details[0]["selected"] = ["b", "r"]
        else:
            f2l_pair_details[0]["selected"] = [cube_coloring.cube_reference[5][1][1]] + solve_cube.selected_f2l_pair
            f2l_pair_details[0]["selected"] = solve_cube.selected_f2l_pair

        corner_indices = cube_coloring.corner_indices["top"] + [[[5, 0, 2], [2, 2, 2], [3, 2, 0]]]
        edge_indices = cube_coloring.edge_indices["top"] + [[[2, 1, 2], [3, 1, 0]]]
        indices = [corner_indices, edge_indices]

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
        return f2l_pair_details

    def compare_to_f2l_algorithm_state(self, cube_reference, algorithm_state):
        algorithm_state_f2l_details = self.determine_f2l_pair_details_from_state(algorithm_state, True)
        
        cube_reference = cube_rotations.rotate_cube_to_required_location(cube_reference, solve_cube.selected_f2l_pair[0])

        for u_turn in range(3):
            cube_reference_f2l_details = self.determine_f2l_pair_details_from_state(cube_reference, False)
            if cube_reference_f2l_details == algorithm_state_f2l_details:
                return True
            else:
                cube_rotations.set_cube_state(cube_reference)
                cube_rotations.rotate_face("U")
                cube_reference = cube_rotations.cube_state
        return False

    def search_through_f2l_algorithms(self, cube_reference):
        f2l_file_list = get_file_list_from_folder("algorithms\\f2l")

        for index in range(len(f2l_file_list)):
            algorithm_state, algorithm = read_state_from_text_file(
                f2l_file_list[index])
            if self.compare_to_f2l_algorithm_state(cube_reference,
                                                   algorithm_state):
                return algorithm

        return "No algorithms found."

    def calculate_oll_color_order(self, state):
        oll_color_list = [state[face][row][column] for
                          face, row, column in cube_coloring.oll_indices]

        color_order = [y for y in range(len(oll_color_list)) if oll_color_list[y] == "y"]

        return color_order

    def compare_to_oll_algorithm_state(self, cube_reference, algorithm_state):
        algorithm_color_order = self.calculate_oll_color_order(algorithm_state)

        for u_turn in range(3):
            color_order = self.calculate_oll_color_order(cube_reference)

            if color_order == algorithm_color_order:
                return True
            else:
                cube_rotations.set_cube_state(cube_reference)
                cube_rotations.rotate_face("U")
                cube_reference = cube_rotations.cube_state
        return False

    def search_through_oll_algorithms(self, cube_reference):
        oll_file_list = get_file_list_from_folder("algorithms\\oll")

        for index in range(len(oll_file_list)):
            algorithm_state, algorithm = read_state_from_text_file(oll_file_list[index])
            if self.compare_to_oll_algorithm_state(cube_reference,
                                                   algorithm_state):
                return algorithm

        return "No algorithms found."

    def calculate_pll_color_order(self, state):
        pll_color_list = [state[face][row][column] for
                          face, row, column in cube_coloring.pll_indices]

        r = [r for r in range(len(pll_color_list)) if pll_color_list[r] == "r"]
        g = [g for g in range(len(pll_color_list)) if pll_color_list[g] == "g"]
        o = [o for o in range(len(pll_color_list)) if pll_color_list[o] == "o"]
        b = [b for b in range(len(pll_color_list)) if pll_color_list[b] == "b"]

        color_order = [r, g, o, b]

        return color_order

    def compare_to_pll_algorithm_state(self, cube_reference, algorithm_state):
        # needs to be modified to give cube rotations and u turns
        # also to work with different start colors
        # try implement with other algorithms

        algorithm_color_order = self.calculate_pll_color_order(algorithm_state)

        for u_turn in range(3):
            color_order = self.calculate_pll_color_order(cube_reference)

            if color_order == algorithm_color_order:
                return True
            else:
                for index in range(1, 4):
                    if color_order[index] == algorithm_color_order[0]:
                        for shift in range(index):
                            color_order.append(color_order.pop(0))

                        if color_order == algorithm_color_order:
                            return True

                cube_rotations.set_cube_state(cube_reference)
                cube_rotations.rotate_face("U")
                cube_reference = cube_rotations.cube_state
        return False

    def search_through_pll_algorithms(self, cube_reference):
        pll_file_list = get_file_list_from_folder("algorithms\\pll")

        for index in range(len(pll_file_list)):
            algorithm_state, algorithm = read_state_from_text_file(pll_file_list[index])
            if self.compare_to_pll_algorithm_state(cube_reference, algorithm_state):
                return algorithm

        return "No algorithms found."


class SolveCube:
    def __init__(self):
        self.selected_tile_index = []
        self.selected_f2l_pair = []
        self.selected_cross_piece = []
        self.next_stage = "cross"
        # self.cross_disable_list = self.create_cross_disable_list()
        # self.f2l_disable_list = self.create_f2l_disable_list()

    def update_next_stage(self):
        are_solved = [
            cube_coloring.is_cross_solved(cube_coloring.cube_reference),
            cube_coloring.is_f2l_solved(cube_coloring.cube_reference),
            cube_coloring.is_oll_solved(cube_coloring.cube_reference),
            cube_coloring.is_pll_solved(cube_coloring.cube_reference)
        ]
        stage_names = ["cross", "f2l", "oll", "pll", "solved"]
        for index in range(4):
            is_solved = are_solved[index]
            if not is_solved:
                self.next_stage = stage_names[index]
                break
        self.next_stage = stage_names[-1]

    def create_cross_disable_list(self):
        disable_list = cube_coloring.cross_indices
        disable_list.remove([5, 1, 1])
        return disable_list

    def create_f2l_disable_list(self):
        disable_list = cube_coloring.f2l_indices
        centre_index_reference = [[face, 1, 1] for face in range(1, 5)]
        for index_reference in  centre_index_reference:
            disable_list.remove(index_reference)
        return disable_list

    def disable_tiles_that_are_not_in_cross_or_solved(self):
        cube_coloring.enable_or_disable_all_tiles("normal")
        cross_disable_list = []
        for index_1, index_2 in cube_coloring.edge_indices["bottom"]:
            face_1, row_1, column_1 = index_1
            face_2, row_2, column_2 = index_2

            face_1_color = cube_coloring.cube_reference[face_1][1][1]
            face_2_color = cube_coloring.cube_reference[face_2][1][1]

            tile_color_1 = cube_coloring.cube_reference[face_1][row_1][column_1]
            tile_color_2 = cube_coloring.cube_reference[face_2][row_2][column_2]

            if [tile_color_1, tile_color_2] != [face_1_color, face_2_color]:
                cross_disable_list.append(index_1)
                cross_disable_list.append(index_2)

        self.disable_tiles_not_in_list(cross_disable_list)

    def disable_tiles_that_are_not_in_f2l_or_solved(self):
        cube_coloring.enable_or_disable_all_tiles("normal")
        f2l_disable_list = []

        for index in range(4):
            edge_tile_1, edge_tile_2 = cube_coloring.edge_indices["middle"][index]
            corner_tile_1, corner_tile_2, corner_tile_3 = cube_coloring.corner_indices["bottom"][index]

            f2l_tiles = [edge_tile_1, edge_tile_2, corner_tile_1, corner_tile_2, corner_tile_3]

            for face, row, column in f2l_tiles:
                if cube_coloring.cube_reference[face][row][column] != cube_coloring.cube_reference[face][1][1]:
                    f2l_disable_list += f2l_tiles
                    break

        self.disable_tiles_not_in_list(f2l_disable_list)

    def disable_tiles_if_required(self):
        self.update_next_stage()
        if self.next_stage == "cross":
            self.disable_tiles_that_are_not_in_cross_or_solved()
            return True
        elif self.next_stage == "f2l":
            self.disable_tiles_that_are_not_in_f2l_or_solved()
            return True
        else:
            return False

    def disable_tiles_not_in_list(self, list_of_indices):
        remove_button = get_dictionary_details(color_palette.palette_details,
                                               "remove_button", "button")
        color_palette.enable_or_disable_palette_buttons([remove_button],
                                                        "disabled")

        for face in range(6):
            for row in range(3):
                for column in range(3):
                    if [face, row, column] not in list_of_indices:
                        cube_coloring.enable_or_disable_tile(face, row, column,
                                                             "disabled")

    def set_selected_piece(self, face, row, column):
        self.selected_tile_index = [face, row, column]
        if self.next_stage == "cross":
            self.set_selected_cross_piece()
        elif self.next_stage == "f2l":
            self.set_selected_f2l_piece()

    def set_selected_cross_piece(self):
        self.selected_cross_piece = []
        for edge in cube_coloring.edge_indices["bottom"]:
            if self.selected_tile_index in edge:
                tile_1, tile_2 = edge
                face_1, row_1, column_1 = tile_1
                face_2, row_2, column_2 = tile_2
                color_1 = cube_coloring.cube_reference[face_1][1][1]
                color_2 = cube_coloring.cube_reference[face_2][1][1]

                self.selected_cross_piece.append(color_1)
                self.selected_cross_piece.append(color_2)

        rotated_cube = cube_rotations.rotate_cube_to_required_location(
            cube_coloring.cube_reference, color_1)
        cube_coloring.color_tiles(rotated_cube)

        solve.enable_or_disable_solve_button("normal")

    def set_selected_f2l_piece(self):
        self.selected_f2l_pair = []
        for index in range(4):
            f2l_edges = cube_coloring.edge_indices["middle"]
            f2l_corners = cube_coloring.corner_indices["bottom"][:]
            f2l_corners.insert(0, f2l_corners.pop())

            if self.selected_tile_index in f2l_edges[index] or self.selected_tile_index in f2l_corners[index]:
                tile_1, tile_2 = f2l_edges[index]

                color_1 = cube_coloring.cube_reference[tile_1[0]][1][1]
                color_2 = cube_coloring.cube_reference[tile_2[0]][1][1]

                self.selected_f2l_pair.append(color_1)
                self.selected_f2l_pair.append(color_2)

        # face, row, column = self.selected_tile_index
        # f2l_color_1 = cube_coloring.cube_reference[face][1][1]
        #
        # if column == 2:
        #     f2l_color_2 = cube_coloring.cube_reference[(face + 1) % 5][1][1]
        #     self.selected_f2l_pair.append(f2l_color_1)
        #     self.selected_f2l_pair.append(f2l_color_2)
        # elif column == 0:
        #     new_face = face - 1
        #     if new_face == 0:
        #         new_face = 4
        #     f2l_color_2 = cube_coloring.cube_reference[new_face][1][1]
        #     self.selected_f2l_pair.append(f2l_color_2)
        #     self.selected_f2l_pair.append(f2l_color_1)

        rotated_cube = cube_rotations.rotate_cube_to_required_location(
            cube_coloring.cube_reference, self.selected_f2l_pair[0])
        cube_coloring.color_tiles(rotated_cube)

        solve.enable_or_disable_solve_button("normal")

    def solve_section(self):
        stage = self.next_stage
        if stage == "cross":
            algorithm = determine_algorithm.search_through_cross_algorithms(cube_coloring.cube_reference)
        elif stage == "f2l":
            algorithm = determine_algorithm.search_through_f2l_algorithms(cube_coloring.cube_reference)
        elif stage == "oll":
            algorithm = determine_algorithm.search_through_pll_algorithms(cube_coloring.cube_reference)
        elif stage == "pll":
            algorithm = determine_algorithm.search_through_pll_algorithms(cube_coloring.cube_reference)
        else:
            algorithm = "Solved"

        algorithm_display.change_algorithm(algorithm)

        if algorithm != "No algorithms found." and algorithm != "Solved":
            cube_rotations.set_cube_state(cube_coloring.cube_reference)
            cube_rotations.perform_algorithm(algorithm)

            cube_coloring.color_tiles(cube_rotations.cube_state)

            self.disable_tiles_if_required()




color_palette = ColorPalette()
selected_color_label = SelectedColorLabel()
checkboxes = CheckBoxes()
start_color_menu = StartColorOptionMenu()
cube_coloring = CubeColoring()
solve = SolveButton()
algorithm_display = AlgorithmDisplay()
determine_algorithm = DetermineAlgorithm()
cube_rotations = CubeRotations(cube_coloring.cube_reference,
                               cube_coloring.edge_indices,
                               cube_coloring.corner_indices)
selected_cross_piece_label = SelectedCrossPieceColor()
selected_f2l_piece_label = SelectedF2LPieceColors()
solve_cube = SolveCube()


class RubiksApp(customtkinter.CTk):
    WIDTH = settings.width
    HEIGHT = settings.height

    def __init__(self):
        super().__init__()

        self.title(settings.title)
        self.geometry(f"{RubiksApp.WIDTH}x{RubiksApp.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

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

        selected_color_label.create_label(self.left_frame)

        start_color_menu.create_option_menu(self.left_frame)

        checkboxes.create_checkboxes(self.left_frame)

        selected_cross_piece_label.create_label_frame(self.left_frame)
        selected_cross_piece_label.create_selected_cross_label(selected_cross_piece_label.label_frame)

        selected_f2l_piece_label.create_label_frame(self.left_frame)
        selected_f2l_piece_label.create_selected_f2l_label(selected_f2l_piece_label.label_frame)

        # =============== color palette frame ==============

        # add buttons for color palette argument = list of dictionaries
        color_palette.create_buttons(self.color_palette_frame)

        # ============== cube frame ========================

        # add cube face frames
        cube_coloring.create_face_frames(self.cube_frame)

        # add tiles/buttons to each face
        cube_coloring.create_and_add_tiles()

        # ============ solve frame =============================

        solve.create_solve_button(self.solve_frame)
        solve.enable_or_disable_solve_button("disabled")
        algorithm_display.create_label(self.solve_frame)

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = RubiksApp()
    app.mainloop()
