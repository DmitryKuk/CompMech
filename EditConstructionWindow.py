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
		
		self.panedWindow = PanedWindow(self, orient = HORIZONTAL)
		self.panedWindow.pack(fill = BOTH, expand = 1)
		
		# Левая панель: редактор узлов
		self.nodeList = NodeListWidget(self.panedWindow)
		self.panedWindow.add(self.nodeList)
		self.nodeList.addNode(self.application.construction.defaultNode)
		
		# Правая панель: редактор стержней
		self.barList = BarListWidget(self.panedWindow)
		self.panedWindow.add(self.barList)
		self.barList.addBar(self.application.construction.defaultBar)
		
		self.bind("<Destroy>", self.onWindowDestroy)
		
		self.onConstructionChanged()
	
	
	def onWindowDestroy(self, event):
		self.application.onEditConstructionWindowDestroy(self)
	
	
	def onApplyButtonClicked(self):
		pass
	
	
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
