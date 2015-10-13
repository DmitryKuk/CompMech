#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *

from Node import Node
from Style import defaultValueBG
from ElementListWidget import *


class NodeListWidget(ElementListWidget):
	def __init__(self, parent, showError):
		columns = ("Заделка", "F")
		
		ElementListWidget.__init__(self, parent, label = "Узлы", columns = columns,
								   showError = showError)
		
		# Настройки отображения таблицы
		self.tree.column( columns[0], anchor = CENTER, width = 100)
		self.tree.heading(columns[0], anchor = CENTER, text = columns[0])
		
		self.tree.column( columns[1], anchor = E, width = 80)
		self.tree.heading(columns[1], anchor = E, text = columns[1])
		
		
		# Параметры выбранного узла
		self.F        = (StringVar(), StringVar())
		self.fixed    = (IntVar(),    IntVar())
		
		
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
	
	
	def onButtonAddClicked(self):
		try:
			label = self.label[1].get()
			F     = self.F[1].get()
			
			m = { "fixed": False if self.fixed[1].get() == 0 else True }
			if label != "": m.update({ "label": label })
			if F != "": m.update({ "F": F })
			
			n = Node(json = m)
			n.i = len(self.tree.get_children())
			
			self.addNode(n)
		except Exception as e:
			self.showError(str(e))
	
	
	def onButtonApplyClicked(self, item = None):
		item = ElementListWidget.onButtonApplyClicked(self, item)
		if item is None: return None
		
		F     = self.F[0].get()
		fixed = self.fixed[0].get()
		
		self.tree.set(item, "F", F)
		self.tree.set(item, "Заделка", "свободен" if fixed == 0 else "зафиксирован")
		
		return item
	
	
	def updateSelectedFrame(self, item = None, values = None):
		(item, values) = ElementListWidget.updateSelectedFrame(self, item, values)
		
		if item is None:
			F     = ""
			fixed = 0
		else:
			F     = values["F"]
			fixed = 1 if values["Заделка"] == "зафиксирован" else 0
		
		self.F[0].set(F)
		self.fixed[0].set(fixed)
	
	
	def addNode(self, node):
		self.addElement((node.label, str(node.i),
						 "зафиксирован" if node.fixed else "свободен", str(node.F)))
	
	
	def setDefaultNode(self, node):
		ElementListWidget.setDefaultElement(self, node.label)
		
		self.F[1].set(node.F)
		self.fixed[1].set(node.fixed)
