import customtkinter
from other_functions import create_cube_representation, get_dictionary_details
from settings import settings
from coloring import color_tiles


class CubeRepresentationFrame(customtkinter.CTkFrame):
    """
    This class represents the frame containing the visual cube representation,
    and has the attributes and methods to model it as such.
    """
    face_frames = {
        'white_face': None,
        'orange_face': None,
        'green_face': None,
        'red_face': None,
        'blue_face': None,
        'yellow_face': None
    }
    cube_tile_instances = create_cube_representation(None)

    tile_size = 54

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_face_frames()
        self.create_and_add_tiles()

    def create_face_frames(self):
        """Creates the layout of the cube faces using frames."""

        cube_layout = [
            ['space', 'frame', 'space', 'space'],
            ['frame'] * 4,
            ['space', 'frame', 'space', 'space']
        ]
        face_keys = list(self.face_frames.keys())
        face_index = 0

        for row in range(3):
            for column in range(4):
                if cube_layout[row][column] == 'frame':
                    face = customtkinter.CTkFrame(master=self)
                    face.grid(row=row, column=column, padx=5, pady=5)

                    self.face_frames[face_keys[face_index]] = face
                    face_index += 1

    def create_and_add_tiles(self):
        """Adds the tiles/buttons to each face frame."""
        face_index = 0

        default_color = get_dictionary_details(settings.color_details, 'd')
        # loops through the instances of the face frames
        for face in self.face_frames.values():
            for row in range(3):
                for column in range(3):
                    tile = customtkinter.CTkButton(
                        master=face,
                        text='',
                        fg_color=default_color["light_color"],
                        hover_color=default_color["dark_color"],
                        width=self.tile_size,
                        height=self.tile_size)
                    tile.grid(row=row, column=column, padx=4, pady=4)
                    # Adds the button instance to the list representing the cube
                    self.cube_tile_instances[face_index][row][column] = tile

            face_index += 1

    def enable_or_disable_all_tiles(self, normal_disabled):
        """
        Enables or disables all the tiles on the cube using the
        enable_or_disable_tile method.

        :param normal_disabled: Either 'normal' to enable or 'disabled' to
        disable all the tiles.
        """
        for face in range(6):
            for row in range(3):
                for column in range(3):
                    self.enable_or_disable_tile(face, row, column, normal_disabled)

    def enable_or_disable_tile(self, face_index, row_index, column_index, normal_disabled):
        """
        Uses the indices to reference and disables a specific button of the cube.
        """
        # gets the button instances from the color palette button's details
        button = self.cube_tile_instances[face_index][row_index][column_index]
        tile_color = button.cget("fg_color")

        if normal_disabled == "normal":
            light_or_dark = "light_color"
        elif normal_disabled == "disabled":
            light_or_dark = 'dark_color'

        fg_color = get_dictionary_details(settings.color_details,
                                          tile_color,
                                          light_or_dark)
        button.configure(state=normal_disabled, fg_color=fg_color)

    def disable_tiles_not_in_list(self, enable_list):
        """Disables all the tiles that are not in the enable list."""

        self.enable_or_disable_all_tiles("disabled")

        for face, row, column in enable_list:
            self.enable_or_disable_tile(face, row, column, "normal")

    def update_tile_colors(self, state):
        """Changes the colours on the button instances representing the cube to
        reflect the values of the state passed in."""
        color_tiles(self.cube_tile_instances, state)

