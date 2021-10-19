from ui.window import Window

from storage.user_preferences import load_preferences
from ui.theme.theme_repository import load_all_themes
from ui.menu_views import open_main_menu


if __name__ == '__main__':
    load_all_themes()
    load_preferences()

    main_window = Window(screen_name="Craps")

    open_main_menu(main_window)

    main_window.open()
