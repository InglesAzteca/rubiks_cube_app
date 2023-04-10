import customtkinter
from other_functions import settings, get_dictionary_details

from view import View
from controller import Controller
from model import Model

from algorithm_display_and_state_reset import StateManipulationAndAlgorithmDisplayFrame


class App(customtkinter.CTk):
    l_colors = get_dictionary_details(settings.color_details,
                                      return_value="light_color")
    d_colors = get_dictionary_details(settings.color_details,
                                      return_value="dark_color")

    def __init__(self):
        super().__init__()

        self.l1 = customtkinter.CTkLabel(master=self,
                                         text="",
                                         fg_color=self.l_colors[0],
                                         height=32,
                                         width=160,
                                         corner_radius=10)
        self.l1.grid(row=0, column=0, padx=10, pady=10)

        self.l2 = customtkinter.CTkLabel(master=self,
                                         text="",
                                         fg_color=self.l_colors[1],
                                         height=32,
                                         width=160,
                                         corner_radius=8)
        self.l2.grid(row=0, column=1, padx=10, pady=10)

        self.l3 = customtkinter.CTkLabel(master=self,
                                         text="",
                                         fg_color=self.l_colors[2],
                                         height=32,
                                         width=160,
                                         corner_radius=8)
        self.l3.grid(row=0, column=2, padx=10, pady=10)

        self.l4 = customtkinter.CTkLabel(master=self,
                                         text="",
                                         fg_color=self.l_colors[3],
                                         height=32,
                                         width=160,
                                         corner_radius=8)
        self.l4.grid(row=0, column=3, padx=10, pady=10)

        self.l5 = customtkinter.CTkLabel(master=self,
                                         text="",
                                         fg_color=self.l_colors[4],
                                         height=32,
                                         width=160,
                                         corner_radius=8)
        self.l5.grid(row=0, column=4, padx=10, pady=10)

        self.l6 = customtkinter.CTkLabel(master=self,
                                         text="",
                                         fg_color=self.l_colors[5],
                                         height=32,
                                         width=160,
                                         corner_radius=8)
        self.l6.grid(row=0, column=5, padx=10, pady=10)

        self.l7 = customtkinter.CTkLabel(master=self,
                                         text="",
                                         fg_color=self.l_colors[6],
                                         height=32,
                                         width=160,
                                         corner_radius=8)
        self.l7.grid(row=0, column=6, padx=10, pady=10)

        self.d1 = customtkinter.CTkLabel(master=self,
                                         text="",
                                         fg_color=self.d_colors[0],
                                         height=32,
                                         width=160,
                                         corner_radius=8)
        self.d1.grid(row=1, column=0, padx=10, pady=10)

        self.d2 = customtkinter.CTkLabel(master=self,
                                         text="",
                                         fg_color=self.d_colors[1],
                                         height=32,
                                         width=160,
                                         corner_radius=8)
        self.d2.grid(row=1, column=1, padx=10, pady=10)

        self.d3 = customtkinter.CTkLabel(master=self,
                                         text="",
                                         fg_color=self.d_colors[2],
                                         height=32,
                                         width=160,
                                         corner_radius=8)
        self.d3.grid(row=1, column=2, padx=10, pady=10)

        self.d4 = customtkinter.CTkLabel(master=self,
                                         text="",
                                         fg_color=self.d_colors[3],
                                         height=32,
                                         width=160,
                                         corner_radius=8)
        self.d4.grid(row=1, column=3, padx=10, pady=10)

        self.d5 = customtkinter.CTkLabel(master=self,
                                         text="",
                                         fg_color=self.d_colors[4],
                                         height=32,
                                         width=160,
                                         corner_radius=8)
        self.d5.grid(row=1, column=4, padx=10, pady=10)

        self.d6 = customtkinter.CTkLabel(master=self,
                                         text="",
                                         fg_color=self.d_colors[5],
                                         height=32,
                                         width=160,
                                         corner_radius=8)
        self.d6.grid(row=1, column=5, padx=10, pady=10)

        self.d7 = customtkinter.CTkLabel(master=self,
                                         text="",
                                         fg_color=self.d_colors[6],
                                         height=32,
                                         width=160,
                                         corner_radius=8)
        self.d7.grid(row=1, column=6, padx=10, pady=10)




app = App()
app.mainloop()
