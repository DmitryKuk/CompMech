#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *
from tkinter.ttk import Notebook

from Graph import Graph
from GraphOptionsWidget import GraphOptionsWidget


class DetailWindow(Toplevel):
	def __init__(self, application, barNumber = 0, **kwargs):
		Toplevel.__init__(self)
		
		self.application = application
		
		self.barNumber = barNumber
		
		self.title("%s%sДетали" % (self.application.name, self.application.nameDelim))
		
		self.graph = Graph(self, width = 1000, height = 400,
						   offsetFunc = self.application.logic.offsetFunc,
						   onCursorMovement = self.application.logic.onCursorMovement,
						   **kwargs)
		self.graph.grid(column = 0, row = 0, rowspan = 4, sticky = N + E + S + W)
		
		# Делаем колонку с виджетом с графиком растяжимой
		self.columnconfigure(0, weight = 1)
		
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
		
		self.bind("<Configure>", self.onWindowConfigure)
		self.bind("<Destroy>", self.onWindowDestroy)
		
		self.onConstructionChanged()
	
	
	def onButtonPrevClicked(self):
		barsCount = self.application.logic.barsCount()
		if barsCount > 0: self.barNumber = (self.barNumber - 1) % barsCount
		self.draw()
	
	
	def onButtonNextClicked(self):
		barsCount = self.application.logic.barsCount()
		if barsCount > 0: self.barNumber = (self.barNumber + 1) % barsCount
		self.draw()
	
	
	def onWindowConfigure(self, event):
		if type(event.widget) != Label:	# Игнорируем события от меток (когда меняется надпись)
			self.draw()
			# Кеширование размера окна не работает! Нужна принудительная перерисовка
	
	
	def onWindowDestroy(self, event):
		self.application.onDetailWindowDestroy(self)
	
	
	def onConstructionChanged(self):
		if self.barNumber not in range(0, self.application.logic.barsCount()):
			self.barNumber = 0
		
		state1 = NORMAL if not self.application.logic.constructionEmpty()  else DISABLED
		state2 = NORMAL if self.application.logic.constructionCalculated() else DISABLED
		
		self.graphOptions.set(drawConstruction = (None, state1),
							  drawLoads        = (None, state1),
							  drawN            = (None, state2),
							  drawU            = (None, state2),
							  drawSigma        = (None, state2))
		
		self.draw()
	
	
	def draw(self):
		self.update()
		self.application.logic.draw(self.graph, barNumber = self.barNumber,
									**self.graphOptions.get())
