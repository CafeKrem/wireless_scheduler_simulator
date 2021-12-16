import numpy as np
import matplotlib.pyplot as plt


fig = plt.figure()
x = np.arange(10)
y = 2.5 * np.sin(x / 20 * np.pi)
yerr = np.linspace(0.05, 0.2, 10)

plt.errorbar([i for i in range (0,17,2)], [0, 2, 4, 4, 6, 8, 10, 15, 18], yerr=None, label='both limits (default)')

### Si on veut une seconde courbe

#plt.errorbar(x, y + 2, yerr=yerr, uplims=True, label='uplims=True')

#plt.errorbar(x, y + 1, yerr=yerr, uplims=True, lolims=True,
#              label='uplims=True, lolims=True')

upperlimits = [True, False] * 5
lowerlimits = [False, True] * 5
plt.errorbar(x, y, yerr=yerr, uplims=upperlimits, lolims=lowerlimits,
             label='subsets of uplims and lolims')

plt.legend(loc='lower right')
plt.show()