#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *
from tkinter.ttk import Notebook

from Graph import Graph
from GraphOptionsWidget import GraphOptionsWidget
from AxisOptionsWidget import AxisOptionsWidget


class DetailWindow(Toplevel):
	def __init__(self, application, barNumber = 0, **kwargs):
		Toplevel.__init__(self)
		
		self.application = application
		self.barNumber = barNumber
		
		self.title("%s%sДетали" % (self.application.name, self.application.nameDelim))
		
		
		# График
		self.graph = Graph(self, width = 1000, height = 400,
						   offsetFunc = self.application.logic.offsetFunc,
						   onCursorMovement = self.application.logic.onCursorMovement,
						   **kwargs)
		self.graph.grid(column = 0, row = 0, rowspan = 7, sticky = N + E + S + W)
		
		# Делаем колонку с виджетом с графиком растяжимой
		self.columnconfigure(0, weight = 1)
		
		
		# Панель справа
		self.buttonPrev = Button(self, text = "←", command = self.onButtonPrevClicked)
		self.buttonPrev.grid(column = 1, row = 0, sticky = E + W)
		
		self.buttonNext = Button(self, text = "→", command = self.onButtonNextClicked)
		self.buttonNext.grid(column = 2, row = 0, sticky = E + W)
		
		# Пустое пространство (растяжимое)
		self.rowconfigure(1, weight = 1)
		
		# Настройки отображения содержимого
		self.graphOptions = GraphOptionsWidget(
			self,
			command = self.draw,
			optionsDesc = [
				("drawConstruction", "Конструкция", True,  DISABLED),
				("drawLoads",        "Нагрузки",    True,  DISABLED),
				("drawN",            "График Nx",   False, DISABLED),
				("drawU",            "График U",    False, DISABLED),
				("drawSigma",        "График σ",    False, DISABLED)
			]
		)
		self.graphOptions.grid(column = 1, row = 2, columnspan = 2, sticky = E + W)
		
		# Пустое пространство (растяжимое)
		self.rowconfigure(3, weight = 1)
		
		# Панель под графиком
		self.axisOptions = AxisOptionsWidget(
			self,
			label = "Деления:",
			command = self.draw,
			optionsDesc = [
				("divsX",     "Ось X:",  0, NORMAL),
				("divsN",     "Ось Nx:", 0, DISABLED),
				("divsU",     "Ось U:",  0, DISABLED),
				("divsSigma", "Ось σ:",  0, DISABLED),
			]
		)
		self.axisOptions.grid(column = 0, row = 7, sticky = E + W)
		
		
		self.buttonComponents = Button(self, text = "Компоненты",
									   command = self.onComponentsButtonClicked, state = DISABLED)
		self.buttonComponents.grid(column = 1, row = 5, columnspan = 2, sticky = E + W)
		
		self.buttonMatrices = Button(self, text = "Матрицы", command = self.onMatricesButtonClicked,
									 state = DISABLED)
		self.buttonMatrices.grid(column = 1, row = 6, columnspan = 2, sticky = E + W)
		
		
		self.bind("<Configure>", self.onWindowConfigure)
		self.bind("<Destroy>", self.onWindowDestroy)
		
		
		self.update()
		self.onConstructionChanged()
	
	
	def onButtonPrevClicked(self):
		barsCount = self.application.logic.barsCount()
		if barsCount > 0: self.barNumber = (self.barNumber - 1) % barsCount
		self.draw()
	
	
	def onButtonNextClicked(self):
		barsCount = self.application.logic.barsCount()
		if barsCount > 0: self.barNumber = (self.barNumber + 1) % barsCount
		self.draw()
	
	
	def onMatricesButtonClicked(self):
		self.application.createMatricesWindow(self.barNumber)
	
	
	def onComponentsButtonClicked(self):
		self.application.createComponentsDumpWindow(self.barNumber)
	
	
	def onWindowConfigure(self, event):
		if type(event.widget) != Label:	# Игнорируем события от меток (когда меняется надпись)
			self.draw()
			# Кеширование размера окна не работает! Нужна принудительная перерисовка
	
	
	def onWindowDestroy(self, event):
		self.application.onWindowDestroy(self)
	
	
	def onConstructionChanged(self):
		if self.barNumber not in range(0, self.application.logic.barsCount()):
			self.barNumber = 0
		
		state1 = NORMAL if not self.application.logic.constructionEmpty()  else DISABLED
		state2 = NORMAL if self.application.logic.constructionCalculated() else DISABLED
		
		# Панель справа
		self.graphOptions.set(drawConstruction = (None, state1),
							  drawLoads        = (None, state1),
							  drawN            = (None, state2),
							  drawU            = (None, state2),
							  drawSigma        = (None, state2))
		
		self.buttonComponents["state"] = state2
		self.buttonMatrices["state"]   = state2
		
		# Панель под графиком
		self.axisOptions.set(divsX     = (None, NORMAL),
							 divsN     = (None, state2),
							 divsU     = (None, state2),
							 divsSigma = (None, state2))
		
		self.draw()
	
	
	def draw(self):
		options = self.graphOptions.get()
		options.update(self.axisOptions.get())
		
		self.application.logic.draw(self.graph, barNumber = self.barNumber, **options)
