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
		
		
		# [A] * {deltas} = {b}
		self.A = None
		self.b = None
		self.deltas = None
		
		
		if constructionFile is None:	# Пустая конструкция
			return None
		
		
		try:
			construction = json.load(constructionFile)
		except Exception as e:
			raise Exception("Невозможно обработать файл конструкции: %s" % e)
		
		
		try:
			self.defaultNode = Node(construction["default"]["node"])
		except KeyError:
			if showMessage is not None:
				showMessage("Не заданы параметры узла по умолчанию. " \
							"Не расстраивайтесь, это бывает.")
		
		try:
			self.defaultBar = Bar(construction["default"]["bar"])
		except KeyError:
			if showMessage is not None:
				showMessage("Не заданы параметры стержня по умолчанию. " \
							"Не расстраивайтесь, это бывает.")
		
		
		try:
			lastWasBar = True
			
			for item in construction["construction"]:
				element = self.elementFromJSON(item)
				
				if type(element) == Bar:
					if lastWasBar:
						self.elements.append(copy.deepcopy(self.defaultNode))
					lastWasBar = True
				else:
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
		
		
		# Вычисляем размеры конструкции, максимальные нагрузки и координаты элементов
		x = 0
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
	
	
	def calculate(self):
		bars = (len(self.elements) - 1) / 2
		if bars > 0:
			self.A = zeros(bars + 1)
			self.b = zeros(bars + 1, 1)
			self.deltas = []
			
			i = 0
			for element in self.elements:
				element.calculate()
				
				if type(element) == Bar:
					self.A += diag(zeros(i), element.K, zeros(bars - i - 1))
					
					# Учитываем реакции стержня
					self.b[    i, 0] -= element.Q[0, 0]
					self.b[i + 1, 0] -= element.Q[1, 0]
					
					i += 1
				else:
					# Учитываем сосредоточенную нагрузку на узел
					self.b[i] += element.F
					
					self.deltas.append(Symbol("delta%s" % i))
			
			i = 0
			for element in self.elements:
				if type(element) == Node:
					if element.fixed:
						self.A.row_del(i)
						self.A.col_del(i)
						
						self.A = self.A \
							.col_insert(i, zeros(bars, 1)) \
							.row_insert(i, zeros(1, i) \
										   .row_join(Matrix([[1.0]])) \
										   .row_join(zeros(1, bars - i)))
					i += 1
	
	
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
