#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *

from ElementListWidget import ElementListWidget


class BarListWidget(ElementListWidget):
	def __init__(self, parent):
		columns = ("Метка", "№", "L", "A", "E", "[σ]", "q")
		
		ElementListWidget.__init__(self, parent, label = "Стержни:", columns = columns)
		
		# Настройки отображения таблицы
		self.tree.column( columns[0], anchor = W, width = 150)
		self.tree.heading(columns[0], anchor = W, text = columns[0])
		
		for x in columns[1:]:
			self.tree.column( x, anchor = E, width = 80)
			self.tree.heading(x, anchor = E, text = x)
	
	
	def addBar(self, bar):
		self.addElement((bar.label, str(bar.i), str(bar.L), str(bar.A), str(bar.E), str(bar.Sigma),
						 str(bar.q)))
