import toml
from theme_properties import ThemeProperty


class Theme:

    def __init__(self, file_path: str):
        self.name = None
        self.author = None
        self.description = None
        self.version = None

        self.properties = {
            ThemeProperty.PRIMARY_BUTTON: "",
            ThemeProperty.SECONDARY_BUTTON: ""
        }

        self.load_from_file(file_path)

    def load_from_file(self, file_path):
        with open(file_path, 'r') as file:
            data = toml.loads(file.read())

        meta = data.get("meta")
        self.name = meta.get("name")
        self.author = meta.get("author")
        self.description = meta.get("description")
        self.version = meta.get("version")

        for simple_key in data.get("colors").keys():
            full_key = f"colors.{simple_key}"
            self.properties[ThemeProperty(full_key)] = data.get("colors").get(simple_key)

    def get_color(self, color_property: ThemeProperty) -> str:
        return self.properties.get(color_property)
