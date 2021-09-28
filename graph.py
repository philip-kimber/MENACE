import matplotlib.pyplot as plt
from matplotlib import animation


class Graph:
    def __init__(self, main):
        self.main = main
        self.fig = plt.figure()
        self.ax = plt.axes()


    def show(self):
        self.anim = animation.FuncAnimation(self.fig, self.animate, interval=1000)
        plt.show()

    def animate(self, i):
        self.ax.clear()
        self.ax.plot(self.main.menace.beads_over_time)
