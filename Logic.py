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
		self.application.mainWindow.onConstructionChanged()
	
	
	def offsetFunc(self, realSize, virtSize):
		return (40, 40, 40, 40)
	
	
	def drawConstruction(self, drawElements = True, drawLoads = True,
						 drawN = False, drawu = False, drawSigma = False):
		self.application.elements = {}
		
		graph = self.application.mainWindow.graph
		graph.clear()
		
		# Устанавливаем максимальные нагрузки
		graph.setVirtSize(self.application.construction.size())
		graph.setMaxLoads(*self.application.construction.loads())
		graph.setMaxComponents(*self.application.construction.components())
		
		# Ось Oy рисуем до элементов, чтобы поверх неё отобразилась ось узла (x = 0)
		graph.drawCoordinateAxisY()
		
		# Сначала рисуем только стержни, чтобы нагрузки узлов отображались поверх них
		for element in self.application.construction.elements:
			if type(element) == Bar:
				IDs = graph.drawBar(element, drawElements, drawLoads)
				for ID in IDs: self.application.elements[ID] = element
		
		# Рисуем узлы (с нагрузками)
		for element in self.application.construction.elements:
			if type(element) == Node:
				IDs = graph.drawNode(element, drawElements, drawLoads)
				for ID in IDs: self.application.elements[ID] = element
		
		# Рисуем эпюры
		if (drawN or drawu or drawSigma) and self.calculated():
			for element in self.application.construction.elements:
				if type(element) == Bar:
					IDs = graph.drawBarCurves(element, drawN, drawu, drawSigma)
					for ID in IDs: self.application.elements[ID] = element
		
		# Ось Ox рисуем после элементов, чтобы её было видно
		graph.drawCoordinateAxisX()
		
		graph.setTitle("Конструкция")
	
	
	def elementDescStr(self, elementID):
		return str(self.application.elements[elementID])
	
	
	def calculate(self):
		self.application.construction.calculate()
		
		print("A =")
		pprint(self.application.construction.A)
		print("\nb =")
		pprint(self.application.construction.b)
		print()
		
		# Уведомляем главное окно о том, что конструкция рассчитана
		self.application.mainWindow.onConstructionChanged()
	
	
	def calculated(self):
		return self.application.construction.calculated
	
	
	def constructionEmpty(self):
		return self.application.construction.empty
