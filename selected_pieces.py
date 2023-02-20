import customtkinter
from other_functions import get_dictionary_details, settings


class SelectedCrossPieceColor:
    def __init__(self):
        self.label_frame = None
        self.text_label = None
        self.color_1_label = None

    def create_label_frame(self, frame):
        self.label_frame = customtkinter.CTkFrame(master=frame,
                                                  corner_radius=6)
        self.label_frame.grid(row=5, column=0, padx=16, pady=16)

    def create_selected_cross_label(self, frame):
        default_color = get_dictionary_details(settings.color_details,
                                               "default", "light_color")
        self.text_label = customtkinter.CTkLabel(master=frame,
                                                 height=32,
                                                 width=102,
                                                 text="Selected Cross")
        self.text_label.grid(row=0, column=0, padx=6)

        self.color_1_label = customtkinter.CTkLabel(master=frame,
                                                    text="",
                                                    width=20,
                                                    height=20,
                                                    fg_color=default_color,
                                                    corner_radius=3)
        self.color_1_label.grid(row=0, column=1, padx=6)

    def change_selected_cross_color(self, color):
        self.color_1_label.configure(fg_color=color)


class SelectedF2LPieceColors:
    def __init__(self):
        self.label_frame = None
        self.text_label = None
        self.color_1_label = None
        self.color_2_label = None

    def create_label_frame(self, frame):
        self.label_frame = customtkinter.CTkFrame(master=frame,
                                                  corner_radius=6)
        self.label_frame.grid(row=6, column=0)

    def create_selected_f2l_label(self, frame):
        default_color = get_dictionary_details(settings.color_details,
                                               "default", "light_color")
        self.text_label = customtkinter.CTkLabel(master=frame,
                                                 height=32,
                                                 width=82,
                                                 text="Selected F2L")
        self.text_label.grid(row=0, column=0, padx=6)

        self.color_1_label = customtkinter.CTkLabel(master=frame,
                                                    text="",
                                                    width=20,
                                                    height=20,
                                                    fg_color=default_color,
                                                    corner_radius=3)
        self.color_1_label.grid(row=0, column=1)

        self.color_2_label = customtkinter.CTkLabel(master=frame,
                                                    text="",
                                                    width=20,
                                                    height=20,
                                                    fg_color=default_color,
                                                    corner_radius=3)
        self.color_2_label.grid(row=0, column=2, padx=6)

    def change_selected_f2l_colors(self, color_1, color_2):
        self.color_1_label.configure(fg_color=color_1)
        self.color_2_label.configure(fg_color=color_2)
