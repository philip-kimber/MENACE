import menace_commons as commons

import random


def winning_move(board, config, player=2):
    # Returns colour map value for square in board where given player
    # (as in player param, 1=X, 2=O) should move in order to win, otherwise returns -1 if cannot win
    for wp in commons.WIN_POSITIONS:
        key = [board[s] for s in wp]
        if key.count(player) == 2 and key.count(0) == 1: # Can win
            return config.COLOUR_MAP[wp[key.index(0)]]
    return -1

def opponent_random(board, config):
    # Simulation player that just picks a random free square
    weights = [1 if s == 0 else 0 for s in board]
    return random.choices(config.COLOUR_MAP[0:9], weights=weights, k=1)[0]

def opponent_basic(board, config):
    # Simulation player that wins if it can, otherwise just picks a random square
    wm = winning_move(board, config, 2)
    if wm != -1:
        return wm
    return opponent_random(board, config)

def opponent_intermediate(board, config):
    # Simulation player that wins if it can, blocks if it must, otherwise random
    my_wm = winning_move(board, config, 2)
    if my_wm != -1: return my_wm
    op_wm = winning_move(board, config, 1)
    if op_wm != -1: return op_wm
    return opponent_random(board, config)

def opponent_perfect(board, config):
    # Simulation player that always plays a perfect game
    if board.count(0) == 8: # First move: go for centre if possible, else a corner
        if board[4] == 0: return config.COLOUR_MAP[4]
        else: return random.choices(config.COLOUR_MAP[0:9], weights=[1,0,1,0,0,0,1,0,1], k=1)[0]
    elif board.count(0) == 6: # Second move
        # Block if opponent can win
        op_wm = winning_move(board, config, 1)
        if op_wm != -1: return op_wm
        # If we have the centre, go for an edge that is not opposite an opponent square
        if board[4] == 2:
            out = random.choices(config.COLOUR_MAP[0:9],
                                  weights=[sq if board[i] == 0 and board[[0,7,0,5,0,3,0,1,0][i]] != 1 else 0
                                           for i, sq in enumerate([0,1,0,1,0,1,0,1,0])], k=1)[0]
            return out
        else: # Take a corner
            return random.choices(config.COLOUR_MAP[0:9],
                                  weights=[sq if board[i] == 0 else 0 for i, sq in enumerate([1,0,1,0,0,0,1,0,1])], k=1)[0]
    else: # Third and fifth moves
        # Win if possible, or block, or go randomly and it leads to draw
        my_wm = winning_move(board, config, 2)
        if my_wm != -1: return my_wm
        op_wm = winning_move(board, config, 1)
        if op_wm != -1: return op_wm
        return random.choices(config.COLOUR_MAP[0:9], weights=[1 if s == 0 else 0 for s in board], k=1)[0]

