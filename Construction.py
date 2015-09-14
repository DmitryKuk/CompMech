#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

import json, copy

from Bar import *
from Node import *


class Construction:
	def __init__(self, constructionFile = None):
		self.defaultBar = Bar()
		self.defaultNode = Node()
		self.elements = []
		self.sizeX, self.sizeY = 0, 0
		
		
		if constructionFile is None:	# Пустая конструкция
			return None
		
		
		construction = json.load(constructionFile)
		
		
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
					lastWasBar = False
				
				self.elements.append(element)
				
			if lastWasBar:
				self.elements.append(copy.deepcopy(self.defaultNode))
		except KeyError:
			print("В конструкции нет элементов. Вы в порядке?")
		
		
		# Вычисляем размер конструкции и координаты элементов
		x = 0
		for element in self.elements:
			(elSizeX, elSizeY) = element.size()
			self.sizeX += elSizeX
			self.sizeY = max(self.sizeY, elSizeY)
			
			element.x = copy.deepcopy(x)	# Координата элемента
			x += elSizeX
	
	
	def elementFromJSON(self, item):
		isBar = similarToBar(item)
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
