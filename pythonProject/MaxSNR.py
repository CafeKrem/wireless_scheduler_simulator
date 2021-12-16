import Scheduler as sch


class MaxSNR(sch.Scheduler):

    ###
    # je prends en compte le MaxSNR pour l'allocation des unités de ressources
    
    def findMaxOfIndice(dictionnaire: dict, indice: int):
        max = 0
        m =''
        if((dictionnaire == None)):
            return None
        for mobile,value in dictionnaire.items():
            valueIndice = value[indice]
            if valueIndice > max:
                max = valueIndice
                m = mobile
        return (m,max)

    def findNameOfValue(dictionnaire: dict, max: int):
        for value in dictionnaire.items():
            if (value[1][0] == max) or (value[1][1] == max):
                return value[0]

    def allocuteUR(self, mapMobileMkn,longueurUR):
        data = [None for x in range(longueurUR)]
        dictDemandeMobile = {m:m.bitsNeeded for m in mapMobileMkn.keys()}
        if(mapMobileMkn== {}):
            return data
        for index in range(longueurUR):
            tuple = MaxSNR.findMaxOfIndice(mapMobileMkn, index)
            dictDemandeMobile[tuple[0]] = dictDemandeMobile[tuple[0]] - tuple[1]
            if(dictDemandeMobile[tuple[0]] <= 0):
                mapMobileMkn.pop(tuple[0])
                if(mapMobileMkn == {}):
                    data[index] = tuple
                    return  data
            data[index]=tuple
        return data


if(__name__ == "__main__"):
    ledictionnaire = {"Antoine": [42, 56, 4, 3, 34], "Mathieu": [34, 52, 5, 2, 5], "clement": [12, 14, 12, 1, 1], "Emeline": [1, 41, 12, 18, 0]}
    r = MaxSNR()
    print(r.allocuteUR(ledictionnaire,5))
