from tkinter import Frame
from ui.theme.theme_repository import get_current_theme
from ui.theme.theme_properties import ThemeProperty
from ui.window import Window
from ui.widget.cbutton import CrapsButton
from storage.stats_database import get_stats
from gamble.automated_game import emulate_game


def open_main_menu(window: Window):
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
        f"Average throws/round: {format(stats['average_throws'], '.1f')} ({automated_stats['average_throws']})",
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
                opaque=False,
                callback=lambda event: open_main_menu(window)).show_grid(column=0, row=1, padx=10)

    CrapsButton(master=frame, width=80, height=40,
                text="1",
                callback=lambda event: emulate_game(1)).show_grid(column=1, row=1, padx=10)
    CrapsButton(master=frame, width=80, height=40,
                text="10",
                callback=lambda event: emulate_game(10)).show_grid(column=2, row=1, padx=10)
    CrapsButton(master=frame, width=80, height=40,
                text="100",
                callback=lambda event: emulate_game(100)).show_grid(column=3, row=1, padx=10)
    CrapsButton(master=frame, width=80, height=40,
                text="1000",
                callback=lambda event: emulate_game(1000)).show_grid(column=4, row=1, padx=10)

    frame.grid(column=0, row=12, columnspan=3, pady=20)

    back_button = CrapsButton(master=window, width=300, height=40,
                              text="<< BACK",
                              text_type="bold",
                              callback=lambda event: open_main_menu(window))
    back_button.show_grid(column=0, row=14, pady=20, padx=20)

    window.update()


def open_settings_menu(window: Window):
    window.clear_widgets()

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


def __multiline_text(window: Window, text_lines: list, column: int = 1, start_row: int = 1):
    index = 0
    for line in text_lines:
        CrapsButton(master=window,
                    height=33, width=int(window.get_width() / 2),
                    text_size=16,
                    text_type="normal",
                    opaque=False,
                    text=line).show_grid(column=column, row=start_row + index)
        index += 1
