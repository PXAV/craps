"""
This file contains functions, which display the
"""

from tkinter import Frame
from ui.theme.theme_repository import get_current_theme, next_theme, previous_theme
from ui.theme.theme_properties import ThemeProperty
from ui.window import Window
from ui.widget.cbutton import CrapsButton
from storage.stats_database import get_stats
from gamble.automated_game import emulate_game_async


def open_main_menu(window: Window):
    """
    Draws the main menu widgets to the given window.

    :param window: The window to draw the main menu widgets to.
    """
    import gamble.user_game
    window.clear_widgets()
    window.reset_custom_grid()

    title_label = CrapsButton(master=window, width=300, height=40,
                              text="CRAPS", text_type="bold", text_size=26,
                              opaque=False)
    title_label.show_grid(column=1, row=0, columnspan=2, pady=((window.get_height() / 8), 0))

    play_button = CrapsButton(master=window, width=300, height=40,
                              text="PLAY!",
                              callback=lambda event: gamble.user_game.start_game(window))
    play_button.show_grid(column=1, row=1, columnspan=2, pady=(20, 10), padx=(40, 0))

    stats_button = CrapsButton(master=window, width=300, height=40,
                               text="STATISTICS",
                               callback=lambda event: open_statistics_page(window))
    stats_button.show_grid(column=1, row=2, columnspan=2, pady=10, padx=(40, 0))

    rules_button = CrapsButton(master=window, width=300, height=40,
                               text="RULES",
                               callback=lambda event: open_rules_menu(window))
    rules_button.show_grid(column=1, row=3, columnspan=2, pady=10, padx=(40, 0))

    settings_button = CrapsButton(master=window, width=300, height=40,
                                  text="SETTINGS",
                                  callback=lambda event: open_settings_menu(window))
    settings_button.show_grid(column=1, row=4, columnspan=2, pady=10, padx=(40, 0))

    quit_button = CrapsButton(master=window, width=300, height=40,
                              text="QUIT",
                              primary=False,
                              callback=lambda event: exit(0))
    quit_button.show_grid(column=1, row=5, columnspan=2, pady=10, padx=(40, 0))

    window.update()


def open_rules_menu(window: Window):
    """
    Opens the rule page on the current window.
    :param window: The window to open the rules menu on.
    """
    window.clear_widgets()

    title_label = CrapsButton(master=window, width=300, height=40,
                              text="RULES", text_type="bold", text_size=26,
                              opaque=False)
    title_label.show_grid(column=1, row=0, columnspan=2, pady=((window.get_height() / 8), 0))

    __multiline_text(window, [
        "You start with two dices",
        " - If their sum is 7 or 11, you win",
        " - If their sum is 2, 3 or 12, you lose",
        "For any other case, you will throw the dice infinitely, till",
        "1. The sum is equal to 7: You lose",
        "2. The sum is equal to your first sum: You win",
    ], column=1, start_row=1)

    back_button = CrapsButton(master=window, width=300, height=40,
                              text="Understood",
                              callback=lambda event: open_main_menu(window))
    back_button.show_grid(column=1, row=9,
                          padx=(window.get_width() / 20, 0),
                          pady=(0, window.get_height() / 8))

    window.update()


