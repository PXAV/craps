from enum import IntEnum


class GamePhase(IntEnum):
    INITIAL_DICE = 1,
    DRAW_DICE = 2,
    END_VICTORY = 3,
    END_LOSS = 4
