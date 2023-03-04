import customtkinter
from other_functions import get_dictionary_details, settings


button_color = get_dictionary_details(settings.color_details, "d", "light_color")


class AlgorithmDisplay:
    def __init__(self):
        self.label = None

    def create_label(self, frame):
        self.label = customtkinter.CTkLabel(
            master=frame,
            height=32,
            width=650,
            corner_radius=6,
            fg_color=button_color,
            text="")
        self.label.grid(row=0, column=2, padx=16, pady=16)

    def change_algorithm(self, algorithm):
        self.label.configure(text=algorithm)