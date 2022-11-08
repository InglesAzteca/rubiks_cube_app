import tkinter
import customtkinter

customtkinter.set_appearance_mode(
    "Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue")  # Themes: "blue" (standard), "green", "dark-blue"


class RubiksApp(customtkinter.CTk):
    WIDTH = 1120
    HEIGHT = 720

    color_details = [
        {'color_name': 'red', 'color_reference': 'r', 'main_color': 'red',
         'hover_color': '#b00502'},
        {'color_name': 'blue', 'color_reference': 'b', 'main_color': 'blue',
         'hover_color': '#19158a'},
        {'color_name': 'yellow', 'color_reference': 'y', 'main_color': 'yellow',
         'hover_color': '#91991f'},
        {'color_name': 'orange', 'color_reference': 'o', 'main_color': 'orange',
         'hover_color': '#a16312'},
        {'color_name': 'green', 'color_reference': 'g', 'main_color': 'green',
         'hover_color': '#0e5207'},
        {'color_name': 'white', 'color_reference': 'w', 'main_color': 'white',
         'hover_color': '#afb8ae'},
        {'color_name': 'default', 'color_reference': 'd',
         'main_color': '#1f6aa5', 'hover_color': '#1f6aa5'}
    ]
    color_palette_buttons = {
        'red_button': None,
        'blue_button': None,
        'yellow_button': None,
        'orange_button': None,
        'green_button': None,
        'white_button': None
    }
    selected_color = None

    cube_face_frames = {'white_face': None,
                        'orange_face': None,
                        'green_face': None,
                        'red_face': None,
                        'blue_face': None,
                        'yellow_face': None}

    cube = None

    cube_coloring_reference = None

    start_color = None

    def __init__(self):
        super().__init__()

        self.title("Rubik's App")
        self.geometry(f"{RubiksApp.WIDTH}x{RubiksApp.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # =========== create frames ===================

        # configure grid layout (2x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.coloring_toggles_frame = customtkinter.CTkFrame(master=self,
                                                             width=180,
                                                             corner_radius=0)
        self.coloring_toggles_frame.grid(row=0, column=0, sticky='nswe',
                                         rowspan=2)

        self.color_palette_frame = customtkinter.CTkFrame(master=self)
        self.color_palette_frame.grid(row=0, column=1, sticky='nswe', padx=20,
                                      pady=20)

        self.cube_frame = customtkinter.CTkFrame(master=self)
        self.cube_frame.grid(row=1, column=1, sticky='nswe', padx=20, pady=20)

        # ================ coloring toggles frame ===================

        # configure grid layout (1x6)
        self.coloring_toggles_frame.grid_columnconfigure(0, weight=1)
        self.coloring_toggles_frame.grid_rowconfigure(5, weight=1)

        self.start_color_menu = customtkinter.CTkOptionMenu(
            master=self.coloring_toggles_frame,
            values=["White",
                    "Yellow",
                    "Green",
                    "Blue",
                    "Orange",
                    "Red"],
            command=self.start_color_menu_callback)
        self.start_color_menu.grid(row=0, column=0, padx=20, pady=10)
        self.start_color_menu.set("Start From")  # set initial value

        self.cross_check_var = tkinter.IntVar()
        self.cross_checkbox = customtkinter.CTkCheckBox(
            master=self.coloring_toggles_frame,
            text="Cross",
            command=self.cross_checkbox_event,
            variable=self.cross_check_var,
            onvalue=1,
            offvalue=0)
        self.cross_checkbox.grid(row=1, column=0, padx=20, pady=10)

        self.f2l_check_var = tkinter.IntVar()
        self.f2l_checkbox = customtkinter.CTkCheckBox(
            master=self.coloring_toggles_frame,
            text="F2L  ",
            command=self.f2l_checkbox_event,
            variable=self.f2l_check_var,
            onvalue=1,
            offvalue=0)
        self.f2l_checkbox.grid(row=2, column=0, padx=20, pady=10)

        self.oll_check_var = tkinter.IntVar()
        self.oll_checkbox = customtkinter.CTkCheckBox(
            master=self.coloring_toggles_frame,
            text="OLL  ",
            command=self.oll_checkbox_event,
            variable=self.oll_check_var,
            onvalue=1,
            offvalue=0)
        self.oll_checkbox.grid(row=3, column=0, padx=20, pady=10)

        # =============== color palette frame ==============

        # configure grid layout (6x1)
        self.color_palette_frame.grid_columnconfigure(5, weight=1)
        self.color_palette_frame.grid_rowconfigure(0, weight=1)

        # add buttons for color palette argument = list of dictionaries
        self.create_color_palette()

        # ============== cube frame ========================

        # configure grid layout (4x3)
        self.color_palette_frame.grid_columnconfigure(3, weight=1)
        self.color_palette_frame.grid_rowconfigure(2, weight=1)

        # add cube face frames
        self.create_cube_face_frames()

        # add tiles to each face
        self.cube = self.create_cube_representation(
            None)  # creates an empty cube with default value None
        self.add_tiles_to_faces()

        self.cube_coloring_reference = self.create_cube_representation(
            'd')  # creates an empty cube with default value d

    def create_cube_representation(self, default_value):
        faces, rows, columns = (6, 3, 3)
        return [[[default_value for column in range(columns)] for row in
                 range(rows)] for face in range(faces)]

    def create_color_palette(self):
        '''Creates and adds buttons to the color_palette_frame according to the
        amount of items in the parameter colors (In this case 6). This must be a list of
        dictionaries containg the main color and the hover color.'''
        row = 0
        column = 0
        button_keys = list(
            self.color_palette_buttons.keys())  # creates a list of the keys in color_palette_buttons
        colors = self.order_colors(list("rbyogw"))

        for color in colors:
            button = customtkinter.CTkButton(master=self.color_palette_frame,
                                             text='',
                                             fg_color=color['main_color'],
                                             hover_color=color['hover_color'],
                                             command=lambda
                                                 color=color: self.get_color(
                                                 color))
            button.grid(row=row, column=column, pady=5, padx=5)
            # adds the button instance to the dictionary using the button_keys list and the column as the index
            self.color_palette_buttons[button_keys[column]] = button

            column += 1

    def create_cube_face_frames(self):
        '''Creates the layout of the cube faces using frames.'''
        cube_layout = [
            ['space', 'frame', 'space', 'space'],
            ['frame'] * 4,
            ['space', 'frame', 'space', 'space']
        ]
        cube_face_keys = list(
            self.cube_face_frames.keys())  # creates a list of the keys in cube_face_frames
        face_index = 0

        for row in range(3):
            for column in range(4):
                if cube_layout[row][column] == 'frame':
                    face = customtkinter.CTkFrame(master=self.cube_frame)
                    face.grid(row=row, column=column)
                    # adds the frame instance to the dictionary using the cube_face_keys list and the face_index
                    self.cube_face_frames[cube_face_keys[face_index]] = face
                    face_index += 1

    def add_tiles_to_faces(self):
        size = 60
        face_index = 0

        for face in self.cube_face_frames.values():
            for row in range(3):
                for column in range(3):
                    tile = customtkinter.CTkButton(master=face,
                                                   text='',
                                                   width=size,
                                                   height=size,
                                                   command=lambda
                                                       face_index=face_index,
                                                       row=row,
                                                       column=column: self.color_tile(
                                                       face_index, row, column))
                    tile.grid(row=row, column=column, padx=3, pady=3)

                    self.cube[face_index][row][column] = tile

            face_index += 1

    def get_color(self, color):
        self.selected_color = color

    def color_tile(self, face_index, row_index, colum_index):
        main_color = self.selected_color["main_color"]
        hover_color = self.selected_color["hover_color"]

        self.cube[face_index][row_index][colum_index].configure(
            fg_color=main_color, hover_color=hover_color)

    def start_color_menu_callback(self, start_color):
        self.start_color = start_color.lower()
        self.color_centre_tiles(self.start_color)

    def color_centre_tiles(self, start_color):
        default_color_order = list('wogrby')

        rotation_details = {'yellow': ('X', 0),
                            'white': ('X', 2),
                            'green': ('X', 1, -1),
                            'blue': ('X', 1),
                            'orange': ('Z', 1, -1),
                            'red': ('Z', 1)
                            }
        for key in rotation_details.keys():
            if key == start_color:
                color_order = self.cube_rotation(default_color_order,
                                                 *rotation_details[key])
                break

        colors = self.order_colors(color_order)

        for face_index in range(6):
            main_color = colors[face_index]["main_color"]
            hover_color = colors[face_index]["hover_color"]

            self.cube_coloring_reference[face_index][1][1] = colors[
                'color_reference']
            # call coloring function instead
            self.cube[face_index][1][1].configure(fg_color=main_color,
                                                  hover_color=hover_color)

    def order_colors(self, order):
        color_list = self.color_details[:6]

        for index in range(len(order)):
            for color in color_list:
                if order[index] == color['main_color'][0]:
                    order[index] = color
                    color_list.remove(color)
        return order

    def cross_checkbox_event(self):
        print(self.cross_check_var.get())
        # if self.cross_check_var.get() == 1:
        #     self.cube_coloring_reference[]

    def f2l_checkbox_event(self):
        print(self.f2l_check_var.get())

    def oll_checkbox_event(self):
        print(self.oll_check_var.get())

    def color_cross_tiles(self):
        # fix this shit
        self.cube_coloring_reference[1][2][1] = 'o'
        self.cube_coloring_reference[2][2][1] = 'y'
        self.cube_coloring_reference[3][2][1] = 'r'
        self.cube_coloring_reference[4][2][1] = 'w'
        self.cube_coloring_reference[5][0][1] = 'b'
        self.cube_coloring_reference[5][1][2] = 'b'
        self.cube_coloring_reference[5][2][1] = 'b'
        self.cube_coloring_reference[5][1][0] = 'b'

    def cube_rotation(self, cube_state, X_Y_Z, amount, prime=1):
        '''Rotates the cube. prime = 1 or -1 if -2 the prime rotation is performed.'''

        # rotation cordinates
        X = [[0, 2], [2, 5], [5, 4]]
        Y = [[1, 2], [2, 3], [3, 4]]
        Z = [[0, 1], [1, 5], [5, 3]]

        if X_Y_Z == 'X':
            rotation = X
        elif X_Y_Z == 'Y':
            rotation = Y
        elif X_Y_Z == 'Z':
            rotation = Z

        # creates a slice, inverts list
        for n in range(amount):
            for r in rotation[::prime]:
                r = r[::prime]
                cube_state[r[0]], cube_state[r[1]] = cube_state[r[1]], \
                                                     cube_state[r[0]]

        return cube_state

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = RubiksApp()
    app.mainloop()
