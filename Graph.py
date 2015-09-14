#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *


def zeroOffsetFunc(self, realSize, virtSize):
	return 0


class Graph(Frame):
	def __init__(self, mainWindow,
				 offsetWFunc = zeroOffsetFunc,
				 offsetNFunc = zeroOffsetFunc,
				 offsetEFunc = zeroOffsetFunc,
				 offsetSFunc = zeroOffsetFunc,
				 **kwargs):
		# Данные
		self.virtualSize = (0, 0)	# В физических единицах от начала координат
		
		self.sizeStr = StringVar()
		self.elementStr = StringVar()
		self.cursorStr = StringVar()
		
		# Смещения
		self.offset = (0, 0, 0, 0)	# W, N, E, S
		
		# Функции смещения
		self.offsetWFunc = offsetWFunc
		self.offsetNFunc = offsetNFunc
		self.offsetEFunc = offsetEFunc
		self.offsetSFunc = offsetSFunc
		
		# Линии осей (идентификаторы холста)
		self.coordinateAxis = (None, None)
		
		self.mainWindow = mainWindow
		
		
		# Frame
		kwargs["borderwidth"] = 1
		kwargs["relief"] = "ridge"
		Frame.__init__(self, mainWindow, **kwargs)
		
		
		# Холст
		canvasKwargs = { "cursor": "crosshair" }
		if "width" in kwargs:	canvasKwargs["width"] = kwargs["width"]
		if "height" in kwargs:	canvasKwargs["height"] = kwargs["height"]
		
		self.canvas = Canvas(self, **canvasKwargs)
		self.canvas.grid(column = 0, row = 0, sticky = N + E + S + W)
		
		self.canvas.bind("<Motion>", self.onMouseMotion)
		self.canvas.bind("<Leave>", self.onMouseLeave)
		self.canvas.bind("<Configure>", self.onWindowConfigure)
		
		# Делаем холст растяжимым
		self.columnconfigure(0, weight = 1)
		self.rowconfigure(0, weight = 1)
		
		
		# Панель с метками
		self.labelArea = Frame(self)
		self.labelArea.grid(column = 0, row = 1, sticky = N + E + S + W)
		
		# Метки
		self.sizeLabel = Label(self.labelArea, textvariable = self.sizeStr, anchor = W)
		self.sizeLabel.grid(column = 0, row = 0, sticky = W)
		
		self.elementLabel = Label(self.labelArea, textvariable = self.elementStr, anchor = W)
		self.elementLabel.grid(column = 1, row = 0, sticky = W + E)
		self.labelArea.columnconfigure(1, weight = 1)
		
		self.cursorLabel = Label(self.labelArea, textvariable = self.cursorStr, anchor = E)
		self.cursorLabel.grid(column = 2, row = 0, sticky = E)
		
		self.onWindowConfigure(None)
	
	
	def onMouseMotion(self, event):
		self.updateCursorPos(event.x, event.y)
	
	
	def onMouseLeave(self, event):
		self.updateCursorPos()
	
	
	def onWindowConfigure(self, event):
		self.updateOffset()
		self.updateLabels()
	
	
	def updateLabels(self, cursorX = None, cursorY = None):
		self.sizeStr.set("Размер: (%.3f, %.3f)" % self.virtSize())
		self.updateCursorPos(cursorX, cursorY)
	
	
	def updateCursorPos(self, cursorX = None, cursorY = None):
		needDescStr = True
		
		if cursorX is None:
			cursorX = self.realOffset()[0]				# => vX = 0
			needDescStr = False
		
		if cursorY is None:
			rH = self.realHeight()
			(oW, oE, oN, oS) = self.realOffset()
			cursorY = 0.5 * (rH - oS + oN)				# => vY = 0
			needDescStr = False
		
		self.cursorStr.set("(%.3f, %.3f)" % self.realToVirtCoord((cursorX, cursorY)))
		
		# Пытаемся получить информацию о ближайшем элементе
		elementID = self.canvas.find_closest(cursorX, cursorY, halo = 10)
		
		try:
			elementDescStr = self.mainWindow.application.logic.elementDescStr(elementID[0])
		except KeyError:
			needDescStr = False
		except IndexError:
			needDescStr = False
		
		if needDescStr: self.elementStr.set(elementDescStr)
		else: self.elementStr.set("")
		
		# Тест преобразований координат
		# vC = self.realToVirtCoord((cursorX, cursorY))
		# rC = self.virtToRealCoord(vC)
		
		# if rC[0] != cursorX or rC[1] != cursorY:
		# 	print("Точки не совпадают:\n(%f, %f)\n(%f, %f)\n" % (cursorX, cursorY, rC[0], rC[1]))
	
	
	def setVirtualSize(self, size):
		self.virtualSize = size
		self.updateLabels()
	
	
	# Размеры
	def realWidth(self):
		return float(self.canvas.winfo_width())
	
	
	def realHeight(self):
		return float(self.canvas.winfo_height())
	
	
	def realSize(self):
		return (self.realWidth(), self.realHeight())
	
	
	def virtWidth(self):
		return float(self.virtualSize[0])
	
	
	def virtHeight(self):
		return float(self.virtualSize[1])
	
	
	def virtSize(self):
		return (self.virtWidth(), self.virtHeight())
	
	
	def updateOffset(self):
		rS, vS = self.realSize(), self.virtSize()
		self.offset = (self.offsetWFunc(rS, vS),
					   self.offsetNFunc(rS, vS),
					   self.offsetEFunc(rS, vS),
					   self.offsetSFunc(rS, vS))
	
	
	def realOffset(self):
		return self.offset
	
	
	def virtOffset(self):
		(oW, oE, oN, oS) = self.realOffset()
		
		# Масштабные коэффициенты
		sX = self.virtWidth()  / (self.realWidth()  - oW - oE)
		sY = self.virtHeight() / (self.realHeight() - oN - oS)
		
		return (oW * sX, oN * sY, oE * sX, oS * sY)
	
	
	# Преобразования координат
	def realToVirtCoord(self, realCoord):
		(rX, rY) = realCoord
		(rW, rH) = self.realSize()
		(vW, vH) = self.virtSize()
		
		(oW, oE, oN, oS) = self.realOffset()
		
		if rW - oW - oE <= 0:	vX = 0
		else:					vX = (rX - oW) / (rW - oW - oE) * vW
		
		if rH - oN - oS <= 0:	vY = 0
		else:					vY = (0.5 + (oN - rY) / (rH - oN - oS)) * vH
		
		# Отладочный вывод
		# print("(rX, rY) = (%f, %f)" % (rX, rY))
		# print("(rW, rH) = (%f, %f)" % (rW, rH))
		# print("(vW, vH) = (%f, %f)" % (vW, vH))
		# print("(vX, vY) = (%f, %f)" % (vX, vY))
		# print()
		
		return (vX, vY)
	
	
	def virtToRealX(self, vX):
		rW, vW = self.realWidth(), self.virtWidth()
		(oW, oE, oN, oS) = self.realOffset()
		
		if vW <= 0:	rX = 0
		else:		rX = vX * (rW - oW - oE) / vW + oW
		
		return rX
	
	
	def virtToRealY(self, vY):
		rH, vH = self.realHeight(), self.virtHeight()
		(oW, oE, oN, oS) = self.realOffset()
		
		if vH <= 0:	rY = 0
		else:		rY = (0.5 - vY / vH) * (rH - oN - oS) + oN
		
		return rY
	
	
	def virtToRealCoord(self, virtCoord):
		# (vX, vY) = virtCoord
		# (rW, rH) = self.realSize()
		# (vW, vH) = self.virtSize()
		
		# (oW, oE, oN, oS) = self.realOffset()
		
		# if vW <= 0:	rX = 0
		# else:		rX = vX * (rW - oW - oE) / vW + oW
		
		# if vH <= 0:	rY = 0
		# else:		rY = (0.5 - vY / vH) * (rH - oN - oS) + oN
		
		return (self.virtToRealX(virtCoord[0]), self.virtToRealY(virtCoord[1]))
	
	
	def drawBar(self, x, L, H, q, **kwargs):
		leftTop     = self.virtToRealCoord((    x,  0.5 * H))
		rightBottom = self.virtToRealCoord((x + L, -0.5 * H))
		
		return self.canvas.create_rectangle(leftTop[0],     leftTop[1],
											rightBottom[0], rightBottom[1],
											**kwargs)
	
	def drawNode(self, x, F, **kwargs):
		return self.drawVAxis(x, fill = "green", dash = (3, 3), **kwargs)
	
	
	def drawLineReal(self, p0, p1, **kwargs):
		return self.canvas.create_line(p0[0], p0[1], p1[0], p1[1], **kwargs)
	
	
	def drawLine(self, point0, point1, **kwargs):
		p0, p1 = self.virtToRealCoord(point0), self.virtToRealCoord(point1)
		return self.drawLineReal(p0[0], p0[1], p1[0], p1[1], **kwargs)
	
	
	def drawHAxis(self, vY = 0, **kwargs):
		rW = self.realWidth()
		rY = self.virtToRealY(vY)
		
		return self.drawLineReal((0, rY), (rW - 5, rY), **kwargs)
	
	
	def drawVAxis(self, vX = 0, **kwargs):
		rH = self.realHeight()
		rX = self.virtToRealX(vX)
		
		return self.drawLineReal((rX, rH), (rX, 5), **kwargs)
	
	
	def drawAxis(self, center = (0, 0), **kwargs):
		axisX = self.drawHAxis(center[1], **kwargs)
		axisY = self.drawVAxis(center[0], **kwargs)
		return (axisX, axisY)
	
	
	def drawCoordinateAxisX(self):
		axisArgs = { "fill": "blue", "arrow": LAST, "dash": (5, 5), "state": DISABLED }
		
		if self.virtualSize[0] != 0 and self.virtualSize[1] != 0:
			self.coordinateAxis = (self.drawHAxis(0, **axisArgs), self.coordinateAxis[1])
		return self.coordinateAxis
	
	
	def drawCoordinateAxisY(self):
		axisArgs = { "fill": "blue", "arrow": LAST, "dash": (5, 5), "state": DISABLED }
		
		if self.virtualSize[0] != 0 and self.virtualSize[1] != 0:
			self.coordinateAxis = (self.coordinateAxis[0], self.drawVAxis(0, **axisArgs))
		return self.coordinateAxis
	
	
	def drawCoordinateAxis(self):
		axisArgs = { "fill": "blue", "arrow": LAST, "dash": (5, 5), "state": DISABLED }
		
		if self.virtualSize[0] != 0 and self.virtualSize[1] != 0:
			self.coordinateAxis = self.drawAxis((0, 0), **axisArgs)
		return self.coordinateAxis
	
	
	def clear(self):
		self.canvas.delete(*self.canvas.find_all())
		self.coordinateAxis = (None, None)
