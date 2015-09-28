#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from ConstructionElement import ConstructionElement


class Node(ConstructionElement):
	def __init__(self, json = None, default = None):
		ConstructionElement.__init__(self, json, default)
		
		self.fixed = False
		self.F = 0
		
		self.Delta = None	# Смещение узла; вычисляется конструкцией
		
		if json is not None:
			if default is None:
				self.fixed = json.get("fixed", False)
				self.F = json.get("F", 0)
			else:
				self.fixed = json.get("fixed", default.fixed)
				self.F = json.get("F", default.F)
		elif default is not None:
			self.fixed = default.fixed
			self.F = default.F
	
	
	def __str__(self):
		fixedStr = "зафиксирован" if self.fixed else "свободен"
		
		return "Узел [%d]%s: x = %s; F = %s; %s; Δ%d = %s" \
			   % (self.i,
				  " \"" + self.label + "\"" if self.label != "" else "",
				  self.x, self.F, fixedStr, self.i, self.Delta)
	
	
	def size(self):
		return (0, 0)
	
	
	def loads(self):
		return (self.F, 0)


def similarToNode(json):
	for keyword in ["fixed", "F"]:
		if keyword in json:
			return True
	return False
