#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *


class MainWindow:
	def __init__(self, application):
		self.canvas = Canvas(application.root,
							 width = 500, height = 200,
							 bg = "red",
							 cursor = "crosshair")
		self.canvas.pack()
		
		self.button = Button(application.root)
		self.button["text"] = "Нажми меня"
		self.button.bind("<Button-1>", self.onButtonClicked)
		self.button.pack()
	
	
	def onButtonClicked(self, event):
		print("Кнопка нажата!")
