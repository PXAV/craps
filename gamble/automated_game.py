"""
One task of the project was to analyze which of the parties wins most with the game
in the long-term: the casino or the player? To find that out in an experiment-based way,
you can use this file to run a given amount of automated games and write the resulting data
to a dedicated table in the database. The data produced by this file can be seen in the
Statistics page.
"""

from random import randint
from storage.stats_database import DatabaseConnection, add_game
from threading import Thread


class EmulatorThread(Thread):
    """
    The EmulatorThread class is a custom thread implementation used to
    queue game emulations in an async thread to avoid blocking the UI main
    thread, which would make the UI unresponsive for the time the game emulation
    is running.

    To run the game, simply pass the amount of rounds in the constructor and
    call the start() method.
    """

    def __init__(self, iterations: int):
        """
        Constructs a new emulator thread with a given amount of iterations.
        This does not yet start the thread. Call the start() method for this.

        :param iterations: How many rounds should be played by the computer
        """
        super().__init__()
        self.iterations = iterations

    def run(self):
        """
        Overrides the default run() method of the thread class, which normally
        simply calls the target method passed in the constructor arguments. When
        using an EmulatorThread, there is no need to pass the target method in
        the constructor.

        :return:
        """
        emulate_game(iterations=self.iterations, use_default_db=False)


def emulate_game_async(iterations: int = 1):
    """
    Starts an asynchronous emulation of x craps rounds and writes the resulting
    statistics to the database.

    :param iterations: The amount of rounds the computer should play
    :return:
    """
    EmulatorThread(iterations).start()


def emulate_game(iterations: int = 1, use_default_db: bool = True):
    """
    Starts a synchronous emulation of x rounds of craps games and writes the
    results to the database.

    :param iterations:      The amount of rounds to play by the computer
    :param use_default_db:  True if this function is run from the main thread and the
                            normal database connection data can be used, False is this is
                            run from an async thread and a new connection has to be established.
    :return:
    """

    # if this method is called from an async thread, initialize a new database
    # connection in the current thread, as we cannot access connection objects
    # created from other threads.
    database: DatabaseConnection
    if not use_default_db:
        database = DatabaseConnection()

    def add_game_safe(won: bool, instant: bool, total_throws: int):
        """
        This method checks if the game is run from the main thread or async thread and
        uses the correct database instance accordingly. The sqlite3 package of python is
        not thread-safe and does therefore not allow you to access the same connection and
        cursor instance from different threads. The game therefore keeps one default instance
        for both of those objects in the memory in case the statistics are added from
        the main thread, but has the ability to dynamically create new connections to the
        DB in case the stats are added from a different thread.

        :param won:             Whether the computer has won the game.
        :param instant:         Whether the game was won instantly (no draw on first dice)
        :param total_throws:    How often the computer has thrown the dice
        :return:
        """

        # if run from the main thread, use static connection objects
        if use_default_db:
            add_game(True, won, instant, total_throws)

        # if not, use the newly created instance
        else:
            database.add_game(True, won, instant, total_throws)

    for i in range(iterations):
        initial_dice_sum = __random_dice_sum()
        dice_sum = initial_dice_sum

        # check if the game is won or lost instantly. If so, continue immediately
        # to avoid entering the while loop.
        if dice_sum == 7 or dice_sum == 11:
            print("GAME FINISHED(won=True, instant=True, throws=1)")
            add_game_safe(won=True, instant=True, total_throws=1)
            continue
        if dice_sum == 2 or dice_sum == 3 or dice_sum == 12:
            print("GAME FINISHED(won=False, instant=True, throws=1)")
            add_game_safe(won=False, instant=True, total_throws=1)
            continue

        # when there was a draw on the first throw, enter an infinite while
        # loop that can only be ended when the player dices a 7 or his initial dice
        # sum.
        throws = 1
        while True:
            throws += 1
            dice_sum = __random_dice_sum()
            if dice_sum == 7:
                print(f"GAME FINISHED(won=False, instant=False, throws={throws})")
                add_game_safe(won=False, instant=False, total_throws=throws)
                break  # break out from while loop
            if dice_sum == initial_dice_sum:
                print(f"GAME FINISHED(won=True, instant=False, throws={throws})")
                add_game_safe(won=True, instant=False, total_throws=throws)
                break  # break out from while loop
        continue  # continue in the for loop and start the next game


def __random_dice_sum() -> int:
    """
    Generates a random dice sum from two dices with 6 sides.
    So the maximum number returned by this method is 12, while
    2 is the minimum.

    :return: A random number from 2 to 12.
    """
    return randint(2, 12)


