#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

import math


class Bar:
	def __init__(self, json = None, default = None):
		self.L = 0
		self.A = 0
		self.E = 0
		self.Sigma = 0
		self.q = 0
		
		if json != None:
			if default == None:
				self.L = json.get("L", 0)
				self.A = json.get("A", 0)
				self.E = json.get("E", 0)
				self.Sigma = json.get("Sigma", 0)
				self.q = json.get("q", 0)
			else:
				self.L = json.get("L", default.L)
				self.A = json.get("A", default.A)
				self.E = json.get("E", default.E)
				self.Sigma = json.get("Sigma", default.Sigma)
				self.q = json.get("q", default.q)
	
	
	def __str__(self):
		return "{'L': %s, 'A': %s, 'E': %s, 'Sigma': %s, 'q': %s}" % (self.L, self.A,
																	  self.E, self.Sigma,
																	  self.q)
	
	
	def size(self):
		return (self.L, math.sqrt(self.A))


def similarToBar(json):
	for keyword in ["L", "A", "E", "Sigma", "q"]:
		if keyword in json:
			return True
	return False
