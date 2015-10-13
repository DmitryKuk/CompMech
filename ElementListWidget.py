#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *
from tkinter.ttk import Treeview

from Style import defaultValueBG


emptySpaceSize = 10

class ElementListWidget(Frame):
	def __init__(self, parent, label, columns, showError):
		Frame.__init__(self, parent)
		
		self.showError = showError
		
		self.columnconfigure(0, weight = 1)
		self.rowconfigure(1, weight = 1)
		
		
		# Название таблицы
		self.titleLabel = Label(self, text = label)
		self.titleLabel.grid(column = 0, row = 0, sticky = W + E)
		
		
		# Таблица значений
		columns = ("Метка", "№") + columns
		self.tree = Treeview(self, columns = columns, displaycolumns = columns,
							 selectmode = "browse")
		self.tree.grid(column = 0, row = 1, sticky = W + N + E + S)
		
		# Настраиваем внешний вид таблицы (первые колонки)
		self.tree.column("#0", width = 0, stretch = 0)	# Прячем колонку с иконкой
		
		self.tree.column( columns[0], anchor = W, width = 150)
		self.tree.heading(columns[0], anchor = W, text = columns[0])
		
		self.tree.column( columns[1], anchor = E, width = 80)
		self.tree.heading(columns[1], anchor = E, text = columns[1])
		
		self.tree.bind("<<TreeviewSelect>>", self.onSelectionChanged)
		
		
		# Панель с кнопками
		self.buttonPanel = Frame(self)
		self.buttonPanel.grid(column = 0, row = 2, sticky = W + E)
		
		self.buttonPanel.columnconfigure(0, weight = 1)
		self.buttonPanel.columnconfigure(3, minsize = emptySpaceSize, weight = 0)
		self.buttonPanel.columnconfigure(6, minsize = emptySpaceSize, weight = 0)
		self.buttonPanel.columnconfigure(9, weight = 1)
		
		# Кнопки добавления/удаления элемента
		self.buttonAdd = Button(self.buttonPanel, text = "+", width = 3,
								command = self.onButtonAddClicked)
		self.buttonAdd.grid(column = 1, row = 0)
		
		self.buttonRemove = Button(self.buttonPanel, text = "-", width = 3, state = DISABLED,
								   command = self.onButtonRemoveClicked)
		self.buttonRemove.grid(column = 2, row = 0)
		
		# Кнопки перемещения элемента
		self.buttonUp = Button(self.buttonPanel, text = "↑", width = 3, state = DISABLED,
							   command = self.onButtonUpClicked)
		self.buttonUp.grid(column = 4, row = 0)
		
		self.buttonDown = Button(self.buttonPanel, text = "↓", width = 3, state = DISABLED,
								 command = self.onButtonDownClicked)
		self.buttonDown.grid(column = 5, row = 0)
		
		# Кнопки применить/отменить (для выбранного элемента)
		self.buttonCancel = Button(self.buttonPanel, text = "✗", width = 3,
								   command = self.updateSelectedFrame)
		self.buttonCancel.grid(column = 7, row = 0)
		
		self.buttonApply = Button(self.buttonPanel, text = "✓", width = 3,
								  command = self.onButtonApplyClicked)
		self.buttonApply.grid(column = 8, row = 0)
		
		
		# Редактирование выделенного элемента
		self.i     = StringVar()
		self.label = (StringVar(), StringVar())
		
		self.selectedFrame = Frame(self)
		self.selectedFrame.grid(column = 0, row = 3, sticky = W + E)
		
		# Номер
		Label(self.selectedFrame, text = "№:") \
			.grid(column = 0, row = 0)
		Label(self.selectedFrame, textvariable = self.i, width = 3, justify = RIGHT) \
			.grid(column = 1, row = 0)
		
		# Пустое пространство
		self.selectedFrame.columnconfigure(2, minsize = emptySpaceSize, weight = 0)
		
		# Метка
		Entry(self.selectedFrame, textvariable = self.label[0]) \
			.grid(column = 3, row = 0, sticky = W + E)
		
		Entry(self.selectedFrame, textvariable = self.label[1], bg = defaultValueBG) \
			.grid(column = 4, row = 0, sticky = W + E)
		
		# Виджет для элементов классов-потомков
		self.detailFrame = Frame(self.selectedFrame)
		self.detailFrame.grid(column = 3, row = 1, columnspan = 2, sticky = W + N + E + S)
		
		self.selectedFrame.columnconfigure(3, weight = 1)
		self.selectedFrame.columnconfigure(4, weight = 1)
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
	
	
	def onButtonAddClicked(self):
		pass
	
	
	def onButtonRemoveClicked(self):
		item = self.selectedItem()
		if item is None: return
		
		next = self.tree.next(item)
		self.tree.delete(item)
		
		while next != "":
			i = int(self.tree.set(next, "№"))
			self.tree.set(next, "№", i - 1)
			next = self.tree.next(next)
		
		self.onSelectionChanged()
	
	
	def onButtonApplyClicked(self, item = None):
		if item is None: item = self.selectedItem()
		if item is None: return None
		
		label = self.label[0].get()
		self.tree.set(item, "Метка", label)
		
		return item
	
	
	def onSelectionChanged(self, event = None):
		item = self.selectedItem()
		
		# Обновляем состояние кнопок
		state = DISABLED if item is None else NORMAL
		for x in (self.buttonRemove, self.buttonUp, self.buttonDown):
			x["state"] = state
		
		self.updateSelectedFrame(item)
	
	
	def selectedItem(self):
		selection = self.tree.selection()
		return None if type(selection) == type("") else selection[0]
	
	
	def clear(self):
		for item in self.tree.get_children():
			self.tree.delete(item)
	
	
	def updateSelectedFrame(self, item = None, values = None):
		if item is None: item = self.selectedItem()
		values = None
		
		if item is None:
			i     = ""
			label = ""
		else:
			if values is None: values = self.tree.set(item)
			
			i     = values["№"]
			label = values["Метка"]
		
		self.i.set(i)
		self.label[0].set(label)
		
		return (item, values)
	
	
	def addElement(self, values):
		self.tree.insert(parent = "", index = END, values = values)
	
	
	def setDefaultElement(self, label):
		self.label[1].set(label)
	
	
	def elementsCount(self):
		return len(self.tree.get_children())
	
	
	def elements(self, transform):
		return [ transform(item) for item in self.tree.get_children() ]
