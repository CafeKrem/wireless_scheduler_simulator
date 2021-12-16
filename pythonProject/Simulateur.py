# coding=utf-8
import csv
import os
from typing import TYPE_CHECKING
import logging

# from pythonProject.Courbe import Courbe


if TYPE_CHECKING:
    import Packet

import Antenne as a
import Mobile as m

from datetime import datetime

NB_UR = int(os.environ.get('NB_UR' , default=128*5))
MKN_MIN = int(os.environ.get('MKN_MIN', default=0))
MKN_MAX_P = int(os.environ.get('MKN_MAX_P', default=100))
MKN_MAX_L = int(os.environ.get('MKN_MAX_L', default= 70))
NB_MOBILES = os.environ.get('NB_MOBILES')
TAILLE_PACKET = int(os.environ.get('TAILLE_PACKET',default=40))
SIMULATOR_TIME = int(os.environ.get('SIMULATOR_TIME',default=10000))
ANTENNES_CSV = os.environ.get('ANTENNES_CSV', default='parameter/antennesTest1.csv')
MOBILES_CSV = os.environ.get('MOBILES_CSV', default='parameter/mobilesTest1.csv')
SCHEDULER = os.environ.get('SCHEDULER' , default='RoundRobin')
CSV_OUTPUT = str(os.environ.get('CSV_OUTPUT' , default = 'result.csv'))
IS_INTERFERENCE = False
NB_PACKET_PAR_MOBILE = 7
NOW = datetime.now()
number = 0

