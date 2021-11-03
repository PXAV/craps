"""
This is the main file of Craps' theming system.
"""

from __init__ import working_directory
from ui.theme.theme import Theme
from pathlib import Path
import os
from storage.user_preference import UserPreference

# caches all themes currently available by {'name': Theme object}
all_themes = {}

# get first theme in theme directory as default theme
theme_directory = Path(f"{working_directory}/resources/theme/")
current_theme = Theme(str(theme_directory / os.listdir(theme_directory)[0]))


def load_all_themes():
    """
    Loads all themes from the theme directory and puts them into
    the cache to reduce execution times and disk load.
    """

    theme_files = os.listdir(theme_directory)
    print(theme_files)
    for current_file in theme_files:
        print(f'Loading theme from {theme_directory / current_file}')
        new_theme = Theme(str(theme_directory / current_file))
        all_themes[new_theme.name] = new_theme


def set_current_theme(name: str):
    """
    Updates the theme to a theme with the given name.
    While this updates the theme in the user's configuration file,
    it will not update the colors in the GUI, so please
    run the draw method of your current page again to also
    update the colors.

    :param name: The name of the new theme to set.
    """
    from storage.user_preferences import set_preference
    global current_theme

    # if there is no theme with the given name, send an error to the console
    # and exit from function.
    if all_themes.get(name) is None:
        raise NameError(f'Cannot set theme {name}. Theme does not exist.')

    current_theme = all_themes.get(name)
    set_preference(UserPreference.THEME, name)


def next_theme(window, button):
    """
    Checks which theme is currently applied and switches
    to a theme with a higher index. The index is usually determined
    by the order of theme files in the theme directory.

    This method is meant to be used for the arrow buttons in the theme
    selection in the settings page as it directly updates the settings
    page after having updated the theme.

    :param window:  The window to instantly update the theme to.
    :param button:  The button which displays the theme name in the settings.
    """
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
    """
    Checks which theme is currently applied and switches
    to a theme with a lower index. The index is usually determined
    by the order of theme files in the theme directory.

    This method is meant to be used for the arrow buttons in the theme
    selection in the settings page as it directly updates the settings
    page after having updated the theme.

    :param window:  The window to instantly update the theme to.
    :param button:  The button which displays the theme name in the settings.
    """
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
    """
    Gets the theme that is currently configured by the user.
    Make sure to use this method for getting color values instead
    of importing the current_theme field of this file, as this
    method updates with every change made during application runtime.

    :return: The theme currently applied by the user.
    """
    return current_theme


def __index_themes() -> dict:
    """
    A utility method used to give each theme in the cache
    an index, so that they can be ordered. Having this order
    is important for the previous_theme() and next_theme() functions
    to determine which theme actually is the next and previous one.

    :return: A dictionary built with the pattern {'theme_name':index}
    """

    index_dict = {}
    index = 0
    for theme_name in all_themes.keys():
        index_dict[index] = theme_name
        index += 1
    return index_dict
