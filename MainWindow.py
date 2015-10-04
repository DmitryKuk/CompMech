#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *
import tkinter.filedialog, tkinter.messagebox

from Graph import Graph
from GraphOptionsWidget import GraphOptionsWidget


class MainWindow(Tk):
	def __init__(self, application, **kwargs):
		Tk.__init__(self)
		
		self.application = application
		
		self.title("%s%sКонструкция" % (self.application.name, self.application.nameDelim))
		
		self.graph = Graph(self, width = 1000, height = 400, **kwargs)
		self.graph.grid(column = 0, row = 0, rowspan = 8, sticky = N + E + S + W)
		
		# Делаем колонку с виджетом с графиком растяжимой
		self.columnconfigure(0, weight = 1)
		
		self.buttonOpenFile = Button(self, text = "Открыть файл",
									 command = self.onButtonOpenFileClicked)
		self.buttonOpenFile.grid(column = 1, row = 0, sticky = E + W)
		
		self.buttonCalculate = Button(self, text = "Рассчитать",
									  command = self.onCalculateButtonClicked, state = DISABLED)
		self.buttonCalculate.grid(column = 1, row = 1, sticky = E + W)
		
		# Пустое пространство (растяжимое)
		self.rowconfigure(2, weight = 1)
		
		# Настройки отображения содержимого
		self.graphOptions = GraphOptionsWidget(
			self,
			command = self.drawConstruction,
			optionsDesc = [
				("drawConstruction", "Конструкция", True,  DISABLED),
				("drawLoads",        "Нагрузки",    True,  DISABLED),
				("drawN",            "Эпюра Nx",    False, DISABLED),
				("drawU",            "Эпюра U",     False, DISABLED),
				("drawSigma",        "Эпюра σ",     False, DISABLED)
			]
		)
		self.graphOptions.grid(column = 1, row = 3, sticky = E + W)
		
		# Пустое пространство (растяжимое)
		self.rowconfigure(4, weight = 1)
		
		self.buttonDetails = Button(self, text = "Детали", command = self.onDetailButtonClicked)
		self.buttonDetails.grid(column = 1, row = 5, sticky = E + W)
		
		self.buttonAbout = Button(self, text = "О программе", command = self.onAboutButtonClicked)
		self.buttonAbout.grid(column = 1, row = 6, sticky = E + W)
		
		# Пустое пространство (нерастяжимое)
		self.rowconfigure(7, weight = 0, minsize = 20)
		
		self.bind("<Configure>", self.onWindowConfigure)
	
	
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
	
	
	def onDetailButtonClicked(self):
		print("Here!")
	
	
	def onAboutButtonClicked(self):
		tkinter.messagebox.showinfo(
			"%s%sО программе" % (self.application.name, self.application.nameDelim),
			self.application.about()
		)
	
	
	def onWindowConfigure(self, event):
		if type(event.widget) != Label:	# Игнорируем события от меток (когда меняется надпись)
			self.drawConstruction()
			# Кеширование размера окна не работает! Нужна принудительная перерисовка
	
	
	def onConstructionChanged(self):
		# Обновляем окна с деталями конструкции
		# for window in self.application.detailWindows:
		# 	window.onConstructionChanged()
		
		state1 = NORMAL if not self.application.logic.constructionEmpty() else DISABLED
		state2 = NORMAL if self.application.logic.calculated()            else DISABLED
		
		self.buttonCalculate["state"] = state1
		self.graphOptions.set(drawConstruction = (None, state1),
							  drawLoads        = (None, state1),
							  drawN            = (None, state2),
							  drawU            = (None, state2),
							  drawSigma        = (None, state2))
		
		self.drawConstruction()
	
	
	def drawConstruction(self):
		self.application.logic.drawConstruction(**self.graphOptions.get())
	
	
	def showMessage(self, message):
		tkinter.messagebox.showinfo("Информация", message)
	
	
	def showError(self, message):
		tkinter.messagebox.showerror("Ошибка", message)
