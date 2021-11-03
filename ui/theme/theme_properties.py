from enum import Enum


class ThemeProperty(Enum):
    """
    This enum contains all possible color values a theme can have.
    You can use this enum to get colors with the get_color(...) method
    of the Theme class.
    """

    PRIMARY_BACKGROUND = "colors.primary_background"
    SECONDARY_BACKGROUND = "colors.secondary_background"

    PRIMARY_TEXT = 'colors.primary_text'
    SECONDARY_TEXT = 'colors.secondary_text'

    DICE_INDICATOR_ACTIVE = "colors.dice_indicator_active"

    PRIMARY_BUTTON = 'colors.primary_button'
    SECONDARY_BUTTON = 'colors.secondary_button'

    @staticmethod
    def values():
        """
        Compiles a list of all possible settings the user can
        configure.

        :return: A list of all enum states in the current class.
        """
        return list(map(str, ThemeProperty))
