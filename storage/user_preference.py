from enum import Enum


class UserPreference(Enum):
    THEME = 'settings.theme'

    @staticmethod
    def values():
        return list(map(str, UserPreference))
