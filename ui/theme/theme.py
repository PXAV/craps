import toml
from theme_properties import ThemeProperty


class Theme:

    def __init__(self, name: str):
        self.name = name
        self.data = None
        self.properties = {
            ThemeProperty.PRIMARY_BUTTON: "",
            ThemeProperty.SECONDARY_BUTTON: ""
        }

    def load_from_file(self, file_path):
        with open(file_path, 'r') as file:
            data = toml.loads(file.read())

        for simple_key in data.get("colors").keys():
            full_key = f"colors.{simple_key}"
            self.properties[ThemeProperty(full_key)] = data.get("colors").get(simple_key)

    def get_color(self, color_property: ThemeProperty) -> str:
        return self.properties.get(color_property)
