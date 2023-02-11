import customtkinter


class AlgorithmDisplay:
    def __init__(self):
        self.label = None

    def create_label(self, frame):
        self.label = customtkinter.CTkLabel(
            master=frame,
            height=32,
            width=650,
            corner_radius=6,
            fg_color="red",
            text="")
        self.label.grid(row=0, column=2, padx=16, pady=16)

    def change_algorithm(self, algorithm):
        self.label.configure(text=algorithm)