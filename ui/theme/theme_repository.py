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


def next_theme(window, button):
    from ui.menu_views import open_settings_menu
    indexed_themes = __index_themes()
    values = list(indexed_themes.values())
    current_theme_index = values.index(current_theme.name)
    if len(values) > current_theme_index + 1:
        set_current_theme(values[current_theme_index + 1])
        button.update_text(values[current_theme_index + 1])
    else:
        set_current_theme(values[0])
        button.update_text(values[0])
    open_settings_menu(window)


def previous_theme(window, button):
    from ui.menu_views import open_settings_menu
    indexed_themes = __index_themes()
    values = list(indexed_themes.values())
    current_theme_index = values.index(current_theme.name)
    if current_theme_index - 1 <= 0:
        set_current_theme(values[current_theme_index - 1])
        button.update_text(values[current_theme_index - 1])
    else:
        set_current_theme(values[0])
        button.update_text(values[0])
    open_settings_menu(window)


def get_current_theme() -> Theme:
    return current_theme


def __index_themes() -> dict:
    index_dict = {}
    index = 0
    for theme_name in all_themes.keys():
        index_dict[index] = theme_name
        index += 1
    return index_dict