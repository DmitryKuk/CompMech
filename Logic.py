#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

import math

from Construction import Construction
from Bar import Bar
from Node import Node

class Logic:
	def emptyConstruction(self):
		return Construction()
	
	
	def getConstructionFromFile(self, constructionFile):
		return Construction(constructionFile)
	
	
	def size(self, construction):
		return construction.size()
	
	
	def offsetWEFunc(self, realSize, virtSize):
		return 40
	
	
	def offsetNSFunc(self, realSize, virtSize):
		return 40 #realSize[1] * 0.15
	
	
	def drawConstruction(self, construction, graph):
		graph.clear()
		graph.setVirtualSize(self.size(construction))
		
		x = 0
		for element in construction.elements:
			if type(element) == Bar:
				# print("Стержень: %s" % element)
				graph.drawBar(x, element.L, math.sqrt(element.A), fill = "yellow")
				x += element.L
		
		graph.drawCoordinateAxis()
