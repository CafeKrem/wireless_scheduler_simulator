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

def displayCourbeCumul(data,fileName,metrique="DELAY",title="",ylabel="",ylim=None,xlim=None, xlabel="nombre d'utilisateurs"):
    grouped = data
    fig, ax = plt.subplots(figsize=(10, 4))
    groupedDelay = grouped.groupby(["SCHEDULER","NB_USER"]).mean()
    print(groupedDelay)
    groupedDelay = groupedDelay.groupby("SCHEDULER")[metrique]
    print(groupedDelay)
    keys = [('MaxSNR'), ('RoundRobin')]
    print(groupedDelay.get_group('MaxSNR'))
    lineMaxSNR, = ax.plot([8 * i for i in range(1,8)], groupedDelay.get_group('MaxSNR'), label="MaxSNR",
                                c='red')
    lineRoundRobin, = ax.plot([8 * i for i in range(1,8)], groupedDelay.get_group('RoundRobin'),
                                    label="RoundRobin", c='blue')
    ax.legend()
    plt.title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    if (xlim != None):
        plt.xlim(xlim[0], xlim[1])
    if (ylim != None):
        plt.ylim(ylim[0], ylim[1])
    #plt.show()
    plt.savefig(f"ResultatCourbe/{fileName}")
def displayCourbe(data,fileName,metrique="DELAY",title="", xlim=None,ylim=None,x=None, xlabel="nombre d'utilisateurs", ylabel ="emptylabel"):
    if(x ==None):
        x =[x * 8 for x in range(1,8)]
    grouped = data
    fig, ax = plt.subplots(figsize=(10, 4))
    groupedDelay = grouped.groupby(["USER_TYPE", "SCHEDULER"])[metrique]
    keys = [('LOIN', 'MaxSNR'), ('LOIN', 'RoundRobin'), ('PROCHE', 'MaxSNR'), ('PROCHE', 'RoundRobin')]
    lineMaxSNRProche, = ax.plot(x , groupedDelay.get_group(('PROCHE', 'MaxSNR')), label="MaxSNR,PROCHE",
                                c='red')
    lineMaxSNRLoin, = ax.plot(x , groupedDelay.get_group(('LOIN', 'MaxSNR')), label="MaxSNR,LOIN", c='red')
    lineMaxSNRLoin.set_dashes([2, 2, 10, 2])
    print(list(groupedDelay.get_group(('LOIN', 'MaxSNR'))))
    lineRoundRobinProche, = ax.plot(x , groupedDelay.get_group(('PROCHE', 'RoundRobin')),
                                    label="RoundRobin,PROCHE", c='blue')
    lineRoundRobinLoin, = ax.plot(x , groupedDelay.get_group(('LOIN', 'RoundRobin')), label="RoundRobin,LOIN",
                                  c='blue')
    lineRoundRobinLoin.set_dashes([2, 2, 10, 2])
    ax.legend()
    plt.title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    if(xlim != None):
        plt.xlim(xlim[0], xlim[1])
    if(ylim  != None):
        plt.ylim(ylim[0],ylim[1])
    #plt.show()
    plt.savefig(f"ResultatCourbe/{fileName}")

def displayCourbeMoy(data,fileName,metrique="DELAY",title="", xlim=None,ylim=None,x=None, xlabel="nombre d'utilisateur", ylabel ="emptylabel"):
    if(x ==None):
        x =[x * 8 for x in range(1,8)]
    grouped = data
    fig, ax = plt.subplots(figsize=(10, 4))
    groupedDelay = grouped.groupby(["USER_TYPE", "SCHEDULER"])[metrique]
    keys = [('LOIN', 'MaxSNR'), ('LOIN', 'RoundRobin'), ('PROCHE', 'MaxSNR'), ('PROCHE', 'RoundRobin')]
    lineMaxSNRProche, = ax.plot(x , groupedDelay.get_group(('PROCHE', 'MaxSNR')), label="MaxSNR,PROCHE",
                                c='red')
    lineMaxSNRLoin, = ax.plot(x , groupedDelay.get_group(('LOIN', 'MaxSNR')), label="MaxSNR,LOIN", c='red')
    lineMaxSNRLoin.set_dashes([2, 2, 10, 2])
    print(list(groupedDelay.get_group(('LOIN', 'MaxSNR'))))
    lineRoundRobinProche, = ax.plot(x , groupedDelay.get_group(('PROCHE', 'RoundRobin')),
                                    label="RoundRobin,PROCHE", c='blue')
    lineRoundRobinLoin, = ax.plot(x , groupedDelay.get_group(('LOIN', 'RoundRobin')), label="RoundRobin,LOIN",
                                  c='blue')
    lineRoundRobinLoin.set_dashes([2, 2, 10, 2])
    ax.legend()
    plt.title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    if(xlim != None):
        plt.xlim(xlim[0], xlim[1])
    if(ylim  != None):
        plt.ylim(ylim[0],ylim[1])
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

    multiAntenne = pd.read_csv("Resultat_CSV/simuMultiAntenneSpectralNuitFinal.csv")
    macroAntenne = pd.read_csv("Resultat_CSV/simuGrosseAntenneSpectralNuitFinal.csv")


    subMultiple = multiAntenne.groupby(["USER_TYPE", "SCHEDULER", "NB_USER" ]).mean()
    subMacro = macroAntenne.groupby(["USER_TYPE", "SCHEDULER", "NB_USER" ]).mean()
    displayCourbe(subMacro,"présentation/courbeDelayMacroFinal.png",metrique="DELAY",
                  ylabel="délai",
                  ylim=(0,2500),
                  title="variation du delai en fonction de la charge le cas 1 macro antenne")
    displayCourbe(subMultiple, "présentation/courbeDelayMicroFinal.png",metrique="DELAY",
                  title="variation du delai en fonction de la charge le cas 4 micro antennes",
                  ylim=(0, 2500),
                  ylabel="délai")
    displayCourbeCumul(subMacro, "présentation/courbeDelayMoyenMacroFinal.png", metrique="DELAY",
                  ylabel="délai",
                  ylim=(0, 2500),
                  title="variation du delai en fonction de la charge le cas 1 macro antenne")
    displayCourbeCumul(subMultiple, "présentation/courbeDelayMoyenMicroFinal.png", metrique="DELAY",
                  title="variation du delai en fonction de la charge le cas 4 micro antennes",
                  ylim=(0, 2500),
                  ylabel="délai")
    displayCourbeCumul(subMacro, "présentation/courbeTauxURMacroFinal.png", metrique="UR_USAGE",
                  ylabel= "taux d'utilsation de la bande de fréquence",
                  title="variation du taux d'utilisation des UR en fonction de la charge le cas 1 macro antenne")
    displayCourbeCumul(subMultiple, "présentation/courbreTauxURMicroFinal.png", metrique="UR_USAGE",
                    ylabel= "taux d'utilsation de la bande de fréquence",
                  title="variation du taux d'utilisation des UR en fonction de la charge le cas 4 micro antennes")

    displayCourbeCumul(subMacro, "présentation/courbreSpectralMacroFinal.png", metrique="SPECTRAL_EFFICIENT",
                  ylabel="efficacité spectrale",
                  ylim=(17,19),
                  title="variation de l'efficacité spectrale en fonction de la charge le cas une macro antenne")
    displayCourbeCumul(subMultiple, "présentation/courbreSpectralMicroFinal.png", metrique="SPECTRAL_EFFICIENT",
                  ylabel="efficacité spectrale",
                  ylim=(17,19),
                  title="variation de l'efficacité spectrale en fonction de la charge le cas 4 micro antennes")
