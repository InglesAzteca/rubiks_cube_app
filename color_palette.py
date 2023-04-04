import tkinter
import customtkinter
from other_functions import order_colors, get_dictionary_details
from settings import settings


class ColorPaletteFrame(customtkinter.CTkFrame):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_palette()

    def create_palette(self):
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

            button = customtkinter.CTkButton(master=self,
                                             width=100,
                                             height=25,
                                             textvariable=variable,
                                             fg_color=color['dark_color'],
                                             hover_color=color['dark_color'],
                                             state="disabled")
            button.grid(row=row, column=column, pady=6, padx=6)
            # adds the button instance to the dictionary containing the buttons details
            self.palette_details[index]['button'] = button

            index += 1
            column += 1

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

    def update_palette_variables(self, number_of_colors_on_cube):
        variables = get_dictionary_details(self.palette_details[:6], return_value="variable")
        palette_references = get_dictionary_details(self.palette_details[:6], return_value="color_reference")

        for index in range(len(variables)):
            palette_reference = palette_references[index]
            variable_number = 9 - number_of_colors_on_cube[palette_reference]
            variables[index].set(str(variable_number))

            if variable_number > 0:
                self.enable_or_disable_palette_buttons(palette_reference, "normal")
            elif variable_number == 0:
                self.enable_or_disable_palette_buttons(palette_reference, "disabled")

