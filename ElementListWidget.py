#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *
from tkinter.ttk import Treeview


class ElementListWidget(Frame):
	def __init__(self, parent, label, columns, onSelectionChanged = None):
		Frame.__init__(self, parent)
		
		self.onSelectionChangedCommand = onSelectionChanged
		
		self.titleLabel = Label(self, text = label, anchor = W)
		self.titleLabel.grid(column = 0, row = 0, sticky = W + E)
		
		# Кнопки перемещения элемента
		self.buttonUp = Button(self, text = "↑", width = 3, command = self.onButtonUpClicked)
		self.buttonUp.grid(column = 1, row = 0)
		
		self.buttonDown = Button(self, text = "↓", width = 3, command = self.onButtonDownClicked)
		self.buttonDown.grid(column = 2, row = 0)
		
		# Таблица значений
		self.tree = Treeview(self, columns = columns, displaycolumns = columns,
							 selectmode = "browse")
		self.tree.column("#0", width = 0, stretch = 0)	# Прячем колонку с иконкой
		
		self.tree.grid(column = 0, row = 1, columnspan = 4, sticky = W + N + E + S)
		self.columnconfigure(0, weight = 1)
		self.rowconfigure(1, weight = 1)
		
		self.tree.bind("<<TreeviewSelect>>", self.onSelectionChanged)
		self.onSelectionChanged()
	
	
	def onButtonUpClicked(self):
		item = self.selectedItem()
		if item is None: return
		
		prev = self.tree.prev(item)
		if prev != "":
			parent, index = self.tree.parent(item), self.tree.index(item)
			self.tree.move(item, parent, index - 1)
			
			# Корректируем индексы
			self.tree.set(item, "№", index - 1)
			self.tree.set(prev, "№", index)
	
	
	def onButtonDownClicked(self):
		item = self.selectedItem()
		if item is None: return
		
		next = self.tree.next(item)
		if next != "":
			parent, index = self.tree.parent(item), self.tree.index(item)
			self.tree.move(item, parent, index + 1)
			
			# Корректируем индексы
			self.tree.set(item, "№", index + 1)
			self.tree.set(next, "№", index)
	
	
	def onSelectionChanged(self, event = None):
		item = self.selectedItem()
		
		# Обновляем состояние кнопок
		state = DISABLED if item is None else NORMAL
		for x in (self.buttonUp, self.buttonDown):
			x["state"] = state
		
		# Сообщаем "наверх"
		if self.onSelectionChangedCommand is not None:
			self.onSelectionChangedCommand()
	
	
	def selectedItem(self):
		selection = self.tree.selection()
		return None if type(selection) == type("") else selection[0]
	
	
	def clear(self):
		self.tree.delete(*self.tree.get_children())
	
	
	def addElement(self, values):
		self.tree.insert(parent = "", index = END, values = values)
