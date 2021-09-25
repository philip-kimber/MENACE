import random


# Possible rotations of the board, as patterns for rotate_shape function
ROTATIONS = [
    [0,1,2,3,4,5,6,7,8],
    [0,3,6,1,4,7,2,5,8],
    [6,3,0,7,4,1,8,5,2],
    [6,7,8,3,4,5,0,1,2],
    [8,7,6,5,4,3,2,1,0],
    [8,5,2,7,4,1,6,3,0],
    [2,5,8,1,4,7,0,3,6],
    [2,1,0,5,4,3,8,7,6]
    ]

# Possible positions for either player to win, used by is_win function
WIN_POSITIONS = [
    [0,1,2],
    [3,4,5],
    [6,7,8],
    [0,3,6],
    [1,4,7],
    [2,5,8],
    [0,4,8],
    [2,4,6]
    ]

# Configs for number of beads in each box to start
INITIAL_BOX_BEADS = [8,8,8, 8,8,8, 8,8,8]
INITIAL_WEIGHTS = [4, 2, 1] # Weight in 2nd move boxes, 4th move boxes, 6th move boxes

# Mapping of colours of beads to spaces on board. Each colour must have a single character reference
# and this is written here in board order, rows-first
COLOUR_MAP = ['r','o','y',
              'g','b','i',
              'v','w','l',
              'D'] # The final colour (COLOUR_MAP[9]) represents where the box is empty and MENACE resigns

# The amount by which we change the beads in each eventuality, written here as a list of
# [change if MENACE draws, change if MENACE wins, change if MENACE loses]
INCENTIVES = [+1, +3, -1]

def find_box(board, all_boxes):
    # Finds the necessary box for a board position
    # Returns a tuple of (index of box, index of rotation applied)
    for i_box, box in enumerate(all_boxes):
        for i_rot, rot in enumerate(ROTATIONS):
            shp = rotate_shape(box.shape, rot)
            if shp == board:
                return i_box, i_rot
    return -1, -1 # Returns -1,-1 if error/not found

def rotate_shape(lst, order):
    # Returns shape list rotated in order
    out = []
    for x in order:
        out.append(lst[x])
    return out

def is_win(lst):
    # Returns 1, 2 if X, O respectively have won, else 0
    for wp in WIN_POSITIONS:
        is_x = [True if lst[sq] == 1 else False for sq in wp]
        is_o = [True if lst[sq] == 2 else False for sq in wp]
        if False not in is_x: return 1
        if False not in is_o: return 2
    return 0

def box_choice(box):
    # Performs the weighted random choice from a matchbox
    # Returns the appropriate COLOUR_MAP character
    if sum(box.beads) == 0:
        return COLOUR_MAP[9] # MENACE resigns
    return random.choices(COLOUR_MAP[0:9], weights=box.beads, k=1)[0]

def print_bead_changes(described_moves):
    # Amalgamates the total changes of numbers of beads in boxes and prints this out
    # Takes described_moves a list of tuples as (box id, bead colour character, count before, count after)

    # Reorganise moves into boxes, then beads
    moves = {}
    for mv in described_moves:
        if mv[0] not in moves.keys():
            moves[mv[0]] = {}
        if mv[1] not in moves[mv[0]]:
            moves[mv[0]][mv[1]] = []
        moves[mv[0]][mv[1]].append(mv)

    # Work out changes and print
    for box_id in sorted(moves.keys()):
        for col in moves[box_id].keys():
            lst = moves[box_id][col]
            count_before = lst[0][2]
            count_after = lst[len(lst)-1][3]
            change = count_after - count_before
            print("Beads (aggregate): box #{0}, do {1} of '{2}' coloured bead, should then be {3} of those in".format(
                box_id, (change if change < 0 else "+" + str(change)), col, count_after))

def print_results(results):
    # Prints the results of a set of games, from a list of [number drawn, number MENACE won, number player won]
    print("In {0} games:".format(sum(results)))
    print("{0} won by MENACE".format(results[1]))
    print("{0} won by Player".format(results[2]))
    print("{0} drawn".format(results[0]))
    
