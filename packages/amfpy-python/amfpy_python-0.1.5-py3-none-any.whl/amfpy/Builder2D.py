import matplotlib.pyplot as plt
from .constants import *


class Drawer:

    def plotAtom(self, x: float, y: float, atomnumber: int):
        plt.plot(x, y, marker="o", color=getAtomColor(atomnumber), zorder=2)

    def plotBond(self, xlist: list, ylist: list):
        plt.plot(xlist, ylist, color="dimgrey", linewidth=2, zorder=1)

    @staticmethod
    def plotAll():
        plt.show()
