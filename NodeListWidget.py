#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *

from Style import defaultValueBG
from ElementListWidget import *


class NodeListWidget(ElementListWidget):
	def __init__(self, parent):
		columns = ("Заделка", "F")
		
		ElementListWidget.__init__(self, parent, label = "Узлы", columns = columns)
		
		# Настройки отображения таблицы
		self.tree.column( columns[0], anchor = CENTER, width = 100)
		self.tree.heading(columns[0], anchor = CENTER, text = columns[0])
		
		self.tree.column( columns[1], anchor = E, width = 80)
		self.tree.heading(columns[1], anchor = E, text = columns[1])
		
		
		# Параметры выбранного узла
		self.F     = (StringVar(), StringVar())
		self.fixed = (IntVar(),    IntVar())
		
		
		# Нагрузка
		f1 = Frame(self.detailFrame)
		f1.grid(column = 0, row = 0, sticky = W + N + E + S)
		f1.columnconfigure(1, weight = 1)
		f1.columnconfigure(2, weight = 1)
		
		Label(f1, text = "F:", justify = RIGHT) \
			.grid(column = 0, row = 0)
		Entry(f1, textvariable = self.F[0]) \
			.grid(column = 1, row = 0, sticky = W + E)
		Entry(f1, textvariable = self.F[1], bg = defaultValueBG) \
			.grid(column = 2, row = 0, sticky = W + E)
		
		# Заделка
		f2 = Frame(self.detailFrame)
		f2.grid(column = 0, row = 1, sticky = W + N + E + S)
		f2.columnconfigure(0, weight = 1)
		f2.columnconfigure(1, weight = 1)
		
		Checkbutton(f2, variable = self.fixed[0],
			text = "Зафиксирован", justify = LEFT) \
			.grid(column = 0, row = 0, sticky = W + E)
		Checkbutton(f2, variable = self.fixed[1], bg = defaultValueBG,
			text = "Зафиксирован", justify = LEFT) \
			.grid(column = 1, row = 0, sticky = W + E)
		
		self.detailFrame.columnconfigure(2, minsize = emptySpaceSize, weight = 0)
		self.detailFrame.columnconfigure(1, weight = 1)
	
	
	def updateSelectedFrame(self, item = None, values = None):
		(item, values) = ElementListWidget.updateSelectedFrame(self, item, values)
		
		if item is None:
			self.F[0].set("")
			self.fixed[0].set(0)
		else:
			self.F[0].set(values["F"])
			self.fixed[0].set(1 if values["Заделка"] == "зафиксирован" else 0)
	
	
	def addNode(self, node):
		self.addElement((node.label, str(node.i),
						 "зафиксирован" if node.fixed else "свободен", str(node.F)))
	
	
	def setDefaultNode(self, node):
		ElementListWidget.setDefaultElement(self, node.label)
		
		self.F[1].set(node.F)
		self.fixed[1].set(node.fixed)
