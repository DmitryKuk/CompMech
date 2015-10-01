#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *
import tkinter.filedialog, tkinter.messagebox

from Graph import Graph


class MainWindow(Tk):
	def __init__(self, application, **kwargs):
		Tk.__init__(self)
		
		self.application = application
		
		self.title("Стержни от Димыча")
		
		self.graph = Graph(self, width = 1000, height = 400, **kwargs)
		self.graph.grid(column = 0, row = 0, rowspan = 11, sticky = N + E + S + W)
		
		# Делаем колонку с виджетом с графиком растяжимой
		self.columnconfigure(0, weight = 1)
		
		self.buttonOpenFile = Button(self, text = "Открыть файл",
									 command = self.onButtonOpenFileClicked)
		self.buttonOpenFile.grid(column = 1, row = 0, sticky = E + W)
		
		self.buttonCalculate = Button(self, text = "Рассчитать",
									  command = self.onCalculateButtonClicked, state = DISABLED)
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
		
		
		self.displayu = IntVar()
		self.displayuCB = Checkbutton(self, text = "Эпюра u", command = self.onCBClicked,
									  variable = self.displayu, state = DISABLED)
		self.displayuCB.grid(column = 1, row = 7, sticky = E + W)
		
		
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
	
	
	def onButtonOpenFileClicked(self):
		filename = tkinter.filedialog.askopenfilename(parent = self)
		
		if filename != "":
			try:
				file = open(filename, "r")
				self.application.logic.processConstructionFile(file,
															   showMessage = self.showMessage,
															   showError = self.showError)
				file.close()
			except IOError as e:
				self.showError("Невозможно открыть файл: %s" % e)
			# except Exception as e:
			# 	print("Неизвестная ошибка: %s" % e)
	
	
	def onCalculateButtonClicked(self):
		self.application.logic.calculate()
	
	
	def onWindowConfigure(self, event):
		if type(event.widget) != Label:	# Игнорируем события от меток (когда меняется надпись)
			self.drawConstruction()
			# Кеширование размера окна не работает! Нужна принудительная перерисовка
	
	
	def onCBClicked(self):
		self.drawConstruction()
	
	
	def onConstructionChanged(self):
		if self.application.logic.constructionEmpty():
			self.buttonCalculate["state"] = DISABLED
			
			for cb in self.displayElementsCB, self.displayLoadsCB:
				cb["state"] = DISABLED
		else:
			self.buttonCalculate["state"] = NORMAL
			
			for cb in self.displayElementsCB, self.displayLoadsCB:
				cb["state"] = NORMAL
		
		
		if self.application.logic.calculated():
			for cb in self.displayNCB, self.displayuCB, self.displaySigmaCB:
				cb["state"] = NORMAL
			
			self.button3["state"] = NORMAL
		else:
			for cb in self.displayNCB, self.displayuCB, self.displaySigmaCB:
				cb["state"] = DISABLED
			
			self.button3["state"] = DISABLED
		
		
		self.drawConstruction()
	
	
	def drawConstruction(self):
		self.application.logic.drawConstruction(
			drawElements = True if self.displayElements.get() == 1 else False,
			drawLoads	 = True if self.displayLoads.get()	  == 1 else False,
			drawN		 = True if self.displayN.get()		  == 1 else False,
			drawu		 = True if self.displayu.get()		  == 1 else False,
			drawSigma	 = True if self.displaySigma.get()	  == 1 else False
		)
	
	
	def showMessage(self, message):
		tkinter.messagebox.showinfo("Информация", message)
	
	
	def showError(self, message):
		tkinter.messagebox.showerror("Ошибка", message)