def open_statistics_page(window: Window):
    """
    Opens the statistics page to the given window.

    :param window: The window to open the page on.
    """
    window.clear_widgets()

    title_label = CrapsButton(master=window, width=300, height=40,
                              text="STATISTICS", text_type="bold", text_size=26,
                              opaque=False)
    title_label.show_grid(column=1, row=0, columnspan=2, pady=((window.get_height() / 8), 0))

    stats = get_stats()
    automated_stats = get_stats(automated=True)

    win_rate = 0.0
    if stats['rounds_played'] > 0:
        win_rate = stats['rounds_won'] / (stats["rounds_won"] + stats["rounds_lost"]) * 100

    computer_win_rate = 0.0
    if automated_stats['rounds_played'] > 0:
        computer_win_rate = automated_stats['rounds_won'] / (automated_stats["rounds_won"]
                                                             + automated_stats["rounds_lost"]) * 100

    __multiline_text(window, [
        f"Your statistics (computer's statistics)",
        f"Rounds played: {stats['rounds_played']} ({automated_stats['rounds_played']})",
        f"  ➥ Won: {stats['rounds_won']} ({automated_stats['rounds_won']})",
        f"  ➥ Lost: {stats['rounds_lost']} ({automated_stats['rounds_lost']})",
        f"  ➥ Win rate: {format(win_rate, '.1f')}% ({format(computer_win_rate, '.1f')}%)",
        f"Instant wins: {stats['instant_wins']} ({automated_stats['instant_wins']})",
        f"Instant losses: {stats['instant_losses']} ({automated_stats['instant_losses']})",
        f"Average throws/round: {format(stats['average_throws'], '.1f')} ({format(automated_stats['average_throws'], '.1f')})",
        f"",
        f"Note: The computer's statistics are gained from automated games",
    ], column=1, start_row=1)

    refresh_button = CrapsButton(master=window, width=300, height=40,
                                 text="Refresh Statistics",
                                 primary=False,
                                 callback=lambda event: open_statistics_page(window))
    refresh_button.show_grid(column=1, row=11)

    frame = Frame(master=window, width=500, height=40,
                  background=get_current_theme().get_color(ThemeProperty.PRIMARY_BACKGROUND))

    CrapsButton(master=frame, width=300, height=40,
                text="Let computer play some rounds:",
                opaque=False).show_grid(column=0, row=1, padx=10)

    CrapsButton(master=frame, width=80, height=40,
                text="1",
                callback=lambda event: emulate_game_async(1)).show_grid(column=1, row=1, padx=10)
    CrapsButton(master=frame, width=80, height=40,
                text="10",
                callback=lambda event: emulate_game_async(10)).show_grid(column=2, row=1, padx=10)
    CrapsButton(master=frame, width=80, height=40,
                text="100",
                callback=lambda event: emulate_game_async(100)).show_grid(column=3, row=1, padx=10)
    CrapsButton(master=frame, width=80, height=40,
                text="1000",
                callback=lambda event: emulate_game_async(1000)).show_grid(column=4, row=1, padx=10)

    frame.grid(column=0, row=12, columnspan=3, pady=20)

    back_button = CrapsButton(master=window, width=300, height=40,
                              text="<< BACK",
                              text_type="bold",
                              callback=lambda event: open_main_menu(window))
    back_button.show_grid(column=0, row=14, pady=20, padx=20)

    window.update()


def open_settings_menu(window: Window):
    """
    Opens the settings menu to the given window.

    :param window: The window to open the statistics page to.
    """
    window.clear_widgets()
    window.config(background=get_current_theme().get_color(ThemeProperty.PRIMARY_BACKGROUND))

    CrapsButton(master=window,
                height=40, width=200,
                text_size=24,
                text_type="bold",
                opaque=False,
                text="Settings").show_grid(column=0, row=0)
    CrapsButton(master=window,
                height=40, width=200,
                text_size=24,
                text_type="bold",
                opaque=False,
                text="UI Theme").show_grid(column=0, row=1)

    theme_changer_frame = Frame(master=window, width=700, height=50,
                                background=get_current_theme().get_color(ThemeProperty.PRIMARY_BACKGROUND))

    previous_theme_button = CrapsButton(master=theme_changer_frame,
                                        height=40, width=50,
                                        text_size=24,
                                        text_type="bold",
                                        text_position=(20, 10),
                                        text="<",
                                        callback=lambda event: previous_theme(window, theme_button))
    previous_theme_button.show_grid(column=0, row=0)

    theme_button = CrapsButton(master=theme_changer_frame,
                               height=40, width=300,
                               text_size=24,
                               text_type="bold",
                               text_position=(25, 10),
                               primary=False,
                               text=get_current_theme().name)
    theme_button.show_grid(column=1, row=0, padx=10)

    next_theme_button = CrapsButton(master=theme_changer_frame,
                                    height=40, width=50,
                                    text_size=24,
                                    text_type="bold",
                                    text_position=(20, 10),
                                    text=">",
                                    callback=lambda event: next_theme(window, theme_button))
    next_theme_button.show_grid(column=2, row=0)

    theme_changer_frame.grid(column=0, columnspan=3, row=2, padx=20)

    back_button = CrapsButton(master=window, width=300, height=40,
                              text="BACK",
                              callback=lambda event: open_main_menu(window))
    back_button.show_grid(column=0, row=9,
                          padx=20,
                          pady=20)

    window.update()


def __multiline_text(window: Window, text_lines: list, column: int = 1, start_row: int = 1):
    """
    Draws a multi-lined text on the given window.

    :param window:      The window to draw the text on.
    :param text_lines:  The actual text to draw. Each list item represents a new line.
    :param column:      The column to display the text in.
    :param start_row:   From which row to start drawing from. The row index is incremented by one with each line.
    """
    index = 0
    for line in text_lines:
        CrapsButton(master=window,
                    height=33, width=int(window.get_width() / 2),
                    text_size=16,
                    text_type="normal",
                    opaque=False,
                    text=line).show_grid(column=column, row=start_row + index)
        index += 1
