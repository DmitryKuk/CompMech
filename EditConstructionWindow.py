#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *
import tkinter.messagebox


class EditConstructionWindow(Toplevel):
	def __init__(self, application, barNumber = None, **kwargs):
		Toplevel.__init__(self)
		
		self.application = application
		
		self.title("%s%sРедактор конструкции" % (self.application.name, self.application.nameDelim))
		
		
		# def onEntryFocusIn(reason, name, text):
		# 	if reason == "focusin":
		# 		widget = self.nametowidget(name)
		# 		widget.select_range(0, END)
		# 		widget.icursor(END)
		# 	elif text == "":
		# 		self.nametowidget(name).insert(0, "0")
		# 	return True
		
		# self.onEntryFocusInCommand = self.register(onEntryFocusIn)
		# validateArgs = { "validate": "focus",
		# 				 "validatecommand": (self.onEntryFocusInCommand, "%V", "%W", "%P") }
		
		
		self.canvas = Canvas(self, width = 500, height = 500, scrollregion = (0, 0, 500, 500))
		self.canvas.bind("<MouseWheel>", lambda event: self.canvas.yview_scroll(-event.delta, UNITS))
		self.canvas.grid(column = 0, row = 0, sticky = W + N + E + S)
		self.columnconfigure(0, weight = 1)
		self.rowconfigure(0, weight = 1)
		
		
		self.yScrollbar = Scrollbar(self, orient = VERTICAL, command = self.canvas.yview)
		self.yScrollbar.grid(column = 1, row = 0, sticky = N + S)
		
		self.canvas["yscrollcommand"] = self.yScrollbar.set
		
		
		self.frame1 = Frame(self.canvas)
		self.fromLabel = Label(self.frame1, text = "from")
		self.fromLabel.grid(column = 0, row = 0)
		
		self.fromVar = StringVar()
		self.fromEntry = Entry(self.frame1, textvariable = self.fromVar, justify = RIGHT)
		self.fromEntry.grid(column = 1, row = 0, sticky = W + E)
		self.frame1.columnconfigure(1, weight = 1)
		
		
		self.frame2 = Frame(self.canvas)
		self.toLabel = Label(self.frame2, text = "to")
		self.toLabel.grid(column = 0, row = 0)
		
		self.toVar = StringVar()
		self.toEntry = Entry(self.frame2, textvariable = self.toVar, justify = RIGHT)
		self.toEntry.grid(column = 1, row = 0, sticky = W + E)
		self.frame2.columnconfigure(3, weight = 1)
		
		
		self.frame3 = Frame(self.canvas)
		self.stepLabel = Label(self.frame3, text = "dx:")
		self.stepLabel.grid(column = 0, row = 0)
		
		self.stepVar = StringVar()
		self.stepEntry = Entry(self.frame3, textvariable = self.stepVar, justify = RIGHT)
		self.stepEntry.grid(column = 1, row = 0, sticky = W + E)
		self.frame3.columnconfigure(5, weight = 1)
		
		
		self.frame4 = Frame(self.canvas)
		self.calculateButton = Button(self.frame4, text = "Рассчитать")
		self.calculateButton.grid(column = 6, row = 0, columnspan = 2)
		
		
		self.canvas.create_window(250,  40, window = self.frame1)
		self.canvas.create_window(250,  80, window = self.frame2)
		self.canvas.create_window(250, 120, window = self.frame3)
		self.canvas.create_window(250, 160, window = self.frame4)
		
		
		self.onConstructionChanged(False)
	
	
	def onWindowDestroy(self, event):
		self.application.onEditConstructionWindowDestroy(self)
	
	
	def onApplyButtonClicked(self):
		# try:
		# 	self.calculate()
		# except Exception as e:
		# 	self.showError(e)
		pass
	
	
	def onConstructionChanged(self, constructed = True):
		# if not constructed:
		# 	for var in self.fromVar, self.toVar, self.stepVar:
		# 		var.set("0")
		# 	return
		
		# try:
		# 	self.calculate()
		# except Exception:
		# 	self.clear()
		pass
	
	
	def onPointCalculated(self, barNumber, x, N, U, Sigma):
		self.tree.insert(parent = "", index = "end",
						 values = ("—" if barNumber is None else str(barNumber),
								   "%.14f" % x, "%.14f" % N,
								   "%.14f" % U, "%.14f" % Sigma))
	
	
	def createTree(self):
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
	
	
	def clear(self):
		del self.tree
		self.createTree()
	
	
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
