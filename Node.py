#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from ConstructionElement import ConstructionElement


class Node(ConstructionElement):
	def __init__(self, json = None, default = None):
		ConstructionElement.__init__(self, json, default)
		
		self.fixed = False
		self.F = 0.0
		
		self.Delta = None	# Смещение узла; вычисляется конструкцией
		
		if json is not None:
			if default is None:
				fixed = json.get("fixed", False)
				F     = json.get("F", 0.0)
				
				Delta = json.get("Delta")
			else:
				fixed = json.get("fixed", default.fixed)
				F     = json.get("F", default.F)
				
				Delta = json.get("Delta", default.Delta)
		elif default is not None:
			fixed = default.fixed
			F     = default.F
			
			Delta = default.Delta
		else:
			fixed = False
			F     = 0.0
			
			Delta = None
		
		
		try:
			self.F = float(F)
		except:
			raise Exception("Некорректная нагрузка на узел (ожидается: число)")
		
		try:
			self.fixed = bool(fixed)
		except:
			raise Exception("Некорректные данные о заделке (ожидается: булево значение")
		
		try:
			self.Delta = float(Delta)
		except:
			pass
	
	
	def dump(self):
		retDict = ConstructionElement.dump(self)
		
		retDict.update({
			"fixed": self.fixed,
			
			"F": self.F
		})
		
		if self.calculated():
			retDict.update({ "Delta": round(self.Delta, 15) })
		
		return retDict
	
	
	def __str__(self):
		fixedStr = "зафиксирован" if self.fixed else "свободен"
		
		return \
			"Узел [%d]%s:  x = %.3f;  F = %.3f;  %s%s" \
			% (self.i,
			   "" if self.label == "" else "  \"" + self.label + "\"",
			   self.x, self.F, fixedStr,
			   "" if self.Delta is None else ";  Δ%d = %.3f" % ( self.i, self.Delta))
	
	
	def size(self):
		return (0, 0)
	
	
	def loads(self):
		return (self.F, 0)
	
	
	def calculated(self):
		return False if self.Delta is None else True


def similarToNode(json):
	for keyword in [ "fixed", "F", "Delta" ]:
		if keyword in json:
			return True
	return False
