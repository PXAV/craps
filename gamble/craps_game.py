from ui.window import Window
from ui.widget.cbutton import CrapsButton
from ui.widget.cdice_indicator import DiceIndicator
from gamble.game_phase import GamePhase
from random import randint

game_phase = GamePhase.INITIAL_DICE
first_dice_sum: int = 0

first_init_dice: CrapsButton = CrapsButton(master=None)
second_init_dice: CrapsButton = CrapsButton(master=None)
result_init: CrapsButton = CrapsButton(master=None)
dice_button: CrapsButton = CrapsButton(master=None)

dice_indicator: DiceIndicator = DiceIndicator(master=None)


def __back_to_main_menu(window: Window):
    from ui.menu_views import open_main_menu
    open_main_menu(window)


def __initial_dice(window: Window):
    global game_phase, first_dice_sum
    if game_phase is not GamePhase.INITIAL_DICE:
        return

    first = randint(1, 6)
    second = randint(1, 6)
    first_dice_sum = first + second

    first_init_dice.update_text(f"{first}")
    second_init_dice.update_text(f"{second}")
    result_init.update_text(f"{first_dice_sum}")

    # if dice_sum == 7 or dice_sum == 11:
    #     game_phase = GamePhase.END_VICTORY
    #     dice_button.update_text("YOU WIN!")
    # elif dice_sum == 3 or dice_sum == 3 or dice_sum == 12:
    #     dice_button.update_text("YOU LOSE!")
    #     game_phase = GamePhase.END_LOSS
    # else:
    game_phase = GamePhase.DRAW_DICE
    dice_button.update_text("DRAW!")
    __initial_draw(window, first_dice_sum)


def __initial_draw(window: Window, dice_sum: int):
    global dice_indicator

    indicator_width = first_init_dice.get_width() + second_init_dice.get_width() + result_init.get_width()

    dice_indicator = DiceIndicator(master=window,
                                   width=int(indicator_width * 3), height=30,
                                   initial_attempts=[dice_sum], max_shown_attempts=22)
    dice_indicator.show_grid(column=0, row=3, columnspan=5, padx=20)

    repeat_dice_button = CrapsButton(master=window, width=300, height=50,
                                     text="DICE", text_type="bold", text_size=30, text_position=(30, 30),
                                     border_radius=5,
                                     callback=lambda event: __repeat_dice(window))
    repeat_dice_button.show_grid(column=0, row=5, pady=20)


def __repeat_dice(window: Window):
    global dice_indicator, game_phase, first_dice_sum
    if game_phase is not GamePhase.DRAW_DICE:
        return

    first = randint(1, 6)
    second = randint(1, 6)
    dice_sum = first + second

    dice_indicator.add_attempt(dice_sum)

    if dice_sum == 7:
        game_phase = GamePhase.END_LOSS
    elif dice_sum == first_dice_sum:
        game_phase = GamePhase.END_VICTORY


def start_game(window: Window):
    global first_init_dice, second_init_dice, result_init, dice_button

    window.clear_widgets()

    page_title = CrapsButton(master=window, width=300,
                             text="CRAPS", text_type="bold", text_size=26,
                             opaque=False,
                             callback=lambda event: __back_to_main_menu(window))
    page_title.show_grid(column=0, row=0, pady=20)

    first_init_dice = CrapsButton(master=window, width=80, height=80,
                                  text="?", text_type="bold", text_size=30, text_position=(30, 30),
                                  border_radius=5)
    first_init_dice.show_grid(column=0, row=1, pady=20)

    second_init_dice = CrapsButton(master=window, width=80, height=80,
                                   text="?", text_type="bold", text_size=30, text_position=(30, 30),
                                   border_radius=5)
    second_init_dice.show_grid(column=2, row=1, pady=20)

    CrapsButton(master=window,
                text="+", text_type="bold", text_size=30,
                opaque=False).show_grid(column=1, row=1, pady=20)

    CrapsButton(master=window,
                text="=", text_type="bold", text_size=30,
                opaque=False).show_grid(column=3, row=1, pady=20)

    result_init = CrapsButton(master=window, width=150, height=80,
                              text="?", text_type="bold", text_size=30, text_position=(30, 30),
                              border_radius=15)
    result_init.show_grid(column=4, row=1, pady=20)

    dice_button = CrapsButton(master=window, width=200, height=40,
                              text="DICE!", text_size=20,
                              callback=lambda event: __initial_dice(window))
    dice_button.show_grid(column=2, row=2, pady=10)

    window.update()
