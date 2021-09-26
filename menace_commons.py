import random


# MenaceConfig object will be used to keep track of the configurations
class MenaceConfig:

    def __init__(self):
        # Configs for number of beads in each box to start
        self.INITIAL_BOX_BEADS = [8,8,0, 0,8,0, 0,0,0]
        self.INITIAL_WEIGHTS = [4, 2, 1] # Weight in 2nd move boxes, 4th move boxes, 6th move boxes

        # Mapping of colours of beads to spaces on board. Each colour must have a single character reference
        # and this is written here in board order, rows-first
        self.COLOUR_MAP = ['r','o','y',
                           'g','b','i',
                           'v','w','l',
                           'D'] # The final colour (COLOUR_MAP[9]) represents where the box is empty and MENACE resigns

        # The amount by which we change the beads in each eventuality, written here as a list of
        # [change if MENACE draws, change if MENACE wins, change if MENACE loses]
        self.INCENTIVES = [+1, +3, -1]

    def as_dct(self):
        # Return the configurations in dictionary form for logging
        dct = {
            "INITIAL_BOX_BEADS": self.INITIAL_BOX_BEADS,
            "INITIAL_WEIGHTS": self.INITIAL_WEIGHTS,
            "COLOUR_MAP": self.COLOUR_MAP,
            "INCENTIVES": self.INCENTIVES
            }
        return dct

    def printout(self):
        # Print the current config setting
        print("""    First box initial beads: {0},{1},{2},
                            {3},{4},{5},
                            {6},{7},{8}
                            
""".format(*self.INITIAL_BOX_BEADS))
        print("""   Initial weights for MENACE's moves:
        Second move boxes: {0}
        Third move boxes: {1}
        Fourth move boxes: {2}
""".format(*self.INITIAL_WEIGHTS))
        print("""   Colour map: {0},{1},{2},
                {3},{4},{5},
                {6},{7},{8},
                {9} for resign
""".format(*self.COLOUR_MAP))
        print("""
    Incentives:
        When the game is a draw: {0}
        When MENACE wins: {1}
        When MENACE loses: {2}
""".format(*[i if i < 0 else "+"+str(i) for i in self.INCENTIVES]))
        print()

def menace_config_from_dct(dct):
    # Produces a populated config object from dictionary from log (no error checking)
    out = MenaceConfig()
    if "INITIAL_BOX_BEADS" in dct.keys():
        out.INITIAL_BOX_BEADS = dct["INITIAL_BOX_BEADS"]
    if "INITIAL_WEIGHTS" in dct.keys():
        out.INITIAL_WEIGHTS = dct["INITIAL_WEIGHTS"]
    if "COLOUR_MAP" in dct.keys():
        out.COLOUR_MAP = dct["COLOUR_MAP"]
    if "INCENTIVES" in dct.keys():
        out.INCENTIVES = dct["INCENTIVES"]
    return out

def menace_config_from_prompt():
    # Produces a populated config object by prompting the command line
    # No error checking at this stage
    out = MenaceConfig()
    print()
    print("\tEnter first box initial beads in order of list")
    initial_box_beads = []
    for _ in range(9):
        initial_box_beads.append(int(input("\t\t>")))
    out.INITIAL_BOX_BEADS = initial_box_beads
    weights_2nd = int(input("\tEnter initial weights for MENACE second move boxes: "))
    weights_3rd = int(input("\tEnter initial weights for MENACE third move boxes: "))
    weights_4th = int(input("\tEnter initial weights for MENACE fourth move boxes: "))
    out.INITIAL_WEIGHTS = [weights_2nd, weights_3rd, weights_4th]
    print("\tEnter colour bead initials in order of list (tenth is resign indicator)")
    colour_map = []
    for _ in range(10):
        colour_map.append(input("\t\t>").strip())
    out.COLOUR_MAP = colour_map
    inc_draw = int(input("\tEnter incentive for draw: "))
    inc_win = int(input("\tEnter incentive for MENACE win: "))
    inc_lose = int(input("\tEnter incentive for MENACE lose: "))
    out.INCENTIVES = [inc_draw, inc_win, inc_lose]
    print()
    return out

def menace_config_compare(cfg, comp):
    # Returns boolean for whether a config (as lifted from log perhaps) is the same as another
    # True = they are the same, False = different
    if cfg.INITIAL_BOX_BEADS != comp.INITIAL_BOX_BEADS: return False
    if cfg.INITIAL_WEIGHTS != comp.INITIAL_WEIGHTS: return False
    if cfg.COLOUR_MAP != comp.COLOUR_MAP: return False
    if cfg.INCENTIVES != comp.INCENTIVES: return False
    return True
        

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

def box_choice(box, cfg):
    # Performs the weighted random choice from a matchbox
    # Returns the appropriate COLOUR_MAP character
    # Requires the config for the COLOUR_MAP
    if sum(box.beads) == 0:
        return cfg.COLOUR_MAP[9] # MENACE resigns
    return random.choices(cfg.COLOUR_MAP[0:9], weights=box.beads, k=1)[0]

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
    
