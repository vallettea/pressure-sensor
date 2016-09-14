# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import glob
from scipy.interpolate import UnivariateSpline
from numpy import linspace

courbes = [
	("2016-05-03T15_03_27*.txt",0,250,2,0),
	("2016-05-03T15_39_25*.txt",0,300,2,0),
	("2016-06-09T13_16_18*.txt",100,325,2,0),
	("2016-06-16T13_24_14*.txt",0,1100,2,1),
	("2016-06-16T13_47_10*.txt",10,60,2,1),
	("2016-07-16T16_58_03*.txt",0,700,2,0),
	("2016-07-16T17_42_40*.txt",0,5900,2,1),
	("2016-09-02T14_25_11*.txt",0,700,1,1),
	("2016-09-07T19_40_50*.txt",50,200,1,1),
]

for i,courbe in enumerate(courbes):

	name, xmin,xmax,nb_courbes, inverse = courbe

	xx = []
	yy1 = []
	yy2 = []
	file = glob.glob("../data/" + name)[0]
	with open(file, "r") as input:
		
		try:
			data = input.read().split('\n')

			for line in data:
				x, y1, y2 = line.split(";")
				xx += [int(x)]
				yy1 += [float(y1)]
				yy2 += [float(y2)]
		except:
			pass


	
	if inverse == 1:
		yy3 = yy2
		yy2 = np.array(yy1)
		yy1 = np.array(yy3)
	else:
		yy2 = np.array(yy2)
		yy1 = np.array(yy1)

	yy2 = yy2 - yy2[0]*np.ones(len(yy2))

	if nb_courbes == 1:
		fig, (ax0) = plt.subplots(nrows=1, sharex=True)
		ax0.plot(xx, yy1, "k")
		ax0.set_title("Pression d'injection")
		ax0.set_xlim([xmin,xmax])
		ax0.set_xlabel('Temps (s)')
		ax0.set_ylabel('pressure (mmHg)')
		plt.savefig("../figs/plot_" + str(i) +"_" + name + ".png")
	else:

		fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=True)
		error1 = yy1*0.02
		ax0.errorbar(xx, yy1, yerr=error1, fmt='-', c="k")
		# ax0.plot(xx, yy1, "k")
		if i == 5 or i == 6:
			ax0.set_title("Pression bouteille A")
		else:
			ax0.set_title("Pression intra-crânienne")
		ax0.set_xlim([xmin,xmax])
		ax0.set_ylabel('pressure (mmHg)')

		win = int(len(xx)/100)
		s = UnivariateSpline(xx, yy2, s=win)
		xs = linspace(xmin, xmax, len(yy2))
		ys = s(xs)
		if i == 5 or i == 6:
			ax0.set_title("Pression bouteille B")
		else:
			ax1.set_title("Pression peri-lymphatique")
		error2 = yy2*0.02
		ax1.errorbar(xx, yy2, yerr=error2, fmt='-', c="k")
		ax1.plot(xx, yy2, "k")
		ax1.plot(xs, ys, "r", lw=2)
		ax1.set_xlim([xmin,xmax])
		ax1.set_xlabel('Temps (s)')
		ax1.set_ylabel('pressure (mmHg)')
	plt.savefig("../figs/plot_" + str(i) + "_" + name + ".png")