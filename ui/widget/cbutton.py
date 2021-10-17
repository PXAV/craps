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
                 primary: bool = True,
                 callback: callable = None,
                 **kw):
        super().__init__(master, width=width, height=height, bd=0, highlightthickness=0, **kw)
        background_color = current_theme.get_color(ThemeProperty.PRIMARY_BACKGROUND)
        self.config(background=background_color)
        button_color = current_theme.get_color(ThemeProperty.PRIMARY_BUTTON) if primary else current_theme.get_color(ThemeProperty.SECONDARY_BUTTON)
        image = Image.new(
            "RGB",
            (width, height),
            background_color
        )
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((0, 0, width, height), radius=17, fill=button_color)
        if text is not None and text is not "":
            font_to_load = normal_font
            draw.text((width / 8, height / 3), text, fill="white", font=ImageFont.truetype(
                font=str(Path(f"{working_directory}/{normal_font}")),
                size=text_size)
            )
        self.img = ImageTk.PhotoImage(image)

        if callback is not None:
            self.callback = callback
            self.bind("<Button-1>", self.on_clicked())

    def on_clicked(self):
        self.callback()

    def show(self, *args, **kwargs):
        self.pack(*args, **kwargs)
        self.create_image(int(self["width"]) / 2, int(self["height"]) / 2, image=self.img)




