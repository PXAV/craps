from enum import Enum


class UserPreference(Enum):
    """
    This enum class saves all settings, which can be configured by
    the user in the main menu's settings page. This is used to avoid
    hard-coded preference paths in the source code. If the path in the
    TOML file changes, it's enough to modify the enum value here and
    the rest of the code will adjust.
    """

    THEME = 'theme'

    @staticmethod
    def values() -> list:
        """
        Compiles a list of all possible settings the user can
        configure.

        :return: A list of all enum states in the current class.
        """
        return list(map(str, UserPreference))
