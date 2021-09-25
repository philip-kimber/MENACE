import menace_commons as commons
from generate_boxes import get_boxes

import time
import json


class Menace:

    def __init__(self):
        # Generate matchboxes
        self.all_boxes = get_boxes()

        # List of [number of games drawn, games MENACE won, games MENACE lost]
        # Sum of this list will be number of games played
        self.games_played = [0, 0, 0]

        # Set up log file
        self.log_path = time.strftime("MENACE_log_%Y_%m_%d_%H%M_%S.json")
        try:
            f = open(self.log_path, "x")
            f.close()
        except FileExistsError:
            # Given that filename includes seconds counter, unlikely to be a problem, but this is the easiest way to be on the safe side
            raise FileExistsError("File '{0}' exists; was going to use for log file but do not want to overwrite. Restart program".format(self.log_path))
        log_template = {"CONFIG": {}, "GAMES":[]}
        with open(self.log_path, "w") as f:
            json.dump(log_template, f, indent=4) # Write the initial log boilerplate to the file

    def log_game(self, lst):
        # Write the transcript of a game to the log file
        # Takes lst parameter, which is simply a list of every raw colour move (directly as chosen by boxes/player, no rotation needed)
        decoded = [commons.COLOUR_MAP.index(m) for m in lst] # Decode it so that the log is not reliant on the colour map (although this will be in CONFIG)
        with open(self.log_path, "r") as f:
            dct = json.load(f)
        dct["GAMES"].append(decoded)
        with open(self.log_path, "w") as f:
            json.dump(dct, f, indent=4)

    def play_game(self, fetch, fetch_args={}, result_cb=lambda x,y,z:None, result_args={}):
        # Plays game, fetching moves via fetch function and calling back the result by result function
        # fetch as passed should be a function taking following args:
        # - is_fetch: 1 or 0, which is 0 where the call is just for an announcement (e.g 'find box 12'), and 1 where the function must return
        # - text: str, which is the text, either the announcement or prompt
        # - board: board list, in case the prompt needs to show the state of the board
        # - args: dictionary, the arguments for the fetch function as passed to this function in fetch_args
        # fetch should return (if is_fetch==1) a single-character string of one of the colours from commons.COLOUR_MAP
        # result_cb as passed should be a function taking following args:
        # - state: 0, 1, 2 as corresponding to commons.is_win (0=draw, 1=X win, 2=O win)
        # - moves: a list of tuples of menaces moves: (box number, bead selected) corresponding to the moves local var that keeps track
        # - args: dictionary, the arguments for the result_cb function as passed ot this function in result_args
        # result_cb should not return anything

        # Set up the game board (as in boxes.py: 0=empty, 1=X, 2=O)
        board = [0,0,0, 0,0,0, 0,0,0]

        # Remember the raw colour moves, for logging
        log_cache = []

        # Play the moves, keeping track of beads selected
        moves = [] # List of tuples of MENACE's moves (box number, bead selected)
        is_resign = 0
        for _ in range(4):
            # MENACE goes first
            box_ref = commons.find_box(board, self.all_boxes)
            fetch(0, "Find box #{0}".format(box_ref[0]), board, fetch_args) # Tell user the number of the box to find
            menace_move_raw = fetch(1, "MENACE turn: Enter initial of bead colour: ", board, fetch_args) # Ask user for result of bead choice from box
            if menace_move_raw not in commons.COLOUR_MAP: # user input error handling
                good = 0
                while not good:
                    menace_move_raw = fetch(1, "TRY AGAIN! MENACE turn: Enter initial of bead colour: ", board, fetch_args)
                    if menace_move_raw in commons.COLOUR_MAP: good = 1
            if commons.COLOUR_MAP.index(menace_move_raw) == 9: # Indicates MENACE has resigned
                fetch(0, "MENACE resigns", board, fetch_args)
                log_cache.append(menace_move_raw)
                is_resign = 1
                break
            rotated_map = commons.rotate_shape(commons.COLOUR_MAP[0:9], commons.ROTATIONS[box_ref[1]]) # If we had to rotate to find the box, apply this backwards
            menace_real_move = rotated_map.index(menace_move_raw)
            if board[menace_real_move] != 0: fetch(0, "ERROR", board, fetch_args)
            moves.append((box_ref[0], menace_move_raw))
            log_cache.append(menace_move_raw)
            board[menace_real_move] = 1
            fetch(0, "MENACE moves in square '{0}'".format(commons.COLOUR_MAP[menace_real_move]), board, fetch_args) # Tell user where MENACE actually moves

            # Check for win, after MENACE's move
            if commons.is_win(board): break

            # Now player's turn
            usr_move = fetch(1, "Player turn: Enter initial of move colour: ", board, fetch_args) # Ask user where player has moved
            if usr_move not in commons.COLOUR_MAP or board[commons.COLOUR_MAP.index(usr_move)] != 0: # user input error handling
                good = 0
                while not good:
                    usr_move = fetch(1, "TRY AGAIN! Player turn: Enter initial of move colour: ", board, fetch_args)
                    if usr_move in commons.COLOUR_MAP and board[commons.COLOUR_MAP.index(usr_move)] == 0: good = 1
            board[commons.COLOUR_MAP.index(usr_move)] = 2
            log_cache.append(usr_move)
            fetch(0, "Player moves in square '{0}'".format(usr_move), board, fetch_args) # Not strictly necessary but ease of use, tells user where player has moved

            # Check for win, after player's move
            if commons.is_win(board): break

        # Final move of the game (MENACE fills the only empty square)
        if not is_resign and not commons.is_win(board):
            menace_move = board.index(0)
            log_cache.append(commons.COLOUR_MAP[menace_move])
            board[menace_move] = 1
            fetch(0, "MENACE final turn: MENACE moves in square '{0}'".format(commons.COLOUR_MAP[menace_move]), board, fetch_args)

        state = commons.is_win(board) if not is_resign else 2 # The commons.INCENTIVES list is organised so that we can use state as an index
        if state == 1: # MENACE has won
            fetch(0, "Game: MENACE wins", board, fetch_args)
        elif state == 2: # Player has won
            fetch(0, "Game: Player wins", board, fetch_args)
        else: # state = 0, draw
            fetch(0, "Game: Draw", board, fetch_args)
        
        self.games_played[state] += 1 # Update draw/win/loss counter

        # Apply the incentives and tell user which beads to add/take away
        for move in moves:
            # Print incentive
            fetch(0, "Beads: box #{0}, do {1} of '{2}' coloured bead".format(
                move[0],
                ("+" + str(commons.INCENTIVES[state]) if commons.INCENTIVES[state] >= 0 else str(commons.INCENTIVES[state])),
                move[1]), board, fetch_args)

            # Do incentive: avoid emptying the first box, to prevent MENACE from 'dying'
            bead_i = commons.COLOUR_MAP.index(move[1])
            is_revived = 0
            if move[0] == 0:
                copy_beads = [bead for bead in self.all_boxes[0].beads]
                copy_beads[bead_i] += commons.INCENTIVES[state]
                if sum(copy_beads) <= 0: # Revival situation
                    fetch(0, "Beads REVIVAL: leave 1 '{0}' coloured bead in box #0, to avoid MENACE dying".format(move[1]), board, fetch_args)
                    self.all_boxes[0].beads = [0,0,0, 0,0,0, 0,0,0]
                    self.all_boxes[0].beads[bead_i] = 1
                    is_revived = 1
            if not is_revived:
                if self.all_boxes[move[0]].beads[bead_i] + commons.INCENTIVES[state] >= 0: self.all_boxes[move[0]].beads[bead_i] += commons.INCENTIVES[state]
                else: self.all_boxes[move[0]].beads[bead_i] = 0

        # Callback the result
        result_cb(state, moves, result_args)

        # Log the game
        self.log_game(log_cache)

    def play_game_usr(self):
        # Play a game with prompts to the command line, for user to enter moves
        def fetch(is_fetch, text, board, args):
            if is_fetch:
                return input(text)
            else:
                print(text)
        self.play_game(fetch)

    def play_game_lst(self, lst, prnt=0):
        # Play a game from a list of numbers for moves, as from log file
        # If prnt=1, will print the game as it goes along
        encoded = [commons.COLOUR_MAP[x] for x in lst]
        ptr = [0]
        def fetch(is_fetch, text, board, args):
            if is_fetch:
                out = args["encoded"][args["ptr"][0]]
                args["ptr"][0] += 1
                if args["prnt"] == 1:
                    print(text, end="")
                    print(out)
                return out
            else:
                if args["prnt"] == 1:
                    print(text)
        self.play_game(fetch, fetch_args={"encoded":encoded, "ptr":ptr, "prnt":prnt})


if __name__ == "__main__":
    menace = Menace()
    while True:
        menace.play_game_usr()
    
