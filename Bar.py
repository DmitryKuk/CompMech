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
				L     = json.get("L", 0.0)
				A     = json.get("A", 0.0)
				E     = json.get("E", 0.0)
				Sigma = json.get("Sigma", 0.0)
				q     = json.get("q", 0.0)
				
				K     = json.get("K")
				Q     = json.get("Q")
				U0    = json.get("U0")
				UL    = json.get("UL")
			else:
				L     = json.get("L", default.L)
				A     = json.get("A", default.A)
				E     = json.get("E", default.E)
				Sigma = json.get("Sigma", default.Sigma)
				q     = json.get("q", default.q)
				
				K     = json.get("K", default.K)
				Q     = json.get("Q", default.Q)
				U0    = json.get("U0", default.U0)
				UL    = json.get("UL", default.UL)
		elif default is not None:
			L     = default.L
			A     = default.A
			E     = default.E
			Sigma = default.Sigma
			q     = default.q
			
			K     = default.K
			Q     = default.Q
			U0    = default.U0
			UL    = default.UL
		else:
			L     = 0.0
			A     = 0.0
			E     = 0.0
			Sigma = 0.0
			q     = 0.0
			
			K     = None
			Q     = None
			U0    = None
			UL    = None
		
		
		if K is None or Q is None or U0 is None or UL is None:
			self.K  = None
			self.Q  = None
			self.U0 = None
			self.UL = None
		else:
			try:
				self.K  = eval(K)
				self.Q  = eval(Q)
				self.U0 = float(U0)
				self.UL = float(UL)
			except:
				self.K  = None
				self.Q  = None
				self.U0 = None
				self.UL = None
		
		
		try:
			self.L     = float(L)
		except:
			raise Exception("Некорректная длина стержня (ожидается: число)")
		
		try:
			self.A     = float(A)
		except:
			raise Exception("Некорректная площадь поперечного сечения стержня (ожидается: число)")
		
		try:
			self.E     = float(E)
		except:
			raise Exception("Некорректный модуль упругости стержня (ожидается: число)")
		
		try:
			self.Sigma = float(Sigma)
		except:
			raise Exception("Некорректное допускаемое напряжение (ожидается: число)")
		
		try:
			self.q     = float(q)
		except:
			raise Exception("Некорректная нагрузка на стержень (ожидается: число)")
		
		
		if default is not None:
			if self.L <= 0:
				raise Exception("Некорректная длина стержня: L = %f " \
								"(ожидается: L > 0; %s)" % (self.L, self))
			
			if self.A <= 0:
				raise Exception("Некорректная площадь поперечного сечения стержня: A = %f " \
								"(ожидается: A > 0; %s)" % (self.A, self))
			
			if self.E <= 0:
				raise Exception("Некорректный модуль упругости стержня: E = %f " \
								"(ожидается: E > 0; %s)" % (self.E, self))
		
		self.height = 0 if self.A <= 0 else math.sqrt(self.A)
	
	
	def dump(self):
		retDict = ConstructionElement.dump(self)
		
		retDict.update({
			"L": self.L,
			"A": self.A,
			
			"E": self.E,
			"Sigma": self.Sigma,
			
			"q": self.q
		})
		
		if self.calculated():
			retDict.update({
				"K": str(self.K),
				"Q": str(self.Q),
				"U0": round(self.U0, 15),
				"UL": round(self.UL, 15)
			})
		print(retDict)
		print()
		return retDict
	
	
	def calculated(self):
		return False if self.U0 is None else True
	
	
	def calculate(self):
		self.K = None if self.L <= 0 else \
				 self.E * self.A / self.L * Matrix([[1, -1], [-1, 1]])
		
		self.Q = self.q * self.L / 2 * Matrix([[-1], [-1]])
	
	
	def __str__(self):
		return \
			"Стержень (%d)%s:  x = %.3f;  L = %.3f;  A = %.3f;  E = %.3f;  [σ] = %.3f;  q = %.3f" \
			% (self.i,
			   "" if self.label == "" else "  \"" + self.label + "\"",
			   self.x, self.L, self.A, self.E, self.Sigma, self.q)
	
	
	def supportDescStr(self, x):
		return ("x(local) = %.3f" % (x - self.x)) \
			   + ("" if self.U0 is None else \
				  ";  Nx(x) = %.3f;  U(x) = %.3f;  σ(x) = %.3f;  U0 = %.3f;  UL = %.3f" \
				  % (self.NGlobal(x), self.UGlobal(x), self.SigmaGlobal(x), self.U0, self.UL))
	
	
	def size(self):
		return (self.L, self.height)
	
	
	def loads(self):
		return (0, self.q)
	
	
	def maxComponents(self):
		return ( \
			max(abs(self.NLocal(0)), abs(self.NLocal(self.L))), \
			max(abs(self.ULocal(0)), abs(self.ULocal(self.L))), \
			max(abs(self.SigmaLocal(0)), abs(self.SigmaLocal(self.L)), \
				abs(self.Sigma)) \
		)
	
	
	def ULocal(self, x):
		return (1 - x / self.L) * self.U0 \
			   + x / self.L * self.UL \
			   + self.q * self.L / (2 * self.E * self.A) * x * (1 - x / self.L)
	
	
	def UGlobal(self, x):
		return self.ULocal(x - self.x)
	
	
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
	
	
	def ULineLocal(self):
		return [(0, self.ULocal(0)), (self.L, self.ULocal(self.L))]
	
	
	def ULineGlobal(self):
		local = self.ULineLocal()
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
	for keyword in [ "L", "A", "E", "Sigma", "q", "U0", "UL" ]:
		if keyword in json:
			return True
	return False
