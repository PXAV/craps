import toml
from ui.theme.theme_properties import ThemeProperty


class Theme:
    """
    Represents a UI theme. A theme is used to dynamically adjust the colors of the user interface.
    The user can choose which color theme to use, which make the application look dark, light or anything
    in between. Read more about themes in the theme_repository.py.

    This class is used as a mean to save the properties of a theme and load it from its theme file
    if needed.
    """

    def __init__(self, file_path: str):
        """
        Initializes a new theme and automatically loads it from the
        given file.

        :param file_path: The file path to the theme configuration file (including file extension)
        """

        # define theme metadata
        self.name = None
        self.author = None
        self.description = None
        self.version = None

        self.properties = {}

        print(f"Initializing theme from {file_path}")
        self.__load_from_file(file_path)

    def get_color(self, color_property: ThemeProperty) -> str:
        """
        Gets a color from this theme. The output produced from this method
        can directly be used as input/argument in the tkinter library.

        :param color_property: The color type you want (primary/secondary background/button etc.)
        :return: The HEX color value as a string (e. g. '#ffffff' for white)
        """
        return self.properties.get(color_property)

    def __load_from_file(self, file_path):
        """
        Loads a file from the given file path. It will load the TOML string and
        automatically write the theme properties to the attributes of this class,
        so that they can be queried from outside.

        This method is automatically executed by the constructor and should therefore
        not be run from anywhere else to avoid unexpected behavior.

        :param file_path: The file path to the theme configuration file (including file extension)
        """

        with open(file_path, 'r') as file:
            data = toml.loads(file.read())

        # the toml file is split into two paragraphs:
        # meta: name, author, etc.
        # colors: actual HEX color values
        # Those two dictionaries therefore have to be split up in the following:

        meta = data.get("meta")
        self.name = meta.get("name")
        self.author = meta.get("author")
        self.description = meta.get("description")
        self.version = meta.get("version")

        for simple_key in data.get("colors").keys():
            full_key = f"colors.{simple_key}"
            self.properties[ThemeProperty(full_key)] = data.get("colors").get(simple_key)
