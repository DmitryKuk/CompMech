#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *
from tkinter.ttk import Treeview


emptySpaceSize = 10

class ElementListWidget(Frame):
	def __init__(self, parent, label, columns):
		Frame.__init__(self, parent)
		
		# Название таблицы
		self.titleLabel = Label(self, text = label, anchor = W)
		self.titleLabel.grid(column = 0, row = 0, sticky = W + E)
		
		
		# Кнопки перемещения элемента
		self.buttonUp = Button(self, text = "↑", width = 3, state = DISABLED,
							   command = self.onButtonUpClicked)
		self.buttonUp.grid(column = 1, row = 0)
		
		self.buttonDown = Button(self, text = "↓", width = 3, state = DISABLED,
								 command = self.onButtonDownClicked)
		self.buttonDown.grid(column = 2, row = 0)
		
		
		# Таблица значений
		columns = ("Метка", "№") + columns
		self.tree = Treeview(self, columns = columns, displaycolumns = columns,
							 selectmode = "browse")
		
		# Настраиваем внешний вид таблицы (первые колонки)
		self.tree.column("#0", width = 0, stretch = 0)	# Прячем колонку с иконкой
		
		self.tree.column( columns[0], anchor = W, width = 150)
		self.tree.heading(columns[0], anchor = W, text = columns[0])
		
		self.tree.column( columns[1], anchor = E, width = 80)
		self.tree.heading(columns[1], anchor = E, text = columns[1])
		
		
		self.tree.grid(column = 0, row = 1, columnspan = 4, sticky = W + N + E + S)
		self.columnconfigure(0, weight = 1)
		self.rowconfigure(1, weight = 1)
		
		
		self.tree.bind("<<TreeviewSelect>>", self.onSelectionChanged)
		
		
		# Редактирование выделенного элемента
		self.i     = StringVar()
		self.label = StringVar()
		
		self.selectedFrame = Frame(self)
		self.selectedFrame.grid(column = 0, row = 2, columnspan = 3, sticky = W + N + E + S)
		
		# Номер
		Label(self.selectedFrame, text = "№:") \
			.grid(column = 0, row = 0)
		Label(self.selectedFrame, textvariable = self.i, width = 3, justify = RIGHT) \
			.grid(column = 1, row = 0)
		
		# Пустое пространство
		self.selectedFrame.columnconfigure(2, minsize = emptySpaceSize, weight = 0)
		
		# Метка
		Entry(self.selectedFrame, textvariable = self.label) \
			.grid(column = 3, row = 0, sticky = W + E)
		
		# Виджет для элементов классов-потомков
		self.detailFrame = Frame(self.selectedFrame)
		self.detailFrame.grid(column = 3, row = 1, sticky = W + N + E + S)
		
		self.selectedFrame.columnconfigure(3, weight = 1)
		self.selectedFrame.rowconfigure(1, weight = 1)
	
	
	def onButtonUpClicked(self):
		item = self.selectedItem()
		if item is None: return
		
		prev = self.tree.prev(item)
		if prev != "":
			parent, index = self.tree.parent(item), self.tree.index(item)
			self.tree.move(item, parent, index - 1)
			
			# Корректируем номера элементов
			self.tree.set(item, "№", index - 1)
			self.tree.set(prev, "№", index)
			
			self.updateSelectedFrame(item)
	
	
	def onButtonDownClicked(self):
		item = self.selectedItem()
		if item is None: return
		
		next = self.tree.next(item)
		if next != "":
			parent, index = self.tree.parent(item), self.tree.index(item)
			self.tree.move(item, parent, index + 1)
			
			# Корректируем номера элементов
			self.tree.set(item, "№", index + 1)
			self.tree.set(next, "№", index)
			
			self.updateSelectedFrame(item)
	
	
	def onSelectionChanged(self, event = None):
		item = self.selectedItem()
		
		# Обновляем состояние кнопок
		state = DISABLED if item is None else NORMAL
		for x in (self.buttonUp, self.buttonDown):
			x["state"] = state
		
		self.updateSelectedFrame(item)
	
	
	def updateSelectedFrame(self, item = None, values = None):
		if item is None: item = self.selectedItem()
		values = None
		
		if item is None:
			self.i.set("")
			self.label.set("")
		else:
			if values is None: values = self.tree.set(item)
			
			self.i.set(values["№"])
			self.label.set(values["Метка"])
		
		return (item, values)
	
	
	def selectedItem(self):
		selection = self.tree.selection()
		return None if type(selection) == type("") else selection[0]
	
	
	def clear(self):
		for item in self.tree.get_children():
			self.tree.delete(item)
	
	
	def addElement(self, values):
		self.tree.insert(parent = "", index = END, values = values)
