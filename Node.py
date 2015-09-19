#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from ConstructionElement import ConstructionElement


class Node(ConstructionElement):
	def __init__(self, json = None, default = None):
		ConstructionElement.__init__(self, json, default)
		
		self.fixed = False
		self.F = 0
		
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
		if self.fixed:	fixedStr = "зафиксирован"
		else:			fixedStr = "свободен"
		
		if len(self.label) > 0:
			return "Узел \"%s\": x = %s; F = %s; %s" \
				% (self.label, self.x, self.F, fixedStr)
		else:
			return "Узел: x = %s; F = %s; %s" \
				% (self.x, self.F, fixedStr)
	
	
	def size(self):
		return (0, 0)
	
	
	def loads(self):
		return (self.F, 0)


def similarToNode(json):
	for keyword in ["fixed", "F"]:
		if keyword in json:
			return True
	return False
