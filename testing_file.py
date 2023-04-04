import customtkinter

from view import View
from controller import Controller
from model import Model


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.tab_view = View(master=self)
        self.tab_view.grid(row=0, column=0)

        self.model = Model()

        self.controller = Controller(self.model, self.tab_view)


app = App()
app.mainloop()
