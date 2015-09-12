#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from Construction import Construction


class Logic:
	def emptyConstruction(self):
		return Construction()
	
	
	def getConstructionFromFile(self, constructionFile):
		return Construction(constructionFile)
	
	
	def size(self, construction):
		return construction.size()
	
	
	def drawConstruction(self, construction, graph):
		graph.setVirtualSize(self.size(construction))
