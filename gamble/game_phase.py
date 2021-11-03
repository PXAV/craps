from enum import IntEnum


class GamePhase(IntEnum):
    """
    This enum is used to describe which phase the player is currently in
    while playing the game. This is useful to handle and validate actions
    between the UI components, however it is not used for the automated
    games.
    """

    # The player is dicing for the first time in the round
    INITIAL_DICE = 1,

    # The player has thrown a draw in the first dice and is
    # now dicing till he gets a 7 or his initial result.
    DRAW_DICE = 2,

    # The game has ended, the player won.
    END_VICTORY = 3,

    # The game has ended, the player lost.
    END_LOSS = 4
