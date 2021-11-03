from ui.window import Window
from ui.widget.cbutton import CrapsButton
from ui.widget.cdice_indicator import DiceIndicator
from gamble.game_phase import GamePhase
from random import randint
from storage.stats_database import add_game

# the current game phase. Used to validate actions from every function.
game_phase = GamePhase.INITIAL_DICE

# saves the dice sum achieved on the first try
# this is used to compare it with the numbers achieved in
# draw dicing later. If the number equals this number, the
# game is won.
first_dice_sum: int = 0

# saves all widgets buttons with dynamic properties, so that they
# can be modified from other functions later.
first_init_dice: CrapsButton = CrapsButton(master=None)
second_init_dice: CrapsButton = CrapsButton(master=None)
result_init: CrapsButton = CrapsButton(master=None)
dice_button: CrapsButton = CrapsButton(master=None)

dice_indicator: DiceIndicator = DiceIndicator(master=None)


def __back_to_main_menu(window: Window):
    """
    Opens the main menu page, which will clear all widgets currently visible.

    :param window: The window to draw the main menu on.
    :return:
    """
    from ui.menu_views import open_main_menu
    open_main_menu(window)


def __initial_dice(window: Window):
    """
    Draws all inti

    :param window:
    :return:
    """
    global game_phase, first_dice_sum
    if game_phase is not GamePhase.INITIAL_DICE:
        return

    first = randint(1, 6)
    second = randint(1, 6)
    first_dice_sum = first + second

    first_init_dice.update_text(f"{first}")
    second_init_dice.update_text(f"{second}")
    result_init.update_text(f"{first_dice_sum}")

    if first_dice_sum == 7 or first_dice_sum == 11:
        game_phase = GamePhase.END_VICTORY
        add_game(automated=False, won=True, instant=True, throws=1)
        dice_button.update_text("YOU WIN!")
        __end_game(window)
    elif first_dice_sum == 2 or first_dice_sum == 3 or first_dice_sum == 12:
        dice_button.update_text("YOU LOSE!")
        game_phase = GamePhase.END_LOSS
        add_game(automated=False, won=False, instant=True, throws=1)
        __end_game(window)
    else:
        game_phase = GamePhase.DRAW_DICE
        dice_button.update_text("DRAW")
        __initial_draw(window, first_dice_sum)


def __initial_draw(window: Window, dice_sum: int):
    global dice_indicator

    dice_indicator = DiceIndicator(master=window,
                                   width=int(window.get_width() * 0.75), height=30,
                                   initial_attempts=[dice_sum], max_shown_attempts=22)
    dice_indicator.show_grid(column=0, row=3, columnspan=4, pady=10)

    repeat_dice_button = CrapsButton(master=window, width=300, height=50,
                                     text="DICE", text_type="bold", text_size=30, text_position=(100, 15),
                                     border_radius=5,
                                     callback=lambda event: __repeat_dice(window))
    repeat_dice_button.show_grid(column=0, row=4, pady=30, padx=20)


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
        add_game(automated=False, won=False, instant=False, throws=len(dice_indicator.get_attempts()))
        __end_game(window)
    elif dice_sum == first_dice_sum:
        game_phase = GamePhase.END_VICTORY
        add_game(automated=False, won=True, instant=False, throws=len(dice_indicator.get_attempts()))
        __end_game(window)


def __end_game(window: Window):
    global game_phase
    text = "ROUND WON!"
    if game_phase is GamePhase.END_LOSS:
        text = "ROUND LOST!"

    label = CrapsButton(master=window, width=250, height=50,
                        text=text, text_type="bold", text_size=30,
                        border_radius=5,
                        opaque=False,
                        callback=lambda event: __repeat_dice(window))
    label.show_grid(column=1, row=4, pady=30)

    retry_button = CrapsButton(master=window, width=300, height=50,
                               text="RETRY", text_type="bold", text_size=30, text_position=(100, 15),
                               border_radius=5,
                               primary=False,
                               callback=lambda event: start_game(window))
    retry_button.show_grid(column=0, row=5, pady=30, padx=20)

    main_menu_button = CrapsButton(master=window, width=300, height=50,
                                   text="MAIN MENU", text_type="bold", text_size=30, text_position=(50, 15),
                                   border_radius=5,
                                   primary=False,
                                   callback=lambda event: __back_to_main_menu(window))
    main_menu_button.show_grid(column=0, row=6, pady=30, padx=20)


def start_game(window: Window):
    global first_init_dice, second_init_dice, result_init, dice_button, game_phase
    game_phase = GamePhase.INITIAL_DICE

    window.clear_widgets()

    page_title = CrapsButton(master=window, width=150,
                             text="<< CRAPS", text_type="bold", text_size=26,
                             opaque=False,
                             callback=lambda event: __back_to_main_menu(window))
    page_title.show_grid(column=0, row=0, pady=20)

    first_init_dice = CrapsButton(master=window, width=100, height=80,
                                  text="?", text_type="bold", text_size=30, text_position=(30, 30),
                                  border_radius=5)
    first_init_dice.show_grid(column=0, row=1, pady=20, padx=20)

    second_init_dice = CrapsButton(master=window, width=100, height=80,
                                   text="?", text_type="bold", text_size=30, text_position=(30, 30),
                                   border_radius=5)
    second_init_dice.show_grid(column=2, row=1, pady=20, padx=20)

    CrapsButton(master=window,
                text="+", text_type="bold", text_size=30, width=30,
                opaque=False).show_grid(column=1, row=1, pady=20)

    CrapsButton(master=window,
                text="=", text_type="bold", text_size=30, width=30,
                opaque=False).show_grid(column=3, row=1, pady=20)

    result_init = CrapsButton(master=window, width=100, height=80,
                              text="?", text_type="bold", text_size=30, text_position=(30, 30),
                              border_radius=15)
    result_init.show_grid(column=4, row=1, pady=20, padx=20)

    dice_button = CrapsButton(master=window, width=100 * 3, height=80,
                              text="DICE!", text_size=20,
                              callback=lambda event: __initial_dice(window))
    dice_button.show_grid(column=0, columnspan=2, row=2, pady=10, padx=20)

    window.update()
