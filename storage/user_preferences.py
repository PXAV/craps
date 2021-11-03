"""
This file is used to access and manipulate user preferences
"""

import toml
import darkdetect
import configuration
from storage.user_preference import UserPreference
from ui.theme.theme_repository import all_themes, set_current_theme

# saves all preferences during application runtime for
# faster execution speeds and reduced disk load.
# If there is a loading error, the app will used the
# default settings defined below:
preferences = {
    UserPreference.THEME: "auto"
}


def get_preference(key: UserPreference) -> any:
    """
    Gets the given preference from the cache. If any external
    file depends on a preference, you should use this function
    instead of importing the preferences dictionary, because the
    preferences dictionary won't be updated with the latest settings
    after the app has been initialized for the first time, while
    this method always provides the latest state.

    :param key: The user preference type you want to get (theme, ...?)
    :return: The value of the requested preference. May be any data type.
    """
    return preferences.get(UserPreference[key])


def set_preference(key: UserPreference, value):
    """
    Updates the given preference to the given value. This methods updates
    the value in the cache as well as the file, so that the change persists
    over application restarts.

    :param key:     The preference type you want to change (theme, ...)
    :param value:   The value to set the preference to. Please make sure to
                    use the correct datatype here as the value parameter is
                    not safely typed for flexibility reasons.
    """
    preferences[key] = value

    # convert preferences dictionary to a string-only
    # dictionary which can be dumped by the TOML parser
    writable_preferences = {}
    for key in preferences.keys():
        writable_preferences[key.name] = preferences[key]

    # actually dump changes made in the cache to preference file
    with open(configuration.preference_file, "w") as file:
        toml.dump(writable_preferences, file)


def load_preferences():
    """
    Loads all preferences from the TOML configuration file and saves
    them into the cache. This should be done on every application startup.
    """

    with open(configuration.preference_file, "r") as file:
        data = toml.loads(file.read())

    # get the ui theme chosen by the user
    preferences[UserPreference.THEME] = data.get(UserPreference.THEME.name)

    # if the theme does not exist / is not loaded, the app will fall back to
    # auto-mode. Auto mode means that either the default dark or light theme
    # will be chosen depending on the OS settings
    if preferences[UserPreference.THEME] not in all_themes:
        preferences[UserPreference.THEME] = "auto"

    # use 'darkdetect' library to check the OS preference for dark or light mode
    # note that only windows, macOS and some Linux distributions support this feature.
    # KDE linux based desktop environments handle themes differently.
    if preferences[UserPreference.THEME] == "auto":
        preferences[UserPreference.THEME] = "Craps Dark" if darkdetect.isDark() else "Craps Light"

    # finally apply the selected theme
    set_current_theme(preferences[UserPreference.THEME])
