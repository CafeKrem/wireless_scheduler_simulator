from Scheduler import Scheduler

class RoundRobin(Scheduler):
    """
    j'alloue les ressources grâce à l'algorithme round robin
    """
    
    def allocuteUR(self, mapMobileMkn, longueurUR):
        data = [None for x in range(longueurUR)]
        if(mapMobileMkn == {} ):
            return data
        dictDemandeMobile = {m: m.bitsNeeded for m in mapMobileMkn.keys()}
        for index in range (longueurUR):
            nom=index%len(list(mapMobileMkn.items()))
            data[index] = list(mapMobileMkn.items())[nom][0], list(mapMobileMkn.items())[nom][1][index]
            dictDemandeMobile[ data[index][0]] = dictDemandeMobile[ data[index][0]] -  data[index][1]
            if (dictDemandeMobile[ data[index][0]] <= 0):
                mapMobileMkn.pop( data[index][0])
                if (mapMobileMkn == {}):
                    return data
        return data
            
            
    
if(__name__ == "__main__"):
    ledictionnaire = {"Antoine": [42, 56, 4, 3, 34], "Mathieu": [34, 52, 5, 2, 5], "clement": [12, 14, 12, 1, 0], "Emeline": [1, 41, 12, 18, 0]}
    r=RoundRobin()
    print( r.allocuteUR(ledictionnaire))
    
