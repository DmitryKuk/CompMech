#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *
import tkinter.messagebox

from NodeListWidget import NodeListWidget
from BarListWidget import BarListWidget


class EditConstructionWindow(Toplevel):
	def __init__(self, application, barNumber = None, **kwargs):
		Toplevel.__init__(self)
		
		self.application = application
		
		self.title("%s%sРедактор конструкции" % (self.application.name, self.application.nameDelim))
		
		
		# Панели редактора
		self.panedWindow = PanedWindow(self, orient = HORIZONTAL)
		self.panedWindow.grid(column = 0, row = 0, columnspan = 4, sticky = W + N + E + S)
		
		# Левая панель: редактор узлов
		self.nodeList = NodeListWidget(self.panedWindow, showError = self.showError)
		self.panedWindow.add(self.nodeList)
		self.nodeList.addNode(self.application.construction.defaultNode)
		
		# Правая панель: редактор стержней
		self.barList = BarListWidget(self.panedWindow, showError = self.showError)
		self.panedWindow.add(self.barList)
		self.barList.addBar(self.application.construction.defaultBar)
		
		self.rowconfigure(0, weight = 1)
		
		
		# Панель с кнопками снизу
		self.columnconfigure(0, weight = 1)
		
		Button(self, text = "Отменить", command = self.onConstructionChanged) \
			.grid(column = 1, row = 1)
		
		Button(self, text = "Применить", command = self.onApplyButtonClicked) \
			.grid(column = 2, row = 1)
		
		self.columnconfigure(3, minsize = 20, weight = 0)
		
		
		self.bind("<Destroy>", self.onWindowDestroy)
		
		self.onConstructionChanged()
	
	
	def onWindowDestroy(self, event):
		self.application.onWindowDestroy(self)
	
	
	def onApplyButtonClicked(self):
		# try:
		self.application.logic.createConstructionFromElements(
			nodes = self.nodeList.nodes(),
			bars = self.barList.bars(),
			defaultNode = self.nodeList.defaultNode(),
			defaultBar = self.barList.defaultBar()
		)
		# except Exception as e:
		# 	self.showError(str(e))
	
	
	def onConstructionChanged(self):
		self.clear()
		self.application.logic.getDefault(onNodeDetected = self.nodeList.setDefaultNode,
										  onBarDetected  = self.barList.setDefaultBar)
		self.application.logic.getElements(onNodeDetected = self.nodeList.addNode,
										   onBarDetected  = self.barList.addBar)
	
	
	def clear(self):
		self.nodeList.clear()
		self.barList.clear()
	
	
	def showError(self, message):
		tkinter.messagebox.showerror("Ошибка", message)
