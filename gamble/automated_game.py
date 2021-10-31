from ui.window import Window
from ui.widget.cbutton import CrapsButton
from ui.widget.cdice_indicator import DiceIndicator
from gamble.game_phase import GamePhase
from random import randint
from storage.stats_database import add_game


def emulate_game(iterations: int = 1):
    for i in range(iterations):
        initial_dice_sum = __random_dice_sum()
        dice_sum = initial_dice_sum

        if dice_sum == 7 or dice_sum == 11:
            print(f"GAME FINISHED(won=True, instant=True, throws=1)")
            add_game(automated=True, won=True, instant=True, throws=1)
            continue
        if dice_sum == 2 or dice_sum == 3 or dice_sum == 12:
            print(f"GAME FINISHED(won=False, instant=True, throws=1)")
            add_game(automated=True, won=False, instant=True, throws=1)
            continue

        throws = 1
        while True:
            throws += 1
            dice_sum = __random_dice_sum()
            if dice_sum == 7:
                print(f"GAME FINISHED(won=False, instant=False, throws={throws})")
                add_game(automated=True, won=False, instant=False, throws=throws)
                break  # break out from while loop
            if dice_sum == initial_dice_sum:
                print(f"GAME FINISHED(won=True, instant=False, throws={throws})")
                add_game(automated=True, won=True, instant=False, throws=throws)
                break  # break out from while loop
        continue  # continue in the for loop and start the next game


def __random_dice_sum() -> int:
    return randint(1, 6) + randint(1, 6)


