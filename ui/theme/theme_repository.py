from __init__ import working_directory
from ui.theme.theme import Theme
from pathlib import Path
import os

all_themes = {}

# get first theme in theme directory as default theme
theme_directory = Path(f"{working_directory}/resources/theme/")
current_theme = Theme(str(theme_directory / os.listdir(theme_directory)[0]))


def load_all_themes():
    theme_files = os.listdir(theme_directory)
    print(theme_files)
    for current_file in theme_files:
        print(f'Loading theme from {theme_directory / current_file}')
        new_theme = Theme(str(theme_directory / current_file))
        all_themes[new_theme.name] = new_theme


def set_current_theme(name: str):
    global current_theme
    if all_themes.get(name) is None:
        raise NameError(f'Cannot set theme {name}. Theme does not exist.')
    print(f"setting theme to {name} -> {all_themes.get(name)} -> {all_themes.get(name).name}")
    current_theme = all_themes.get(name)
    print(f"set current theme {current_theme.name}")


def get_current_theme() -> Theme:
    return current_theme
