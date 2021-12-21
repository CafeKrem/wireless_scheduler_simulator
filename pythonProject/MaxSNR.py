import pythonProject.Scheduler as sch

class MaxSNR(sch.Scheduler):

    ###
    # je prends en compte le MaxSNR pour l'allocation des unités de ressources

    def findMaxOfIndice(self,dictionnaire: dict, frequencyIndex: int):
        maxPy = max(dictionnaire.items(), key=lambda x: x[1][frequencyIndex])
        return (maxPy[0],maxPy[1][frequencyIndex])
