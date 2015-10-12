#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *
from tkinter.ttk import Treeview


class ElementListWidget(Frame):
	def __init__(self, parent, columns):
		Frame.__init__(self, parent)
		
		self.tree = Treeview(self, columns = columns, displaycolumns = columns)
		self.tree.column("#0", width = 0, stretch = 0)	# Прячем колонку с иконкой
		
		self.tree.grid(column = 0, row = 0, sticky = W + N + E + S)
		self.columnconfigure(0, weight = 1)
		self.rowconfigure(0, weight = 1)
	
	
	def clear(self):
		self.tree.delete(*self.tree.get_children())
	
	
	def addElement(self, values):
		self.tree.insert(parent = "", index = END, values = values)
