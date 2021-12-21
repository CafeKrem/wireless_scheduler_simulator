import abc


#@abc.abstractClass
from pythonProject.Mobile import Mobile


class Scheduler:
    """
    cette méthode s'occupe d'allouer les unités de ressource au mobile en fonction du type de scheduler
    :param: #antenne ()
    :param: # listMobiles
    :param: #snrmap=mapMobileMkn(tableau de mkn (taille 128))
    :param: #mapUniteRessource
    """
    def allocateUR(self, mapMobileMkn, longueurUR):
        data = [None for x in range(longueurUR)]
        dictBitsNeededMobile = {m: m.bitsNeeded for m in mapMobileMkn.keys()}
        if (mapMobileMkn == {}):
            return data
        for index in range(longueurUR):
            tuple = self.findMaxOfIndice(mapMobileMkn, index)
            dictBitsNeededMobile[tuple[0]] = dictBitsNeededMobile[tuple[0]] - tuple[1]
            data[index] = tuple
            if (dictBitsNeededMobile[tuple[0]] <= 0):
                mapMobileMkn.pop(tuple[0])
                if (mapMobileMkn == {}):
                    return data
        return data

    """
    :param: mapMobileMkn contains an association of Mobile and a list of Mkn
    :ptype: dict(Mobile,list)
    :return: return a tuple of Mobile and allocated Mkn
    :rtype: (Mobile, int)
    """
    @abc.abstractmethod
    def findMaxOfIndice(self,mapMobileMkn,index) -> (Mobile,int):
        pass
