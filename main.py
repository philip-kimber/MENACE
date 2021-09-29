import menace_commons as commons
from generate_boxes import get_boxes
import simulations
import menace as menace_py
import threading
import graph

class MenaceApp(threading.Thread):

    def __init__(self):
        super(MenaceApp, self).__init__()
        # Welcome message
        print("""
-----------------------------------------------------------
|  MENACE (Matchbox Educable Noughts And Crosses Engine)  |
|  Gameplay and simulation program                        |
|  * * * * * * * * * * * * * * * * * * * * * * * * * * *  |
|  Philip Kimber ------------------------ September 2021  |
-----------------------------------------------------------
""")

        # Set up default configs
        cfg = commons.MenaceConfig()
        self.graph = graph.Graph(self)


        # Check user is happy with configs
        print("Current configs:")
        cfg.printout()
        change_cfg = self.get_integer_input("Do you want to change these configs  (1=yes, 0=no): ", 0, 1)
        if change_cfg:
            cfg = commons.menace_config_from_prompt()

        # Set up MENACE
        self.menace = menace_py.Menace(cfg)
        self.start()


    def is_valid_integer(self, test, lower_bound, upper_bound):
        if not test.replace("-", "").isnumeric() and test.count("-") < 2: # For some reason the removeprefix function wasn't working for me, this can be messed up so be careful with random -'s in the middle of a number
            return False
        return lower_bound <= int(test) <= upper_bound


    def get_integer_input(self, prompt, lower_bound, upper_bound):
        usr_input = input(prompt).strip()
        while not self.is_valid_integer(usr_input, lower_bound, upper_bound):
            usr_input = input(f"Invalid, please enter a number between {lower_bound} and {upper_bound}: ")
        return int(usr_input)


    def run(self):
        # Enter main loop of commands
        print()
        print("Setup completed. Enter commands or try 'help' to see list")
        while True:
            cmd = input("MENACE>").strip().lower()

            if cmd == "help":
                self.cmd_help()
            elif cmd == "exit":
                self.cmd_exit()
            elif cmd == "config":
                self.cmd_config()
            elif cmd == "game" or cmd == "g":
                self.cmd_game()
            elif cmd == "log":
                self.cmd_log()
            elif cmd == "simulate":
                self.cmd_simulate()
            elif cmd == "results":
                self.cmd_results()
            elif cmd == "beads":
                self.cmd_beads()
            elif cmd == "box":
                self.cmd_box()
            else:
                print("Unrecognised command. Try 'help' for a list of valid ones")

    def cmd_help(self):
        print("List of commands:")
        print("""
    exit: leave the program
    config: view the current configurations and change them
    game (also aliased as 'g'): run and log a game between the physical MENACE and a real opponent
    log: load a log file, playing the games in it
    simulate: simulate game(s) between the simulated MENACE and a simulated opponent
    results: print the list of game results, in order of when they were played (crude list print)
    beads: print the list of number of beads in first box as the games went on 
""")

    def cmd_exit(self):
        sure = self.get_integer_input("Are you sure you want to leave (1=yes, 0=no): ", 0, 1)
        if sure:
            exit()

    def cmd_config(self):
        print("Current configs:")
        self.menace.config.printout()
        change_cfg = self.get_integer_input("Do you want to change these configs  (1=yes, 0=no): ", 0, 1)
        if change_cfg:
            print("Note that changes in config relating to initial beads etc. will not come into effect, as boxes already generated") # Nor, indeed, will the log be updated
            new_cfg = commons.menace_config_from_prompt()
            self.menace.config = new_cfg

    def cmd_game(self):
        print()
        self.menace.play_game_usr()
        print()

    def cmd_log(self):
        logf = input("Path of log file: ").strip()
        cfg_update = self.get_integer_input("Update config to match log file if different  (1=yes, 0=no): ", 0, 1)
        prnt = self.get_integer_input("Print the gameplay as it happens  (1=yes, 0=no): ", 0, 1)
        results = self.get_integer_input("Show results afterwards  (1=yes, 0=no): ", 0, 1)
        bead_displ = self.get_integer_input("Show the aggregate bead changes afterwards  (1=yes, 0=no): ", 0, 1)
        print()
        self.menace.play_games_log(logf, cfg_update, prnt, results, bead_displ)
        print()

    def cmd_simulate(self):
        raw_opponent = int(input("""Choose player opponent for MENACE in simulation:
    0 - Random opponent: simply chooses any free square
    1 - 'Basic' opponent: wins if possible, otherwise goes randomly
    2 - 'Intermediate' opponent: wins of possible, blocks if necessary, otherwise random
    3 - Perfect opponent: plays a perfect game, forcing at least a draw
Choice: """
))
        opponent = [simulations.opponent_random, simulations.opponent_basic, simulations.opponent_intermediate, simulations.opponent_perfect][raw_opponent]
        no_of_games = self.get_integer_input("Number of games to simulate: ", 0, 1000)
        prnt = self.get_integer_input("Print the gameplay as it happens  (1=yes, 0=no): ", 0, 1)
        results = self.get_integer_input("Show results afterwards  (1=yes, 0=no): ", 0, 1)
        bead_displ = self.get_integer_input("Show the aggregate bead changes afterwards  (1=yes, 0=no): ", 0, 1)
        print()
        self.menace.simulate_games(opponent, no_of_games, prnt, results, bead_displ)
        print()

    def cmd_results(self):
        print()
        print("Results of each game: 0 = draw, 1 = MENACE win, 2 = Player win")
        print(self.menace.state_over_time)
        print()

    def cmd_beads(self):
        print()
        print("Number of beads in first box, after each game")
        print("Box began with {0} beads".format(self.menace.initial_first_box_beads))
        print(self.menace.beads_over_time)
        print()

    def cmd_box(self):
        print()
        box = self.get_integer_input("What box would you like to manage? ", 0, len(self.menace.all_boxes) - 1)
        print()
        print("This box should be:")
        print("\n".join([" ".join(i) for i in self.menace.all_boxes[box].readable_full()]))
        edited = False
        if self.get_integer_input("Would you like to edit this box?  (1=yes, 0=no): ", 0, 1) == 1:
            done_editing = False
            while not done_editing:
                usr_input = input("Enter the colour to edit: ").strip()
                while usr_input not in self.menace.config.COLOUR_MAP:
                    usr_input = input("Invalid colour try again: ")

                colour_to_edit = self.menace.config.COLOUR_MAP.index(usr_input)
                self.menace.all_boxes[box].beads[colour_to_edit] += self.get_integer_input("Enter the amount to edit it by: ", -1000, 1000)
                edited = True

                done_editing = self.get_integer_input("Are you done editing this box?  (1=yes, 0=no): ", 0, 1) == 1

        if edited:
            print("The box now looks like:")
            print("\n".join([" ".join(i) for i in self.menace.all_boxes[box].readable_full()]))

        print()



if __name__ == "__main__":
    app = MenaceApp()
    app.graph.show()  # make sure that this happens on the main thread.

