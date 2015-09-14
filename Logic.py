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
		self.application.elements = {}
	
	
	def processConstructionFile(self, constructionFile):
		self.application.construction = Construction(constructionFile)
		self.drawConstruction()
	
	
	def offsetFunc(self, realSize, virtSize):
		return 40
	
	
	def drawConstruction(self):
		self.application.elements = {}
		self.application.mainWindow.graph.clear()
		self.application.mainWindow.graph.setVirtualSize(self.application.construction.size())
		
		# Ось Oy рисуем до элементов, чтобы поверх неё отобразилась ось узла (x = 0)
		self.application.mainWindow.graph.drawCoordinateAxisY()
		
		for element in self.application.construction.elements:
			elID = None
			if type(element) == Bar:
				# print("Стержень: %s" % element)
				elID = self.application.mainWindow.graph.drawBar(element.x,
																 element.L, element.height,
																 element.q,
																 fill = "yellow",
																 activefill = "orange")
			else:
				elID = self.application.mainWindow.graph.drawNode(element.x, element.F)
			
			self.application.elements[elID] = element
		
		# Ось Ox рисуем после элементов, чтобы её было видно
		self.application.mainWindow.graph.drawCoordinateAxisX()
	
	
	def elementDescStr(self, elementID):
		return self.application.elements[elementID].__str__()
