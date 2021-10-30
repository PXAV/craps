import sqlite3
from configuration import stats_database

cursor: sqlite3.Cursor
connection: sqlite3.Connection


def connect_database():
    global cursor, connection

    connection = sqlite3.connect(stats_database)
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS rounds ("
                   "id INTEGER PRIMARY KEY, "
                   "won INT NOT NULL, "
                   "instant INT NOT NULL,"
                   "throws INT NOT NULL)")

    cursor.execute("CREATE TABLE IF NOT EXISTS automated_rounds ("
                   "id INT PRIMARY KEY, "
                   "won INT NOT NULL, "
                   "instant INT NOT NULL,"
                   "throws INT NOT NULL)")

    connection.commit()


def add_game(won: bool, instant: bool, throws: int):
    global cursor

    cursor.execute(f"INSERT INTO rounds (won, instant, throws) VALUES ("
                   f"{1 if won else 0}, "
                   f"{1 if instant else 0}, "
                   f"{throws})")
    connection.commit()


def get_stats() -> dict:
    """
    Compiles a dictionary containing all statistics which are relevant for the
    statistics page accessible from the main menu. The keys will look as follows:
    "rounds_played", "rounds_won", "rounds_lost", "win_rate", "average_throws", "instant_losses", "instant_wins"

    :return:
    """
    global cursor
    output = {}

    all_rounds = cursor.execute("SELECT throws FROM rounds").fetchall()
    output["rounds_played"] = len(all_rounds)

    won_rounds = cursor.execute("SELECT id FROM rounds WHERE won = 1").fetchall()
    output["rounds_won"] = len(won_rounds)
    output["rounds_lost"] = len(all_rounds) - len(won_rounds)

    instant_losses = cursor.execute("SELECT id FROM rounds WHERE won = 0 AND instant = 1").fetchall()
    output["instant_losses"] = len(instant_losses)

    instant_wins = cursor.execute("SELECT id FROM rounds WHERE won = 1 AND instant = 1").fetchall()
    output["instant_wins"] = len(instant_wins)

    # if the player has not played so far, don't calculate statistics
    if output["rounds_played"] == 0:
        return {}

    total_throws = 0
    for round_meta in all_rounds:
        throws: int = round_meta[0]
        total_throws += throws

    output["average_throws"] = total_throws / len(all_rounds)

    return output
