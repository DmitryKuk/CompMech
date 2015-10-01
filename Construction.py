#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

import json, copy
from sympy import *

from Bar import *
from Node import *


class Construction:
	def __init__(self, constructionFile = None, showMessage = None, showError = None):
		self.defaultBar = Bar()
		self.defaultNode = Node()
		self.elements = []
		self.sizeX, self.sizeY = 0, 0
		
		
		# Максимальные нагрузки
		self.maxF, self.specq = 0, 0
		self.maxqOnL = 0			# Относительная распределённая нагрузка = q / L
		
		self.maxN = 0
		self.maxu = 0
		self.maxSigma = 0
		
		
		# [A] * {Deltas} = {b}
		self.A = None
		self.b = None
		self.Deltas = None
		
		self.calculated = False	# Конструкция была рассчитана
		
		
		if constructionFile is None:	# Пустая конструкция
			return
		
		
		try:
			construction = json.load(constructionFile)
		except Exception as e:
			raise Exception("Невозможно обработать файл конструкции: %s" % e)
		
		
		try:
			self.defaultNode = Node(construction["default"]["node"])
		except KeyError:
			print("Не заданы параметры узла по умолчанию. Не расстраивайтесь, это бывает.")
		
		try:
			self.defaultBar = Bar(construction["default"]["bar"])
		except KeyError:
			print("Не заданы параметры стержня по умолчанию. Не расстраивайтесь, это бывает.")
		
		
		try:
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
		except KeyError:
			if showMessage is not None:
				showMessage("В конструкции нет элементов. Вы в порядке?")
		except Exception as e:
			if showError is not None:
				showError(str(e))
		
		
		# Вычисляем размеры конструкции, максимальные нагрузки, координаты и номера элементов
		x, i = 0, 0
		for element in self.elements:
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
	
	
	def calculate(self):
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
			
			for element in self.elements:
				if type(element) == Bar:
					element.U0 = res[self.Deltas[element.i    ]]
					element.UL = res[self.Deltas[element.i + 1]]
				else:
					element.Delta = res[self.Deltas[element.i]]
			
			self.maxN = 0
			self.maxu = 0
			self.maxSigma = 0
			
			for element in self.elements:
				if type(element) == Bar:
					elN = max(abs(element.NLocal(0)), abs(element.NLocal(element.L)))
					self.maxN = max(self.maxN, elN)
					
					elu = max(abs(element.uLocal(0)), abs(element.uLocal(element.L)))
					self.maxu = max(self.maxu, elu)
					
					elSigma = max(abs(element.SigmaLocal(0)), abs(element.SigmaLocal(element.L)),
								  abs(element.Sigma))
					self.maxSigma = max(self.maxSigma, elSigma)
			
			self.calculated = True
		else:
			if len(self.elements) == 1:	# Единственный узел неподвижен
				self.element[0].Delta = 0.0
				
				self.maxN = 0
				self.maxu = 0
				self.maxSigma = 0
				
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
	
	
	def size(self):
		return (self.sizeX, self.sizeY)
	
	
	def loads(self):
		return (self.maxF, self.specq, self.maxqOnL)
	
	
	def components(self):
		return (self.maxN, self.maxu, self.maxSigma)
