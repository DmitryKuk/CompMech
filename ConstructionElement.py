#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)


class ConstructionElement:
	def __init__(self, json = None, default = None):
		self.label = ""
		self.x = None	# Будет рассчитано конструкцией
		self.i = None	# Номер узла; будет рассчитано конструкцией
		
		if json is not None:
			if default is None:
				self.label = json.get("label", "")
			else:
				self.label = json.get("label", default.label)
		elif default is not None:
			self.label = default.label
	
	
	def calculate(self):
		pass
	
	
	def size(self):
		return (0, 0)
	
	
	def loads(self):
		return (0, 0)
