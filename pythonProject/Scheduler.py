import abc


#@abc.abstractClass
class Scheduler:
    """
    cette méthode s'occupe d'allouer les unités de ressource au mobile en fonction du type de scheduler
    :param: #antenne ()
    :param: # listMobiles
    :param: #snrmap=mapMobileMkn(tableau de mkn (taille 128))
    :param: #mapUniteRessource

    """
    

    @abc.abstractmethod
    def allocuteUR(self, mapMobileMkn,longueurUR):
        pass
