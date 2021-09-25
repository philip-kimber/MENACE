import menace_commons as commons

import random


def winning_move(board, player=2):
    # Returns colour map value for square in board where given player
    # (as in player param, 1=X, 2=O) should move in order to win, otherwise returns -1 if cannot win
    for wp in commons.WIN_POSITIONS:
        key = [board[s] for s in wp]
        if key.count(player) == 2 and key.count(0) == 1: # Can win
            return commons.COLOUR_MAP[wp[key.index(0)]]
    return -1

def opponent_random(board):
    # Simulation player that just picks a random free square
    weights = [1 if s == 0 else 0 for s in board]
    return random.choices(commons.COLOUR_MAP[0:9], weights=weights, k=1)[0]

def opponent_basic(board):
    # Simulation player that wins if it can, otherwise just picks a random square
    wm = winning_move(board, 2)
    if wm != -1:
        return wm
    return opponent_random(board)

# TODO perfect game opponent
    
