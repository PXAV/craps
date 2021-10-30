from ui.window import Window
from ui.widget.cbutton import CrapsButton
from storage.stats_database import get_stats


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

    win_rate = 0.0
    if stats['rounds_played'] > 0:
        win_rate = stats['rounds_won'] / (stats["rounds_won"] + stats["rounds_lost"]) * 100

    __multiline_text(window, [
        f"Rounds played: {stats['rounds_played']}",
        f"  ➥ Won: {stats['rounds_won']}",
        f"  ➥ Lost: {stats['rounds_lost']}",
        f"  ➥ Win rate: {format(win_rate, '.1f')}%",
        f"Instant wins: {stats['instant_wins']}",
        f"Instant losses: {stats['instant_losses']}",
        f"Average throws/round: {format(stats['average_throws'], '.1f')}",
    ], column=1, start_row=1)

    back_button = CrapsButton(master=window, width=300, height=40,
                              text="Done",
                              callback=lambda event: open_main_menu(window))
    back_button.show_grid(column=1, row=9,
                          padx=(window.get_width() / 20, 0),
                          pady=(0, window.get_height() / 8))

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
