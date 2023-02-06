class ColorPalette:
    """A class representing the color palette of the app."""
    def __init__(self):
        """Initialize attributes."""
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

    def create_color_palette(self, frame):
        """Creates and adds buttons to the color_palette_frame according to the
        amount of items in the parameter colors (In this case 6). This must be a
        list of dictionaries containing the main color and the hover color."""
        row = 0
        column = 0
        index = 0
        colors = self.order_colors(list("rbyogwd"))  # returns a ordered copy of the color details

        for color in colors:
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
                                             command=lambda button=self.palette_details[index]: self.palette_details(button))
            button.grid(row=row, column=column, pady=6, padx=6)
            # adds the button instance to the dictionary containing the buttons details
            self.palette_details[index]['button'] = button

            index += 1
            column += 1

    def order_colors(self, order):
        """Returns a ordered copy of the color details."""

        color_list = color_details[:]  # creates the copy

        for index in range(len(order)):
            # loops through color list until all the values in the list order, equal the coresponding color details
            for color in color_list:
                if order[index] == color['color_reference']:
                    order[index] = color  # turns the color reference to the color details
                    color_list.remove(color)  # removes that color
        return order

    def color_palette_button_event(self, button):
        """Stores the current selected button."""
        self.selected_color = button["color_reference"]

    def change_color_palette_variable(self, tile_color_reference, palette_color_reference):
        if tile_color_reference != "d" or palette_color_reference == "d":
            self.change_button_variable_by(tile_color_reference, 1)

        if palette_color_reference != "d":
            self.change_button_variable_by(palette_color_reference, -1)

    def change_button_variable_by(self, palette_color_reference, amount):
        color_palette_variable = get_dictionary_details(
            self.palette_details, palette_color_reference, "variable")

        new_variable_number = int(color_palette_variable.get()) + amount
        color_palette_variable.set(str(new_variable_number))
        if new_variable_number > 0:
            self.change_button_state(palette_color_reference, "normal")
        elif new_variable_number == 0:
            self.change_button_state(palette_color_reference, "disabled")

            default_color = get_dictionary_details(color_details,
                                                        "d",
                                                        "light_color")
            self.selected_color_label["color_reference"] = "d"
            self.selected_color_label["label"].configure(fg_color=default_color)

    def change_button_state(self, reference, state):
        color_dictionary = get_dictionary_details(color_details, reference)
        if state == "normal":
            color = color_dictionary["light_color"]
        elif state == "disabled":
            color = color_dictionary["dark_color"]

        palette_button = get_dictionary_details(
            color_palette_button_details, reference, "button")
        palette_button.configure(state=state, fg_color=color)