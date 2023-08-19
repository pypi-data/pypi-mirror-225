from .BondBuilder import *
from .Builder2D import *

bondbuilder = BondBuilder()


class Origin:

    cList = {}

    def __init__(self, oriname):
        self.drawer = Drawer()
        self.name = oriname
        self.atomList = []
        self.bondList = []

    def add(self, args: list):
        self.cList[args.copy()[0]] = args.copy()
        print(args)

    def buildOriginPrefab(self, identifier: str, coords):
        x, y, z = coords
        print(self.cList[identifier][1:])
        for atom in self.cList[identifier][1:]:
            if len(atom) > 1:
                if atom.split()[0] == "ATOM":
                    self.atomList.append(
                        ["ATOM", atom.split()[1], atom.split()[2], str(float(atom.split()[3]) + float(x)),
                         str(float(atom.split()[4]) + float(y))])

                    self.drawer.plotAtom(float(atom.split()[3]) + float(x), float(atom.split()[4]) + float(y),
                                         atom.split()[2])

                elif atom.split()[0] == "BND":
                    self.bondList.append(atom.split())

                    if self.bondList[-1][2] == "1":

                        # print("X1: ", x1, ", X2: ", x2, ", Y1: ", y1, ", Y2: ", y2)
                        # print(self.atomList[len(self.bondList) - 1])
                        bondbuilder.singleBond(self.atomList, self.bondList)
                    elif self.bondList[-1][2] == "2":
                        bondbuilder.doubleBond(self.atomList, self.bondList)
                    elif self.bondList[-1][2] == "3":
                        bondbuilder.tripleBond(self.atomList, self.bondList)
                    else:
                        self.drawer.plotBond([float(self.atomList[int(self.bondList[-1][3]) - 1][3]),
                                              float(self.atomList[int(self.bondList[-1][4]) - 1][3])],
                                             [float(self.atomList[int(self.bondList[-1][3]) - 1][4]),
                                              float(self.atomList[int(self.bondList[-1][4]) - 1][4])])
                        # plt.plot(color='g', zorder=2, linewidth=2)

                else:
                    break
            else:
                list(self.cList[identifier]).remove(atom)
        self.atomList = []
        self.bondList = []
