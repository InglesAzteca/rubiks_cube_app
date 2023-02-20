# import tkinter
# import customtkinter
#
# customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
# customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
#
# app = customtkinter.CTk()
# app.geometry("400x780")
# app.title("CustomTkinter simple_example.py")
#
# frame_1 = customtkinter.CTkFrame(master=app)
# frame_1.pack(pady=20, padx=60, fill="both", expand=True)
#
# label = customtkinter.CTkLabel(master=frame_1, text='boobs', width=110, height=20, fg_color='red')
# label.place(relx = 1, x =-4, y = 7, anchor = tkinter.NE)
#
# # b1 = customtkinter.CTkLabel(frame_1, text = "Click me !")
# # b1.place(relx = 1, x =-2, y = 2, anchor = tkinter.NE)
#
# app.mainloop()

import other_functions

# from main import CubeColoring
#
# c = CubeColoring()
# print(c.f2l_indices)
from cube_rotations import CubeRotations
from other_functions import *

# edge = cube_coloring.edge_indices
# corner = cube_coloring.corner_indices
#
# cube = read_state_from_text_file("algorithms/solved")[0]
#
# cr = CubeRotations(cube, edge, corner)
# display_cube(cr.cube_state)
# cr.rotate_face("d", -1, 3)
# # cr.rotate_tiles_on_face(1, -1, 1)
# display_cube(cr.cube_state)
#
# l = get_file_list_from_folder("algorithms\\pll")
# print(l)
# with open(l[0], "r") as f:
#     print(f.readlines())

# change_bottom_two_rows_on_cube(get_file_list_from_folder("algorithms\\pll"), cube_coloring.pll_indices)
# pll_indices = cube_coloring.pll_indices
# state, algorithms = read_state_from_text_file("algorithms/pll/Aa.txt")
# solved_state, solved_algorithm = read_state_from_text_file("algorithms/solved")
# print(pll_indices)
# for face in range(6):
#     for row in range(3):
#         for column in range(3):
#             if [face, row, column] not in pll_indices:
#                 state[face][row][column] = solved_state[face][row][column]
# display_cube(state)
# write_state_to_text_file(state, "algorithms/pll/Aa.txt", algorithms)
# from main import DetermineAlgorithm, CubeColoring
# from other_functions import display_cube, read_state_from_text_file
# c = CubeColoring()
# d = DetermineAlgorithm()
# cube_reference, alg = read_state_from_text_file("algorithms/solved")
#
# display_cube(cube_reference)
# display_cube(d.rotate_f2l_to_required_location(cube_reference))
# vowels list

# from main import CubeColoring
#
# c = CubeColoring()
# print(c.edge_indices["middle"])
# c.corner_indices["bottom"].insert(0, c.corner_indices["bottom"].pop())
# print(c.corner_indices["bottom"])
#
# print(c.edge_indices["bottom"])

l = [1]
if not l:
    print("x")






