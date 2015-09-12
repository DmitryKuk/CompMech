#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

import json

from Bar import *
from Node import *


class Construction:
	def __init__(self, constructionFile = None):
		self.defaultBar = Bar()
		self.defaultNode = Node()
		self.elements = []
		
		
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
				element = self.element(item)
				
				if type(element) == Bar:
					if lastWasBar:
						self.elements.append(self.defaultNode)
					lastWasBar = True
				else:
					lastWasBar = False
				
				self.elements.append(element)
				
			if lastWasBar:
				self.elements.append(self.defaultNode)
		except KeyError:
			print("В конструкции нет элементов. Вы в порядке?")
	
	
	def element(self, item):
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
		sizeX, sizeY = 0, 0
		
		for element in self.elements:
			(elSizeX, elSizeY) = element.size()
			sizeX += elSizeX
			sizeY = max(sizeY, elSizeY)
		
		return (sizeX, sizeY)
