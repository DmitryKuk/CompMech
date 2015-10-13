#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *

from Bar import Bar
from Style import defaultValueBG
from ElementListWidget import *


class BarListWidget(ElementListWidget):
	def __init__(self, parent, showError):
		columns = ("L", "A", "E", "[σ]", "q")
		
		ElementListWidget.__init__(self, parent, label = "Стержни", columns = columns,
								   showError = showError)
		
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
	
	
	def onButtonAddClicked(self):
		try:
			label = self.label[1].get()
			L     = self.L[1].get()
			A     = self.A[1].get()
			E     = self.E[1].get()
			Sigma = self.Sigma[1].get()
			q     = self.q[1].get()
			
			m = {}
			if label != "": m.update({ "label": label })
			if L     != "": m.update({ "L":     L })
			if A     != "": m.update({ "A":     A })
			if E     != "": m.update({ "E":     E })
			if Sigma != "": m.update({ "Sigma": Sigma })
			if q     != "": m.update({ "q":     q })
			
			n = Bar(json = m)
			n.i = len(self.tree.get_children())
			
			self.addBar(n)
		except Exception as e:
			self.showError(str(e))
	
	
	def onButtonApplyClicked(self, item = None):
		item = ElementListWidget.onButtonApplyClicked(self, item)
		if item is None: return None
		
		L     = self.L[0].get()
		A     = self.A[0].get()
		E     = self.E[0].get()
		Sigma = self.Sigma[0].get()
		q     = self.q[0].get()
		
		self.tree.set(item, "L",   L)
		self.tree.set(item, "A",   A)
		self.tree.set(item, "E",   E)
		self.tree.set(item, "[σ]", Sigma)
		self.tree.set(item, "q",   q)
		
		return item
	
	
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
	
	
	def bars(self):
		def bar(item):
			v = self.tree.set(item)
			
			label = v["Метка"]
			L     = v["L"]
			A     = v["A"]
			E     = v["E"]
			Sigma = v["[σ]"]
			q     = v["q"]
			
			defaultNode = Bar(json = {
				"label": label,
				"L":     L,
				"A":     A,
				"E":     E,
				"Sigma": Sigma,
				"q":     q
			})
			
			return Bar(default = defaultNode)
		
		return ElementListWidget.elements(self, bar)
