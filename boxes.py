

class MBox:

    def __init__(self, shape=None, beads=None):
        # The shape of the board for this box
        self.shape = shape if shape is not None else [0,0,0, 0,0,0, 0,0,0]
        # The beads and their positions in the box
        self.beads = beads if beads is not None else [0,0,0, 0,0,0, 0,0,0]

        # TODO:
        # Describes how this box is reached by the other boxes, as a list in:
        # nth 0th move box (always 0), nth 2nd move box, nth 4th move box, etc as needed
        self.path = []

    def __eq__(self, other):
        return self.shape == other.shape and self.beads == other.beads

    # Methods generally for debugging/printing:
    def readable_shape(self):
        # To print the shape in columns
        sh = ["_" if s == 0 else "X" if s == 1 else "O" for s in self.shape]
        return [sh[0:3], sh[3:6], sh[6:9]]
    def readable_full(self):
        # As above but includes bead numbers where applicable and non-zero
        # Will not work nicely if a bead number is greater than 9
        sh = ["_" if s == 0 else "X" if s == 1 else "O" for s in self.shape]
        for i in range(len(sh)):
            if sh[i] == "_" and self.beads[i] != 0:
                sh[i] = str(self.beads[i])
        return [sh[0:3], sh[3:6], sh[6:9]]

    def __repr__(self):
        return "\n".join(["".join(item) for item in self.readable_shape()])
    def __str__(self): return self.__repr__()


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
START_WEIGHT_0 = 8
START_WEIGHT_2 = 4
START_WEIGHT_4 = 2
START_WEIGHT_6 = 1

def rotate_shape(lst, order):
    ## Returns shape list rotated in order
    out = []
    for x in order:
        out.append(lst[x])
    return out

def is_win(lst):
    ## Returns 1, 2 if X, O respectively have won, else 0
    for wp in WIN_POSITIONS:
        is_x = [True if lst[sq] == 1 else False for sq in wp]
        is_o = [True if lst[sq] == 2 else False for sq in wp]
        if False not in is_x: return 1
        if False not in is_o: return 2
    return 0

def get_boxes():
    ## Generates the basic matchbox positions and bead setups
    ## Returns a list of the list of boxes for each move depth [0th move, 2nd move, 4th move, 6th move]
    ## Each list is a list of MBox objects
    
    out = []

    ## Move 0 MBox
    first = MBox()
    first.shape = [0,0,0, 0,0,0, 0,0,0]
    first.beads = [START_WEIGHT_0 for x in range(9)] ## TODO decide whether to weight equally or not, or allow as option
    out.append([first])

    ## Move 2 MBoxes
    # Shapes:
    seconds = []
    for x in range(9):
        for o in range(9):
            if x == o: continue
            m = MBox()
            m.shape[x] = 1
            m.shape[o] = 2
            flag = 0
            for order in ROTATIONS: # Remove boxes which are the same as others when rotated
                for box in seconds:
                    if rotate_shape(m.shape, order) == box.shape:
                        flag = 1
            if not flag:
                seconds.append(m)
    # Beads:
    for box in seconds:
        bead_positions = []
        for i, sq in enumerate(box.shape):
            if sq != 0: continue

            flag = 0
            shape_as = [s for s in box.shape]
            shape_as[i] = 1
            # Also remove beads for squares where it would make the resulting board the same as others when rotated
            # This could be an option, but unlikely we would use this
            for order in ROTATIONS:
                for pos in bead_positions:
                    if rotate_shape(shape_as, order) == pos:
                        flag = 1
            if not flag:
                box.beads[i] = START_WEIGHT_2
                bead_positions.append(shape_as)
    
    out.append(seconds)
    
    ## Move 4 MBoxes
    # Shapes:
    thirds = []
    for sec in seconds:
        for x in range(9):
            if sec.shape[x] != 0 or sec.beads[x] == 0:
                continue
            for y in range(9):
                if x == y or sec.shape[x] != 0 or sec.shape[y] != 0:
                    continue
                box = MBox([s for s in sec.shape])
                box.shape[x] = 1
                box.shape[y] = 2
                flag = 0
                for order in ROTATIONS:
                    for comp in thirds:
                        if rotate_shape(box.shape, order) == comp.shape:
                            flag = 1
                if not flag:
                    thirds.append(box)

    # Beads:
    for box in thirds:
        bead_positions = []
        for i, sq in enumerate(box.shape):
            if sq != 0: continue

            flag = 0
            shape_as = [s for s in box.shape]
            shape_as[i] = 1
            for order in ROTATIONS:
                for pos in bead_positions:
                    if rotate_shape(shape_as, order) == pos:
                        flag = 1
            if not flag:
                box.beads[i] = START_WEIGHT_4
                bead_positions.append(shape_as)
    

    out.append(thirds)
    
    ## Move 6 MBoxes (some of this code is quite repetitive/copy-paste from above)
    # Shapes:
    fourths = []
    for thi in thirds:
        for x in range(9):
            if thi.shape[x] != 0 or thi.beads[x] == 0:
                continue
            for y in range(9):
                if x == y or thi.shape[x] != 0 or thi.shape[y] != 0:
                    continue
                box = MBox([s for s in thi.shape])
                box.shape[x] = 1
                box.shape[y] = 2
                flag = 0
                for order in ROTATIONS:
                    for comp in fourths:
                        if rotate_shape(box.shape, order) == comp.shape:
                            flag = 1
                if not flag:
                    if not is_win(box.shape):
                        fourths.append(box) # Remove combinations already won

    # Beads:
    for box in fourths:
        bead_positions = []
        for i, sq in enumerate(box.shape):
            if sq != 0: continue

            flag = 0
            shape_as = [s for s in box.shape]
            shape_as[i] = 1
            for order in ROTATIONS:
                for pos in bead_positions:
                    if rotate_shape(shape_as, order) == pos:
                        flag = 1
            if not flag:
                box.beads[i] = START_WEIGHT_6
                bead_positions.append(shape_as)
    
    out.append(fourths)
    
    ## Return list
    return out


if __name__ == "__main__":
    ## To print all box combinations, run this script
    boxes = get_boxes()
    all_boxes = []
    for move in boxes:
        for box in move:
            all_boxes.append(box)

    cols = int(input("Number of columns: "))
    show_beads = int(input("Show beads (1=yes, 0=no): "))
    out = ""
    for i in range(0, len(all_boxes), cols):
        for x in range(i, i+cols):
            out += str(x).zfill(3)
            out += " "
        out += "\n"
        for s in range(0,3):
            for x in range(i, i+cols):
                if x >= len(all_boxes): continue
                if show_beads:
                    out += "".join(all_boxes[x].readable_full()[s])
                else:
                    out += "".join(all_boxes[x].readable_shape()[s])
                out += " "
            out += "\n"
        out += "\n"
            

    print(out)


    



        


