from tkinter import Canvas

from PIL import Image, ImageTk, ImageDraw, ImageFont
from ui.theme.theme_repository import current_theme
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
                 initial_attempts: int = 0,
                 **kw):
        super().__init__(master, width=width, height=height, bd=0, highlightthickness=0, **kw)
        self.window = master
        self.width = width
        self.height = height
        self.attempts = initial_attempts

        self.background_color = current_theme.get_color(ThemeProperty.PRIMARY_BACKGROUND)
        self.button_color = current_theme.get_color(
            ThemeProperty.PRIMARY_BUTTON) if primary else current_theme.get_color(ThemeProperty.SECONDARY_BUTTON)
        self.update_properties(width, height,
                               border_radius,
                               text, text_size, text_type, text_align, text_position,
                               primary,
                               opaque)
        self.config(background=self.background_color)
        self.raw_image = None
        self.photo_image = None
        self.__draw_attempts(self.text)

        # bind callback to left mouse button click
        if callback is not None:
            self.bind("<Button-1>", callback)

    def show_pack(self, *args, **kwargs):
        self.pack(*args, **kwargs)
        self.__apply_image()

    def show_grid(self, *args, **kwargs):
        self.grid(*args, **kwargs)
        self.__apply_image()

    def update_attempts(self, attempts: int):
        self.update_properties(self.width, self.height, attempts)

    def update_properties(self,
                          width: int,
                          height: int,
                          attempts: int):
        self.width = width
        self.height = height
        self.attempts = attempts
        self.background_color = current_theme.get_color(ThemeProperty.PRIMARY_BACKGROUND)
        self.button_color = current_theme.get_color(
            ThemeProperty.PRIMARY_BUTTON) if primary else current_theme.get_color(ThemeProperty.SECONDARY_BUTTON)

        self.config(width=self.width)
        self.config(height=self.height)

        self.__draw_attempts(self.text)
        self.__apply_image()
        self.update()

    def __draw_attempts(self, new_text):
        self.text = new_text
        self.raw_image = Image.new(
            "RGB",
            (self.width, self.height),
            self.background_color
        )
        draw = ImageDraw.Draw(self.raw_image)


        if self.opaque:
            draw.rounded_rectangle((0, 0, self.width, self.height), radius=self.border_radius, fill=self.button_color)

        if self.text:
            font_to_load = normal_font
            if self.text_type == "thin":
                font_to_load = thin_font
            elif self.text_type == "bold":
                font_to_load = bold_font

            xy = (self.width / 8, self.height / 3)
            if self.text_position:
                xy = self.text_position

            draw.text(xy, self.text, align=self.text_align, fill="white", font=ImageFont.truetype(
                font=str(Path(f"{working_directory}/{font_to_load}")),
                size=self.text_size)
                      )
        self.photo_image = ImageTk.PhotoImage(self.raw_image)

    def __apply_image(self):
        self.create_image(int(self["width"]) / 2, int(self["height"]) / 2, image=self.photo_image)