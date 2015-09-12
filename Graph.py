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
		self.virtSize = (0, 0)	# В физических единицах от начала координат
		
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
		
		
		# Frame
		kwargs["borderwidth"] = 1
		kwargs["relief"] = "groove"
		Frame.__init__(self, mainWindow, **kwargs)
		
		
		# Холст
		canvasKwargs = { "cursor": "crosshair", "bg": "orange" }
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
		self.updateLabels(event.x, event.y)
	
	
	def onMouseLeave(self, event):
		self.updateLabels()
	
	
	def onWindowConfigure(self, event):
		self.updateOffset()
		self.updateLabels()
	
	
	def updateLabels(self, cursorX = None, cursorY = None):
		if cursorX is None: cursorX = self.offset[0]			# => vX = 0
		if cursorY is None: cursorY = self.realHeight() * 0.5	# => vY = 0
		
		self.sizeStr.set("Размер: (%.3f, %.3f)" % self.virtSize)
		self.elementStr.set("")
		
		self.cursorStr.set("(%.3f, %.3f)" % self.realToVirtCoord((cursorX, cursorY)))
		
		vC = self.realToVirtCoord((cursorX, cursorY))
		rC = self.virtToRealCoord(vC)
	
	
	def setVirtualSize(self, size):
		self.virtSize = size
		self.updateLabels()
	
	
	# Размеры
	def realWidth(self):
		return float(self.canvas.winfo_width())
	
	
	def realHeight(self):
		return float(self.canvas.winfo_height())
	
	
	def realSize(self):
		return (self.realWidth(), self.realHeight())
	
	
	def virtWidth(self):
		return float(self.virtSize[0])
	
	
	def virtHeight(self):
		return float(self.virtSize[1])
	
	
	def virtSize(self):
		return (self.virtWidth(), self.virtHeight())
	
	
	def updateOffset(self):
		self.offset = (self.offsetWFunc(self.realSize(), self.virtSize),
					   self.offsetNFunc(self.realSize(), self.virtSize),
					   self.offsetEFunc(self.realSize(), self.virtSize),
					   self.offsetSFunc(self.realSize(), self.virtSize))
	
	
	def realOffset(self):
		return self.offset
	
	
	# Преобразования координат
	def realToVirtCoord(self, realCoord):
		(rX, rY) = realCoord
		(rW, rH) = self.realSize()
		(vW, vH) = self.virtSize
		
		(oW, oE, oN, oS) = self.realOffset()
		
		if rW <= 0:	vX = 0
		else:		vX = (rX - oW) / (rW - oW - oE) * vW
		
		if rH <= 0:	vY = 0
		else:		vY = ((rH - rY - oS) / (rH - oS - oN) - 0.5) * vH
		
		# Debug print
		# print("(rX, rY) = (%f, %f)" % (rX, rY))
		# print("(rW, rH) = (%f, %f)" % (rW, rH))
		# print("(vW, vH) = (%f, %f)" % (vW, vH))
		# print("(vX, vY) = (%f, %f)" % (vX, vY))
		# print()
		
		return (vX, vY)
	
	
	def virtToRealCoord(self, virtCoord):
		(vX, vY) = virtCoord
		(rW, rH) = self.realSize()
		(vW, vH) = self.virtSize
		
		(oW, oE, oN, oS) = self.realOffset()
		
		if vW <= 0:	rX = 0
		else:		rX = vX * (rW - oW - oE) / vW + oW
		
		if vH <= 0:	rY = 0
		else:		rY = rH - oS - (vY / vH + 0.5) * (rH - oS - oN)
		
		return (rX, rY)
