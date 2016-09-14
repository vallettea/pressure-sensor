# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

xx = []
yy1 = []
yy2 = []
with open("2016-06-16T13-24-14.973122.txt", "r") as input:
	
	try:
		data = input.read().split('\n')

		for line in data:
			x, y1, y2 = line.split(";")
			xx += [int(x)]
			yy1 += [float(y1)]
			yy2 += [float(y2)]
	except:
		pass


error = 51.7149326*0.02*np.ones(len(xx))


fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=True)
# ax0.errorbar(xx, yy1, yerr=error, fmt='-')
ax0.plot(xx, yy1)
ax0.set_title("Pression d'entrée")

# ax1.errorbar(xx, yy2, yerr=error, fmt='-')
ax1.plot(xx, yy2)
ax1.set_title("Pression de sortie")
plt.show()