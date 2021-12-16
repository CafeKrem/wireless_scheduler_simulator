import Mobile
from Antenne import Antenne

"""
calcule la distance entre un mobile et une antenne
"""


def distance(antenne, mobile):
    assert (isinstance(antenne, Antenne))
    assert (isinstance(mobile, Mobile))
    # calcule la distance


"""
calcule le mkn, c'est à dire le nombre de bits pour une mobile k sur une unité de resource n
"""


def mKNInstantane(antenne, mobile):
    assert (isinstance(antenne, Antenne))
    assert (isinstance(mobile, Mobile))
    # produit le Mkn avec de l'aléatoire avec un poids sur la distance


"""
genère des packets. en instanciant la class Packet
"""


def generateurPacket():


# TODO

"""
renvoie le temps nécéssaire à l'envoie d'un packet de l'antenne au mobile
"""


def tempsTransmission(antenne, mobile):
    assert (isinstance(antenne, Antenne))
    assert (isinstance(mobile, Mobile))
