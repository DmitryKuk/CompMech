#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

import json, copy
from sympy import *

from Bar import *
from Node import *


class Construction:
	def __init__(self, file = None,
				 nodes = None, bars = None):
		self.defaultBar = Bar()
		self.defaultNode = Node()
		self.elements = []
		self.sizeX, self.sizeY = 0.0, 0.0
		
		
		# Максимальные нагрузки
		self.maxF, self.specq = 0.0, 0.0
		self.maxqOnL = 0.0			# Относительная распределённая нагрузка = q / L
		
		self.maxN = 0.0
		self.maxU = 0.0
		self.maxSigma = 0.0
		
		# Координаты узлов для бинарного поиска ближайшего узла и стержня
		self.nodeXs = []
		
		
		# [A] * {Deltas} = {b}
		self.A = None
		self.b = None
		self.Deltas = None
		
		self.calculated = False		# Конструкция была рассчитана
		
		
		if file is None:
			if nodes is None or bars is None:	# Создаём конструкцию из элементов
				return
			else:
				if len(nodes) != len(bars) + 1:
					raise Exception("Некорректная конструкция " \
									"(ожидается: количество узлов = количество стержней + 1)")
				
				for i in range(0, len(bars)):
					self.elements.append(nodes[i])
					self.elements.append(bars[i])
				self.elements.append(nodes[-1])
		else:
			try:
				construction = json.load(file)
			except Exception as e:
				raise Exception("Невозможно обработать файл конструкции: %s" % e)
			
			
			try:
				self.defaultNode = Node(construction["default"]["node"])
			except KeyError:
				pass
			
			try:
				self.defaultBar = Bar(construction["default"]["bar"])
			except KeyError:
				pass
			
			
			try:
				self.A = eval(construction["A"])
				self.b = eval(construction["b"])
				
				self.calculated = True
			except KeyError:
				self.A = None
				self.b = None
				
				self.calculated = False
			
			
			lastWasBar = True
			
			for item in construction["construction"]:
				element = self.elementFromJSON(item)
				
				if type(element) == Bar:
					if lastWasBar:
						self.elements.append(copy.deepcopy(self.defaultNode))
					lastWasBar = True
				else:
					if not lastWasBar:
						self.elements.append(copy.deepcopy(self.defaultBar))
					lastWasBar = False
				
				self.elements.append(element)
			
			if lastWasBar:
				self.elements.append(copy.deepcopy(self.defaultNode))
		
		
		# Вычисляем размеры конструкции, максимальные нагрузки, координаты и номера элементов
		x, i = 0, 0
		for element in self.elements:
			self.calculated = self.calculated and element.calculated()
			
			# Размеры
			(elSizeX, elSizeY) = element.size()
			self.sizeX += elSizeX
			self.sizeY = max(self.sizeY, elSizeY)
			
			# Нагрузки
			(F, q) = element.loads()
			self.maxF = max(self.maxF, abs(F))
			
			# Относительная распределённая нагрузка
			if elSizeX > 0:
				qOnL = float(abs(q)) / elSizeX
				if qOnL > self.maxqOnL:
					self.maxqOnL, self.specq = qOnL, abs(q)
			
			# Координата элемента
			element.x = copy.deepcopy(x)
			x += elSizeX
			
			# Номер элемента
			element.i = copy.deepcopy(i)
			if type(element) == Bar: i += 1
		
		# Предвычисляем список с координатами узлов (для бинарного поиска элементов)
		for element in self.elements:
			if type(element) == Node: self.nodeXs.append(element.x)
		
		if len(self.elements) == 0:
			self.calculated = False
		
		if self.calculated:
			for element in self.elements:
				if type(element) == Bar:
					c = element.maxComponents()
					
					self.maxN     = max(self.maxN,     c[0])
					self.maxU     = max(self.maxU,     c[1])
					self.maxSigma = max(self.maxSigma, c[2])
	
	
	def dump(self, file):
		retDict = {
			"default": {
				"node": self.defaultNode.dump(),
				"bar": self.defaultBar.dump()
			},
			
			"construction": [ element.dump() for element in self.elements ]
		}
		
		if self.calculated:
			retDict.update({ "A": str(self.A), "b": str(self.b) })
		
		json.dump(
			retDict,
			file
		)
	
	
	def calculate(self):
		if self.empty(): return
		
		bars = (len(self.elements) - 1) / 2
		if bars > 0:
			self.A = zeros(bars + 1)
			self.b = zeros(bars + 1, 1)
			self.Deltas = []
			
			for element in self.elements:
				element.calculate()
				
				if type(element) == Bar:
					self.A += diag(zeros(element.i), element.K, zeros(bars - element.i - 1))
					
					# Учитываем реакции стержня
					self.b[element.i    , 0] -= element.Q[0, 0]
					self.b[element.i + 1, 0] -= element.Q[1, 0]
				else:
					# Учитываем сосредоточенную нагрузку на узел
					self.b[element.i] += element.F
					
					self.Deltas.append(Symbol("Delta%s" % element.i))
			
			for element in self.elements:
				if type(element) == Node:
					if element.fixed:
						self.A.row_del(element.i)
						self.A.col_del(element.i)
						
						self.A = self.A \
							.col_insert(element.i, zeros(bars, 1)) \
							.row_insert(element.i, zeros(1, element.i) \
												   .row_join(Matrix([[1.0]])) \
												   .row_join(zeros(1, bars - element.i)))
						
						self.b[element.i, 0] = 0
			
			# Вычисляем перемещения узлов
			res = solve_linear_system(self.A.row_join(self.b), *self.Deltas)
			if res is None:
				raise Exception("Конструкция не может быть рассчитана!")
			
			for element in self.elements:
				if type(element) == Bar:
					element.U0 = res[self.Deltas[element.i    ]]
					element.UL = res[self.Deltas[element.i + 1]]
				else:
					element.Delta = res[self.Deltas[element.i]]
			
			self.maxN = 0.0
			self.maxU = 0.0
			self.maxSigma = 0.0
			
			for element in self.elements:
				if type(element) == Bar:
					c = element.maxComponents()
					
					self.maxN     = max(self.maxN,     c[0])
					self.maxU     = max(self.maxU,     c[1])
					self.maxSigma = max(self.maxSigma, c[2])
			
			self.calculated = True
		else:
			if len(self.elements) == 1:	# Единственный узел неподвижен
				self.elements[0].Delta = 0.0
				
				self.maxN = 0.0
				self.maxU = 0.0
				self.maxSigma = 0.0
				
				self.calculated = True
			else:
				self.calculated = False
	
	
	def elementFromJSON(self, item):
		isBar  = similarToBar(item)
		isNode = similarToNode(item)
		
		if isBar and (not isNode):
			return Bar(item, self.defaultBar)
		elif (not isBar) and isNode:
			return Node(item, self.defaultNode)
		elif isBar and isNode:
			raise Exception("Элемент конструкции похож на стержень и узел одновременно: %s" % item)
		else:
			raise Exception("Элемент конструкции не похож на стержень или узел: %s" % item)
	
	
	def size(self, barNumber = None):
		return (self.sizeX, self.sizeY) if barNumber is None \
			   else self.bar(barNumber).size()
	
	
	def maxLoads(self, barNumber = None):
		if barNumber is None:
			return (self.maxF, self.specq, self.maxqOnL)
		else:
			bar = self.bar(barNumber)
			nodeL, nodeR = self.nodeLeft(barNumber), self.nodeRigth(barNumber)
			return (max(abs(nodeL.F), abs(nodeR.F)), abs(bar.q), abs(float(bar.q) / bar.L))
	
	
	def maxComponents(self, barNumber = None):
		return (self.maxN, self.maxU, self.maxSigma) if barNumber is None \
			   else self.bar(barNumber).maxComponents()
	
	
	def empty(self):
		return True if self.elementsCount() == 0 else False
	
	
	def elementsCount(self):
		return len(self.elements)
	
	def barsCount(self):
		return self.elementsCount() // 2
	
	def nodesCount(self):
		elementsCount = self.elementsCount()
		return elementsCount // 2 + 1 if elementsCount > 0 else 0
	
	
	def element(self, i):
		return self.elements[i]
	
	def bar(self, barNumber):
		return self.element(2 * barNumber + 1)
	
	def node(self, nodeNumber):
		return self.element(2 * nodeNumber)
	
	
	def nodeLeft(self, barNumber):
		return self.node(barNumber)
	
	def nodeRight(self, barNumber):
		return self.node(barNumber + 1)
	
	
	def barFirst(self):
		return self.bar(0)
	
	def barLast(self):
		return self.bar(self.barsCount() - 1)
	
	
	def nodeFirst(self):
		return self.node(0)
	
	def nodeLast(self):
		return self.node(self.nodesCount() - 1)
