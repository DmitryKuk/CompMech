#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

import math
from sympy import *

from ConstructionElement import ConstructionElement


class Bar(ConstructionElement):
	def __init__(self, json = None, default = None):
		ConstructionElement.__init__(self, json, default)
		
		self.L = 0.0
		self.A = 0.0
		self.E = 0.0
		self.Sigma = 0.0
		self.q = 0.0
		
		self.height = 0.0
		
		self.K = None	# Матрица реакций
		self.Q = None	# Вектор реакций
		
		self.U0, self.UL = None, None
		
		if json is not None:
			if default is None:
				self.L = float(json.get("L", 0.0))
				self.A = float(json.get("A", 0.0))
				self.E = float(json.get("E", 0.0))
				self.Sigma = float(json.get("Sigma", 0.0))
				self.q = float(json.get("q", 0.0))
			else:
				self.L = float(json.get("L", default.L))
				self.A = float(json.get("A", default.A))
				self.E = float(json.get("E", default.E))
				self.Sigma = float(json.get("Sigma", default.Sigma))
				self.q = float(json.get("q", default.q))
		elif default is not None:
			self.L = float(default.L)
			self.A = float(default.A)
			self.E = float(default.E)
			self.Sigma = float(default.Sigma)
			self.q = float(default.q)
		
		if json is not None or default is not None:
			if self.L <= 0:
				raise Exception("Некорректная длина стержня: L = %f " \
								"(ожидается: L > 0; %s)" % (self.L, self))
			
			if self.A <= 0:
				raise Exception("Некорректная площадь поперечного сечения стержня: A = %f " \
								"(ожидается: A > 0; %s)" % (self.A, self))
		
		self.height = math.sqrt(self.A)		# Квадратное сечение
	
	
	def calculate(self):
		self.K = None if self.L <= 0 else \
				 self.E * self.A / self.L * Matrix([[1, -1], [-1, 1]])
		
		self.Q = self.q * self.L / 2 * Matrix([[-1], [-1]])
	
	
	def __str__(self):
		return "Стержень (%d)%s: x = %s; L = %s; A = %s; E = %s; σ = %s; q = %s; U0 = %s; UL = %s" \
			   % (self.i,
				  " \"" + self.label + "\"" if self.label != "" else "",
				  self.x, self.L, self.A, self.E, self.Sigma, self.q, self.U0, self.UL)
	
	
	def size(self):
		return (self.L, self.height)
	
	
	def loads(self):
		return (0, self.q)


def similarToBar(json):
	for keyword in ["L", "A", "E", "Sigma", "q"]:
		if keyword in json:
			return True
	return False
