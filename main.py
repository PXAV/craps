from ui.window import Window

from storage.user_preferences import load_preferences
from ui.theme.theme_repository import load_all_themes

if __name__ == '__main__':
    load_all_themes()
    load_preferences()

    main_window = Window()
    main_window.open()
