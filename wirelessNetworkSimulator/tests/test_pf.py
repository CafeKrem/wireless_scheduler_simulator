import wirelessNetworkSimulator.tests.test_Scheduler as scheduler
from wirelessNetworkSimulator.pf import pf


class Testpf(scheduler.TestScheduler):

    def newScheduler(cls):
        return pf()
    def test_allocate_ur(self):
        nb_ur = 4
        packet_Size = 1000
        mobileProche = self.createMobile("Proche", 0, 0, nb_ur)
        mobileLoin = self.createMobile("Loin", 0, 0, nb_ur)
        mobileLoin.previousUR = [3,3,3,3]
        mobileProche.previousUR = [8,9,9,10]
        # createPacket need the current tic,
        currentTic = 0
        # here I just want to test if maxSNR work correctly I ignore the packet_Size
        mobileProche.createPacket(currentTic, packet_Size)
        mobileLoin.createPacket(currentTic, packet_Size)
        mapMobileMkn = {mobileProche:
                            [10, 5, 5, 7],
                        mobileLoin:
                            [7, 7, 7, 1]}
        table = self.scheduler.allocateUR(mapMobileMkn, nb_ur)
        self.assertEqual(list(map(lambda x: x[0].name, table)),
                         [mobileLoin.name, mobileLoin.name, mobileLoin.name, mobileProche.name])
        self.assertEqual(list(map(lambda x: x[1], table)), [7, 7, 7, 7])
