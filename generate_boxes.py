import menace_commons as commons


class MBox:

    def __init__(self, shape=None, beads=None):
        # The shape of the board for this box
        # As stored on board: 0=empty, 1=X, 2=O
        self.shape = shape if shape is not None else [0,0,0, 0,0,0, 0,0,0]
        # The beads and their positions in the box
        self.beads = beads if beads is not None else [0,0,0, 0,0,0, 0,0,0]
    
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


def get_boxes():
    # Generates the basic matchbox positions and bead setups
    # Returns a list of all the matchboxes

    # Generate move 0 MBox (blank board)
    box_levels = [[MBox([0,0,0, 0,0,0, 0,0,0], [x for x in commons.INITIAL_BOX_BEADS])]]

    # Generate remaining MBoxes, appending each level to box_levels
    for move in range(3):
        cur_boxes = []

        # Shapes
        for parent in box_levels[len(box_levels)-1]:
            for x in range(9):
                if parent.shape[x] != 0 or parent.beads[x] == 0:
                    continue
                for y in range(9):
                    if x == y or parent.shape[x] != 0 or parent.shape[y] != 0:
                        continue
                    box = MBox([s for s in parent.shape])
                    box.shape[x] = 1
                    box.shape[y] = 2
                    flag = 0
                    for order in commons.ROTATIONS: # Remove boxes that are identical to others when rotated
                        for comp in cur_boxes:
                            if commons.rotate_shape(box.shape, order) == comp.shape:
                                flag = 1
                    if not flag:
                        if not commons.is_win(box.shape): # Remove combinations already won
                            cur_boxes.append(box)

        # Beads
        for box in cur_boxes:
            bead_positions = []
            for i, sq in enumerate(box.shape):
                if sq != 0: continue

                flag = 0
                shape_as = [s for s in box.shape]
                shape_as[i] = 1
                for order in commons.ROTATIONS:
                    for pos in bead_positions:
                        if commons.rotate_shape(shape_as, order) == pos:
                            flag = 1
                if not flag:
                    box.beads[i] = commons.INITIAL_WEIGHTS[move]
                    bead_positions.append(shape_as)
    
        box_levels.append(cur_boxes)
    
    # Amalgamate into one list
    out = []
    for lvl in box_levels:
        for box in lvl:
            out.append(box)
    
    return out


def print_boxes():
    ## Prints the generated box combinations, in columns and with or without beads
    all_boxes = get_boxes()

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


if __name__ == "__main__":
    print_boxes()
    
