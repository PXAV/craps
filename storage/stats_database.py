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


def add_game(automated: bool, won: bool, instant: bool, throws: int):
    global cursor

    cursor.execute(f"INSERT INTO rounds (won, instant, throws) VALUES ("
                   f"{1 if won else 0}, "
                   f"{1 if instant else 0}, "
                   f"{throws})")
    connection.commit()


def get_stats(automated: bool = False) -> dict:
    """
    Compiles a dictionary containing all statistics which are relevant for the
    statistics page accessible from the main menu. The keys will look as follows:
    "rounds_played", "rounds_won", "rounds_lost", "win_rate", "average_throws", "instant_losses", "instant_wins"

    :return:
    """
    global cursor
    query_index = 1 if automated else 0
    output = {}

    all_rounds_query = ("SELECT throws FROM rounds",
                        "SELECT throws FROM automated_rounds")
    all_rounds = cursor.execute(all_rounds_query[query_index]).fetchall()
    output["rounds_played"] = len(all_rounds)

    won_rounds_query = ("SELECT id FROM rounds WHERE won = 1",
                        "SELECT id FROM automated_rounds WHERE won = 1")
    won_rounds = cursor.execute(won_rounds_query[query_index]).fetchall()
    output["rounds_won"] = len(won_rounds)
    output["rounds_lost"] = len(all_rounds) - len(won_rounds)

    instant_losses_query = ("SELECT id FROM rounds WHERE won = 0 AND instant = 1",
                            "SELECT id FROM automated_rounds WHERE won = 0 AND instant = 1")
    instant_losses = cursor.execute(instant_losses_query[query_index]).fetchall()
    output["instant_losses"] = len(instant_losses)

    instant_wins_query = ("SELECT id FROM rounds WHERE won = 1 AND instant = 1",
                          "SELECT id FROM automated_rounds WHERE won = 1 AND instant = 1")
    instant_wins = cursor.execute(instant_wins_query[query_index]).fetchall()
    output["instant_wins"] = len(instant_wins)

    # if the player has not played so far, don't calculate statistics
    if output["rounds_played"] == 0:
        return {
            "rounds_played": 0,
            "rounds_won": 0,
            "rounds_lost": 0,
            "win_rate": 0,
            "average_throws": 0,
            "instant_losses": 0,
            "instant_wins": 0,
        }

    total_throws = 0
    for round_meta in all_rounds:
        throws: int = round_meta[0]
        total_throws += throws

    output["average_throws"] = total_throws / len(all_rounds)

    return output
