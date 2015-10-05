#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

import math
from sympy import *
from bisect import bisect_left

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
		self.draw()
		self.application.onConstructionChanged()
	
	
	def offsetFunc(self, realSize, virtSize):
		return (40, 40, 40, 40)
	
	
	def draw(self, graph = None, barNumber = None,
			 drawConstruction = True, drawLoads = True,
			 drawN = False, drawU = False, drawSigma = False):
		if graph is None:
			graph = self.application.mainWindow.graph
		graph.clear()
		
		if barNumber is not None and barNumber >= self.barsCount():
			return
		
		
		# Устанавливаем размеры конструкции, максимальные нагрузки и проч.
		if not self.constructionEmpty():
			graph.setVirtSize(self.application.construction.size(barNumber))
			
			# Масштабируем нагрузки по конструкции
			graph.setMaxLoads(*self.application.construction.maxLoads(barNumber = None))
		
		if self.constructionCalculated():
			graph.setMaxComponents(*self.application.construction.maxComponents(barNumber))
		
		# Ось Oy рисуем до элементов
		if not self.constructionEmpty():
			graph.drawCoordinateAxisY()
		
		elements = self.application.construction.elements
		
		
		if barNumber == None:	# Номер стержня не указан => рисуем всю конструкцию
			title = "Конструкция"
			
			# Сначала рисуем только стержни, чтобы нагрузки узлов отображались поверх них
			for element in elements:
				if type(element) == Bar:
					graph.drawBar(element, drawBar = drawConstruction, drawLoads = drawLoads)
			
			# Рисуем узлы (с нагрузками)
			for element in elements:
				if type(element) == Node:
					graph.drawNode(element, drawNode = drawConstruction, drawLoads = drawLoads)
			
			# Рисуем эпюры
			if (drawN or drawU or drawSigma) and self.constructionCalculated():
				for element in elements:
					if type(element) == Bar:
						graph.drawBarCurves(element,
											drawN = drawN, drawU = drawU, drawSigma = drawSigma)
		else:	# Указан номер стержня => рисуем его и 2 ближайших узла
			barLabel = elements[2 * barNumber + 1].label
			if barLabel != "": barLabel = " \"" + barLabel + "\""
			title = "Стержень (%d)%s" % (barNumber, barLabel)
			
			# Рисуем стержень
			bar = elements[2 * barNumber + 1]
			graph.setLocalCoordinate(bar.x)
			
			graph.drawBar(bar, drawBar = drawConstruction, drawLoads = drawLoads)
			
			# Рисуем соседние узлы
			for element in elements[2 * barNumber], elements[2 * barNumber + 2]:
				graph.drawNode(element, drawNode = drawConstruction, drawLoads = drawLoads)
			
			# Рисуем эпюры
			graph.drawBarCurves(bar, drawN = drawN, drawU = drawU, drawSigma = drawSigma)
		
		
		# Ось Ox рисуем после элементов, чтобы её было видно
		if not self.constructionEmpty():
			graph.drawCoordinateAxisX()
		
		# Надпись на графике
		graph.setTitle(title)
	
	
	def nearestBar(self, x):
		if self.constructionEmpty(): return (None, None)
		
		construction = self.application.construction
		elements = construction.elements
		nodeXs = construction.nodeXs
		
		nearestNode, nearestBar = None, None
		
		i = bisect_left(nodeXs, x)
		if i == 0:
			nearestNode = elements[0]
		else:
			i -= 1
			if 2 * i + 1 < self.elementsCount():
				nearestBar = elements[2 * i + 1]
				
				xl, xr = elements[2 * i].x, elements[2 * i + 2].x
				if abs(x - xl) < abs(xr - x):
					nearestNode = elements[2 * i]
				else:
					nearestNode = elements[2 * i + 2]
			else:
				nearestNode = elements[-1]
		
		return nearestBar
	
	
	def nearestData(self, x, realToVirtXLen):
		if self.constructionEmpty(): return (None, None)
		
		construction = self.application.construction
		elements = construction.elements
		nodeXs = construction.nodeXs
		
		nearestNode, nearestBar = None, None
		
		i = bisect_left(nodeXs, x)
		if i == 0:
			nearestNode = elements[0]
		else:
			i -= 1
			if 2 * i + 1 < self.elementsCount():
				nearestBar = elements[2 * i + 1]
				
				xl, xr = elements[2 * i].x, elements[2 * i + 2].x
				if abs(x - xl) < abs(xr - x):
					nearestNode = elements[2 * i]
				else:
					nearestNode = elements[2 * i + 2]
			else:
				nearestNode = elements[-1]
		
		# Узел в окрестностях 10 пикселей считаем ближе, чем стержень
		nearest = nearestNode if abs(x - nearestNode.x) < realToVirtXLen(10) else nearestBar
		return (nearest, nearestBar)
	
	
	def onCursorMovement(self, graph, realCoord, virtCoord, scale):
		if realCoord[0] == None:
			elementDescStr = "\n"
		else:
			(nearest, nearestBar) = self.nearestData(virtCoord[0], scale.realToVirtXLen)
			
			elementDescStr  = "" if nearest is None else str(nearest)
			elementDescStr += "\n"
			elementDescStr += "" if nearestBar is None else nearestBar.supportDescStr(virtCoord[0])
		
		graph.setElementStr(elementDescStr)
	
	
	def onMouse1Clicked(self, graph, realCoord, virtCoord, scale):
		(nearest, nearestBar) = self.nearestData(virtCoord[0], scale.realToVirtXLen)
		if nearestBar is not None:
			self.application.createDetailWindow(barNumber = nearestBar.i)
	
	
	def calculate(self):
		self.application.construction.calculate()
		
		# Уведомляем главное окно о том, что конструкция рассчитана
		self.application.onConstructionChanged()
	
	
	def elementsCount(self):
		return len(self.application.construction.elements)
	
	
	def barsCount(self):
		return self.elementsCount() // 2
	
	
	def nodesCount(self):
		return self.elementsCount() // 2 + 1 if self.elementsCount() > 0 else 0
	
	
	def constructionEmpty(self):
		return self.application.construction.empty
	
	
	def constructionCalculated(self):
		return self.application.construction.calculated
	
	
	def matrices(self):
		if not self.constructionCalculated():
			s = "<Не рассчитано>"
			return [ s, s, s ]
		
		c = self.application.construction
		Deltas = []
		for element in self.application.construction.elements:
			if type(element) == Node:
				Deltas.append(element.Delta)
		
		return [ pretty(x) for x in (c.A, c.b, Matrix(self.nodesCount(), 1, Deltas)) ]
	
	
	def calculateComponents(self, xFrom, xTo, xStep, onPointCalculated):
		if (xFrom > xTo and xStep > 0) or (xFrom < xTo and xStep < 0):
			raise Exception("Некорректный диапазон или шаг: (%.3f; %.3f), dx = %.3f" \
							% (xFrom, xTo, xStep))
		
		if self.constructionEmpty():
			raise Exception("Конструкция не задана")
		
		if not self.constructionCalculated():
			raise Exception("Конструкция не рассчитана")
		
		
		bar = self.application.construction.elements[1] if xFrom == 0 else self.nearestBar(xFrom)
		def calculatePoint(x):
			if bar is None: onPointCalculated(x, 0, 0, 0)
			else: onPointCalculated(x, bar.NGlobal(x), bar.UGlobal(x), bar.SigmaGlobal(x))
		
		
		if xStep == 0:
			calculatePoint(xFrom)
			return
		
		if xStep >= 0:
			barNumber = 0
			while xFrom <= xTo:
				if xFrom < 0 or xFrom > self.application.construction.size()[0]:
					onPointCalculated(xFrom, 0, 0, 0)
				else:
					if bar is None or xFrom > bar.x + bar.L:
						bar = self.application.construction.elements[2 * barNumber + 1]
						barNumber += 1
					calculatePoint(xFrom)
				
				xFrom += xStep
		else:
			barNumber = self.barsCount() - 1
			while xFrom >= xTo:
				if xFrom < 0 or xFrom > self.application.construction.size()[0]:
					onPointCalculated(xFrom, 0, 0, 0)
				else:
					if bar is None or xFrom < bar.x:
						bar = self.application.construction.elements[2 * barNumber + 1]
						barNumber -= 1
					calculatePoint(xFrom)
				
				xFrom += xStep
