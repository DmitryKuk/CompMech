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
		self.graph.grid(column = 0, row = 0, rowspan = 4, sticky = N + E + S + W)
		
		# Делаем колонку с виджетом с графиком растяжимой
		self.columnconfigure(0, weight = 1)
		
		self.button1 = Button(self, text = "Открыть файл", command = self.onButtonOpenFileClicked)
		self.button1.grid(column = 1, row = 0, sticky = E + W)
		
		self.button2 = Button(self, text = "Рассчитать", command = self.onCalculateButtonClicked)
		self.button2.grid(column = 1, row = 1, sticky = E + W)
		
		# Пустое пространство (растяжимое)
		self.rowconfigure(2, weight = 1)
		
		self.button3 = Button(self, text = "Нажми меня", command = self.onButtonClicked, state = DISABLED)
		self.button3.grid(column = 1, row = 3, sticky = E + W)
		
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
	
	
	def onConstructionChanged(self):
		self.button3["state"] = NORMAL if self.application.logic.calculated() else DISABLED
		self.drawConstruction()
	
	
	def drawConstruction(self):
		drawCurve = self.application.logic.calculated()
		self.application.logic.drawConstruction(drawCurve, drawCurve, drawCurve)
	
	
	def showMessage(self, message):
		tkinter.messagebox.showinfo("Информация", message)
	
	
	def showError(self, message):
		tkinter.messagebox.showerror("Ошибка", message)
