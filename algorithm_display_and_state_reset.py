import customtkinter
from other_functions import get_dictionary_details, settings


class AlgorithmDisplayAndStateResetFrame(customtkinter.CTkFrame):
    """
    This class models the frame containing the main algorithm display, reset
    button and the save button in my application.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.algorithm_frame = customtkinter.CTkFrame(master=self)
        self.algorithm_frame.grid(row=1, column=0, columnspan=2, padx=16, pady=16, sticky="nsew")

        self.textbox_label = customtkinter.CTkLabel(master=self.algorithm_frame,
                                                    text="Algorithm Display",
                                                    font=customtkinter.CTkFont(
                                                        size=16, weight="bold"))
        self.textbox_label.grid(row=0, column=0, columnspan=2, pady=8)

        self.algorithm_text_box = customtkinter.CTkTextbox(master=self.algorithm_frame,
                                                           font=("font", 16),
                                                           width=400,
                                                           height=584)
        self.algorithm_text_box.grid(row=1, column=0, columnspan=2, padx=8, pady=8 ,sticky="nsew")

        self.reset_state_button = customtkinter.CTkButton(master=self,
                                                          text="Reset State",
                                                          width=146,
                                                          height=32)
        self.reset_state_button.grid(row=2, column=0, padx=10, pady=8)

        self.save_solve_button = customtkinter.CTkButton(master=self,
                                                         text="Save Solve",
                                                         state="disabled",
                                                         width=146,
                                                         height=32)
        self.save_solve_button.grid(row=2, column=1, padx=16)

    def enable_or_disable_reset_state_button(self, normal_disabled):
        if normal_disabled == "normal":
            light_or_dark = "light_color"
        elif normal_disabled == "disabled":
            light_or_dark = 'dark_color'

        fg_color = get_dictionary_details(settings.color_details, "d", light_or_dark)
        self.reset_state_button.configure(state=normal_disabled,
                                          fg_color=fg_color)

    def enable_or_disable_save_solve_button(self, normal_disabled):
        if normal_disabled == "normal":
            light_or_dark = "light_color"
        elif normal_disabled == "disabled":
            light_or_dark = 'dark_color'

        fg_color = get_dictionary_details(settings.color_details, "d", light_or_dark)
        self.save_solve_button.configure(state=normal_disabled,
                                         fg_color=fg_color)

    def clear_algorithm_display(self):
        self.algorithm_text_box.delete("0.0", "end")

    def add_algorithm_to_display(self, algorithm):
        text = self.algorithm_text_box.get("0.0", "end")
        self.algorithm_text_box.delete("0.0", "end")
        self.algorithm_text_box.insert("0.0", text + algorithm + "\n")

