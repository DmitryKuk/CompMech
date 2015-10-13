#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *

from ElementListWidget import ElementListWidget


class NodeListWidget(ElementListWidget):
	def __init__(self, parent):
		columns = ("Заделка", "F")
		
		ElementListWidget.__init__(self, parent, label = "Узлы:", columns = columns)
		
		# Настройки отображения таблицы
		self.tree.column( columns[0], anchor = CENTER, width = 100)
		self.tree.heading(columns[0], anchor = CENTER, text = columns[0])
		
		self.tree.column( columns[1], anchor = E, width = 80)
		self.tree.heading(columns[1], anchor = E, text = columns[1])
	
	
	def addNode(self, node):
		self.addElement((node.label, str(node.i),
						 "зафиксирован" if node.fixed else "свободен", str(node.F)))
