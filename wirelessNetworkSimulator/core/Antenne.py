from random import randint
import statistics
import wirelessNetworkSimulator.core.Simulateur as s
import wirelessNetworkSimulator.core.scheduler.Scheduler as sch
class Antenne:
    @staticmethod
    def getScheduler(scheduler):
        classIndex = list(map(lambda x: x.__name__, sch.Scheduler.__subclasses__())).index(scheduler)
        return sch.Scheduler.__subclasses__()[classIndex]

    def __init__(self, name=None, x1=None, y=None, scheduler='RoundRobin', nb_UR=None):
        self.name = name
        self.x = x1
        self.y = y
        if(self.nb_UR == None):
            self.nb_UR = s.NB_UR
        else:
            self.nb_UR = nb_UR
        self.mobiles = []
        self.mknMoyen =None
        self.scheduler = Antenne.getScheduler(scheduler)()
        self.tauxUtilisationMoyen = []
        self.efficaciteSpectral = []
        self.nbPacketMoyen = None
    def setScheduler(self,sec ):
        self.scheduler = self.getScheduler(sec)
    def setX(self, x):
        self.x = x
    def setY(self,y):
        self.y = y
    def setName(self, name):
        self.name = name
    def setScheduler(self, scheduler):
        self.scheduler = scheduler

    def __repr__(self):
        return self.__str__()
    def __str__(self):

        res=f'antenne {self.name} with couple { (self.x, self.y)} \n'
        res += f'\tmobiles\t: {self.mobiles}\n'
        res += f'\tscheduler\t: {self.scheduler.__class__.__name__}\n'
        return res
    def addMobile(self, mobile):
        self.mobiles.append(mobile)
    
    def removeMobile(self, mobile):
        self.mobiles.remove(mobile)
    def distance(self, mobile):
        pass
    def envoie_packet(self, mobile):
        pass
    def generePacket(self ):
        pass
    def getMknMoyen(self):
        if(self.mknMoyen == None):
            self.mknMoyen = statistics.mean(list(map(lambda x: x.mknMoyen, self.mobiles)))
        return self.mknMoyen

    def nextTic(self, ticCourant):
        #nbPacketMoyenParMobile = self.nbPacketParMobile(s.NB_UR, s.TAILLE_PACKET, self.getMknMoyen())
        # print(nbPacketMoyenParMobile)
       # print(f"nombre de packets Moyen généré par mobile {s.NB_PACKET_PAR_MOBILE}")
        for m in self.mobiles:
            for x in range(randint(0 , s.NB_PACKET_PAR_MOBILE *2 )):
                m.createPacket(ticCourant)
        mobileParlant = list(filter(lambda x: x.buffer != [],self.mobiles))
        mobileMkn = {x : x.genereMknInstantane() for x in mobileParlant}#x.mknMoyen
        tableauAffectation = self.scheduler.allocateUR(mobileMkn, self.nb_UR)
        self.addTauxUtilisationUR(tableauAffectation, ticCourant)
        self.addEfficaciteSpectral(tableauAffectation, ticCourant)
        for tuple in tableauAffectation:
            if(tuple == None):
                continue
            m, mkn = tuple
            if(m.buffer == []):
                continue
            bitRestant = m.buffer[0].consomateur_Bit(mkn)
            while(bitRestant != 0):
                packet = m.buffer[0]
                m.packetArrive(packet, ticCourant)
                if(m.buffer == []):
                    bitRestant = 0
                if(m.buffer != []):
                    bitRestant = m.buffer[0].consomateur_Bit(bitRestant)

    def nbPacketParMobile(self, nb_ur , taille_packet , mknMoyen):
        if(self.nbPacketMoyen == None):
            self.nbPacketMoyen = int((nb_ur * mknMoyen) / taille_packet/ 16)
            print(f"nombre de packet moyen {self.nbPacketMoyen}")
            print(f"mkn moyen {self.nbPacketMoyen}")
            return self.nbPacketMoyen
        else:
            return int((nb_ur * mknMoyen) / taille_packet / 16)
        
    def addTauxUtilisationUR(self, ur, ticCourant):
        if (ticCourant % 500 == 0):
            self.tauxUtilisationMoyen.append(1 - ur.count(None)/self.nb_UR)
        """
        if(self.tauxUtilisationMoyen == None):
            self.tauxUtilisationMoyen = 1 - ur.count(None)/self.nb_UR
        else:
            self.tauxUtilisationMoyen = (self.tauxUtilisationMoyen* ticCourant +  (1 - ur.count(None)/self.nb_UR))/ (ticCourant + 1)
         
         """   #print(self.tauxUtilisationMoyen)
    def addEfficaciteSpectral(self, ur, ticCourant):
        if(ticCourant % 500 == 0):
            #filterList = map(lambda x: x[1],list(filter(lambda x: x != None , ur)))
            filterList = list(map(lambda x: x[1], list(filter(lambda x: x != None, ur))))
            if(filterList == []):
                return None
            self.efficaciteSpectral.append(sum(filterList)/len(filterList))
