import tkinter

from ui.window import Window
from storage.user_preferences import load_preferences
from ui.theme.theme_repository import load_all_themes
from ui.widget.cbutton import CrapsButton
from tkinter import Frame
from ui.theme.theme_repository import current_theme, all_themes
from ui.theme.theme_properties import ThemeProperty
from tkinter import SW


def open_main_menu(window: Window):
    import gamble.craps_game
    window.clear_widgets()
    window.reset_custom_grid()

    title_label = CrapsButton(master=window, width=300, height=40,
                              text="CRAPS", text_type="bold", text_size=26,
                              opaque=False)
    title_label.show_grid(column=1, row=0, columnspan=2, pady=((window.get_height() / 8), 0))

    play_button = CrapsButton(master=window, width=300, height=40,
                              text="PLAY!",
                              callback=lambda event: gamble.craps_game.start_game(window))
    play_button.show_grid(column=1, row=1, columnspan=2, pady=(20, 10), padx=(40, 0))

    stats_button = CrapsButton(master=window, width=300, height=40,
                               text="STATISTICS")
    stats_button.show_grid(column=1, row=2, columnspan=2, pady=10, padx=(40, 0))

    rules_button = CrapsButton(master=window, width=300, height=40,
                               text="RULES")
    rules_button.show_grid(column=1, row=3, columnspan=2, pady=10, padx=(40, 0))

    settings_button = CrapsButton(master=window, width=300, height=40,
                                  text="SETTINGS",
                                  callback=lambda event: open_settings_menu(window))
    settings_button.show_grid(column=1, row=4, columnspan=2, pady=10, padx=(40, 0))

    quit_button = CrapsButton(master=window, width=300, height=40,
                              text="QUIT",
                              callback=lambda event: exit(0))
    quit_button.show_grid(column=1, row=5, columnspan=2, pady=10, padx=(40, 0))

    window.update()


def open_settings_menu(window: Window):
    window.clear_widgets()

    window.configure_grid(10)

    CrapsButton(master=window,
                height=40, width=200,
                text_size=24,
                text_type="bold",
                opaque=True,
                text="UI THEME").show_grid(column=1, row=0)

    back_button = CrapsButton(master=window, width=300, height=40,
                              text="BACK",
                              callback=lambda event: open_main_menu(window))
    back_button.show_grid(column=1, row=9,
                          padx=(window.get_width() / 20, 0),
                          pady=(0, window.get_height() / 12))

    window.update()
