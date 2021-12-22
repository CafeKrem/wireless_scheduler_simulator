from abc import abstractmethod
from unittest import TestCase
from wirelessNetworkSimulator.Mobile import Mobile
from wirelessNetworkSimulator.Scheduler import Scheduler


class TestScheduler(Scheduler, TestCase):
    NB_UR = 32
    TAILLE_PACKET = 40

    def setUp(self) -> None:
        super(TestScheduler, self).setUp()
        self.scheduler = self.newScheduler()
    """
    :return: return a new scheduler
    """
    @abstractmethod
    def newScheduler(self):
        pass
    def test_allocate_ur(self):
        mobilesMkn = {}
        scheduledTable = self.scheduler.allocateUR(mobilesMkn, self.NB_UR)
        self.assertEqual(scheduledTable.count(None), self.NB_UR)

    @staticmethod
    def createMobile(name, x, y, nb_ur):
        return Mobile(name, (x, y), nb_ur)

    def test_allocate_ur_1(self):
        mobile = TestScheduler.createMobile("testMobile" , 0 , 0 , self.NB_UR)
        # createPacket need the current tic,
        currentTic = 0
        mobile.previousUR = [8, 9, 9, 10]# magic number ignore it, it's only used by pf
        mobile.createPacket(currentTic,self.TAILLE_PACKET)
        mapMobileMkn = {mobile : [10 for i in range(self.NB_UR)]}
        table = self.scheduler.allocateUR(mapMobileMkn,self.NB_UR)
        self.assertEqual(table.count(None), self.NB_UR - 4 ) # 4 unite resource will be allocate for 'testMobile'