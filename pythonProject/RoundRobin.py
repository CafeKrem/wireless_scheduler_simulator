from pythonProject.Scheduler import Scheduler

class RoundRobin(Scheduler):


    def findMaxOfIndice(self, mapMobileMkn,index):
        name = index % len(mapMobileMkn)
        tuple = list(mapMobileMkn.items())[name][0], list(mapMobileMkn.items())[name][1][index]
        return tuple
            
