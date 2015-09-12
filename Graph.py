#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *


class Graph(Frame):
	def __init__(self, mainWindow, **kwargs):
		# Данные
		self.virtualSize	= (0, 0)	# В физических единицах от начала координат
		
		self.sizeStr = StringVar()
		self.elementStr = StringVar()
		self.cursorStr = StringVar()
		
		
		# Frame
		kwargs["borderwidth"] = 1
		kwargs["relief"] = "groove"
		Frame.__init__(self, mainWindow, kwargs)
		
		
		# Холст
		canvasKwargs = { "cursor": "crosshair", "bg": "orange" }
		if "width" in kwargs:
			canvasKwargs["width"] = kwargs["width"]
		if "height" in kwargs:
			canvasKwargs["height"] = kwargs["height"]
		
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
		
		self.updateLabels()
	
	
	def onMouseMotion(self, event):
		self.updateLabels(event.x, event.y)
	
	
	def onMouseLeave(self, event):
		self.updateLabels()
	
	
	def onWindowConfigure(self, event):
		self.updateLabels()
	
	
	def updateLabels(self, cursorX = 0 , cursorY = 0):
		self.sizeStr.set("Размер: (%.4f, %.4f)" % self.virtualSize)
		self.elementStr.set("")
		
		# Вычисляем положение курсора в виртуальных координатах
		realX, realY = self.canvas.winfo_width(), self.canvas.winfo_height()
		(virtX, virtY) = self.virtualSize
		
		if realX == 0: cursorX = 0
		else: cursorX *= virtX / realX
		
		if realY == 0: cursorY = 0
		else: cursorY = (realY - cursorY) * virtY / realY
		
		print("Virtual: (%.4f, %.4f)" % (cursorX, cursorY))
		self.cursorStr.set("(%.4f, %.4f)" % (cursorX, cursorY))
	
	
	def setVirtualSize(self, size):
		self.virtualSize = size
		self.updateLabels()
