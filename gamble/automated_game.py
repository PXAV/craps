from random import randint
from storage.stats_database import DatabaseConnection, add_game
from threading import Thread


class EmulatorThread(Thread):
    def __init__(self, iterations: int):
        super().__init__()
        self.iterations = iterations

    def run(self):
        emulate_game(iterations=self.iterations, use_default_db=False)


def emulate_game_async(iterations: int = 1):
    EmulatorThread(iterations).start()


def emulate_game(iterations: int = 1, use_default_db: bool = True):
    database: DatabaseConnection
    if not use_default_db:
        database = DatabaseConnection()

    def add_game_safe(automated: bool, won: bool, instant: bool, total_throws: int):
        if use_default_db:
            add_game(automated, won, instant, total_throws)
        else:
            database.add_game(automated, won, instant, total_throws)

    for i in range(iterations):
        initial_dice_sum = __random_dice_sum()
        dice_sum = initial_dice_sum

        if dice_sum == 7 or dice_sum == 11:
            print("GAME FINISHED(won=True, instant=True, throws=1)")
            add_game_safe(automated=True, won=True, instant=True, total_throws=1)
            continue
        if dice_sum == 2 or dice_sum == 3 or dice_sum == 12:
            print("GAME FINISHED(won=False, instant=True, throws=1)")
            add_game_safe(automated=True, won=False, instant=True, total_throws=1)
            continue

        throws = 1
        while True:
            throws += 1
            dice_sum = __random_dice_sum()
            if dice_sum == 7:
                print(f"GAME FINISHED(won=False, instant=False, throws={throws})")
                add_game_safe(automated=True, won=False, instant=False, total_throws=throws)
                break  # break out from while loop
            if dice_sum == initial_dice_sum:
                print(f"GAME FINISHED(won=True, instant=False, throws={throws})")
                add_game_safe(automated=True, won=True, instant=False, total_throws=throws)
                break  # break out from while loop
        continue  # continue in the for loop and start the next game


def __random_dice_sum() -> int:
    return randint(1, 6) + randint(1, 6)


