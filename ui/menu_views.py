import tkinter

from ui.window import Window
from storage.user_preferences import load_preferences
from ui.theme.theme_repository import load_all_themes
from ui.widget.cbutton import CrapsButton
from tkinter import Frame
from ui.theme.theme_repository import current_theme
from ui.theme.theme_properties import ThemeProperty


def open_main_menu(window: Window):
    window.clear_widgets()

    play_button = CrapsButton(master=window,width=300, height=40,
                              text="PLAY!",
                              callback=lambda event: print("clicked"))
    play_button.show_grid(column=1, row=0, columnspan=2, pady=(20, 10), padx=(40, 0))

    stats_button = CrapsButton(master=window, width=300, height=40,
                               text="STATISTICS")
    stats_button.show_grid(column=1, row=1, columnspan=2, pady=10, padx=(40, 0))

    settings_button = CrapsButton(master=window, width=300, height=40,
                                  text="SETTINGS",
                                  callback=lambda event: open_settings_menu(window))
    settings_button.show_grid(column=1, row=2, columnspan=2, pady=10, padx=(40, 0))

    quit_button = CrapsButton(master=window, width=300, height=40,
                              text="QUIT",
                              callback=lambda event: exit(0))
    quit_button.show_grid(column=1, row=3, columnspan=2, pady=10, padx=(40, 0))


def open_settings_menu(window: Window):
    window.clear_widgets()

    window.update()
