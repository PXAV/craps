from tkinter import Canvas

from PIL import Image, ImageTk, ImageDraw, ImageFont
from ui.theme.theme_repository import get_current_theme
from ui.theme.theme_properties import ThemeProperty
from configuration import normal_font, bold_font, thin_font
from __init__ import working_directory
from pathlib import Path
from ui.window import Window


class DiceIndicator(Canvas):

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
        self.pack(*args, **kwargs)
        self.__apply_image()

    def show_grid(self, *args, **kwargs):
        self.grid(*args, **kwargs)
        self.__apply_image()

    def get_attempts(self) -> list:
        return self.attempts

    def add_attempt(self, dice_sum: int):
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

        last_circle_location = 0
        padding = 8
        for indicator in range(0, self.max_shown_attempts):
            circle_color = get_current_theme().get_color(ThemeProperty.DICE_INDICATOR_ACTIVE)
            x_position = self.height * (indicator + 1) + padding * (indicator + 1)

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
