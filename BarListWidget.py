#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *

from Style import defaultValueBG
from ElementListWidget import *


class BarListWidget(ElementListWidget):
	def __init__(self, parent):
		columns = ("L", "A", "E", "[σ]", "q")
		
		ElementListWidget.__init__(self, parent, label = "Стержни", columns = columns)
		
		# Настройки отображения таблицы
		for x in columns:
			self.tree.column( x, anchor = E, width = 80)
			self.tree.heading(x, anchor = E, text = x)
		
		
		# Параметры выбранного стержня
		self.L     = (StringVar(), StringVar())
		self.A     = (StringVar(), StringVar())
		self.E     = (StringVar(), StringVar())
		self.Sigma = (StringVar(), StringVar())
		self.q     = (StringVar(), StringVar())
		
		
		Label(self.detailFrame, text = "L:") \
			.grid(column = 0, row = 0)
		Entry(self.detailFrame, textvariable = self.L[0]) \
			.grid(column = 1, row = 0, sticky = W + E)
		Entry(self.detailFrame, textvariable = self.L[1], bg = defaultValueBG) \
			.grid(column = 2, row = 0, sticky = W + E)
		
		Label(self.detailFrame, text = "A:") \
			.grid(column = 4, row = 0)
		Entry(self.detailFrame, textvariable = self.A[0]) \
			.grid(column = 5, row = 0, sticky = W + E)
		Entry(self.detailFrame, textvariable = self.A[1], bg = defaultValueBG) \
			.grid(column = 6, row = 0, sticky = W + E)
		
		Label(self.detailFrame, text = "E:") \
			.grid(column = 0, row = 1)
		Entry(self.detailFrame, textvariable = self.E[0]) \
			.grid(column = 1, row = 1, sticky = W + E)
		Entry(self.detailFrame, textvariable = self.E[1], bg = defaultValueBG) \
			.grid(column = 2, row = 1, sticky = W + E)
		
		Label(self.detailFrame, text = "[σ]:") \
			.grid(column = 4, row = 1)
		Entry(self.detailFrame, textvariable = self.Sigma[0]) \
			.grid(column = 5, row = 1, sticky = W + E)
		Entry(self.detailFrame, textvariable = self.Sigma[1], bg = defaultValueBG) \
			.grid(column = 6, row = 1, sticky = W + E)
		
		Label(self.detailFrame, text = "q:") \
			.grid(column = 0, row = 2)
		Entry(self.detailFrame, textvariable = self.q[0]) \
			.grid(column = 1, row = 2, sticky = W + E)
		Entry(self.detailFrame, textvariable = self.q[1], bg = defaultValueBG) \
			.grid(column = 2, row = 2, sticky = W + E)
		
		
		self.detailFrame.columnconfigure(3, minsize = emptySpaceSize, weight = 0)
		for x in (1, 2, 4, 5): self.detailFrame.columnconfigure(x, weight = 1)
	
	
	def updateSelectedFrame(self, item = None, values = None):
		(item, values) = ElementListWidget.updateSelectedFrame(self, item, values)
		
		if item is None:
			for x in (self.L, self.A, self.E, self.Sigma, self.q):
				x[0].set("")
		else:
			self.L[0].set(values["L"])
			self.A[0].set(values["A"])
			self.E[0].set(values["E"])
			self.Sigma[0].set(values["[σ]"])
			self.q[0].set(values["q"])
	
	
	def addBar(self, bar):
		self.addElement((bar.label, str(bar.i), str(bar.L), str(bar.A), str(bar.E), str(bar.Sigma),
						 str(bar.q)))
	
	
	def setDefaultBar(self, bar):
		ElementListWidget.setDefaultElement(self, bar.label)
		
		self.L[1].set(bar.L)
		self.A[1].set(bar.A)
		self.E[1].set(bar.E)
		self.Sigma[1].set(bar.Sigma)
		self.q[1].set(bar.q)
