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
		
		self.panedWindow = PanedWindow(self, orient = VERTICAL, sashwidth = 5, sashrelief = "sunken")
		self.panedWindow.pack(fill = BOTH, expand = 1)
		
		self.mainWidget = Frame(self.panedWindow)
		self.panedWindow.add(self.mainWidget, sticky = W + N+ E + S)
		
		# Делаем колонку с виджетом с графиком растяжимой
		self.mainWidget.columnconfigure(0, weight = 1)
		# Пустое пространство (растяжимое)
		self.mainWidget.rowconfigure(1, weight = 1)
		# Пустое пространство (растяжимое)
		self.mainWidget.rowconfigure(3, weight = 1)
		
		
		self.graph = Graph(self.mainWidget, width = 1000, height = 400,
						   offsetFunc = self.application.logic.offsetFunc,
						   onCursorMovement = self.application.logic.onCursorMovement,
						   **kwargs)
		self.graph.grid(column = 0, row = 0, rowspan = 4, sticky = N + E + S + W)
		
		
		self.buttonPrev = Button(self.mainWidget, text = "←", command = self.onButtonPrevClicked)
		self.buttonPrev.grid(column = 1, row = 0, sticky = E + W)
		
		self.buttonNext = Button(self.mainWidget, text = "→", command = self.onButtonNextClicked)
		self.buttonNext.grid(column = 2, row = 0, sticky = E + W)
		
		
		# Настройки отображения содержимого
		self.graphOptions = GraphOptionsWidget(
			self.mainWidget,
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
		
		
		self.infoWidget = Notebook(self.panedWindow)
		self.panedWindow.add(self.infoWidget, sticky = W + N+ E + S)
		
		self.barInfoVar = StringVar()
		self.updateBarInfo()
		self.barInfoTab = Label(self.infoWidget, textvariable = self.barInfoVar)
		self.infoWidget.add(self.barInfoTab, text = "Стержень", sticky = W + N + E + S)
		
		
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
	
	
	def updateBarInfo(self):
		self.barInfoVar.set(self.application.logic.barInfo(self.barNumber))
	
	
	def draw(self):
		self.update()
		self.application.logic.draw(self.graph, barNumber = self.barNumber,
									**self.graphOptions.get())
	
	
	def showMessage(self, message):
		tkinter.messagebox.showinfo("Информация", message)
	
	
	def showError(self, message):
		tkinter.messagebox.showerror("Ошибка", message)
