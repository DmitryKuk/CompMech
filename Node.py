#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)


class Node:
	def __init__(self, json = None, default = None):
		self.fixed = False
		self.F = 0
		
		if not (json is None):
			if default is None:
				self.fixed = json.get("fixed", False)
				self.F = json.get("F", 0)
			else:
				self.fixed = json.get("fixed", default.fixed)
				self.F = json.get("F", default.F)
	
	
	def __str__(self):
		return "{'fixed': %s, 'F': %s}" % (self.fixed, self.F)
	
	
	def size(self):
		return (0, 0)


def similarToNode(json):
	for keyword in ["fixed", "F"]:
		if keyword in json:
			return True
	return False
