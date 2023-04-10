import customtkinter

from view import View
from model import Model
from controller import Controller

from settings import settings


class RubiksApp(customtkinter.CTk):
    """A class representing my app, that solves a rubik's cube."""

    # setting constants (WIDTH AND HEIGHT)
    WIDTH = settings.width
    HEIGHT = settings.height

    def __init__(self):
        """
        Initialize the attributes of the parent class.
        Then initialize the attributes of my app which uses MVC design.
        (Model, View, Controller)
        """
        super().__init__()

        # title and geometry of the app
        self.title(settings.title)
        self.geometry(f"{RubiksApp.WIDTH}x{RubiksApp.HEIGHT}")

        # creating instances of View, Model and Controller
        self.view = View(master=self)
        self.view.grid(row=0, column=0)

        self.model = Model()

        self.controller = Controller(self.model, self.view)

    def run(self):
        """Starts the main loop of the app."""
        self.mainloop()


if __name__ == "__main__":
    app = RubiksApp()
    app.run()
