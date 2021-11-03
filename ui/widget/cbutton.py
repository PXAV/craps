from tkinter import Canvas, Frame, Tk

from PIL import Image, ImageTk, ImageDraw, ImageFont
from ui.theme.theme_repository import get_current_theme
from ui.theme.theme_properties import ThemeProperty
from configuration import normal_font, bold_font, thin_font
from __init__ import working_directory
from pathlib import Path
from ui.window import Window


class CrapsButton(Canvas):
    """
    This class represents a reusable button widget for tkinter GUIs.
    Although it is used as a button, it extends from the canvas class.
    This is done to have more flexibility in custom styles. Craps simply
    draws an image on the canvas and makes itself independent from
    the different operating system button styles.

    When setting the opaque attribute to false, you can remove the button
    background and use it as a kind of clickable label. The class also offers
    seamless integration into the theming system
    """

    def __init__(self,
                 master: Window or Frame or Tk = None,
                 width: int = 100,
                 height: int = 30,
                 border_radius: int = 17,
                 text: str = None,
                 text_size: int = 14,
                 text_type: str = "normal",
                 text_align: str = "left",
                 text_position: tuple = (),
                 primary: bool = True,
                 opaque: bool = True,
                 callback: callable = None,
                 **kw):
        """
        Creates a new CrapsButton instance. Most of these parameters can be changed
        and updated later.

        :param master:          the parent to draw the button on (either a window or a frame)
        :param width:           width of button in pixels
        :param height:          height of button in pixels
        :param border_radius:   border radius of the background rectangle (determines "roundness")
        :param text:            text to display on the button
        :param text_size:       font size to use
        :param text_type:       font style to use (bold/normal/thin)
        :param text_align:      text alignment within the button (left/right)
        :param text_position:   text position inside the button
        :param primary:         which color to use for the button background
        :param opaque:          whether the background rectangle should be drawn
        :param callback:        command to run when the button is left-clicked.
        :param kw:
        """
        super().__init__(master, width=width, height=height, bd=0, highlightthickness=0, **kw)
        self.window = master
        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.text = text
        self.text_size = text_size
        self.text_type = text_type
        self.text_align = text_align
        self.text_position = text_position
        self.primary = primary
        self.opaque = opaque
        self.background_color = get_current_theme().get_color(ThemeProperty.PRIMARY_BACKGROUND)
        self.button_color = get_current_theme().get_color(
            ThemeProperty.PRIMARY_BUTTON) if primary else get_current_theme().get_color(ThemeProperty.SECONDARY_BUTTON)
        self.update_properties(width, height,
                               border_radius,
                               text, text_size, text_type, text_align, text_position,
                               primary,
                               opaque)
        self.config(background=self.background_color)
        self.raw_image = None
        self.photo_image = None
        self.__draw_text(self.text)

        # bind callback to left mouse button click
        if callback is not None:
            self.bind("<Button-1>", callback)

    def show_pack(self, *args, **kwargs):
        """
        Finally displays the button in the given master window using
        tkinter's pack manager.

        :param args:    arguments for master.pack() method
        :param kwargs:  arguments for master.pack() method
        """
        self.pack(*args, **kwargs)
        self.__apply_image()

    def show_grid(self, *args, **kwargs):
        """
        Finally displays the button in the given master window using
        tkinter's grid manager.

        :param args:    arguments for master.grid() method
        :param kwargs:  arguments for master.grid() method
        """
        self.grid(*args, **kwargs)
        self.__apply_image()

    def get_width(self) -> int:
        """
        Gets the width of the button in pixels.
        :return: width of button in pixels.
        """
        return self.width

    def get_height(self) -> int:
        """
        Gets the height of the button in pixels.
        :return: height of button in pixels.
        """
        return self.height

    def update_text(self, new_text):
        """
        Immediately updates the text in the button to the given string.

        :param new_text: The new text to display
        """
        self.update_properties(self.width, self.height, self.border_radius, new_text, self.text_size,
                               self.text_type, self.text_align, self.text_position, self.primary, self.opaque)

    def update_properties(self,
                          width: int,
                          height: int,
                          border_radius: int,
                          text: str,
                          text_size: int,
                          text_type: str,  # bold, normal, thin
                          text_align: str,
                          text_position: tuple,
                          primary: bool,
                          opaque: bool):
        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.text = text
        self.text_size = text_size
        self.text_type = text_type
        self.text_align = text_align
        self.text_position = text_position
        self.opaque = opaque
        self.background_color = get_current_theme().get_color(ThemeProperty.PRIMARY_BACKGROUND)
        self.button_color = get_current_theme().get_color(
            ThemeProperty.PRIMARY_BUTTON) if primary else get_current_theme().get_color(ThemeProperty.SECONDARY_BUTTON)

        self.config(width=self.width)
        self.config(height=self.height)

        self.__draw_text(self.text)
        self.__apply_image()
        self.update()

    def __draw_text(self, new_text):
        """
        Draws an image on the tkinter canvas containing the text.

        :param new_text: The text to draw on the button.
        """

        self.text = new_text
        self.raw_image = Image.new(
            "RGB",
            (self.width, self.height),
            self.background_color
        )
        draw = ImageDraw.Draw(self.raw_image)

        # only draw a rounded rectangle as background if the button is opaque.
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

            text_color: str
            if self.opaque:
                text_color = get_current_theme().get_color(ThemeProperty.PRIMARY_TEXT)
            else:
                text_color = get_current_theme().get_color(ThemeProperty.SECONDARY_TEXT)

            draw.text(xy, self.text, align=self.text_align,
                      fill=text_color,
                      font=ImageFont.truetype(
                          font=str(Path(f"{working_directory}/{font_to_load}")),
                          size=self.text_size)
                      )
        self.photo_image = ImageTk.PhotoImage(self.raw_image)

    def __apply_image(self):
        """
        Applies the image contained by the photo_image attribute to the button.
        """
        self.create_image(int(self["width"]) / 2, int(self["height"]) / 2, image=self.photo_image)
