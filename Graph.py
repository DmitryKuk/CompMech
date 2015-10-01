#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *
from PIL import Image
import os, subprocess, tempfile

import GraphScale
from GraphScale import GraphScale, zeroOffsetFunc


class Graph(Frame):
	def __init__(self, mainWindow,
				 watchForElement = True,
				 offsetFunc = zeroOffsetFunc,
				 **kwargs):
		# Frame
		kwargs["borderwidth"] = 1
		kwargs["relief"] = "ridge"
		Frame.__init__(self, mainWindow, **kwargs)
		
		self.mainWindow = mainWindow
		
		
		# Обновлять информацию об элементе под курсором
		self.watchForElement = watchForElement
		
		
		# Калькуляторы масштаба (для вычисления координат)
		self.mainScale = GraphScale(offsetFunc)
		self.NSigmaScale = GraphScale(offsetFunc)
		self.uScale = GraphScale(offsetFunc)
		
		
		# Максимальные нагрузки
		self.maxF = 0		# Максимальные нагрузки (в физических единицах; для масштаба)
		self.maxqOnL = 0	# Максимальная относительная распределённая нагрузка = q / L
		self.specq = 0		# q, при котором q / L -> max
		self.maxFReal = 0	# Максимальная длина стрелки силы в пикселях
							# (чтобы оставалась в пределах графика)
		
		
		self.maxNSigma, self.maxu = 0, 0
		
		self.sizeStr = StringVar()
		self.elementStr = StringVar()
		self.cursorStr = StringVar()
		
		
		# Линии осей (идентификаторы холста)
		self.coordinateAxis = (None, None)
		self.axisArgs = { "fill": "blue", "arrow": LAST, "dash": (5, 5),
						  "state": DISABLED, "tags": "coordinateAxis" }
		
		
		# Холст
		canvasArgs = { "cursor": "crosshair", "bg": "#FFFFFF" }
		if "width" in kwargs:	canvasArgs["width"] = kwargs["width"]
		if "height" in kwargs:	canvasArgs["height"] = kwargs["height"]
		
		self.canvas = Canvas(self, **canvasArgs)
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
		
		
		# Контекстное меню
		self.menu = Menu(self, tearoff = 0)
		self.menu.add_command(label = "Сохранить изображение",
							  command = self.onMenuEntrySaveImageClicked)
		
		self.canvas.bind("<ButtonRelease-2>",
						 lambda event: self.menu.post(event.x_root, event.y_root))
	
	
	def onMouseMotion(self, event):
		self.updateCursorPos(event.x, event.y)
	
	
	def onMouseLeave(self, event):
		self.updateCursorPos()
	
	
	def onWindowConfigure(self, event):
		size = (self.canvas.winfo_width(), self.canvas.winfo_height())
		for scale in self.mainScale, self.NSigmaScale, self.uScale:
			scale.setRealSize(size)
		self.updateOffset()
		self.updateLabels()
	
	
	def updateLabels(self, cursorX = None, cursorY = None):
		self.sizeStr.set("Размер: (%.3f, %.3f)" % self.mainScale.virtSize())
		self.updateCursorPos(cursorX, cursorY)
	
	
	def updateCursorPos(self, cursorX = None, cursorY = None):
		needDescStr = True
		
		if cursorX is None:
			cursorX = self.mainScale.virtToRealX(0)
			needDescStr = False
		
		if cursorY is None:
			cursorY = self.mainScale.virtToRealY(0)
			needDescStr = False
		
		self.cursorStr.set("(%.3f, %.3f)" % self.mainScale.realToVirtCoord((cursorX, cursorY)))
		
		if self.watchForElement:
			try:
				ID = None
				
				timesToRepeat = 3	# Чтобы избежать зацикливания
				while timesToRepeat > 0:
					timesToRepeat -= 1
					
					# Пытаемся получить информацию о ближайшем элементе...
					ID = self.canvas.find_closest(cursorX, cursorY, halo = 10, start = ID)[0]
					
					# ...не координатной оси Ox (Oy соответсвует левому узлу)
					if ID != self.coordinateAxis[0]: break
				
				elementDescStr = self.mainWindow.application.logic.elementDescStr(ID)
			except KeyError:
				needDescStr = False
			except IndexError:
				needDescStr = False
			
			if needDescStr: self.setElementStr(elementDescStr)
			else: self.setElementStr("")
		
		# Тест преобразований координат
		# vC = self.realToVirtCoord((cursorX, cursorY))
		# rC = self.mainScale.virtToRealCoord(vC)
		
		# if rC[0] != cursorX or rC[1] != cursorY:
		# 	print("Точки не совпадают:\n(%f, %f)\n(%f, %f)\n" % (cursorX, cursorY, rC[0], rC[1]))
	
	
	def setVirtSize(self, size):
		self.mainScale.setVirtSize(size)
		for scale in self.NSigmaScale, self.uScale:
			scale.setVirtSize((size[0], scale.vH))
		
		self.updateOffset()
		self.updateLabels()
	
	
	def setMaxLoads(self, F, specq, maxqOnL):
		self.maxF, self.specq, self.maxqOnL = abs(F), abs(specq), abs(maxqOnL)
		self.updateOffset()
	
	
	def setMaxComponents(self, maxN, maxu, maxSigma):
		self.maxNSigma, self.maxu = max(abs(maxN), abs(maxSigma)), maxu
		vW = self.mainScale.vW
		
		self.NSigmaScale.setVirtSize((vW, self.maxNSigma * 2.0 / 0.7))
		self.uScale.setVirtSize((vW, self.maxu * 2.0 / 0.25))
		
		self.updateOffset()
	
	
	def setTitle(self, text):
		return self.canvas.create_text(self.mainScale.rW / 2, 10, text = text)
	
	
	def setElementStr(self, text):
		self.elementStr.set(text)
	
	
	def updateOffset(self):
		for scale in self.mainScale, self.NSigmaScale, self.uScale:
			scale.update()
		
		# Обновляем максимальные нагрузки
		oF = self.mainScale.realOffset()
		self.maxFReal = min(oF[0], oF[2])	# W, E
	
	
	def drawBar(self, bar, drawBar = True, drawLoads = True):
		barArgs = { "fill": "yellow", "activefill": "orange", "tags": "bar" }
		qLineArgs = { "fill": "green", "width": 5, "arrow": FIRST, "arrowshape": (5, 12, 13),
					  "tags": "barLoad" }
		
		
		leftTop     = self.mainScale.virtToRealCoord((        bar.x,  0.5 * bar.height))
		rightBottom = self.mainScale.virtToRealCoord((bar.x + bar.L, -0.5 * bar.height))
		
		
		retList = []	# Список идентификаторов нарисованных объектов
		
		
		if drawBar:
			retList.append(self.canvas.create_rectangle(leftTop[0],     leftTop[1],
														rightBottom[0], rightBottom[1],
														**barArgs))
		
		
		if drawLoads and bar.q != 0 and self.maxqOnL != 0 and self.specq != 0:
			qSpace = 5 * self.mainScale.kX		# Пробелы 5 пикселей между стрелками
			qIndent = 12 * self.mainScale.kX	# Отступы в 10 пикселей по границам стержней
			
			qLen = (bar.q ** 2) / (self.maxqOnL * self.specq)	# Длина стрелки q
			
			if bar.q > 0:
				x1, xmin = bar.x + bar.L, bar.x + qIndent
				while x1 > xmin:
					x2 = max(x1 - qLen, xmin)
					retList.append(self.drawLine((x1, 0), (x2, 0), **qLineArgs))
					x1 -= qLen + qSpace
			elif bar.q < 0:
				x1, xmax = bar.x, bar.x + bar.L - qIndent
				while x1 < xmax:
					x2 = min(x1 + qLen, xmax)
					retList.append(self.drawLine((x1, 0), (x2, 0), **qLineArgs))
					x1 += qLen + qSpace
		
		
		return retList
	
	
	def drawBarCurves(self, bar, drawN = False, drawu = False, drawSigma = False):
		NLineArgs = { "fill": "red" }
		uLineArgs = { "fill": "green" }
		SigmaLineArgs = { "fill": "blue" }
		SigmaMaxLineArgs = { "fill": "blue", "dash": (10, 10) }
		
		
		retList = []	# Список идентификаторов нарисованных объектов
		
		
		# Рисуем эпюры N(x), u(x), Sigma(x)
		if drawN:
			retList.append(self.drawCurve(self.NSigmaScale, bar.NLineGlobal(), **NLineArgs))
		
		
		if drawu:
			retList.append(self.drawCurve(self.uScale, bar.uLineGlobal(), **uLineArgs))
		
		
		if drawSigma:
			# SigmaMax, -SigmaMax
			line = bar.SigmaMaxLineGlobal()
			retList.append(self.drawCurve(self.NSigmaScale, line, **SigmaMaxLineArgs))
			
			line = [(line[0][0], -line[0][1]), (line[1][0], -line[1][1])]
			retList.append(self.drawCurve(self.NSigmaScale, line, **SigmaMaxLineArgs))
			
			# Sigma(x)
			retList.append(self.drawCurve(self.NSigmaScale, bar.SigmaLineGlobal(), **SigmaLineArgs))
		
		
		return retList
	
	
	def drawNode(self, node, drawNode = True, drawLoads = True):
		VaxisArgs = { "fill": "green", "dash": (3, 3), "tags": "node" }
		FlineArgs = { "fill": "red", "width": 11, "arrow": LAST, "arrowshape": (5, 12, 13),
					  "tags": "nodeLoad" }
		hatchArgs = { "tags": "nodeHatch" }
		
		
		retList = []
		
		
		# Отображаем узел в виде вертикальной оси
		if node.x == 0:
			retList.append(self.coordinateAxis[1])	# Используем ось Oy, если узел самый левый
		else:
			retList.append(self.drawVAxis(node.x, **VaxisArgs))	# Или рисуем новую
		
		
		# Отображаем штриховку, если узел фиксирован
		if drawNode and node.fixed:
			hatch = (10, 10)	# Размеры штриха (в пикселях)
			hatchNum = 4		# Количество штрихов в каждую сторону от горизонтальной оси
			
			# vHatch = self.mainScale.realToVirtVector(hatch)
			
			(rX, rY) = self.mainScale.virtToRealCoord((node.x, 0))
			
			# Вычисляем координаты штрихов...
			if node.x == 0:		# Узел самый левый -- штриховка слева
				# p1 = (node.x - vHatch[0], -vHatch[1] * hatchNum)
				# p2 = (node.x, -vHatch[1] * (hatchNum - 1))
				p1 = (rX - hatch[0], rY - hatch[1] * (hatchNum - 1))
				p2 = (rX, rY - hatch[1] * hatchNum)
			else:				# Штриховка справа
				# p1 = (node.x, -vHatch[1] * hatchNum)
				# p2 = (node.x + vHatch[0], -vHatch[1] * (hatchNum - 1))
				p1 = (rX, rY - hatch[1] * (hatchNum - 1))
				p2 = (rX + hatch[0], rY - hatch[1] * hatchNum)
			
			# ...и рисуем их
			for i in range(2 * hatchNum):
				# retList.append(self.drawLine(p1, p2, **hatchArgs))
				retList.append(self.drawLineReal(p1, p2, **hatchArgs))
				
				p1 = (p1[0], p1[1] + hatch[1])
				p2 = (p2[0], p2[1] + hatch[1])
		
		
		if drawLoads:
			# Отображаем нагрузку
			if node.F != 0:
				p0 = (node.x - float(node.F * self.maxFReal * self.mainScale.vW)
							   / (self.maxF * self.mainScale.rW), 0)
				p1 = (node.x, 0)
				
				retList.append(self.drawLine(p0, p1, **FlineArgs))
		
		return retList
	
	
	def drawLineReal(self, p0, p1, **kwargs):
		return self.canvas.create_line(p0[0], p0[1], p1[0], p1[1], **kwargs)
	
	
	def drawLine(self, point0, point1, **kwargs):
		p0, p1 = self.mainScale.virtToRealCoord(point0), self.mainScale.virtToRealCoord(point1)
		return self.drawLineReal(p0, p1, **kwargs)
	
	
	def drawCurve(self, scale, line, **kwargs):
		p0, p1 = scale.virtToRealCoord(line[0]), scale.virtToRealCoord(line[1])
		return self.drawLineReal(p0, p1, **kwargs)
	
	
	def drawHAxis(self, vY = 0, **kwargs):
		rW = self.mainScale.rW
		rY = self.mainScale.virtToRealY(vY)
		
		return self.drawLineReal((0, rY), (rW - 5, rY), **kwargs)
	
	
	def drawVAxis(self, vX = 0, **kwargs):
		rH = self.mainScale.rH
		rX = self.mainScale.virtToRealX(vX)
		
		return self.drawLineReal((rX, rH), (rX, 5), **kwargs)
	
	
	def drawAxis(self, center = (0, 0), **kwargs):
		axisX = self.drawHAxis(center[1], **kwargs)
		axisY = self.drawVAxis(center[0], **kwargs)
		return (axisX, axisY)
	
	
	def drawCoordinateAxisX(self):
		(vW, vH) = self.mainScale.virtSize()
		if vW != 0 and vH != 0:
			self.coordinateAxis = (self.drawHAxis(0, **self.axisArgs), self.coordinateAxis[1])
		return self.coordinateAxis[0]
	
	
	def drawCoordinateAxisY(self):
		(vW, vH) = self.mainScale.virtSize()
		if vW != 0 and vH != 0:
			self.coordinateAxis = (self.coordinateAxis[0], self.drawVAxis(0, **self.axisArgs))
		return self.coordinateAxis[1]
	
	
	def drawCoordinateAxis(self):
		self.drawCoordinateAxisX()
		self.drawCoordinateAxisY()
		return self.coordinateAxis
	
	
	def clear(self):
		self.canvas.delete(*self.canvas.find_all())
		self.coordinateAxis = (None, None)
	
	
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
