import customtkinter
import tkinter
from other_functions import get_dictionary_details
from settings import settings


class InputAssistiveFunctionsFrame(customtkinter.CTkFrame):
    selected_color_label = None

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_selected_color_label()
        self.create_option_menu()
        self.create_checkboxes()

    def create_selected_color_label(self):
        light_color = get_dictionary_details(settings.color_details, 'd',
                                             'light_color')
        label = customtkinter.CTkLabel(
            master=self,
            width=146,
            height=32,
            corner_radius=6,
            text="Selected Color",
            fg_color=light_color)
        label.grid(row=0, column=0, padx=16, pady=16)

        self.selected_color_label = label

    def update_selected_color(self, color):
        self.selected_color_label.configure(fg_color=color)

    def create_option_menu(self):
        self.menu_variable = customtkinter.StringVar(value="Start From")  # set initial value
        self.menu_instance = customtkinter.CTkOptionMenu(
            master=self,
            values=["White", "Yellow", "Green", "Blue", "Orange", "Red"],
            command=self.menu_callback,
            variable=self.menu_variable)
        self.menu_instance.grid(row=1, column=0, padx=16, pady=16)

    def menu_callback(self, start_color):
        """This function is called when the start color has been selected."""

        # enables the buttons if the start color hasn't been selected previously
        # if self.start_color is None:
        #     palette_references = get_dictionary_details(
        #         self.palette_details, return_value="color_reference")
        #     self.enable_or_disable_palette_buttons(palette_references, "normal")
        #     self.enable_or_disable_checkboxes("enable")
        #
        #     self.cube_coloring.change_centre_tile_colors()
        #     color_tiles(self.cube_tile_instances, self.cube_coloring.state)
        #
        #     self.update_palette_variables()
        #
        #     self.start_color = "w"
        print(start_color)

    def create_checkboxes(self):
        """Creates check boxes using a list of dictionaries that contains the
        check box details."""

        row = 2
        for index in range(
                len(self.checkbox_details)):  # the number of loops depend on the length of the list
            check_box = self.checkbox_details[index]

            check_box['variable'] = tkinter.IntVar()  # add an integer variable
            # add an check box instance
            check_box['check_box'] = customtkinter.CTkCheckBox(
                master=self,
                text=check_box['text'],
                state=tkinter.DISABLED,
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
        # self.cube_coloring.required_check_box_state_coloring(required_states[state], checkbox_names)
        # color_tiles(self.cube_tile_instances, self.cube_coloring.state)
        # self.update_palette_variables()

        self.change_checkbox_states(required_states[state])

    def enable_or_disable_checkboxes(self, enable_disable):
        """Sets the state of each toggle button to normal/chlickable."""
        for check_box in self.checkbox_details:
            if enable_disable == "enable":
                check_box['check_box'].configure(state=tkinter.NORMAL)
            elif enable_disable == "disable":
                check_box['check_box'].configure(state=tkinter.DISABLED)

    def enable_of_disable_start_color_menu(self, normal_disabled):
        self.menu_instance.configure(state=normal_disabled)

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