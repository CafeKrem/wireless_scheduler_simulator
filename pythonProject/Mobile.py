from random import SystemRandom, randint

import math
import pythonProject.Simulateur as s
import pythonProject.Packet as p
from numpy import random


class Mobile:

    def __init__(self, name="a", coord=(1,1),nb_ur=128*5):
        self.name = name
        self.x = coord[0]
        self.y = coord[1]
        self.buffer = []
        self.bitsNeeded = 0
        self.lenMKn= nb_ur
        self.tableauMknInstane = [-1 for x in range(nb_ur)]
        self.delayMoyen = None
        self.nbPacket = 0
        self.antenne = None
        # self.mknMoyen # généré à partir de la distance
        # self.tableauMknInstane #tableau des mkn généré pour chaque bande de fréquence
        # self.antenne  # référence vers l'antennes avec laquelle elle est connecté.
    def genereMknMoyen(self):
        if(self.isProche()):
            self.mknMoyen = 20
        else:
            self.mknMoyen = 15

    def setY(self, y):
        # assert(y is int)
        self.y = y

    def isProche(self):
        return self.distanceEntreAntenneMobilet((self.antenne.x,self.antenne.y)) < 2
    def setX(self, x):
        # assert(x is int)
        self.x = x

    def setAntenne(self, antenne):
        if(self.antenne == None):
            self.antenne = antenne
            self.antenne.addMobile(self)
        else:
            self.antenne.removeMobile(self)
            self.antenne = antenne
            self.antenne.addMobile(self)
    def __str__(self):
        return self.name + " at position (" + str(self.x) + "," + str(self.y) + ")"

    def __repr__(self):
        return self.__str__()

    def setName(self, name):
        # assert(name is str)
        self.name = name
    def __eq__(self, value):
        return self.name == value.name
    def __hash__(self):
        return hash(self.name)
    def packetArrive(self, packet,ticCourant):
        self.buffer.pop(0)
        packet.tempsArrivee = ticCourant
        self.ajoutDelaiMoyen(packet.calcul_Temps_Transmission())
    def genereMknInstantane(self):
        if self.type == "PROCHE":
            for i in range(self.lenMKn):
                self.tableauMknInstane[i] =self.mknInstant(15000000,5 , 1)
        else:
            if(s.IS_INTERFERENCE):
                # on prend en compte le bruit/ les intérférences
                for i in range(self.lenMKn):
                    self.tableauMknInstane[i] = self.mknInstant(5000000, 20, 10)
            else:
                # on ne prend pas en compte le bruit/ les intérférences
                for i in range(self.lenMKn):
                    self.tableauMknInstane[i] =self.mknInstant(5000000, 20 , 1)
        return self.tableauMknInstane

    def mknInstant(self, puissance, distance, bruit):
        haut = 3 * puissance * random.rayleigh() * (1 / pow(distance, 2))
        return math.floor(math.log((1 + (haut / bruit)), 2))

    def ajoutDelaiMoyen(self, delai):
        if(self.delayMoyen == None):
            self.delayMoyen = delai
            self.nbPacket += 1
        else:
            self.nbPacket += 1
            self.delayMoyen = (self.delayMoyen * (self.nbPacket - 1) + delai)/self.nbPacket

    
    def distanceEntreAntenneMobilet(self, antenne: tuple):
        p1 = antenne
        p2 = (self.x,self.y)
        
        distance = math.sqrt( ((int(p1[0])-int(p2[0]))**2)+((int(p1[1])-int(p2[1]))**2) )
        return distance
    
    def connectionAntenne(self, listAntenne: list):
        min=None
        antennechoisie = None
        for antenne in listAntenne:
            distance = self.distanceEntreAntenneMobilet((antenne.x, antenne.y))
            if min == None:
                min = distance
                antennechoisie = antenne
                
            if distance < min:
                min = distance
                antennechoisie = antenne
        self.setAntenne(antennechoisie)
        if(self.isProche()):
            self.type = "PROCHE"
        else:
            self.type = "LOIN"
        self.genereMknMoyen()
    def decrementBitsNeeded(self,bitcosomer):
        if(self.bitsNeeded < bitcosomer):
            print("klm")
        self.bitsNeeded -= bitcosomer
    def createPacket(self, ticCourant,taillePacket=s.TAILLE_PACKET):
        packet = p.Packet(self, ticCourant,taille=taillePacket)
        self.bitsNeeded += packet.taille
        self.buffer.append(packet)

    def generatorMobile(nb_mobile:int, coordoner:tuple, nom:str):
        return [Mobile(nom+str(i), coordoner) for i in range(nb_mobile)]



if(__name__ == "__main__"):
    m = Mobile()
    # print(m.genereMknInstantane(4))
    print(Mobile.generatorMobile(10, (0,1), "A"))
    # mobilepositioninit = [0,1]
    # listeAntenne = {"A":[0,0], "B":[10, 11], "C": [30,20]}
    # r = Mobile()
    # print(r.connectionAntenne(listeAntenne))

    
