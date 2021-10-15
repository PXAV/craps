from enum import Enum


class ThemeProperty(Enum):
    PRIMARY_TEXT = 'colors.primary_text'
    SECONDARY_TEXT = 'colors.secondary_text'

    PRIMARY_BUTTON = 'colors.primary_button'
    SECONDARY_BUTTON = 'colors.secondary_button'

    @staticmethod
    def values():
        return list(map(str, ThemeProperty))
