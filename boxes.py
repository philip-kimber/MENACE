

class MBox:

    def __init__(self, shape=None, beads=None):
        self.shape = shape if shape is not None else [0,0,0, 0,0,0, 0,0,0]
        self.beads = beads if beads is not None else [0,0,0, 0,0,0, 0,0,0]

        self.path = [] ## Todo implement, for easier organisation and searching

    def __eq__(self, other):
        return self.shape == other.shape and self.beads == other.beads

    ###

    def readable_shape(self):
        sh = ["_" if s == 0 else "X" if s == 1 else "O" for s in self.shape]
        return [sh[0:3], sh[3:6], sh[6:9]]

    def __repr__(self):
        return "\n".join(["".join(item) for item in self.readable_shape()])
    def __str__(self): return self.__repr__()


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
    ## Returns 1, 2 if x, o resp. have won, else 0
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
            for order in ROTATIONS:
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
    
    ## Move 6 MBoxes
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
    pass

    



        


