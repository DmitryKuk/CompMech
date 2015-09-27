#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

import math
from sympy import *

from Construction import Construction
from Bar import Bar
from Node import Node


class Logic:
	def __init__(self, application):
		self.application = application
		
		self.application.construction = Construction()
		self.application.elements = {}
	
	
	def processConstructionFile(self, constructionFile, showMessage = None, showError = None):
		try:
			self.application.construction = Construction(constructionFile, showMessage, showError)
		except Exception as e:
			if showError is not None:
				showError(str(e))
		self.drawConstruction()
	
	
	def offsetFunc(self, realSize, virtSize):
		return 40
	
	
	def drawConstruction(self):
		self.application.elements = {}
		self.application.mainWindow.graph.clear()
		self.application.mainWindow.graph.setVirtualSize(self.application.construction.size())
		self.application.mainWindow.graph.setMaxLoads(*self.application.construction.loads())
		
		# Ось Oy рисуем до элементов, чтобы поверх неё отобразилась ось узла (x = 0)
		self.application.mainWindow.graph.drawCoordinateAxisY()
		
		# Сначала рисуем только стержни, чтобы нагрузки узлов отображались поверх них
		for element in self.application.construction.elements:
			if type(element) == Bar:
				IDs = self.application.mainWindow.graph.drawBar(element)
				for ID in IDs: self.application.elements[ID] = element
		
		# Рисуем узлы (с нагрузками)
		for element in self.application.construction.elements:
			if type(element) == Node:
				IDs = self.application.mainWindow.graph.drawNode(element)
				for ID in IDs: self.application.elements[ID] = element
		
		# Ось Ox рисуем после элементов, чтобы её было видно
		self.application.mainWindow.graph.drawCoordinateAxisX()
		
		self.application.mainWindow.graph.setTitle("Конструкция")
	
	
	def elementDescStr(self, elementID):
		return str(self.application.elements[elementID])
	
	
	def calculate(self):
		self.application.construction.calculate()
		
		print("A =")
		pprint(self.application.construction.A)
		print("\nb =")
		pprint(self.application.construction.b)
		print()
