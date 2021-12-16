import numpy as np
import matplotlib.pyplot as plt

import csv
class Courbe:
    def __init__(self):
        pass
    
    def getCourbe(self, tabx, taby, number):
        plt.plot(tabx, taby)
        plt.savefig(f"ResultatCourbe/demo{number}.pdf")
        

    def readCSVFile(self,csvFileName, number):
        nbClient = []
        USER_TYPE = []
        with open(csvFileName, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='')
            for ligne in spamreader:
                nbClient.append(int(ligne[0]))
                USER_TYPE.append(float(ligne[1]))

        #self.getCourbe(x,y, number)
        return [nbClient]


def displayCourbe(data,fileName,metrique="DELAY",title=""):
    grouped = data
    fig, ax = plt.subplots(figsize=(10, 4))
    groupedDelay = grouped.groupby(["USER_TYPE", "SCHEDULER"])[metrique]
    keys = [('LOIN', 'MaxSNR'), ('LOIN', 'RoundRobin'), ('PROCHE', 'MaxSNR'), ('PROCHE', 'RoundRobin')]
    lineMaxSNRProche, = ax.plot([2 *i for i in range(1,8)], groupedDelay.get_group(('PROCHE', 'MaxSNR')), label="MaxSNR,PROCHE",
                                c='red')
    lineMaxSNRLoin, = ax.plot([2 *i for i in range(1,8)], groupedDelay.get_group(('LOIN', 'MaxSNR')), label="MaxSNR,LOIN", c='red')
    lineMaxSNRLoin.set_dashes([2, 2, 10, 2])
    print(list(groupedDelay.get_group(('LOIN', 'MaxSNR'))))
    lineRoundRobinProche, = ax.plot([2 *i for i in range(1,8)], groupedDelay.get_group(('PROCHE', 'RoundRobin')),
                                    label="RoundRobin,PROCHE", c='blue')
    lineRoundRobinLoin, = ax.plot([2 *i for i in range(1,8)], groupedDelay.get_group(('LOIN', 'RoundRobin')), label="RoundRobin,LOIN",
                                  c='blue')
    lineRoundRobinLoin.set_dashes([2, 2, 10, 2])
    ax.legend()
    plt.title(title)
    #plt.show()
    plt.savefig(f"ResultatCourbe/{fileName}")


if(__name__ == "__main__"):
    """
    r=Courbe()
    x,y = readCSVFile('maxSNR.csv')
    import matplotlib.pyplot as plt
    plt.plot(tabx, taby)
    plt.show() # affiche la figure a l'ecran
    plt.savefig("ResultatCourbe/demo.pdf")
    """
    import pandas as pd
    import matplotlib.pyplot as plt

    multiAntenne = pd.read_csv("Resultat_CSV/Non_EmelineSimulationReuse2AvecBruit.csv")

    #macroAntenne = pd.read_csv("Resultat_CSV/result_MacroAntenne.csv")
    subMultiple = multiAntenne.groupby(["USER_TYPE", "SCHEDULER", "NB_USER" ]).mean()
    #subMacro = macroAntenne.groupby(["USER_TYPE", "SCHEDULER", "NB_USER" ]).mean()
    #displayCourbe(subMacro,"courreDelayMacro.png",metrique="DELAY",title="variation du delay en fonction de la charge le cas macro antenne")
    displayCourbe(subMultiple, "1courbeDelayMicro.png",metrique="DELAY",title="variation du delay en fonction de la charge le cas micro antenne")
    #displayCourbe(subMacro, "courbeTauxURMicro.png", metrique="UR_USAGE",
                  #title="variation du taux d'utilisation de la bande de fréquence en fonction de la charge le cas micro antenne")
    displayCourbe(subMultiple, "1courbreTauxURMicro.png", metrique="UR_USAGE",
                  title="variation u taux d'utilisation de la bande de fréquence en fonction de la charge le cas micro antenne")

