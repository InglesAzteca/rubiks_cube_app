import random

import customtkinter
from other_functions import settings, get_dictionary_details, create_solved_cube, display_cube
from cube import CubeDetails

from view import View
from controller import Controller
from model import Model
from solving import SolveCube



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





solved_cube_state = [
    [['y', 'y', 'y'], ['y', 'y', 'y'], ['y', 'y', 'y']],
    [['r', 'r', 'r'], ['r', 'r', 'r'], ['r', 'r', 'r']],
    [['g', 'g', 'g'], ['g', 'g', 'g'], ['g', 'g', 'g']],
    [['o', 'o', 'o'], ['o', 'o', 'o'], ['o', 'o', 'o']],
    [['b', 'b', 'b'], ['b', 'b', 'b'], ['b', 'b', 'b']],
    [['w', 'w', 'w'], ['w', 'w', 'w'], ['w', 'w', 'w']]
    ]

def random_alg():
    moves = "ULFRBD"
    var = ["", "'", "2"]
    random_algorithm = ""

    for m in range(25):
        random_algorithm += moves[random.randint(0, len(moves)) - 1] + var[random.randint(0, 2)] + " "

    return random_algorithm

def random_selection(solve):
    if solve.is_selection_needed():
        en_list = solve.get_enable_list()
        solve.selected_tile = en_list[random.randint(0, len(en_list) - 1)]


def solve_testing():
    solved = 0
    unsolved = 0
    for s in range(1000):
        solve = SolveCube(create_solved_cube())
        solve.perform_algorithm([random_alg()])
        # display_cube(solve.state)

        while not solve.is_cube_solved():
            try:
                random_selection(solve)
                solve.rotate_cube_due_to_selection()
                solve.solve_section()
            except:
                unsolved += 1
                break
        # display_cube(solve.state)
        if solve.is_cube_solved():
            solved += 1
    print(f"Solved: {solved}")
    print(f"Unsolved: {unsolved}")

solve_testing()
