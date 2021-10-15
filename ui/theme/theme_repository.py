from __init__ import working_directory
from theme import Theme
import os

all_themes = {}

# get first theme in theme directory as default theme
current_theme = Theme(os.path.join(working_directory, "config/theme")[0])


def load_all_themes():
    theme_files = os.listdir(os.path.join(working_directory, "config/theme"))
    for current_file in theme_files:
        new_theme = Theme(current_file)
        all_themes[new_theme.name] = new_theme


def set_current_theme(name: str):
    global current_theme
    if all_themes.get(name) is None:
        raise NameError(f'Cannot set theme {name}. Theme does not exist.')
    current_theme = all_themes.get(name)


def get_current_theme() -> Theme:
    return current_theme
