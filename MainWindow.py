#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *
import tkinter.filedialog, tkinter.messagebox

from Graph import Graph
from GraphOptionsWidget import GraphOptionsWidget
from AxisOptionsWidget import AxisOptionsWidget


class MainWindow(Tk):
	def __init__(self, application, **kwargs):
		Tk.__init__(self)
		
		# устанавливаем в Tkinter кодировку UTF-8
		self.tk.call('encoding', 'system', 'utf-8')
		
		self.application = application
		
		self.title("%s%sКонструкция" % (self.application.name, self.application.nameDelim))
		
		
		# График
		self.graph = Graph(self, width = 1000, height = 400,
						   offsetFunc = self.application.logic.offsetFunc,
						   onCursorMovement = self.application.logic.onCursorMovement,
						   onMouse1Clicked = self.application.logic.onMouse1Clicked,
						   **kwargs)
		self.graph.grid(column = 0, row = 0, rowspan = 11, sticky = N + E + S + W)
		
		# Делаем колонку с виджетом с графиком растяжимой
		self.columnconfigure(0, weight = 1)
		
		
		# Панель справа
		self.buttonOpenFile = Button(self, text = "Открыть файл",
									 command = self.onButtonOpenFileClicked)
		self.buttonOpenFile.grid(column = 1, row = 0, sticky = E + W)
		
		self.buttonOpenFile = Button(self, text = "Сохранить в файл",
									 command = self.onButtonSaveToFileClicked)
		self.buttonOpenFile.grid(column = 1, row = 1, sticky = E + W)
		
		self.buttonEdit = Button(self, text = "Редактировать",
								 command = self.application.createEditConstructionWindow)
		self.buttonEdit.grid(column = 1, row = 2, sticky = E + W)
		
		self.buttonCalculate = Button(self, text = "Рассчитать", state = DISABLED,
									  command = self.onButtonCalculateClicked)
		self.buttonCalculate.grid(column = 1, row = 3, sticky = E + W)
		
		# Пустое пространство (растяжимое)
		self.rowconfigure(4, weight = 1)
		
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
		self.graphOptions.grid(column = 1, row = 5, sticky = E + W)
		
		# Пустое пространство (растяжимое)
		self.rowconfigure(6, weight = 1)
		
		
		self.buttonComponents = Button(self, text = "Компоненты", state = DISABLED,
									   command = self.application.createComponentsDumpWindow)
		self.buttonComponents.grid(column = 1, row = 7, sticky = E + W)
		
		self.buttonMatrices = Button(self, text = "Матрицы", state = DISABLED,
									 command = self.application.createMatricesWindow)
		self.buttonMatrices.grid(column = 1, row = 8, sticky = E + W)
		
		self.buttonDetails = Button(self, text = "Детали", state = DISABLED,
									command = self.application.createDetailWindow)
		self.buttonDetails.grid(column = 1, row = 9, sticky = E + W)
		
		self.buttonAbout = Button(self, text = "О программе", command = self.onAboutButtonClicked)
		self.buttonAbout.grid(column = 1, row = 10, sticky = E + W)
		
		
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
		self.axisOptions.grid(column = 0, row = 11, sticky = E + W)
		
		
		self.bind("<Configure>", self.onWindowConfigure)
		
		
		self.update()
		self.onConstructionChanged()
	
	
	def onButtonOpenFileClicked(self):
		filename = tkinter.filedialog.askopenfilename(parent = self)
		
		if filename != "":
			try:
				file = open(filename, "r")
				
				# try:
				self.application.logic.openConstructionFile(file)
				# except Exception as e:
				# 	self.showError(str(e))
				
				file.close()
			except IOError as e:
				self.showError("Невозможно открыть файл: %s" % e)
	
	
	def onButtonSaveToFileClicked(self):
		filename = tkinter.filedialog.asksaveasfilename(parent = self,
														defaultextension = ".json",
														filetypes = [ ("JSON", ".json") ])
		
		if filename != "":
			try:
				file = open(filename, "w")
				self.application.logic.saveConstructionToFile(file)
				file.close()
			except IOError as e:
				self.showError("Невозможно открыть для записи файл: %s" % e)
			# except Exception as e:
			# 	print("Неизвестная ошибка: %s" % e)
	
	
	def onButtonCalculateClicked(self):
		# try:
		self.application.logic.calculate()
		# except Exception as e:
		# 	self.showError(str(e))
	
	
	def onAboutButtonClicked(self):
		tkinter.messagebox.showinfo(
			"%s%sО программе" % (self.application.name, self.application.nameDelim),
			self.application.about()
		)
	
	
	def onWindowConfigure(self, event):
		if type(event.widget) != Label:	# Игнорируем события от меток (когда меняется надпись)
			self.draw()
			# Кеширование размера окна не работает! Нужна принудительная перерисовка
	
	
	def onConstructionChanged(self):
		state1 = NORMAL if not self.application.logic.constructionEmpty()  else DISABLED
		state2 = NORMAL if self.application.logic.constructionCalculated() else DISABLED
		
		# Панель справа
		self.buttonCalculate["state"] = state1
		self.buttonDetails["state"]   = state1
		
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
		
		self.application.logic.draw(self.graph, **options)
	
	
	def showMessage(self, message):
		tkinter.messagebox.showinfo("Информация", message)
	
	
	def showError(self, message):
		tkinter.messagebox.showerror("Ошибка", message)
