import menace_commons as commons
from generate_boxes import get_boxes


class Menace:

    def __init__(self):
        # Generate matchboxes
        self.all_boxes = get_boxes()
        
    def play_game(self):
        # Initial flowchart-like playing out of the game

        # Set up the game board (as in boxes.py: 0=empty, 1=X, 2=O)
        board = [0,0,0, 0,0,0, 0,0,0]

        # Play the moves, keeping track of beads selected
        moves = [] # List of tuples of MENACE's moves (box number, bead selected)
        for _ in range(4):
            # MENACE goes first
            box_ref = commons.find_box(board, self.all_boxes)
            print("Find box #{0}".format(box_ref[0])) # Tell user the number of the box to find
            menace_move_raw = input("MENACE turn: Enter initial of bead colour: ") # Ask user for result of bead choice from box
            if menace_move_raw not in commons.COLOUR_MAP: # user input error handling
                good = 0
                while not good:
                    menace_move_raw = input("TRY AGAIN! MENACE turn: Enter initial of bead colour: ")
                    if menace_move_raw in commons.COLOUR_MAP: good = 1
            rotated_map = commons.rotate_shape(commons.COLOUR_MAP, commons.ROTATIONS[box_ref[1]]) # If we had to rotate to find the box, apply this backwards
            menace_real_move = rotated_map.index(menace_move_raw)
            if board[menace_real_move] != 0: print("ERROR")
            moves.append((box_ref[0], menace_move_raw))
            board[menace_real_move] = 1
            print("MENACE moves in square '{0}'".format(commons.COLOUR_MAP[menace_real_move])) # Tell user where MENACE actually moves

            t_board = list(map(lambda x: "X" if x == 1 else "O" if x == 2 else "-", board))
            print("\n".join(["".join(t_board[0:3]), "".join(t_board[3:6]), "".join(t_board[6:9])])) # print the board

            # Check for win, after MENACE's move
            if commons.is_win(board): break

            # Now player's turn
            usr_move = input("Player turn: Enter initial of move colour: ") # Ask user where player has moved
            if usr_move not in commons.COLOUR_MAP or board[commons.COLOUR_MAP.index(usr_move)] != 0: # user input error handling
                good = 0
                while not good:
                    usr_move = input("TRY AGAIN! Player turn: Enter initial of move colour: ")
                    if usr_move in commons.COLOUR_MAP and board[commons.COLOUR_MAP.index(usr_move)] == 0: good = 1
            board[commons.COLOUR_MAP.index(usr_move)] = 2
            print("Player moves in square '{0}'".format(usr_move)) # Not strictly necessary but ease of use, tells user where player has moved

            t_board = list(map(lambda x: "X" if x == 1 else "O" if x == 2 else "-", board))
            print("\n".join(["".join(t_board[0:3]), "".join(t_board[3:6]), "".join(t_board[6:9])])) # print the board

            # Check for win, after player's move
            if commons.is_win(board): break

        # Final move of the game (MENACE fills the only empty square)
        if not commons.is_win(board):
            menace_move = board.index(0)
            board[menace_move] = 1
            print("MENACE final turn: MENACE moves in square '{0}'".format(commons.COLOUR_MAP[menace_move]))

        state = commons.is_win(board) # The commons.INCENTIVES list is organised so that we can use state as an index
        if state == 1: # MENACE has won
            print("Game: MENACE wins")
        elif state == 2: # Player has won
            print("Game: Player wins")
        else: # state = 0, draw
            print("Game: Draw")

        # Apply the incentives and tell user which beads to add/take away
        for move in moves:
            # Print incentive
            print("Beads: box #{0}, do {1} of '{2}' coloured bead".format(
                move[0],
                ("+" + str(commons.INCENTIVES[state]) if commons.INCENTIVES[state] >= 0 else str(commons.INCENTIVES[state])),
                move[1]))

            # Do incentive (TODO implement exception that first box can't die)
            bead_i = commons.COLOUR_MAP.index(move[1])
            if self.all_boxes[move[0]].beads[bead_i] + commons.INCENTIVES[state] >= 0: self.all_boxes[move[0]].beads[bead_i] += commons.INCENTIVES[state]
            else: self.all_boxes[move[0]].beads[bead_i] = 0

        # End
        print()


if __name__ == "__main__":
    menace = Menace()
    menace.play_game()
    
