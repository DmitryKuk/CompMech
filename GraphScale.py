#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)


def zeroOffsetFunc(self, realSize, virtSize):
	return (0, 0, 0, 0)


class GraphScale:
	def __init__(self, offsetFunc = zeroOffsetFunc):
		# Размер графика (width, heigth; real, virtual)
		self.vW, self.vH = 0.0, 0.0		# В физических единицах от начала координат
		self.rW, self.rH = 0, 0			# В пикселях
		
		# Смещения
		self.roW, self.roN, self.roE, self.roS = 0, 0, 0, 0		# Реальные
		self.voW, self.voN, self.voE, self.voS = 0, 0, 0, 0		# Виртуальные
		
		# Чистые реальные размеры (реальные, за вычетом смещений)
		self.crW, self.crH = 0, 0
		
		# Масштабные коэффициенты
		self.kX, self.kY = 0.0, 0.0
		
		# Функция смещения
		self.offsetFunc = zeroOffsetFunc
		self.setOffsetFunc(offsetFunc)
		
		self.setRealSize((0, 0))
		self.setVirtSize((0, 0))
		self.update()
	
	
	def __str__(self):
		return "Scale: Real: (%s, %s); Virtual: (%s, %s)" % (self.rW, self.rH, self.vW, self.vH)
	
	
	# Реальные размеры
	def realSize(self):
		return (self.rW, self.rH)
	
	def setRealSize(self, size):
		(self.rW, self.rH) = size
	
	
	# Виртуальные размеры
	def virtSize(self):
		return (self.vW, self.vH)
	
	def setVirtSize(self, size):
		self.vW, self.vH = float(size[0]), float(size[1])
		self.update()
	
	
	# Смещения
	def realOffset(self):
		return (self.roW, self.roN, self.roE, self.roS)
	
	def virtOffset(self):
		return (self.voW, self.voN, self.voE, self.voS)
	
	
	def setOffsetFunc(self, offsetFunc):
		self.offsetFunc = offsetFunc if offsetFunc is not None else zeroOffsetFunc
		self.update()
	
	
	def update(self):
		# Реальные смещения
		self.roW, self.roN, self.roE, self.roS = self.offsetFunc(self.realSize(), self.virtSize())
		
		# Чистые размеры
		self.crW, self.crH = (self.rW - self.roW - self.roE), (self.rH - self.roN - self.roS)
		
		# Масштабные коэффициенты
		self.kX = 0.0 if self.crW <= 0 else self.vW / self.crW
		self.kY = 0.0 if self.crH <= 0 else self.vH / self.crH
		
		# Виртуальные смещения
		self.voW, self.voN, self.voE, self.voS = (self.roW * self.kX), (self.roN * self.kY), \
												 (self.roE * self.kX), (self.roS * self.kY)
	
	
	# Преобразования координат
	def realToVirtX(self, rX):
		return 0.0 if self.crW <= 0 else self.vW * (rX - self.roW) / self.crW
	
	def realToVirtY(self, rY):
		return 0.0 if self.crH <= 0 else self.vH * (0.5 + float(self.roN - rY) / self.crH)
	
	def realToVirtCoord(self, realCoord):
		return (self.realToVirtX(realCoord[0]), self.realToVirtY(realCoord[1]))
	
	
	def virtToRealX(self, vX):
		return 0 if self.vW <= 0 else vX * self.crW / self.vW + self.roW
	
	def virtToRealY(self, vY):
		return 0 if self.vH <= 0 else (0.5 - float(vY) / self.vH) * self.crH + self.roN
	
	def virtToRealCoord(self, virtCoord):
		return (self.virtToRealX(virtCoord[0]), self.virtToRealY(virtCoord[1]))
	
	
	# Преобразования длин
	def realToVirtXLen(self, rL):
		return float(rL) * self.kX
	
	def realToVirtYLen(self, rL):
		return float(rL) * self.kX
	
	def realToVirtVector(self, rV):
		return (self.realToVirtXLen(rV[0]), self.realToVirtYLen(rV[1]))
