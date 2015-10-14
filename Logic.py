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
	
	
	def createConstructionFromElements(self, nodes, bars, defaultNode, defaultBar):
		if len(nodes) == 0 and len(bars) == 0:
			self.application.construction.defaultBar  = defaultBar
			self.application.construction.defaultNode = defaultNode
		else:
			self.application.construction = Construction(nodes = nodes, bars = bars,
														 defaultNode = defaultNode,
														 defaultBar  = defaultBar)
		self.application.onConstructionChanged()
	
	
	def openConstructionFile(self, constructionFile):
		self.application.construction = Construction(file = constructionFile)
		self.application.onConstructionChanged()
	
	
	def saveConstructionToFile(self, constructionFile):
		self.application.construction.dump(constructionFile)
	
	
	def offsetFunc(self, realSize, virtSize):
		return (60, 40, 60, 40)
	
	
	def draw(self, graph = None, barNumber = None,
			 drawConstruction = True, drawLoads = True,			# Элементы для отрисовки
			 drawN = False, drawU = False, drawSigma = False,	# Эпюры/графики
			 divsX = 0, divsN = 0, divsU = 0, divsSigma = 0):	# Деления на осях
		if graph is None:
			graph = self.application.mainWindow.graph
		graph.clear()
		
		if barNumber is not None and barNumber >= self.barsCount():
			return
		
		
		# Устанавливаем размеры конструкции, максимальные нагрузки и проч.
		if not self.constructionEmpty():
			# Ещё понадобится для отрисовки вспомогательных осей
			virtSize = self.application.construction.size(barNumber)
			graph.setVirtSize(virtSize)
			
			# Масштабируем нагрузки по конструкции
			graph.setMaxLoads(*self.application.construction.maxLoads(barNumber = None))
		
		if self.constructionCalculated():
			# Понадобится при отрисовке вспомогательных осей
			maxComponents = self.application.construction.maxComponents(barNumber)
			graph.setMaxComponents(*maxComponents)
		
		elements = self.application.construction.elements
		xOffset = 0
		
		
		if barNumber == None:	# Номер стержня не указан => рисуем всю конструкцию
			title = "Конструкция"
			
			# Сначала рисуем только стержни, чтобы нагрузки узлов отображались поверх них
			if drawConstruction:
				for element in elements:
					if type(element) == Bar:
						graph.drawBar(element, drawBar = True, drawLoads = False)
			
			# Рисуем узлы (с нагрузками)
			for element in elements:
				if type(element) == Node:
					graph.drawNode(element, drawNode = drawConstruction, drawLoads = drawLoads)
			
			# Теперь рисуем только распределённые нагрузки на стержни, чтобы они были поверх F
			if drawLoads:
				for element in elements:
					if type(element) == Bar:
						graph.drawBar(element, drawBar = False, drawLoads = True)
			
			# Рисуем эпюры
			if (drawN or drawU or drawSigma) and self.constructionCalculated():
				for element in elements:
					if type(element) == Bar:
						graph.drawBarCurves(element,
											drawN = drawN, drawU = drawU, drawSigma = drawSigma)
		else:	# Указан номер стержня => рисуем его и 2 ближайших узла
			bar = elements[2 * barNumber + 1]
			label = "" if bar.label == "" else " \"" + bar.label + "\""
			title = "Стержень (%d)%s" % (barNumber, label)
			
			xOffset = bar.x
			
			# Рисуем стержень
			# Сначала рисуем только стержни, чтобы нагрузки узлов отображались поверх них
			graph.drawBar(bar, drawBar = drawConstruction, drawLoads = False)
			
			graph.setLocalCoordinate(bar.x)
			graph.drawBar(bar, drawBar = drawConstruction, drawLoads = drawLoads)
			
			# Рисуем соседние узлы
			for element in elements[2 * barNumber], elements[2 * barNumber + 2]:
				graph.drawNode(element, drawNode = drawConstruction, drawLoads = drawLoads)
			
			# Теперь рисуем только распределённые нагрузки на стержни, чтобы они были поверх F
			graph.drawBar(bar, drawBar = False, drawLoads = drawLoads)
				
			# Рисуем эпюры
			graph.drawBarCurves(bar, drawN = drawN, drawU = drawU, drawSigma = drawSigma)
		
		
		# Рисуем оси
		if not self.constructionEmpty():
			# Координатные оси
			graph.drawCoordinateAxis()
			
			
			# Вспомогательные оси (вертикальные, по Ox)
			if not self.constructionEmpty():	# Вертикальные
				maxX = virtSize[0]
				dx = float(maxX) / (divsX + 1)
				x = xOffset
				while x < maxX + xOffset:
					x += dx
					graph.drawXVAxis(vX = x)
			
			
			# Вспомогательные оси (горизонтальные, по Oy)
			if self.constructionCalculated():	# Горизонтальные
				def drawHAxis(drawer, divs, maxY):
					if divs <= 0: return
					
					dy = float(maxY) / divs
					y = 0.0
					while y < maxY:
						y += dy
						drawer(vY =  y)
						drawer(vY = -y)
				
				
				drawHAxis(graph.drawNHAxis,     divsN,     maxComponents[0])
				drawHAxis(graph.drawUHAxis,     divsU,     maxComponents[1])
				drawHAxis(graph.drawSigmaHAxis, divsSigma, maxComponents[2])
		
		
		# Надпись на графике
		graph.setTitle(title)
	
	
	def nearestBar(self, x):
		if self.constructionEmpty(): return None
		
		c = self.application.construction
		nearestBar = None
		
		i = bisect_left(c.nodeXs, x)
		if i == 0:
			if x == 0 and self.barsCount() > 0:
				nearestBar = c.barFirst()
		else:
			i -= 1
			if i < self.barsCount():
				nearestBar = c.bar(i)
		
		return nearestBar
	
	
	def nearestData(self, x, realToVirtXLen):
		if self.constructionEmpty(): return (None, None)
		
		c = self.application.construction
		nearestBar = self.nearestBar(x)
		
		if nearestBar is None:
			nearestNode = c.nodeFirst() if x < 0 else c.nodeLast()
		else:
			nodeL, nodeR = c.nodeLeft(nearestBar.i), c.nodeRight(nearestBar.i)
			xL, xR = nodeL.x, nodeR.x
			nearestNode = nodeL if abs(x - xL) < abs(xR - x) else nodeR
		
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
	
	
	def matrices(self, barNumber = None):
		if not self.constructionCalculated():
			s = "<Не рассчитано>"
			return [ s, s, s ]
		
		c = self.application.construction
		
		if barNumber is None:
			Deltas = []
			for element in self.application.construction.elements:
				if type(element) == Node:
					Deltas.append(element.Delta)
			
			return [ pretty(x) for x in (c.A, c.b, Matrix(self.nodesCount(), 1, Deltas)) ]
		else:
			if barNumber not in range(0, self.barsCount()):
				s = "<Некорректный номер стержня>"
				return [ s, s, s ]
			
			e = self.application.construction.elements[2 * barNumber + 1]
			return [ pretty(x) for x in (e.K, e.Q, Matrix(2, 1, [e.U0, e.UL])) ]
	
	
	def calculateComponents(self, xFrom, xTo, xStep, onPointCalculated, barNumber = None):
		if (xFrom > xTo and xStep > 0) or (xFrom < xTo and xStep < 0):
			raise Exception("Некорректный диапазон или шаг:\n(%.3f; %.3f), dx = %.3f" \
							% (xFrom, xTo, xStep))
		
		if self.constructionEmpty():
			raise Exception("Конструкция не задана")
		
		if not self.constructionCalculated():
			raise Exception("Конструкция не рассчитана")
		
		
		# Учитываем смещение координат
		if barNumber is None:
			xOffset = 0
		else:
			xOffset = self.application.construction.elements[2 * barNumber + 1].x
			xFrom += xOffset
			xTo   += xOffset
		
		
		# Вспомогательные функции
		barNumber, bar = None, None
		def calculatePoint(x):
			onPointCalculated(bar.i, x - xOffset, \
							  bar.NGlobal(x), bar.UGlobal(x), bar.SigmaGlobal(x))
		
		
		def emptyPointFound(x):
			onPointCalculated(None, x - xOffset, 0, 0, 0)
		
		
		# Вычисляем единственное значение
		if xStep == 0:
			bar = self.nearestBar(xFrom)
			if bar is None: emptyPointFound(xFrom)
			else: calculatePoint(xFrom)
			return
		
		
		# Вычисляем множество значений
		constructionWidth = self.application.construction.size()[0]
		if xStep >= 0:
			# Левее конструкции
			while xFrom <= xTo and xFrom < 0:
				emptyPointFound(xFrom)
				xFrom += xStep
			
			# Конструкция
			if xFrom <= xTo and xFrom <= constructionWidth:
				bar = self.nearestBar(xFrom)
				barNumber = bar.i
				while xFrom <= xTo and xFrom <= constructionWidth:
					if xFrom > bar.x + bar.L:
						barNumber += 1
						bar = self.application.construction.elements[2 * barNumber + 1]
					calculatePoint(xFrom)
					xFrom += xStep
			
			# Правее конструкции
			while xFrom <= xTo:
				emptyPointFound(xFrom)
				xFrom += xStep
		else:
			# Правее конструкции
			while xFrom >= xTo and xFrom > constructionWidth:
				emptyPointFound(xFrom)
				xFrom += xStep
			
			# Конструкция
			if xFrom >= xTo and xFrom >= 0:
				bar = self.nearestBar(xFrom)
				barNumber = bar.i
				while xFrom >= xTo and xFrom >= 0:
					if xFrom < bar.x:
						barNumber -= 1
						bar = self.application.construction.elements[2 * barNumber + 1]
					calculatePoint(xFrom)
					xFrom += xStep
			
			# Левее конструкции
			while xFrom >= xTo:
				emptyPointFound(xFrom)
				xFrom += xStep
	
	
	# Работа с редактором конструкции
	def getDefault(self, onNodeDetected, onBarDetected):
		onNodeDetected(self.application.construction.defaultNode)
		onBarDetected(self.application.construction.defaultBar)
	
	
	def getElements(self, onNodeDetected, onBarDetected):
		for element in self.application.construction.elements:
			if type(element) == Node: onNodeDetected(element)
			else:					  onBarDetected(element)
	
	
	# Работа с конструкцией
	def constructionEmpty(self):
		return self.application.construction.empty()
	
	
	def constructionCalculated(self):
		return self.application.construction.calculated
	
	
	def elementsCount(self):
		return self.application.construction.elementsCount()
	
	
	def barsCount(self):
		return self.application.construction.barsCount()
	
	
	def nodesCount(self):
		return self.application.construction.nodesCount()
	
	
	def bar(self, i):
		return self.construction.bar(i)
	
	
	def node(self, i):
		return self.construction.node(i)
