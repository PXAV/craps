from enum import Enum


class UserPreference(Enum):
    THEME = 'theme'

    @staticmethod
    def values():
        return list(map(str, UserPreference))
