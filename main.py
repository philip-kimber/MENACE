import menace_commons as commons
from generate_boxes import get_boxes
import simulations
import menace as menace_py


class MenaceApp:

    def __init__(self):
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
        

        # Check user is happy with configs
        print("Current configs:")
        cfg.printout()
        change_cfg = int(input("Do you want to change these configs (1=yes, 0=no): "))
        if change_cfg:
            cfg = commons.menace_config_from_prompt()

        # Set up MENACE
        self.menace = menace_py.Menace(cfg)

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
        sure = int(input("Are you sure you want to leave (1=yes, 0=no): "))
        if sure:
            exit()

    def cmd_config(self):
        print("Current configs:")
        self.menace.config.printout()
        change_cfg = int(input("Do you want to change these configs (1=yes, 0=no): "))
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
        cfg_update = int(input("Update config to match log file if different (1=yes, 0=no): "))
        prnt = int(input("Print the gameplay as it happens (1=yes, 0=no): "))
        results = int(input("Show results afterwards (1=yes, 0=no): "))
        bead_displ = int(input("Show the aggregate bead changes afterwards (1=yes, 0=no): "))
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
        no_of_games = int(input("Number of games to simulate: "))
        prnt = int(input("Print the gameplay as it happens (1=yes, 0=no): "))
        results = int(input("Show results afterwards (1=yes, 0=no): "))
        bead_displ = int(input("Show the aggregate bead changes afterwards (1=yes, 0=no): "))
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


if __name__ == "__main__":
    app = MenaceApp()
