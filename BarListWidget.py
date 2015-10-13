#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *

from ElementListWidget import *


class BarListWidget(ElementListWidget):
	def __init__(self, parent):
		columns = ("L", "A", "E", "[σ]", "q")
		
		ElementListWidget.__init__(self, parent, label = "Стержни:", columns = columns)
		
		# Настройки отображения таблицы
		for x in columns:
			self.tree.column( x, anchor = E, width = 80)
			self.tree.heading(x, anchor = E, text = x)
		
		
		# Параметры выбранного стержня
		self.L     = StringVar()
		self.A     = StringVar()
		self.E     = StringVar()
		self.Sigma = StringVar()
		self.q     = StringVar()
		
		
		Label(self.detailFrame, text = "L:").grid(column = 0, row = 0)
		Entry(self.detailFrame, textvariable = self.L).grid(column = 1, row = 0, sticky = W + E)
		
		Label(self.detailFrame, text = "A:").grid(column = 3, row = 0)
		Entry(self.detailFrame, textvariable = self.A).grid(column = 4, row = 0, sticky = W + E)
		
		Label(self.detailFrame, text = "E:").grid(column = 0, row = 1)
		Entry(self.detailFrame, textvariable = self.E).grid(column = 1, row = 1, sticky = W + E)
		
		Label(self.detailFrame, text = "[σ]:").grid(column = 3, row = 1)
		Entry(self.detailFrame, textvariable = self.Sigma).grid(column = 4, row = 1, sticky = W + E)
		
		Label(self.detailFrame, text = "q:").grid(column = 0, row = 2)
		Entry(self.detailFrame, textvariable = self.q).grid(column = 1, row = 2, sticky = W + E)
		
		
		self.detailFrame.columnconfigure(2, minsize = emptySpaceSize, weight = 0)
		self.detailFrame.columnconfigure(1, weight = 1)
		self.detailFrame.columnconfigure(4, weight = 1)
	
	
	def addBar(self, bar):
		self.addElement((bar.label, str(bar.i), str(bar.L), str(bar.A), str(bar.E), str(bar.Sigma),
						 str(bar.q)))
	
	
	def updateSelectedFrame(self, item = None, values = None):
		(item, values) = ElementListWidget.updateSelectedFrame(self, item, values)
		
		if item is None:
			for x in (self.L, self.A, self.E, self.Sigma, self.q):
				x.set("")
		else:
			self.L.set(values["L"])
			self.A.set(values["A"])
			self.E.set(values["E"])
			self.Sigma.set(values["[σ]"])
			self.q.set(values["q"])
