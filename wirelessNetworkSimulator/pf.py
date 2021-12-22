from wirelessNetworkSimulator.Scheduler import Scheduler
from wirelessNetworkSimulator.Mobile import Mobile
from statistics import mean


class pf(Scheduler):
    def getPreviousMkn(self, mapMobileMkn):
        if(self.previousMkn is None):
            self.previousMkn = { m:mean(m.previousUR) for m in mapMobileMkn.keys() }
    def findMaxOfIndice(self, mapMobileMkn, index) -> (Mobile, int):
        self.getPreviousMkn(mapMobileMkn)
        mobile = max(mapMobileMkn, key=lambda x: (mapMobileMkn[x][index]/self.previousMkn[x]))
        return (mobile,mapMobileMkn[mobile][index])

    def allocateUR(self, mapMobileMkn, URSize):
        self.previousMkn = None
        return super().allocateUR(mapMobileMkn, URSize)

