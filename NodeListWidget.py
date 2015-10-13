#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *

from ElementListWidget import *


class NodeListWidget(ElementListWidget):
	def __init__(self, parent):
		columns = ("Заделка", "F")
		
		ElementListWidget.__init__(self, parent, label = "Узлы:", columns = columns)
		
		# Настройки отображения таблицы
		self.tree.column( columns[0], anchor = CENTER, width = 100)
		self.tree.heading(columns[0], anchor = CENTER, text = columns[0])
		
		self.tree.column( columns[1], anchor = E, width = 80)
		self.tree.heading(columns[1], anchor = E, text = columns[1])
		
		
		# Параметры выбранного узла
		self.F     = StringVar()
		self.fixed = IntVar()
		
		
		# Нагрузка
		Label(self.detailFrame, text = "F:", justify = RIGHT) \
			.grid(column = 0, row = 0)
		Entry(self.detailFrame, textvariable = self.F) \
			.grid(column = 1, row = 0, sticky = W + E)
		
		# Заделка
		Checkbutton(self.detailFrame, variable = self.fixed,
			text = "Зафиксирован", justify = LEFT) \
			.grid(column = 3, row = 0)
		
		self.detailFrame.columnconfigure(2, minsize = emptySpaceSize, weight = 0)
		self.detailFrame.columnconfigure(1, weight = 1)
	
	
	def addNode(self, node):
		self.addElement((node.label, str(node.i),
						 "зафиксирован" if node.fixed else "свободен", str(node.F)))
	
	
	def updateSelectedFrame(self, item = None, values = None):
		(item, values) = ElementListWidget.updateSelectedFrame(self, item, values)
		
		if item is None:
			self.F.set("")
			self.fixed = 0
		else:
			self.F.set(values["F"])
			self.fixed.set(1 if values["Заделка"] == "зафиксирован" else 0)
