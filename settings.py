class Settings:
    def __init__(self):
        self.color_details = [
            {'color_name': 'red', 'color_reference': 'r', 'light_color': 'red',
             'dark_color': '#b00502'},
            {'color_name': 'blue', 'color_reference': 'b',
             'light_color': 'blue',
             'dark_color': '#19158a'},
            {'color_name': 'yellow', 'color_reference': 'y',
             'light_color': 'yellow',
             'dark_color': '#91991f'},
            {'color_name': 'orange', 'color_reference': 'o',
             'light_color': 'orange',
             'dark_color': '#a16312'},
            {'color_name': 'green', 'color_reference': 'g',
             'light_color': 'green',
             'dark_color': '#0e5207'},
            {'color_name': 'white', 'color_reference': 'w',
             'light_color': 'white',
             'dark_color': '#afb8ae'},
            {'color_name': 'default', 'color_reference': 'd',
             'light_color': '#2b9ced',
             'dark_color': '#016fbe'}
        ]
        self.width = 1074
        self.height = 800
        self.title = "Rubik's App"


settings = Settings()
