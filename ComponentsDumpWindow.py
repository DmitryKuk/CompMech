#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *
from tkinter.ttk import Treeview
import tkinter.messagebox

from EntryValidation import validateFloat


class ComponentsDumpWindow(Toplevel):
	def __init__(self, application, **kwargs):
		Toplevel.__init__(self)
		
		self.application = application
		
		self.title("%s%sКомпоненты" % (self.application.name, self.application.nameDelim))
		
		self.validateFloatCommand = self.register(validateFloat)
		validateArgs = { "validate": "key", "validatecommand": (self.validateFloatCommand, "%S") }
		
		
		self.fromLabel = Label(self, text = "От x(global):")
		self.fromLabel.grid(column = 0, row = 0)
		
		self.fromVar = StringVar()
		self.fromEntry = Entry(self, textvariable = self.fromVar, **validateArgs)
		self.fromEntry.grid(column = 1, row = 0, sticky = W + E)
		self.columnconfigure(1, weight = 1)
		
		
		self.toLabel = Label(self, text = "До x(global):")
		self.toLabel.grid(column = 2, row = 0)
		
		self.toVar = StringVar()
		self.toEntry = Entry(self, textvariable = self.toVar, **validateArgs)
		self.toEntry.grid(column = 3, row = 0, sticky = W + E)
		self.columnconfigure(3, weight = 1)
		
		
		self.stepLabel = Label(self, text = "dx:")
		self.stepLabel.grid(column = 4, row = 0)
		
		self.stepVar = StringVar()
		self.stepEntry = Entry(self, textvariable = self.stepVar, **validateArgs)
		self.stepEntry.grid(column = 5, row = 0, sticky = W + E)
		self.columnconfigure(5, weight = 1)
		
		
		self.calculateButton = Button(self, text = "Рассчитать",
									  command = self.onCalculateButtonClicked)
		self.calculateButton.grid(column = 6, row = 0, columnspan = 2)
		
		self.rowconfigure(1, weight = 1)
		
		
		self.tree = None
		self.createTree()
		
		self.onConstructionChanged(False)
	
	
	def onWindowDestroy(self, event):
		self.application.onComponentsDumpWindowDestroy(self)
	
	
	def onCalculateButtonClicked(self):
		try:
			self.calculate()
		except Exception as e:
			self.showError(e)
	
	
	def onConstructionChanged(self, constructed = True):
		if not constructed:
			for var in [ self.fromVar, self.toVar, self.stepVar ]:
				var.set("0")
			return
		
		try:
			self.calculate()
		except Exception:
			self.clear()
	
	
	def onPointCalculated(self, x, N, U, Sigma):
		self.lastIID = self.tree.insert(parent = "", index = "end",
										values = ("%.14f" % x, "%.14f" % N,
												  "%.14f" % U, "%.14f" % Sigma))
	
	
	def createTree(self):
		columns = ("x", "Nx", "U", "σ")
		
		self.tree = Treeview(self, columns = columns, displaycolumns = columns)
		self.tree.grid(column = 0, row = 1, columnspan = 7, sticky = W + N + E + S)
		self.tree.column("#0", width = 0, stretch = 0)
		
		for x in columns:
			self.tree.column(x, anchor = E)
			self.tree.heading(x, text = x, anchor = E)
	
	
	def clear(self):
		del self.tree
		self.createTree()
	
	
	def calculate(self):
		self.clear()
		
		for var in [ self.fromVar, self.toVar, self.stepVar ]:
			try:
				float(var.get())
			except ValueError:
				var.set("0")
		
		xFrom = float(self.fromVar.get())
		xTo = float(self.toVar.get())
		xStep = float(self.stepVar.get())
		
		self.application.logic.calculateComponents(xFrom, xTo, xStep,
												   onPointCalculated = self.onPointCalculated)
	
	
	def showError(self, message):
		tkinter.messagebox.showerror("Ошибка", message)
