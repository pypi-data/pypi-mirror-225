from .OriginBuilder import *


class Reader:

    def __init__(self, molecule):
        self.MOLECULE = molecule

        commandlist = []
        atomlist = []
        condition = False
        bondlist = []
        plt.axes().set_facecolor("black")
        with open(self.MOLECULE, "r") as f:
            # filelist = [(lambda x: [a.replace("\n", "") for a in x])(f.readlines()[len(commandList):].copy())]
            for enum, line in enumerate(f):
                if len(line) > 1:
                    commandlist.append(line.split())
                    if commandlist[-1][0] == "END":
                        break
                    if commandlist[-1][0] == "ORI":
                        builder = Origin("".join(commandlist[-1][1:]))
                        file = open(molecule, "r").readlines()[enum:]

                        # asd = (lambda x: [a.replace("\n", "") for a in x])(f.readlines()[len(commandList):].copy())
                        i = 0
                        while "STOP" not in file[i]:
                            i += 1

                        builder.add(
                            (lambda x: [a.replace("\n", "") for a in x])(file[:i]
                                                                         .copy()))

                    if commandlist[-1][0] == "STT":
                        condition = True
                    if condition:
                        if commandlist[-1][0] == "ATOM":
                            atomlist.append(line.split())
                            print(atomlist[-1][2])
                            if atomlist[-1][2] == '8':
                                color = 'red'
                            elif atomlist[-1][2] == '1':
                                color = 'whitesmoke'
                            elif atomlist[-1][2] == '7':
                                color = 'limegreen'
                            elif atomlist[-1][2] == '6':
                                color = 'blue'
                            else:
                                color = 'pink'
                            plt.plot(int(commandlist[-1][3]), int(commandlist[-1][4]),
                                     marker="o", color=color)
                        elif commandlist[-1][0] == "INS":
                            builder.buildOriginPrefab("ORI " + commandlist[-1][1], commandlist[-1][2:])
                        elif commandlist[-1][0] == "BND":
                            bondlist.append(line.split())
                            plt.plot(
                                [float(atomlist[int(bondlist[-1][2]) - 1][3]),
                                 float(atomlist[int(bondlist[-1][3]) - 1][3])],
                                [float(atomlist[int(bondlist[-1][2]) - 1][4]),
                                 float(atomlist[int(bondlist[-1][3]) - 1][4])],
                                color='g', linewidth=2)
