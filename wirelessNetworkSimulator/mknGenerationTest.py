def mknInstant( puissance, distance, bruit):
    from numpy import random
    import math

    haut = 3 * puissance * random.rayleigh() * (1 / pow(distance, 2))
    return math.floor(math.log((1 + (haut / bruit)), 2))

lproche = [mknInstant(15000000,5 , 1)for x in range(100000)]
lloin = [mknInstant(5000000,20 , 10) for x in range(100000)]
import statistics
print(f"loin min {min(lloin)} max {max(lloin)} mean {statistics.mean(lloin)}")
print(f"proche min {min(lproche)} max {max(lproche)} mean {statistics.mean(lproche)}")
import pandas as pd
import matplotlib.pyplot as plt
dProche = pd.DataFrame(lproche)
print(dProche)
dProche.plot(kind='hist')
plt.savefig("histoProche")
dLoin = pd.DataFrame(lloin)
dLoin.plot(kind='hist')
plt.savefig("histoLoinBruit")