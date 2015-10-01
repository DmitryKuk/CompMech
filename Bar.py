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
			
			if self.E <= 0:
				raise Exception("Некорректный модель упругости стержня: E = %f " \
								"(ожидается: E > 0; %s)" % (self.E, self))
		
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
	
	
	def uLocal(self, x):
		return (1 - x / self.L) * self.U0 \
			   + x / self.L * self.UL \
			   + self.q * self.L / (2 * self.E * self.A) * x * (1 - x / self.L)
	
	
	def uGlobal(self, x):
		return self.uLocal(x - self.x)
	
	
	def NLocal(self, x):
		return self.E * self.A / self.L * (self.UL - self.U0) \
			   + self.q * self.L / 2 * (1 - 2 * x / self.L)
	
	
	def NGlobal(self, x):
		return self.NLocal(x - self.x)
	
	
	def SigmaLocal(self, x):
		return self.NLocal(x) / self.A
	
	
	def SigmaGlobal(self, x):
		return self.NGlobal(x) / self.A
	
	
	def NLineLocal(self):
		return [(0, self.NLocal(0)), (self.L, self.NLocal(self.L))]
	
	
	def NLineGlobal(self):
		local = self.NLineLocal()
		local[0] = (local[0][0] + self.x, local[0][1])
		local[1] = (local[1][0] + self.x, local[1][1])
		return local
	
	
	def uLineLocal(self):
		return [(0, self.uLocal(0)), (self.L, self.uLocal(self.L))]
	
	
	def uLineGlobal(self):
		local = self.uLineLocal()
		local[0] = (local[0][0] + self.x, local[0][1])
		local[1] = (local[1][0] + self.x, local[1][1])
		return local
	
	
	def SigmaLineLocal(self):
		return [(0, self.SigmaLocal(0)), (self.L, self.SigmaLocal(self.L))]
	
	
	def SigmaLineGlobal(self):
		local = self.SigmaLineLocal()
		local[0] = (local[0][0] + self.x, local[0][1])
		local[1] = (local[1][0] + self.x, local[1][1])
		return local
	
	
	def SigmaMaxLineLocal(self):
		return [(0, self.Sigma), (self.L, self.Sigma)]
	
	
	def SigmaMaxLineGlobal(self):
		local = self.SigmaMaxLineLocal()
		local[0] = (local[0][0] + self.x, local[0][1])
		local[1] = (local[1][0] + self.x, local[1][1])
		return local


def similarToBar(json):
	for keyword in ["L", "A", "E", "Sigma", "q"]:
		if keyword in json:
			return True
	return False
