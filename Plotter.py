from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
import pandas as pd
import numpy as np
import threading
import serial
import time
import sys


class AddPlot:

	def __init__(self, dict, parent, filepath):
		self.dict = dict
		self.filepath = filepath
		self.datas = list(self.dict['dataList'].keys())
		self.devices = list(self.dict['deviceList'].keys())

		for i in range(len(self.datas)+len(self.devices)):
			if i < len(self.datas):
				self.addPlot(parent, self.datas[i])
			else:
				i -= len(self.datas)
				self.addPlot(parent, self.devices[i])

	def plotDevice(self, name):
		xaxis = self.dict['deviceList'][name]['X-axis']
		yaxis = self.dict['deviceList'][name]['Y-axis']
		ser = serial.Serial(name)
		ax = self.figure.add_subplot(1, 1, 1)
		row = int(xaxis[0][4])
		column = int(yaxis[0][4])

		plotList_x = []
		plotList_y = []

		while True:
			readings = ser.readline().decode('utf-8').split(',')
			readings[-1] = readings[-1][:-2]
			try:
				plotList_x.append(float(readings[row]))
				plotList_y.append(float(readings[column]))
				time.sleep(0.1)
			except ValueError:
				pass
			ax.plot(plotList_x, plotList_y)


	def addPlot(self, parent, name):
		self.widget = QWidget()
		self.figure = plt.figure()
		self.canvas = FigureCanvasQTAgg(self.figure)
		self.toolbar = NavigationToolbar2QT(self.canvas, parent)

		layout = QVBoxLayout()
		layout.addWidget(self.canvas)
		layout.addWidget(self.toolbar)
		self.widget.setLayout(layout)

		parent.insertTab(parent.count()-1, self.widget, name)
		parent.setCurrentIndex(parent.count()-2)

		if name in self.datas:
			xaxis = self.dict['dataList'][name]['X-axis']
			yaxis = self.dict['dataList'][name]['Y-axis']
			fileData = pd.read_csv(self.filepath[0], index_col=0)
			ax = self.figure.add_subplot(1, 1, 1)

			xdata = list(fileData[xaxis[0]])
			ydata = list(fileData[yaxis[0]])

			len_x = len(xdata)
			len_y = len(ydata)

			ax.plot(xdata, ydata)
			plt.xlabel(','.join(xaxis))
			plt.ylabel(''.join(yaxis))

			plt.xticks(np.arange(0, len_x, int(len_x/10)))
			plt.yticks(np.arange(0, len_y, int(len_y/10)))

			plt.grid()

		elif name in self.devices:
			plotdevice = threading.Thread(target=self.plotDevice(name))
			fileData = plotdevice.start()	
