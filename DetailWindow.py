#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *
from tkinter.ttk import Notebook

from Graph import Graph


class DetailWindow(Toplevel):
	def __init__(self, application, barNumber = 0):
		Toplevel.__init__(self)
		
		self.application = application
		
		self.title("Стержни от Димыча — Детали")
		
		self.graph = Graph(self, width = 1000, height = 400, **kwargs)
		self.graph.grid(column = 0, row = 0, rowspan = 11, sticky = N + E + S + W)
		
		# Делаем колонку с виджетом с графиком растяжимой
		self.columnconfigure(0, weight = 1)
		
		self.buttonOpenFile = Button(self, text = "Test 1")
		self.buttonOpenFile.grid(column = 1, row = 0, sticky = E + W)
		
		self.buttonCalculate = Button(self, text = "Test 2")
		self.buttonCalculate.grid(column = 1, row = 1, sticky = E + W)
		
		
		self.rowconfigure(2, weight = 1)	# Пустое пространство (растяжимое)
		
		
		# Настройки отображения содержимого
		self.displayElements = IntVar()
		self.displayElements.set(1)
		self.displayElementsCB = Checkbutton(self, text = "Конструкция", command = self.onCBClicked,
											 variable = self.displayElements, state = DISABLED)
		self.displayElementsCB.grid(column = 1, row = 3, sticky = E + W)
		
		
		self.displayLoads = IntVar()
		self.displayLoads.set(1)
		self.displayLoadsCB = Checkbutton(self, text = "Нагрузки", command = self.onCBClicked,
										  variable = self.displayLoads, state = DISABLED)
		self.displayLoadsCB.grid(column = 1, row = 4, sticky = E + W)
		
		
		self.displayN = IntVar()
		self.displayNCB = Checkbutton(self, text = "Эпюра Nx", command = self.onCBClicked,
									  variable = self.displayN, state = DISABLED)
		self.displayNCB.grid(column = 1, row = 6, sticky = E + W)
		
		
		self.displayU = IntVar()
		self.displayUCB = Checkbutton(self, text = "Эпюра U", command = self.onCBClicked,
									  variable = self.displayU, state = DISABLED)
		self.displayUCB.grid(column = 1, row = 7, sticky = E + W)
		
		
		self.displaySigma = IntVar()
		self.displaySigmaCB = Checkbutton(self, text = "Эпюра σ", command = self.onCBClicked,
										  variable = self.displaySigma, state = DISABLED)
		self.displaySigmaCB.grid(column = 1, row = 8, sticky = E + W)
		
		
		self.rowconfigure(9, weight = 1)	# Пустое пространство (растяжимое)
		
		
		self.button3 = Button(self, text = "Нажми меня", command = self.onButtonClicked, state = DISABLED)
		self.button3.grid(column = 1, row = 10, sticky = E + W)
		
		self.bind("<Configure>", self.onWindowConfigure)
	
	
	def onButtonClicked(self):
		self.showMessage("Кнопка нажата!")
	
	
	def onWindowConfigure(self, event):
		if type(event.widget) != Label:	# Игнорируем события от меток (когда меняется надпись)
			# self.drawConstructionDetail()
			print("drawConstructionDetail()")
			# Кеширование размера окна не работает! Нужна принудительная перерисовка
	
	
	def onCBClicked(self):
		# self.drawConstructionDetail()
		print("onCBClicked()")
	
	
	def onConstructionChanged(self):
		self.drawConstruction()
	
	
	def drawConstruction(self):
		self.application.logic.drawConstruction(
			drawElements = True if self.displayElements.get() == 1 else False,
			drawLoads	 = True if self.displayLoads.get()	  == 1 else False,
			drawN		 = True if self.displayN.get()		  == 1 else False,
			drawu		 = True if self.displayU.get()		  == 1 else False,
			drawSigma	 = True if self.displaySigma.get()	  == 1 else False
		)
	
	
	def showMessage(self, message):
		tkinter.messagebox.showinfo("Информация", message)
	
	
	def showError(self, message):
		tkinter.messagebox.showerror("Ошибка", message)
