#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *
from PIL import Image
import os, subprocess, tempfile

import GraphScale
from GraphScale import GraphScale, zeroOffsetFunc
from Style import *


class Graph(Frame):
	def __init__(self, mainWindow,
				 offsetFunc = zeroOffsetFunc,
				 xOffset = 0,
				 
				 onCursorMovement = None,
				 onMouse1Clicked = None,
				 
				 **kwargs):
		# Frame
		kwargs["borderwidth"] = 1
		kwargs["relief"] = "ridge"
		Frame.__init__(self, mainWindow, **kwargs)
		
		self.mainWindow = mainWindow
		
		
		# Смещение начала координат
		self.xOffset = xOffset
		
		# Калькуляторы масштаба (для вычисления координат)
		self.mainScale = GraphScale(offsetFunc)
		self.NSigmaScale = GraphScale(offsetFunc)
		self.UScale = GraphScale(offsetFunc)
		
		
		# События
		self.onCursorMovementCallback = onCursorMovement
		self.onMouse1ClickedCallback = onMouse1Clicked
		
		
		# Максимальные нагрузки
		self.maxF = 0		# Максимальные нагрузки (в физических единицах; для масштаба)
		self.maxqOnL = 0	# Максимальная относительная распределённая нагрузка = q / L
		self.specq = 0		# q, при котором q / L -> max
		self.maxFReal = 0	# Максимальная длина стрелки силы в пикселях
							# (чтобы оставалась в пределах графика)
		
		
		self.maxNSigma, self.maxU = 0, 0
		
		self.sizeStr = StringVar()
		self.elementStr = StringVar()
		self.cursorStr = StringVar()
		
		
		# Линии осей (идентификаторы холста)
		self.coordinateAxis = (None, None)
		self.rightNodeAxis = None
		
		
		# Холст
		canvasStyle = { "cursor": "crosshair", "bg": "#FFFFFF" }
		if "width" in kwargs:	canvasStyle["width"] = kwargs["width"]
		if "height" in kwargs:	canvasStyle["height"] = kwargs["height"]
		
		self.canvas = Canvas(self, **canvasStyle)
		self.canvas.grid(column = 0, row = 0, sticky = N + E + S + W)
		
		self.canvas.bind("<Motion>", lambda event: self.updateCursorPos(event.x, event.y))
		self.canvas.bind("<Leave>",  lambda event: self.updateCursorPos())
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
		
		self.elementLabel = Label(self.labelArea, textvariable = self.elementStr, anchor = W,
								  justify = LEFT)
		self.elementLabel.grid(column = 1, row = 0, sticky = W + E)
		self.labelArea.columnconfigure(1, weight = 1)
		
		self.cursorLabel = Label(self.labelArea, textvariable = self.cursorStr, anchor = E)
		self.cursorLabel.grid(column = 2, row = 0, sticky = E)
		
		self.onWindowConfigure(None)
		
		
		# Контекстное меню
		self.menu = Menu(self, tearoff = 0)
		self.menu.add_command(label = "Сохранить изображение",
							  command = self.onMenuEntrySaveImageClicked)
		
		self.canvas.bind("<ButtonRelease-2>",
						 lambda event: self.menu.post(event.x_root, event.y_root))
		self.canvas.bind("<ButtonRelease-1>", self.onMouse1Clicked)
	
	
	def onWindowConfigure(self, event):
		size = (self.canvas.winfo_width(), self.canvas.winfo_height())
		for scale in self.mainScale, self.NSigmaScale, self.UScale:
			scale.setRealSize(size)
		self.updateOffset()
		self.updateLabels()
	
	
	def onMouse1Clicked(self, event):
		if self.onMouse1ClickedCallback is not None:
			cursorRealCoord = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
			cursorVirtCoord = self.localToGlobal(self.mainScale.realToVirtCoord(cursorRealCoord))
			
			self.onMouse1ClickedCallback(self, cursorRealCoord, cursorVirtCoord, self.mainScale)
	
	
	def updateLabels(self, cursorX = None, cursorY = None):
		self.sizeStr.set("Размер: (%.3f, %.3f)" % self.mainScale.virtSize())
		self.updateCursorPos(cursorX, cursorY)
	
	
	def updateCursorPos(self, cursorX = None, cursorY = None):
		vX, vY = 0.0, 0.0
		
		if cursorX is not None:
			cursorX = self.canvas.canvasx(cursorX)
			vX = self.mainScale.realToVirtX(cursorX)
		
		if cursorY is not None:
			cursorY = self.canvas.canvasy(cursorY)
			vY = self.mainScale.realToVirtY(cursorY)
		
		globCoord = self.localToGlobal((vX, vY))
		self.cursorStr.set("(%.3f, %.3f)" % globCoord)
		
		if self.onCursorMovementCallback is not None:
			self.onCursorMovementCallback(self, (cursorX, cursorY), globCoord, self.mainScale)
	
	
	def setVirtSize(self, size):
		self.mainScale.setVirtSize(size)
		for scale in self.NSigmaScale, self.UScale:
			scale.setVirtSize((size[0], scale.vH))
		
		self.updateOffset()
		self.updateLabels()
	
	
	def setMaxLoads(self, F, specq, maxqOnL):
		self.maxF, self.specq, self.maxqOnL = abs(F), abs(specq), abs(maxqOnL)
		self.updateOffset()
	
	
	def setMaxComponents(self, maxN, maxU, maxSigma):
		self.maxNSigma, self.maxU = max(abs(maxN), abs(maxSigma)), maxU
		vW = self.mainScale.vW
		
		self.NSigmaScale.setVirtSize((vW, self.maxNSigma * 2.0 / componentOnHeight))
		self.UScale.setVirtSize((vW, self.maxU * 2.0 / componentOnHeight))
		
		self.updateOffset()
	
	
	def setTitle(self, text):
		self.canvas.create_text(self.mainScale.rW / 2, 10, text = text)
	
	
	def setElementStr(self, text):
		self.elementStr.set(text)
	
	
	def updateOffset(self):
		for scale in self.mainScale, self.NSigmaScale, self.UScale:
			scale.update()
		
		# Обновляем максимальные нагрузки
		oF = self.mainScale.realOffset()
		self.maxFReal = min(oF[0], oF[2])	# W, E
	
	
	def drawBar(self, bar, drawBar = True, drawLoads = True):
		leftTop     = self.mainScale.virtToRealCoord(self.globalToLocal((bar.x,
																		 0.5 * bar.height)))
		rightBottom = self.mainScale.virtToRealCoord(self.globalToLocal((bar.x + bar.L,
																		 -0.5 * bar.height)))
		
		
		if drawBar:
			self.canvas.create_rectangle(leftTop[0],     leftTop[1],
										 rightBottom[0], rightBottom[1],
										 **barStyle)
		
		
		if drawLoads and bar.q != 0 and self.maxqOnL != 0 and self.specq != 0:
			qSpace = 5 * self.mainScale.kX		# Пробелы 5 пикселей между стрелками
			qIndent = 12 * self.mainScale.kX	# Отступы в 12 пикселей по границам стержней
			
			# Масштабированная длина стрелки q:
			# qLen = (bar.q ** 2) / (2 * self.maxqOnL * self.specq)
			
			# Фиксированная длина стрелки q:
			qLen = self.mainScale.realToVirtXLen(50)
			
			if bar.q > 0:
				x1, xmin = bar.x + bar.L, bar.x + qIndent
				while x1 > xmin:
					x2 = max(x1 - qLen, xmin)
					self.drawLine((x1, 0), (x2, 0), **qLineStyle)
					x1 -= qLen + qSpace
			elif bar.q < 0:
				x1, xmax = bar.x, bar.x + bar.L - qIndent
				while x1 < xmax:
					x2 = min(x1 + qLen, xmax)
					self.drawLine((x1, 0), (x2, 0), **qLineStyle)
					x1 += qLen + qSpace
	
	
	def drawBarCurves(self, bar, drawN = False, drawU = False, drawSigma = False):
		# Рисуем эпюры N(x), u(x), Sigma(x)
		if drawN:
			self.drawCurve(self.NSigmaScale, bar.NLineGlobal(), **NLineStyle)
		
		
		if drawU:
			rX, maxRX = self.UScale.virtToRealX(bar.x), self.UScale.virtToRealX(bar.x + bar.L)
			rY = self.UScale.virtToRealY(bar.UGlobal(self.UScale.realToVirtX(rX)))
			while rX <= maxRX:
				rXNext = rX + 1
				rYNext = self.UScale.virtToRealY(bar.UGlobal(self.UScale.realToVirtX(rXNext)))
				self.canvas.create_line(rX, rY, rXNext, rYNext, **ULineStyle)
				rX = rXNext
				rY = rYNext
		
		
		if drawSigma:
			# SigmaMax, -SigmaMax
			line = bar.SigmaMaxLineGlobal()
			self.drawCurve(self.NSigmaScale, line, **SigmaMaxLineStyle)
			
			line = [(line[0][0], -line[0][1]), (line[1][0], -line[1][1])]
			self.drawCurve(self.NSigmaScale, line, **SigmaMaxLineStyle)
			
			# Sigma(x)
			self.drawCurve(self.NSigmaScale, bar.SigmaLineGlobal(),
						   **SigmaLineStyle)
	
	
	def drawNode(self, node, drawNode = True, drawLoads = True):
		# Отображаем узел в виде вертикальной оси
		if node.x == self.xOffset:
			self.coordinateAxis[1]	# Используем ось Oy, если узел самый левый
		else:
			self.drawVAxis(node.x, **nodeAxisStyle)	# Или рисуем новую
		
		
		# Отображаем штриховку, если узел фиксирован
		if drawNode and node.fixed:
			hatch = (10, 10)	# Размеры штриха (в пикселях)
			hatchNum = 4		# Количество штрихов в каждую сторону от горизонтальной оси
			
			(rX, rY) = self.mainScale.virtToRealCoord((self.globalToLocalX(node.x), 0))
			
			# Вычисляем координаты штрихов...
			if self.globalToLocalX(node.x) == 0:		# Узел самый левый -- штриховка слева
				p1 = (rX - hatch[0], rY - hatch[1] * (hatchNum - 1))
				p2 = (rX, rY - hatch[1] * hatchNum)
			else:				# Штриховка справа
				p1 = (rX, rY - hatch[1] * (hatchNum - 1))
				p2 = (rX + hatch[0], rY - hatch[1] * hatchNum)
			
			# ...и рисуем их
			for i in range(2 * hatchNum):
				self.drawLineReal(p1, p2, **hatchStyle)
				
				p1 = (p1[0], p1[1] + hatch[1])
				p2 = (p2[0], p2[1] + hatch[1])
		
		
		if drawLoads:
			# Отображаем нагрузку
			if node.F != 0:
				# Масштабированная длина стрелки:
				# p0 = (node.x - float(node.F * self.maxFReal * self.mainScale.vW) \
				# 			   / (self.maxF * self.mainScale.rW), 0)
				# p1 = (node.x, 0)
				
				
				# Фиксированная длина стерлки:
				FSign = +1 if node.F >= 0 else -1
				realFLen = min(self.mainScale.roW, self.mainScale.roE)
				FLen = FSign * self.mainScale.realToVirtXLen(realFLen)
				
				p0 = (node.x - FLen, 0)
				p1 = (node.x, 0)
				self.drawLine(p0, p1, **FLineStyle)
	
	
	def drawLineReal(self, p0, p1, **kwargs):
		self.canvas.create_line(p0[0], p0[1], p1[0], p1[1], **kwargs)
	
	
	def drawLine(self, point0, point1, **kwargs):
		self.drawCurve(scale = self.mainScale, line = [point0, point1], **kwargs)
	
	
	def drawCurve(self, scale, line, **kwargs):
		p0 = scale.virtToRealCoord(self.globalToLocal(line[0]))
		p1 = scale.virtToRealCoord(self.globalToLocal(line[1]))
		self.drawLineReal(p0, p1, **kwargs)
	
	
	def drawHAxis(self, vY = 0, scale = None, **kwargs):
		if scale is None: scale = self.mainScale
		
		rW = scale.rW
		rY = scale.virtToRealY(self.globalToLocalY(vY))
		
		self.drawLineReal((0, rY), (rW - 5, rY), **kwargs)
	
	
	def drawVAxis(self, vX = None, scale = None, **kwargs):
		if scale is None: scale = self.mainScale
		if vX == None: vX = self.xOffset
		
		rH = scale.rH
		rX = scale.virtToRealX(self.globalToLocalX(vX))
		
		self.drawLineReal((rX, rH), (rX, 5), **kwargs)
	
	
	def drawAxis(self, center = (None, 0), **kwargs):
		axisX = self.drawHAxis(center[1], **kwargs)
		axisY = self.drawVAxis(center[0], **kwargs)
	
	
	def drawCoordinateAxisX(self):
		(vW, vH) = self.mainScale.virtSize()
		if vW != 0 and vH != 0:
			self.coordinateAxis = (self.drawHAxis(**coordinateAxisStyle),
								   self.coordinateAxis[1])
	
	
	def drawCoordinateAxisY(self):
		(vW, vH) = self.mainScale.virtSize()
		if vW != 0 and vH != 0:
			self.coordinateAxis = (self.coordinateAxis[0],
								   self.drawVAxis(**coordinateAxisStyle))
		self.coordinateAxis[1],
		self.drawText(self.localToGlobal((0, -self.mainScale.vH / 2)),
										 realOffset = XLabelOffset,
										 text = (labelFormat % self.localToGlobalX(0)),
										 **XLabelStyle)
	
	
	def drawCoordinateAxis(self):
		self.drawCoordinateAxisX()
		self.drawCoordinateAxisY()
	
	
	# Вспомогательные оси
	def drawXVAxis(self, vX):
		self.drawVAxis(vX, scale = self.mainScale, **XAxisStyle),
		self.drawText((vX, -self.mainScale.vH / 2), realOffset = XLabelOffset,
					  text = (labelFormat % vX), **XLabelStyle)
	
	
	def drawNHAxis(self, vY):
		self.drawHAxis(vY, scale = self.NSigmaScale, **NAxisStyle),
		self.drawText(self.localToGlobal((0, vY)), realOffset = NLabelOffset,
					  scale = self.NSigmaScale, text = (labelFormat % vY), **NLabelStyle)
	
	
	def drawUHAxis(self, vY):
		self.drawHAxis(vY, scale = self.UScale, **UAxisStyle),
		self.drawText(self.localToGlobal((0, vY)), realOffset = ULabelOffset,
					  scale = self.UScale, text = (labelFormat % vY), **ULabelStyle)
	
	
	def drawSigmaHAxis(self, vY):
		self.drawHAxis(vY, scale = self.NSigmaScale, **SigmaAxisStyle),
		self.drawText(self.localToGlobal((0, vY)), realOffset = SigmaLabelOffset,
					  scale = self.NSigmaScale, text = (labelFormat % vY), **SigmaLabelStyle)
	
	
	def drawText(self, virtCoord, text, scale = None, realOffset = (0, 0), **kwargs):
		if scale is None: scale = self.mainScale
		
		def textOffset(realCoord):
			return (realCoord[0] + realOffset[0], realCoord[1] + realOffset[1])
		
		realCoord = textOffset(scale.virtToRealCoord(self.globalToLocal(virtCoord)))
		self.canvas.create_text(*realCoord, text = text, **kwargs)
	
	
	# Смещение координатной системы
	def setLocalCoordinate(self, x):
		self.xOffset = x
	
	
	def globalToLocalX(self, vX):
		return vX - self.xOffset
	
	
	def localToGlobalX(self, vX):
		return vX + self.xOffset
	
	
	def globalToLocalY(self, vY):
		return vY
	
	
	def localToGlobalY(self, vY):
		return vY
	
	
	def globalToLocal(self, virtCoord):
		return (self.globalToLocalX(virtCoord[0]), self.globalToLocalY(virtCoord[1]))
	
	
	def localToGlobal(self, virtCoord):
		return (self.localToGlobalX(virtCoord[0]), self.localToGlobalY(virtCoord[1]))
	
	
	# Очистка графика
	def clear(self):
		self.canvas.delete(*self.canvas.find_all())
		self.coordinateAxis = (None, None)
	
	
	# Сохранение изображения
	def saveImage(self, filename):
		# Рабочий вариант 1 с пробегом по всем пикселям холста
		# (width, height) = self.realSize()
		# width, height = int(width), int(height)
		
		# image = Image.new("RGB", (width, height), "white")
		# draw = ImageDraw.Draw(image)
		
		# for y in range(height):
		# 	for x in range(width):
		# 		ids = self.canvas.find_overlapping(x, y, x, y)
		# 		if ids:
		# 			draw.point((x, y), fill = self.canvas.itemcget(ids[-1], "fill"))
		
		# del draw
		# image.save(filename)
		
		
		# Рабочий вариант 2 со временным файлом вместо обычного
		# ps = self.canvas.postscript()
		# file = tempfile.NamedTemporaryFile()			# Создаём временный файл
		# file.write(bytes(ps, "UTF-8"))					# Сохраняем в него Postscript
		# image = Image.open(file.name).save(filename)	# Конвертируем в нужный формат
		# file.close()
		
		# Рабочий вариант 3 со скриншотами
		x1 = self.canvas.winfo_rootx()
		y1 = self.canvas.winfo_rooty()
		
		x2, y2 = x1 + self.canvas.winfo_width(), y1 + self.canvas.winfo_height()
		
		grab((x1, y1, x2, y2)).save(filename)
	
	
	def onMenuEntrySaveImageClicked(self):
		filetypes = [("PNG", "*.png"), ("JPG", ".jpg"), ("BMP", "*.bmp"), ("SVG", "*.svg")]
		filename = filedialog.asksaveasfilename(parent = self,
												defaultextension = ".png",
												filetypes = filetypes)
		if filename != "":
			self.saveImage(filename)


# Взято с https://github.com/python-pillow/Pillow/blob/master/PIL/ImageGrab.py
# PIL.ImageGrab.grab() -- добавлена поддержка Mac OS X 2 месяца назад.
def grab(bbox=None):
	if sys.platform == "darwin":
		f, file = tempfile.mkstemp('.png')
		os.close(f)
		subprocess.call(['screencapture', '-x', file])
		im = Image.open(file)
		im.load()
		os.unlink(file)
	else:
		size, data = grabber()
		im = Image.frombytes(
			"RGB", size, data,
			# RGB, 32-bit line padding, origo in lower left corner
			"raw", "BGR", (size[0]*3 + 3) & -4, -1
			)
	if bbox:
		im = im.crop(bbox)
	return im
