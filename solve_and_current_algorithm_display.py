import customtkinter
from other_functions import get_dictionary_details, settings


default_color = get_dictionary_details(settings.color_details, "d", "light_color")


class SolveAndCurrentAlgorithmDisplayFrame(customtkinter.CTkFrame):
    """
    This class models the frame containing the solve button and the label that
    displays the current algorithm.
    """
    algorithm_display_label = None

    solve_button = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_solve_button()
        self.create_algorithm_display_label()

    def create_solve_button(self):
        """Creates and adds the button instance to the frame."""

        default_color = get_dictionary_details(settings.color_details, 'd')

        self.solve_button = customtkinter.CTkButton(
            master=self,
            width=146,
            height=32,
            text='Solve',
            fg_color=default_color["dark_color"],
            hover_color=default_color["dark_color"],
            state="disabled")

        self.solve_button.grid(row=0, column=0, padx=16, pady=16)

    def enable_or_disable_solve_button(self, normal_disabled, stage_text):
        """
        This method is used to enable or disable the solve button and update the
        text on it.
        """
        if normal_disabled == "normal":
            light_or_dark = "light_color"
        elif normal_disabled == "disabled":
            light_or_dark = 'dark_color'

        fg_color = get_dictionary_details(settings.color_details, "d",
                                          light_or_dark)
        self.solve_button.configure(state=normal_disabled, fg_color=fg_color,
                                    text=stage_text)

    def create_algorithm_display_label(self):
        """
        Creates an instance of the label that displays the current algorithm and
        adds it to the frame."""
        self.algorithm_display_label = customtkinter.CTkLabel(
            master=self,
            height=32,
            width=580,
            corner_radius=6,
            fg_color=default_color,
            text="")
        self.algorithm_display_label.grid(row=0, column=2, padx=16, pady=16)

    def change_algorithm(self, algorithm):
        """This method is used to change the algorithm on the label."""
        self.algorithm_display_label.configure(text=algorithm)
