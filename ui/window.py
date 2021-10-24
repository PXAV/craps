from tkinter import *
from ui.theme.theme_repository import current_theme
from ui.theme.theme_properties import ThemeProperty


class Window(Tk):

    def __init__(self, screen_name: str, width=1200, height=800):
        super().__init__()
        self.width = width
        self.height = height
        self.config(background=current_theme.get_color(ThemeProperty.PRIMARY_BACKGROUND))
        self.geometry(f"{width}x{height}")
        self.title(screen_name)
        self.custom_grid_size = 0

    def open(self):
        self.root.mainloop()

    def get_height(self) -> int:
        return self.height

    def get_width(self) -> int:
        return self.width
