#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *
from tkinter.ttk import Treeview
import tkinter.messagebox


class ComponentsDumpWindow(Toplevel):
	def __init__(self, application, barNumber = None, **kwargs):
		Toplevel.__init__(self)
		
		self.application = application
		self.barNumber = barNumber
		
		
		self.fromLabel = Label(self)
		self.fromLabel.grid(column = 0, row = 0)
		
		self.fromVar = StringVar()
		self.fromEntry = Entry(self, textvariable = self.fromVar, justify = RIGHT)
		self.fromEntry.grid(column = 1, row = 0, sticky = W + E)
		self.columnconfigure(1, weight = 1)
		
		
		self.toLabel = Label(self)
		self.toLabel.grid(column = 2, row = 0)
		
		self.toVar = StringVar()
		self.toEntry = Entry(self, textvariable = self.toVar, justify = RIGHT)
		self.toEntry.grid(column = 3, row = 0, sticky = W + E)
		self.columnconfigure(3, weight = 1)
		
		
		self.stepLabel = Label(self, text = "dx:")
		self.stepLabel.grid(column = 4, row = 0)
		
		self.stepVar = StringVar()
		self.stepEntry = Entry(self, textvariable = self.stepVar, justify = RIGHT)
		self.stepEntry.grid(column = 5, row = 0, sticky = W + E)
		self.columnconfigure(5, weight = 1)
		
		
		self.calculateButton = Button(self, text = "Рассчитать",
									  command = self.onCalculateButtonClicked)
		self.calculateButton.grid(column = 6, row = 0, columnspan = 2)
		
		
		# Таблица рассчитанных значений
		columns = ("№ стержня", "x", "Nx", "U", "σ")
		
		self.tree = Treeview(self, columns = columns, displaycolumns = columns)
		self.tree.grid(column = 0, row = 1, columnspan = 7, sticky = W + N + E + S)
		self.tree.column("#0", width = 0, stretch = 0)
		
		# Настройки отображения таблицы
		self.tree.column(columns[0], anchor = CENTER)
		self.tree.heading(columns[0], text = columns[0], anchor = CENTER)
		
		for x in columns[1:]:
			self.tree.column(x, anchor = E)
			self.tree.heading(x, text = x, anchor = E)
		
		self.rowconfigure(1, weight = 1)
		
		
		self.bind("<Destroy>", self.onWindowDestroy)
		
		
		self.updateTitles()
		self.onConstructionChanged(False)
	
	
	def updateTitles(self):
		if self.barNumber is None:
			titleDescStr = ""
			xDescStr     = "global"
		else:
			titleDescStr = "%sСтержень (%d)" % (self.application.nameDelim, self.barNumber)
			xDescStr     = "local"
		
		self.title("%s%sКомпоненты%s" \
				   % (self.application.name, self.application.nameDelim, titleDescStr))
		
		self.fromLabel["text"] = "От x(" + xDescStr + "):"
		self.toLabel["text"] = "До x(" + xDescStr + "):"
	
	
	def onWindowDestroy(self, event):
		self.application.onWindowDestroy(self)
	
	
	def onCalculateButtonClicked(self):
		try:
			self.calculate()
		except Exception as e:
			self.showError(e)
	
	
	def onConstructionChanged(self, constructed = True):
		if not constructed:
			for var in self.fromVar, self.toVar, self.stepVar:
				var.set("0")
			return
		
		try:
			self.calculate()
		except Exception:
			self.clear()
	
	
	def onPointCalculated(self, barNumber, x, N, U, Sigma):
		if self.barNumber is not None and barNumber != self.barNumber:
			return
		
		self.tree.insert(parent = "", index = "end",
						 values = ("—" if barNumber is None else str(barNumber),
								   "%.14f" % x, "%.14f" % N,
								   "%.14f" % U, "%.14f" % Sigma))
	
	
	def clear(self):
		self.tree.delete(*self.tree.get_children())
	
	
	def calculate(self):
		self.clear()
		
		if self.barNumber not in range(0, self.application.logic.barsCount()):
			self.barNumber = None
			self.updateTitles()
		
		for var in self.fromVar, self.toVar, self.stepVar:
			try:
				float(var.get())
			except ValueError:
				var.set("0")
		
		xFrom = float(self.fromVar.get())
		xTo = float(self.toVar.get())
		xStep = float(self.stepVar.get())
		
		self.application.logic.calculateComponents(xFrom, xTo, xStep, barNumber = self.barNumber,
												   onPointCalculated = self.onPointCalculated)
	
	
	def showError(self, message):
		tkinter.messagebox.showerror("Ошибка", message)
