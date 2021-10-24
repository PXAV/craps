from enum import Enum


class ThemeProperty(Enum):
    PRIMARY_BACKGROUND = "colors.primary_background"
    SECONDARY_BACKGROUND = "colors.secondary_background"

    PRIMARY_TEXT = 'colors.primary_text'
    SECONDARY_TEXT = 'colors.secondary_text'

    DICE_INDICATOR_ACTIVE = "colors.dice_indicator_active"

    PRIMARY_BUTTON = 'colors.primary_button'
    SECONDARY_BUTTON = 'colors.secondary_button'

    @staticmethod
    def values():
        return list(map(str, ThemeProperty))
