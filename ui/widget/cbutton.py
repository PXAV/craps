from tkinter import Tk, Canvas

from PIL import Image, ImageTk, ImageDraw, ImageFont
from ui.theme.theme_repository import current_theme
from ui.theme.theme_properties import ThemeProperty
from configuration import normal_font, bold_font, thin_font
from __init__ import working_directory
from pathlib import Path


class CrapsButton(Canvas):

    def __init__(self,
                 master: Tk or any = None,
                 width: int = 100,
                 height: int = 30,
                 text: str = None,
                 text_size: int = 14,
                 text_type: str = "normal",  # bold, normal, thin
                 text_align: str = "left",
                 primary: bool = True,
                 opaque: bool = True,
                 callback: callable = None,
                 **kw):
        super().__init__(master, width=width, height=height, bd=0, highlightthickness=0, **kw)
        background_color = current_theme.get_color(ThemeProperty.PRIMARY_BACKGROUND)
        button_color = current_theme.get_color(ThemeProperty.PRIMARY_BUTTON) if primary else current_theme.get_color(ThemeProperty.SECONDARY_BUTTON)

        self.config(background=background_color)

        image = Image.new(
            "RGB",
            (width, height),
            background_color
        )
        draw = ImageDraw.Draw(image)

        if opaque:
            draw.rounded_rectangle((0, 0, width, height), radius=17, fill=button_color)

        if text:
            font_to_load = normal_font
            if text_type == "thin":
                font_to_load = thin_font
            elif text_type == "bold":
                font_to_load = bold_font
            draw.text((width / 8, height / 3), text, align=text_align, fill="white", font=ImageFont.truetype(
                font=str(Path(f"{working_directory}/{font_to_load}")),
                size=text_size)
            )
        self.img = ImageTk.PhotoImage(image)

        if callback is not None:
            self.bind("<Button-1>", callback)

    def show_pack(self, *args, **kwargs):
        self.pack(*args, **kwargs)
        self.create_image(int(self["width"]) / 2, int(self["height"]) / 2, image=self.img)

    def show_grid(self, *args, **kwargs):
        self.grid(*args, **kwargs)
        self.create_image(int(self["width"]) / 2, int(self["height"]) / 2, image=self.img)



