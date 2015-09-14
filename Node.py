#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)


class Node:
	def __init__(self, json = None, default = None):
		self.fixed = False
		self.F = 0
		
		self.x = None	# Будет рассчитано конструкцией
		
		if not (json is None):
			if default is None:
				self.fixed = json.get("fixed", False)
				self.F = json.get("F", 0)
			else:
				self.fixed = json.get("fixed", default.fixed)
				self.F = json.get("F", default.F)
	
	
	def __str__(self):
		if self.fixed:	fixedStr = "зафиксирован"
		else:			fixedStr = "свободен"
		return "Узел: x = %s; F = %s; %s" % (self.x, self.F, fixedStr)
	
	
	def size(self):
		return (0, 0)
	
	
	def loads(self):
		return (self.F, 0)


def similarToNode(json):
	for keyword in ["fixed", "F"]:
		if keyword in json:
			return True
	return False
