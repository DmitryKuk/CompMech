#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

import math

from Construction import Construction
from Bar import Bar
from Node import Node


class Logic:
	def __init__(self, application):
		self.application = application
		
		self.application.construction = Construction()
	
	
	def processConstructionFile(self, constructionFile):
		self.application.construction = Construction(constructionFile)
		self.drawConstruction()
	
	
	def offsetFunc(self, realSize, virtSize):
		return 40
	
	
	def drawConstruction(self):
		self.application.mainWindow.graph.clear()
		self.application.mainWindow.graph.setVirtualSize(self.application.construction.size())
		
		x = 0
		for element in self.application.construction.elements:
			if type(element) == Bar:
				# print("Стержень: %s" % element)
				self.application.mainWindow.graph.drawBar(x, element.L, math.sqrt(element.A),
														  fill = "yellow")
				x += element.L
		
		self.application.mainWindow.graph.drawCoordinateAxis()
