from tkinter import *
from ui.theme.theme_repository import get_current_theme
from ui.theme.theme_properties import ThemeProperty


class Window(Tk):
    """
    Custom window implementation offering enhanced grid controls and
    seamless theme integration.
    """

    def __init__(self, screen_name: str, width=1200, height=800):
        super().__init__()
        self.width = width
        self.height = height
        self.config(background=get_current_theme().get_color(ThemeProperty.PRIMARY_BACKGROUND))
        self.geometry(f"{width}x{height}")
        self.title(screen_name)
        self.custom_grid_rows = 0
        self.custom_grid_columns = 0

    def open(self):
        """
        Opens the window and makes it visible to the user.
        """
        self.mainloop()

    def clear_widgets(self):
        """
        Removes all widgets from the window. This removes all buttons,
        frames, canvases, etc. so that you are left with an empty window.
        The background color is kept.
        """
        widget_list = self.grid_slaves()
        for widget in widget_list:
            widget.destroy()

    def configure_grid(self, columns: int, rows: int):
        """
        Configures a custom grid with the given amount of rows
        and columns. This allows you to predefine a grid instead
        of letting tkinter auto-generate it for you

        :param columns: The amount of columns of the grid.
        :param rows:    The amount of rows of the grid
        """
        self.custom_grid_rows = rows
        self.custom_grid_columns = columns
        for row in range(rows - 2):
            self.rowconfigure(row, weight=1)
        for column in range(columns - 2):
            self.columnconfigure(column, weight=1)

    def reset_custom_grid(self):
        """
        Resets the custom grid set with configure_grid() by giving
        each grid cell a scale of 0, so that it becomes useless.
        When you now put a widget in the cell again, tkinter will
        automatically rescale the cells accordingly.
        """
        for i in range(self.custom_grid_rows):
            self.rowconfigure(i, weight=0)
        for i in range(self.custom_grid_columns):
            self.columnconfigure(i, weight=0)

    def get_height(self) -> int:
        """
        Gets the width of the window in pixels.
        :return: The width of the window in pixels.
        """
        return self.height

    def get_width(self) -> int:
        """
        Gets the width of the window in pixels.
        :return: The width of the window in pixels.
        """
        return self.width
