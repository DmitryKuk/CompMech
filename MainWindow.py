#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *
import tkinter.filedialog


class MainWindow:
	def __init__(self, application):
		self.root = Tk()
		
		self.canvas = Canvas(self.root,
							 width = 500, height = 200,
							 bg = "red",
							 cursor = "crosshair")
		self.canvas.grid(column = 0, row = 0, rowspan = 4, sticky=N+E+S+W)
		
		# Making left column (with canvas) stretchible
		self.root.columnconfigure(0, weight = 1)
		
		self.button1 = Button(self.root)
		self.button1["text"] = "Открыть файл"
		self.button1.bind("<Button-1>", self.onButtonOpenFileClicked)
		self.button1.grid(column = 1, row = 0)
		
		# Empty space (stretchible)
		self.root.rowconfigure(1, weight = 1)
		
		self.button2 = Button(self.root)
		self.button2["text"] = "Нажми меня 2"
		self.button2.bind("<Button-1>", self.onButtonClicked)
		self.button2.grid(column = 1, row = 2)
		
		self.button3 = Button(self.root)
		self.button3["text"] = "Нажми меня 3"
		self.button3.bind("<Button-1>", self.onButtonClicked)
		self.button3.grid(column = 1, row = 3)
	
	
	def onButtonClicked(self, event):
		print("Кнопка нажата!")
	
	
	def onButtonOpenFileClicked(self, event):
		f = tkinter.filedialog.askopenfile(mode = 'r', parent = self.root)
		
		if f == None:
			print("Файл не открыт")
		else:
			print("Открыт файл \"%s\"" % f.name)
