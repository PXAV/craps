from tkinter import Canvas

from PIL import Image, ImageTk, ImageDraw, ImageFont
from ui.theme.theme_repository import get_current_theme
from ui.theme.theme_properties import ThemeProperty
from configuration import normal_font, bold_font, thin_font
from __init__ import working_directory
from pathlib import Path
from ui.window import Window


class DiceIndicator(Canvas):
    """
    Represents a custom tkinter widget visualizing the dicing
    progress while playing the game as a normal user. This is only
    the case when the first dice is a draw and the user falls into the
    state of having to dice infinitely until the game ends.

    Each attempt is represented by a bubble, which shows the dice sum
    achieved in that attempt.
    """

    def __init__(self,
                 master: Window = None,
                 width: int = 100,
                 height: int = 30,
                 initial_attempts: list = None,
                 max_shown_attempts: int = 10,
                 text_size: int = 26,
                 text_align: str = "left",
                 text_type: str = "bold",
                 **kw):
        """
        Initializes a new dice indicator.

        :param master:                  The window or frame to display the indicator in.
        :param width:                   The total width in pixels
        :param height:                  The total height in pixels
        :param initial_attempts:        How many attempts to show when the indicator is displayed for the first time.
        :param max_shown_attempts:      How many attempts to show at max.
        :param text_size:               Font size of the text showing the total amount of attempts
        :param text_align:              Text alignment of attempt amount text (left/right)
        :param text_type:               Text type of attempt amount text (bold/thin/normal)
        :param kw:                      Arguments for tkinter parent widget
        """
        super().__init__(master, width=width, height=height, bd=0, highlightthickness=0, **kw)
        self.window = master
        self.width = width
        self.height = height
        self.attempts = initial_attempts if initial_attempts is not None else []
        self.max_shown_attempts = max_shown_attempts
        self.text_align = text_align
        self.text_type = text_type
        self.text_size = text_size

        self.background_color = get_current_theme().get_color(ThemeProperty.PRIMARY_BACKGROUND)
        self.update_properties(width, height, self.attempts)
        self.config(background=self.background_color)
        self.raw_image = None
        self.photo_image = None
        self.__draw_attempts()

    def show_pack(self, *args, **kwargs):
        """
        Finally displays the indicator in the given master window using
        tkinter's pack manager.

        :param args:    arguments for master.pack() method
        :param kwargs:  arguments for master.pack() method
        """
        self.pack(*args, **kwargs)
        self.__apply_image()

    def show_grid(self, *args, **kwargs):
        """
        Finally displays the indicator in the given master window using
        tkinter's grid manager.

        :param args:    arguments for master.grid() method
        :param kwargs:  arguments for master.grid() method
        """
        self.grid(*args, **kwargs)
        self.__apply_image()

    def get_attempts(self) -> list:
        """
        Gets a list of all attempts displayed by this indicator.
        An attempt is represented by the dice sum it generated.

        :return: A list with all attempts shown by this indicator.
        """
        return self.attempts

    def add_attempt(self, dice_sum: int):
        """

        :param dice_sum:
        :return:
        """
        self.attempts.append(dice_sum)
        self.update_properties(self.width, self.height, self.attempts)

    def update_properties(self,
                          width: int,
                          height: int,
                          attempts: list):
        self.width = width
        self.height = height
        if len(attempts) <= 0:
            print("Cannot show 0 attempts or negative amount of attempts!")
            self.attempts = []
        else:
            self.attempts = attempts
        self.background_color = get_current_theme().get_color(ThemeProperty.PRIMARY_BACKGROUND)

        self.config(width=self.width)
        self.config(height=self.height)

        self.__draw_attempts()
        self.__apply_image()
        self.update()

    def __draw_attempts(self):
        self.raw_image = Image.new(
            "RGB",
            (self.width, self.height),
            self.background_color
        )
        draw = ImageDraw.Draw(self.raw_image)

        font_to_load = normal_font
        if self.text_type == "thin":
            font_to_load = thin_font
        elif self.text_type == "bold":
            font_to_load = bold_font

        # the latest x location where an attempt circle has been drawn
        last_circle_location = 0

        # the padding between attempt circles along the x-axis
        padding = 8

        # generate as many circles as there are attempts to display
        for indicator in range(0, self.max_shown_attempts):
            circle_color = get_current_theme().get_color(ThemeProperty.DICE_INDICATOR_ACTIVE)
            x_position = self.height * (indicator + 1) + padding * (indicator + 1)

            # check if
            if indicator + 1 > len(self.attempts):
                circle_color = get_current_theme().get_color(ThemeProperty.SECONDARY_BACKGROUND)

            draw.ellipse((x_position, 0,
                          x_position + self.height, self.height),
                         fill=circle_color)
            last_circle_location = x_position + self.height

            if indicator < len(self.attempts):
                draw.text((x_position + padding, padding,
                           x_position + self.height - padding, self.height - padding),
                          f"{self.attempts[indicator]}",
                          align=self.text_align,
                          fill="white",
                          font=ImageFont.truetype(
                              font=str(Path(f"{working_directory}/{font_to_load}")),
                              size=int(self.text_size * 0.7)))

        draw.text((last_circle_location + 20, 0, self.width, self.height),
                  f"{len(self.attempts)}",
                  align=self.text_align,
                  fill="white",
                  font=ImageFont.truetype(
                      font=str(Path(f"{working_directory}/{font_to_load}")),
                      size=self.text_size))

        self.photo_image = ImageTk.PhotoImage(self.raw_image)

    def __apply_image(self):
        self.create_image(int(self["width"]) / 2, int(self["height"]) / 2, image=self.photo_image)
