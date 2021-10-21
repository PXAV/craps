from ui.window import Window
from ui.widget.cbutton import CrapsButton
from random import randint

first_init_dice: CrapsButton = CrapsButton(master=None)
second_init_dice: CrapsButton = CrapsButton(master=None)
result_init: CrapsButton = CrapsButton(master=None)
dice_button: CrapsButton = CrapsButton(master=None)


def __back_to_main_menu(window: Window):
    from ui.menu_views import open_main_menu
    open_main_menu(window)


def __initial_dice(window: Window):
    first = randint(1, 6)
    second = randint(1, 6)
    dice_sum = first + second

    first_init_dice.update_text(f"{first}")
    second_init_dice.update_text(f"{second}")
    result_init.update_text(f"{dice_sum}")

    if dice_sum == 7 or dice_sum == 11:
        dice_button.update_text("YOU WIN!")
    elif dice_sum == 3 or dice_sum == 3 or dice_sum == 12:
        dice_button.update_text("YOU LOSE!")
    else:
        dice_button.update_text("DRAW!")


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
