
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
              'v','w','l']

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

