#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *
import tkinter.filedialog

from Graph import Graph


class MainWindow(Tk):
	def __init__(self, application, **kwargs):
		Tk.__init__(self)
		
		self.application = application
		
		self.title("Компьютерная механика")
		
		self.graph = Graph(self, width = 700, height = 300, **kwargs)
		self.graph.grid(column = 0, row = 0, rowspan = 4, sticky = N + E + S + W)
		
		# Делаем колонку с виджетом с графиком растяжимой
		self.columnconfigure(0, weight = 1)
		
		self.button1 = Button(self)
		self.button1["text"] = "Открыть файл"
		self.button1.bind("<ButtonRelease-1>", self.onButtonOpenFileClicked)
		self.button1.grid(column = 1, row = 0)
		
		# Пустое пространство (растяжимое)
		self.rowconfigure(1, weight = 1)
		
		self.button2 = Button(self)
		self.button2["text"] = "Нажми меня 2"
		self.button2.bind("<ButtonRelease-1>", self.onButtonClicked)
		self.button2.grid(column = 1, row = 2)
		
		self.button3 = Button(self)
		self.button3["text"] = "Нажми меня 3"
		self.button3.bind("<ButtonRelease-1>", self.onButtonClicked)
		self.button3.grid(column = 1, row = 3)
		
		self.bind("<Configure>", self.onWindowConfigure)
	
	
	def onButtonClicked(self, event):
		print("Кнопка нажата!")
	
	
	def onButtonOpenFileClicked(self, event):
		filename = tkinter.filedialog.askopenfilename(parent = self)
		
		if filename != "":
			try:
				file = open(filename, "r")
				self.application.logic.processConstructionFile(file)
				file.close()
			except IOError as e:
				print("Невозможно открыть файл: %s" % e)
			# except Exception as e:
			# 	print("Неизвестная ошибка: %s" % e)
	
	
	def onWindowConfigure(self, event):
		if type(event.widget) != Label:	# Игнорируем события от меток (когда меняется надпись)
			self.application.logic.drawConstruction()
			# Кеширование размера окна не работает! Нужна принудительная перерисовка
