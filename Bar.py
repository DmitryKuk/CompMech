#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

import math
from sympy import *

from ConstructionElement import ConstructionElement


class Bar(ConstructionElement):
	def __init__(self, json = None, default = None):
		ConstructionElement.__init__(self, json, default)
		
		self.L = 0
		self.A = 0
		self.E = 0
		self.Sigma = 0
		self.q = 0
		
		self.height = 0
		
		if json is not None:
			if default is None:
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
		elif default is not None:
			self.L = default.L
			self.A = default.A
			self.E = default.E
			self.Sigma = default.Sigma
			self.q = default.q
		
		self.height = math.sqrt(self.A)		# Квадратное сечение
		
		# Матрица реакций
		self.K = None if self.L == 0 else \
				 float(self.E * self.A) / self.L * Matrix([[1, -1], [-1, 1]])
		
		# Вектор реакций
		self.Q = float(self.q * self.L) / 2 * Matrix([[-1], [-1]])
	
	
	def __str__(self):
		if len(self.label) > 0:
			return "Стержень \"%s\": x = %s; L = %s; A = %s; E = %s; σ = %s; q = %s" \
				% (self.label, self.x, self.L, self.A, self.E, self.Sigma, self.q)
		else:
			return "Стержень: x = %s; L = %s; A = %s; E = %s; σ = %s; q = %s" \
				% (self.x, self.L, self.A, self.E, self.Sigma, self.q)
	
	
	def size(self):
		return (self.L, self.height)
	
	
	def loads(self):
		return (0, self.q)


def similarToBar(json):
	for keyword in ["L", "A", "E", "Sigma", "q"]:
		if keyword in json:
			return True
	return False
