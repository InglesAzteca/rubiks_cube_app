import customtkinter

from other_functions import get_dictionary_details, settings


class SelectedColorLabel:
    def __init__(self):
        self.color_label_details = {'color_reference': 'd', 'label': None}

    def create_label(self, frame):
        light_color = get_dictionary_details(settings.color_details, 'd', 'light_color')
        label = customtkinter.CTkLabel(
            master=frame,
            width=146,
            height=32,
            corner_radius=6,
            text="Selected Color",
            fg_color=light_color)
        label.grid(row=0, column=0, padx=16, pady=16)

        self.color_label_details["label"] = label

    def update_color(self, color_reference):
        color = get_dictionary_details(settings.color_details, color_reference,
                                       "light_color")
        self.color_label_details["label"].configure(fg_color=color)