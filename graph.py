import matplotlib.pyplot as plt
from matplotlib import animation


class Graph:
    def __init__(self, main):
        self.main = main
        self.fig = plt.figure(1)
        self.fig.suptitle("MENACE overall success over time", fontsize=16)
        self.ax1 = plt.axes()
        self.ax1.set_xlabel("Number of games played")
        self.ax1.set_ylabel("Number of beads in first box (3 x wins + draws - losses)")

        self.fig2 = plt.figure(2)
        self.fig2.suptitle("MENACE's wins, draws and losses over time", fontsize=16)
        self.ax2 = plt.axes()
        self.ax2.set_xlabel("Number of games played")
        self.ax2.set_ylabel("Results")
        self.ax2.legend()

        self.fig3 = plt.figure(3)
        self.fig3.suptitle("Weighted average of score over previous matches", fontsize=16)
        self.ax3 = plt.axes()
        self.ax3.set_xlabel("Number of games played")
        self.ax3.set_ylabel("Weighted average")


    def show(self):
        self.anim = animation.FuncAnimation(self.fig, self.animate, interval=1000)
        self.anim2 = animation.FuncAnimation(self.fig2, self.animate, interval=1000)
        self.anim3 = animation.FuncAnimation(self.fig3, self.animate, interval=1000)
        plt.show()

    def animate(self, i):
        plt.figure(1)
        self.ax1.clear()
        self.ax1.plot(self.main.menace.beads_over_time)
        self.ax1.set_xlabel("Number of games played")
        self.ax1.set_ylabel("Number of beads in first box (3 x wins + draws - losses")

        plt.figure(2)
        self.ax2.clear()
        self.ax2.plot(self.main.menace.wins_over_time, label="Wins")
        self.ax2.plot(self.main.menace.draws_over_time, label="Draws")
        self.ax2.plot(self.main.menace.losses_over_time, label="Losses")
        self.ax2.set_xlabel("Number of games played")
        self.ax2.set_ylabel("Results")
        self.ax2.legend()

        plt.figure(3)
        self.ax3.clear()
        for i in self.main.menace.weighted_win_loss:
            self.ax3.plot(i)
        self.ax3.set_xlabel("Number of games played")
        self.ax3.set_ylabel("Weighted average")

