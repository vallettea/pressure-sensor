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
	("2016-06-09T13_16_18*.txt",100,500,2,0),
	("2016-06-16T13_24_14*.txt",0,200,2,1),
	("2016-06-16T13_47_10*.txt",10,70,2,1),
	("2016-07-16T16_58_03*.txt",0,700,2,0),
	("2016-07-16T17_42_40*.txt",0,6000,2,1),
	("2016-09-02T14_25_11*.txt",0,700,1,1),
	("2016-09-07T19_40_50*.txt",50,250,2,1),
	("2016-09-07T20_00_49*.txt",0,200,2,1),
]

for i,courbe in enumerate(courbes):

	name, xmin,xmax,nb_courbes, inverse = courbe

	xx = []
	yy1 = []
	yy2 = []
	file = glob.glob(name)[0]
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


	error = 51.7149326*0.02*np.ones(len(xx))
	if inverse == 1:
		yy3 = yy2
		yy2 = yy1
		yy1 = yy3

	if nb_courbes == 1:
		fig, (ax0) = plt.subplots(nrows=1, sharex=True)
		ax0.plot(xx, yy1, "k")
		ax0.set_title("Pression")
		ax0.set_xlim([xmin,xmax])
		ax0.set_xlabel('time (s)')
		ax0.set_ylabel('pressure (mmHg)')
		plt.savefig("plots2/plot_" + str(i) + ".png")
	else:

		fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=True)
		# ax0.errorbar(xx, yy1, yerr=error, fmt='-')
		ax0.plot(xx, yy1, "k")
		ax0.set_title("Pression d'entrée")
		ax0.set_xlim([xmin,xmax])
		ax0.set_ylabel('pressure (mmHg)')

		s = UnivariateSpline(xx, yy2, s=1)
		xs = linspace(xmin, xmax, len(yy2))
		ys = s(xs)
		ax1.set_title("Pression de sortie")
		# ax1.errorbar(xx, yy2, yerr=error, fmt='-')
		ax1.plot(xx, yy2, "k")
		ax1.plot(xs, ys, "r")
		ax1.set_xlim([xmin,xmax])
		ax1.set_xlabel('time (s)')
		ax1.set_ylabel('pressure (mmHg)')
	plt.savefig("plots2/plot_" + str(i) + ".png")