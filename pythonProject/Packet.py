import Simulateur


class Packet:

    def __init__(self,mobile,  tempsReelCourant:int,taille:int = Simulateur.TAILLE_PACKET  ):
        self.tempsDepart = tempsReelCourant
        self.tempsArrivee = None
        self.tailleInitiale = taille
        self.taille = taille
        self.nom = mobile.name
        self.mobile = mobile

    def calcul_Temps_Transmission(self):
        self.tempsTransmission = self.tempsArrivee - self.tempsDepart
        return self.tempsTransmission

    def decrementation_Taille_Paquet(self, nbreBits, tempsArrivee):
        self.taille = self.taille - nbreBits
        self.tempsReelCourant = tempsArrivee
    
    def consomateur_Bit(self, bitcosomer:int):
        if self.taille <= bitcosomer:
            r = bitcosomer - self.taille
            self.taille = 0
            self.mobile.decrementBitsNeeded(bitcosomer - r)
            return r
        else:
            self.taille -= bitcosomer
            self.mobile.decrementBitsNeeded(bitcosomer)
            return 0
        
