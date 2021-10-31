import toml
import darkdetect
import configuration
from storage.user_preference import UserPreference
from ui.theme.theme_repository import all_themes, set_current_theme

preferences = {
    UserPreference.THEME: "auto"
}


def get_preference(key: UserPreference):
    return preferences.get(UserPreference[key])


def load_preferences():
    with open(configuration.preference_file, "r") as file:
        data = toml.loads(file.read())

    # get the ui theme chosen by the user
    preferences[UserPreference.THEME] = data.get("settings").get("theme")

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
