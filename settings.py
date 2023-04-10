class Settings:
    def __init__(self):
        self.color_details = [
            {'color_name': 'red', 'color_reference': 'r',
             'light_color': '#c7242f', 'dark_color': '#8c1b22'},
            {'color_name': 'blue', 'color_reference': 'b',
             'light_color': '#316fcc', 'dark_color': '#1d437a'},
            {'color_name': 'yellow', 'color_reference': 'y',
             'light_color': '#ffdd00', 'dark_color': '#948001'},
            {'color_name': 'orange', 'color_reference': 'o',
             'light_color': '#ff6d00', 'dark_color': '#a14602'},
            {'color_name': 'green', 'color_reference': 'g',
             'light_color': '#2abb2a', 'dark_color': '#1b6e1b'},
            {'color_name': 'white', 'color_reference': 'w',
             'light_color': '#ffffff', 'dark_color': '#9c9c9c'},
            {'color_name': 'default', 'color_reference': 'd',
             'light_color': '#3f8bfc', 'dark_color': '#016fbe'}
        ]
        self.width = 1074
        self.height = 800
        self.title = "NMZ Cubez"


settings = Settings()
