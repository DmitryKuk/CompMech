#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *

from ElementListWidget import ElementListWidget


class BarListWidget(ElementListWidget):
	def __init__(self, parent):
		columns = ("L", "A", "E", "[σ]", "q")
		
		ElementListWidget.__init__(self, parent, label = "Стержни:", columns = columns)
		
		# Настройки отображения таблицы
		for x in columns:
			self.tree.column( x, anchor = E, width = 80)
			self.tree.heading(x, anchor = E, text = x)
	
	
	def addBar(self, bar):
		self.addElement((bar.label, str(bar.i), str(bar.L), str(bar.A), str(bar.E), str(bar.Sigma),
						 str(bar.q)))
