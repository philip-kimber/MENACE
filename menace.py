
import boxes

# Mapping of colours of beads to spaces on board. Each colour must have a single character reference
# and this is written here in board order, rows-first
COLOUR_MAP = ['r','o','y',
              'g','b','i',
              'v','w','l']

# The amount by which we change the beads in each eventuality, written here as a list of
# [change if MENACE draws, change if MENACE wins, change if MENACE loses]
INCENTIVES = [+1, +3, -1]


def find_box(board, all_boxes):
    # Finds the necessary box for a board position
    # Returns a tuple of (index of box, index of rotation applied)
    for i_box, box in enumerate(all_boxes):
        for i_rot, rot in enumerate(boxes.ROTATIONS):
            shp = boxes.rotate_shape(box.shape, rot)
            if shp == board:
                return i_box, i_rot
    return -1, -1 # Returns -1,-1 if error/not found
    

class Menace:

    def __init__(self):
        # Generate matchboxes
        self.boxes_src = boxes.get_boxes()

        # Organise into one list, for numbered access
        self.all_boxes = []
        for move in self.boxes_src:
            for box in move:
                self.all_boxes.append(box)
        
    def play_game(self):
        # Initial flowchart-like playing out of the game

        # Set up the game board (as in boxes.py: 0=empty, 1=X, 2=O)
        board = [0,0,0, 0,0,0, 0,0,0]

        # Play the moves, keeping track of beads selected
        moves = [] # List of tuples of MENACE's moves (box number, bead selected)
        for _ in range(4):
            # MENACE goes first
            box_ref = find_box(board, self.all_boxes)
            print("Find box #{0}".format(box_ref[0])) # Tell user the number of the box to find
            menace_move_raw = input("MENACE turn: Enter initial of bead colour: ") # Ask user for result of bead choice from box
            if menace_move_raw not in COLOUR_MAP: # user input error handling
                good = 0
                while not good:
                    menace_move_raw = input("TRY AGAIN! MENACE turn: Enter initial of bead colour: ")
                    if menace_move_raw in COLOUR_MAP: good = 1
            rotated_map = boxes.rotate_shape(COLOUR_MAP, boxes.ROTATIONS[box_ref[1]]) # If we had to rotate to find the box, apply this backwards
            menace_real_move = rotated_map.index(menace_move_raw)
            if board[menace_real_move] != 0: print("ERROR")
            moves.append((box_ref[0], menace_move_raw))
            board[menace_real_move] = 1
            print("MENACE moves in square '{0}'".format(COLOUR_MAP[menace_real_move])) # Tell user where MENACE actually moves

            # Check for win, after MENACE's move
            if boxes.is_win(board): break

            # Now player's turn
            usr_move = input("Player turn: Enter initial of move colour: ") # Ask user where player has moved
            if usr_move not in COLOUR_MAP or board[COLOUR_MAP.index(usr_move)] != 0: # user input error handling
                good = 0
                while not good:
                    usr_move = input("TRY AGAIN! Player turn: Enter initial of move colour: ")
                    if usr_move in COLOUR_MAP and board[COLOUR_MAP.index(usr_move)] == 0: good = 1
            board[COLOUR_MAP.index(usr_move)] = 2
            print("Player moves in square '{0}'".format(usr_move)) # Not strictly necessary but ease of use, tells user where player has moved

            # Check for win, after player's move
            if boxes.is_win(board): break

        # Final move of the game (MENACE fills the only empty square)
        if not boxes.is_win(board):
            menace_move = board.index(0)
            board[menace_move] = 1
            print("(Final move) MENACE moves in square '{0}'".format(COLOUR_MAP[menace_move]))

        state = boxes.is_win(board) # The INCENTIVES list is organised so that we can use state as an index
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
                ("+" + str(INCENTIVES[state]) if INCENTIVES[state] >= 0 else "-" + str(INCENTIVES[state])),
                move[1]))

            # Do incentive (TODO implement exception that first box can't die)
            bead_i = COLOUR_MAP.index(move[1])
            if self.all_boxes[move[0]].beads[bead_i] + INCENTIVES[state] >= 0: self.all_boxes[move[0]].beads[bead_i] += INCENTIVES[state]
            else: self.all_boxes[move[0]].beads[bead_i] = 0

        # End
        print()


if __name__ == "__main__":
    menace = Menace()
    menace.play_game()
            
            
                

        

        