def scenarioMultiAntenne(s,nbMobile, scheduler, nb_UR):
    mobileProche , mobileLoin = multiAntenneScenarioMultiAntenne(nbMobile,nb_UR//4)

    antennA = createAntenne("A" , -5 ,-5,scheduler,nb_UR//4)
    antennB = createAntenne("B", 5, -5,scheduler,nb_UR//4)
    antennC = createAntenne("C", 5, 5,scheduler,nb_UR//4)
    antennD = createAntenne("D", -5, 5,scheduler,nb_UR//4)
    s.mobilesProches = mobileProche
    s.mobilesLoin = mobileLoin
    s.mobiles = mobileProche + mobileLoin
    s.antennes = [antennA , antennB , antennC , antennD]
    s.connectMobileToAntenne()
    print(s.antennes)
    s.start()
    outPutSimu(s)

def scenarioGrosseAntenne(s,nbMobile, scheduler, nb_UR):
    mobileProche , mobileLoin = multiAntenneScenarioMultiAntenne(nbMobile, nb_UR)
    grosseAntenne = createAntenne("centre", 0, 0, scheduler, nb_UR)
    s.mobilesProches = mobileProche
    s.mobilesLoin = mobileLoin
    s.mobiles = mobileProche + mobileLoin
    s.antennes = [grosseAntenne]
    s.connectMobileToAntenne()
    print(s.antennes)
    s.start()
    outPutSimu(s)

def EmelineSimulationUneSeuleAntenneReuse1(s,nbMobile, scheduler, nb_UR):
    print(f"nombre de packet par mobile {NB_PACKET_PAR_MOBILE}")
    mobileProche , mobileLoin = EmelineScenarioUneSeuleAntenne(nbMobile,nb_UR)
    antenneA = createAntenne("antenneA", -5, 0, scheduler, nb_UR)# le cas REUSE-1 => chaque antenne utilise toute la bande de fréquence
    s.mobilesProches = mobileProche
    s.mobilesLoin = mobileLoin
    s.mobiles = mobileProche + mobileLoin
    s.antennes = [antenneA ]
    s.connectMobileToAntenne()
    global IS_INTERFERENCE
    IS_INTERFERENCE = False
    print(s.antennes)
    s.start()
    outPutSimu(s)

def EmelineSimulationUneSeuleAntenneReuse2(s,nbMobile, scheduler, nb_UR):
    mobileProche , mobileLoin = EmelineScenarioUneSeuleAntenne(nbMobile,nb_UR//2)
    antenneA = createAntenne("antenneA", -5, 0, scheduler, nb_UR//2)# le cas REUSE-1 => chaque antenne utilise toute la bande de fréquence
    s.mobilesProches = mobileProche
    s.mobilesLoin = mobileLoin
    s.mobiles = mobileProche + mobileLoin
    s.antennes = [antenneA ]
    s.connectMobileToAntenne()
    global IS_INTERFERENCE
    IS_INTERFERENCE = False
    print(s.antennes)
    s.start()
    outPutSimu(s)

def EmelineSimulationReuse1AvecBruitExecution(s,nbMobile, scheduler, nb_UR):
    mobileProche , mobileLoin = EmelineScenarioReuse(nbMobile,nb_UR)
    antenneA = createAntenne("antenneA", -5, 0, scheduler, nb_UR)# le cas REUSE-1 => chaque antenne utilise toute la bande de fréquence
    antenneB = createAntenne("antenneB", 5, 0, scheduler,
                             nb_UR)  # le cas REUSE-1 => chaque antenne utilise toute la bande de fréquence
    s.mobilesProches = mobileProche
    s.mobilesLoin = mobileLoin
    s.mobiles = mobileProche + mobileLoin
    s.antennes = [antenneA , antenneB]
    s.connectMobileToAntenne()
    global IS_INTERFERENCE
    IS_INTERFERENCE = True
    print(s.antennes)
    s.start()
    outPutSimu(s)

def EmelineSimulationReuse2AvecBruitExecution(s,nbMobile, scheduler, nb_UR):
    mobileProche , mobileLoin = EmelineScenarioReuse(nbMobile,nb_UR//2)
    antenneA = createAntenne("antenneA", -5, 0, scheduler, nb_UR//2)# le cas REUSE-2 => chaque antenne utilise la moitié de la bande
    antenneB = createAntenne("antenneB", 5, 0, scheduler,
                             nb_UR//2)  # le cas REUSE-2 => chaque antenne utilise la moitié de la bande
    s.mobilesProches = mobileProche
    s.mobilesLoin = mobileLoin
    s.mobiles = mobileProche + mobileLoin
    s.antennes = [antenneA , antenneB]
    s.connectMobileToAntenne()
    global IS_INTERFERENCE
    IS_INTERFERENCE = True
    print(s.antennes)
    s.start()
    outPutSimu(s)

def EmelineScenarioReuse(nbMobile,nb_ur):
    mobileProcheAntenneA = [createMobile(f"ProcheA-{i}", -5, 0,nb_ur) for i in range(nbMobile)]
    mobileProcheAntenneB = [createMobile(f"ProcheB-{i}", 5, 0,nb_ur) for i in range(nbMobile)]
    mobileLoinA = [createMobile(f"Loin-A_{i}", -1, 0,nb_ur) for i in range(nbMobile)]
    mobileLoinB = [createMobile(f"Loin-B_{i}", 1, 0,nb_ur) for i in range(nbMobile)]
    loin = mobileLoinB + mobileLoinA
    proche = mobileProcheAntenneB + mobileProcheAntenneA
    return proche, loin

def EmelineScenarioUneSeuleAntenne(nbMobile,nb_ur):
    mobileProcheAntenneA = [createMobile(f"ProcheA-{i}", -5, 0,nb_ur) for i in range(nbMobile)]
    mobileLoinA = [createMobile(f"Loin-A_{i}", -1, 0,nb_ur) for i in range(nbMobile)]
    loin = mobileLoinA
    proche = mobileProcheAntenneA
    return proche, loin

def multiAntenneScenarioMultiAntenne(nbMobile,nb_ur):
    mobileMicroAntenneA = [createMobile(f"LoinA-{i}", -5, -5,nb_ur) for i in range(nbMobile)]
    mobileMicroAntenneB = [createMobile(f"LoinB-{i}", 5, -5,nb_ur) for i in range(nbMobile)]
    mobileMicroAntenneC = [createMobile(f"LoinC-{i}", 5, 5,nb_ur) for i in range(nbMobile)]
    mobileMicroAntenneD = [createMobile(f"LoinD-{i}", -5, 5,nb_ur) for i in range(nbMobile)]
    mobileCentreA = [createMobile(f"Grosse-A_{i}", -1, -1,nb_ur) for i in range(nbMobile)]
    mobileCentreB = [createMobile(f"Grosse-B_{i}", 1, -1,nb_ur) for i in range(nbMobile)]
    mobileCentreC = [createMobile(f"Grosse-C_{i}", 1, 1,nb_ur) for i in range(nbMobile)]
    mobileCentreD = [createMobile(f"Grosse-D_{i}", -1, 1,nb_ur) for i in range(nbMobile)]
    loin = mobileMicroAntenneA + mobileMicroAntenneB + mobileMicroAntenneC + mobileMicroAntenneD
    proche = mobileCentreD +  mobileCentreC +  mobileCentreB +  mobileCentreA
    return proche , loin


def createAntenne(name,x,y,s,ur):
    return a.Antenne(name,x,y,s,ur)
def createMobile(name,x ,y ,nb_ur):
    return m.Mobile(name , (x,y),nb_ur)

class Simulateur:

    def __init__(self, simulationTime):
        self.currentTic = 0
        self.simulationTime = simulationTime
        self.mobiles = []
        self.antennes = []
    """
    responsable de faire tourner l'horloge.
    Indique à toute les antennes d'effectuer un tic
    """
    def connectMobileToAntenne(self):
        for m in self.mobiles:
            m.connectionAntenne(self.antennes)

    def nextTic(self, ticCourant):
        for a in self.antennes:
            a.nextTic(ticCourant)


    """
    point d'éntree de la simulation
    """
    def start(self):
        print(f"nombre utilisateur {len(self.mobiles)}")
        while(self.currentTic <= self.simulationTime):
            #print(f"tic x {self.currentTic} / {self.simulationTime} tic total" )
            self.nextTic(self.currentTic)
            self.currentTic += 1


def readMobileParameterFile(csvFileName, simulator):
    with open(csvFileName, newline='') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',')
        for ligne in spamreader:
            mobileToAdd = m.Mobile()
            mobileToAdd.setX(int(ligne["x"]))
            mobileToAdd.setY(int(ligne["y"]))
            mobileToAdd.setName(ligne["mobileName"])
            simulator.mobiles.append(mobileToAdd)
        
def readAntenneParameterFile(csvFileName, simulator):
    with open(csvFileName, newline='') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',')
        for ligne in spamreader:
            antenneToAdd = a.Antenne(scheduler =SCHEDULER)
            antenneToAdd.setX(int(ligne["x"]))
            antenneToAdd.setY(int(ligne["y"]))
            antenneToAdd.setName(ligne["antenneName"])
            simulator.antennes.append(antenneToAdd)

def main():
    #setupVariaGlobal(parser.parse_args())
    simulator = Simulateur(SIMULATOR_TIME)
    readAntenneParameterFile(ANTENNES_CSV, simulator)
    if(NB_MOBILES == None):
        readMobileParameterFile(MOBILES_CSV,simulator)
    else:
        import Mobile as m
        a = simulator.antennes[0]
        simulator.mobilesProches = m.Mobile.generatorMobile(NB_MOBILES//2,(a.x+1, a.y ), "mobileProche" )
        simulator.mobilesLoins = m.Mobile.generatorMobile(NB_MOBILES//2,(a.x+10, a.y ), "mobileLong" )
        simulator.mobiles = simulator.mobilesLoins + simulator.mobilesProches
    simulator.connectMobileToAntenne()
    logginBasicInfo(simulator)
    print(simulator.antennes)
    simulator.start()
    outPutSimu(simulator)


def outPutSimu(simulator):
    data = []
    nbUser = len(simulator.mobiles)
    for m in simulator.mobiles:
        # ["NB_USER" , "USER_TYPE", "DELAY", "SPECTRAL_EFFICIENCY", "UR_USAGE", "SPECTRAL_EFFICIENT"]
        if (m.delayMoyen == None):
            m.delayMoyen = 0
        print(m.delayMoyen)
        if(m.antenne.efficaciteSpectral == []):
            print("km")
        data.append([nbUser, m.type, m.delayMoyen, sum(m.antenne.tauxUtilisationMoyen)/len(m.antenne.tauxUtilisationMoyen), SCHEDULER, sum(m.antenne.efficaciteSpectral)/len(m.antenne.efficaciteSpectral)])
    writeHeadCSV(data)


def writeHeadCSV(dataToWrite):

    with open(CSV_OUTPUT, "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        #writer.writerow(["NB_USER" , "USER_TYPE", "DELAY", "UR_USAGE"]) #"SPECTRAL_EFFICIENCY"
        for data in dataToWrite:
            writer.writerow(data)

def logginBasicInfo(simualateur):

    logging.basicConfig(filename=f"Log/info{NOW}.log",
                        level=logging.INFO,
                        format='%(levelname)s: %(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S')
    logging.info('##### PARAMETER #######')
    logging.info(f'NB_MOBILES {NB_MOBILES}')
    logging.info(f'MKN_MIN {MKN_MIN}')
    logging.info(f'MKN_MAX_P {MKN_MAX_P}' )
    logging.info(f'MKN_MAX_L {MKN_MAX_L}')
    logging.info(f'TAILLE_PACKET {TAILLE_PACKET}')
    logging.info(f'SIMULATOR_TIME {SIMULATOR_TIME}')
    logging.info("##### ANTENNES #####")
    logging.info(simualateur.antennes)
    logging.info('##### MOBILES ##### ')
    logging.info(simualateur.mobiles)


def setupVariaGlobal(args):
    Simulateur.NB_UR = args.NB_UR
    Simulateur.TAILLE_PACKET = args.TAILLE_PACKET


if (__name__== "__main__"):
    date = datetime.today().strftime('%Y-%m-%d-%s')
    CSV_OUTPUT = f'Resultat_CSV/simuGrosseAntenneSpectralNuit_{date}.csv'
    with open(CSV_OUTPUT, "w") as csv_file:
        # j'écris l'entête ddu fichier CSV
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(["NB_USER" , "USER_TYPE", "DELAY", "UR_USAGE","SCHEDULER","SPECTRAL_EFFICIENT"]) #"SPECTRAL_EFFICIENCY"

    for x in list(range(1,8)):
        for schedul in [ "RoundRobin","MaxSNR"]:#,"RoundRobin"
            NB_MOBILES = x
            SCHEDULER = schedul
            filename = f"Profiling/Report_Mobile{NB_MOBILES}_ID{number}_{date}.txt"
            number +=1
            #import cProfile
            #import re
            #from pstats import SortKey
            #cProfile.run('main()', filename=filename, sort=SortKey.TIME)

            s = Simulateur(SIMULATOR_TIME)
            # le cas où on a une antenne avec NB_MOBILES mobile proche et NB_MOBILES loin
            # en utilisant le scheduler SCHEDULER pour chaque antenne
            # s: le simulateur
            # NB_UR = taille de la bande fréquence (par défaut = 128 *5 )
            #  ((nbUR * mkn)/taillePacket)/ 20 , 20 étant le nombre d'utilisateurs à partir du quel le système part en congestion
           # global NB_PACKET_PAR_MOBILE
            #EmelineSimulationUneSeuleAntenneReuse1(s, NB_MOBILES, SCHEDULER, NB_UR)# bruit non pris en compte car l'antenne n'as pas de voisin
            #EmelineSimulationUneSeuleAntenneReuse2(s, NB_MOBILES, SCHEDULER, NB_UR)# bruit non pris en compte car l'antenne n'as pas de voisin
            # un conseil: choisissez l'un des 4 scénario de simulation afin d'avoir 4 CSV différent.
            #EmelineSimulationReuse2AvecBruitExecution(s, NB_MOBILES, SCHEDULER, NB_UR)
            #EmelineSimulationReuse1AvecBruitExecution(s, NB_MOBILES, SCHEDULER, NB_UR)

            scenarioMultiAntenne(s, NB_MOBILES , schedul , NB_UR )
            #scenarioGrosseAntenne(s, NB_MOBILES , schedul , NB_UR)


