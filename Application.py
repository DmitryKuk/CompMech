#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from MainWindow import MainWindow
from DetailWindow import DetailWindow
from MatricesWindow import MatricesWindow
from ComponentsDumpWindow import ComponentsDumpWindow
from EditConstructionWindow import EditConstructionWindow
from Logic import Logic


class Application:
	def __init__(self):
		self.name = "Стержни от Димыча"
		self.nameDelim = " — "
		
		self.version = "1.0"
		self.timestamp = "Октябрь 2015"
		
		self.construction = None
		
		self.logic = Logic(self)
		
		# Окна
		self.mainWindow = MainWindow(self)
		self.detailWindows			 = set()
		self.matricesWindows		 = set()
		self.componentsDumpWindows	 = set()
		self.editConstructionWindows = set()
		
		self.createEditConstructionWindow()
	
	
	def createDetailWindow(self, barNumber = 0):
		self.detailWindows.add(DetailWindow(self, barNumber = barNumber))
	
	
	def createMatricesWindow(self, barNumber = None):
		self.matricesWindows.add(MatricesWindow(self, barNumber = barNumber))
	
	
	def createComponentsDumpWindow(self, barNumber = None):
		self.componentsDumpWindows.add(ComponentsDumpWindow(self, barNumber = barNumber))
	
	
	def createEditConstructionWindow(self, barNumber = None):
		self.editConstructionWindows.add(EditConstructionWindow(self, barNumber = barNumber))
	
	
	def onDetailWindowDestroy(self, window):
		self.detailWindows.discard(window)
	
	
	def onMatricesWindowDestroy(self, window):
		self.matricesWindows.discard(window)
	
	
	def onComponentsWindowDestroy(self, window):
		self.componentsDumpWindows.discard(window)
	
	
	def onEditConstructionDestroy(self, window):
		self.editConstructionWindows.discard(window)
	
	
	def onConstructionChanged(self):
		self.mainWindow.onConstructionChanged()
		for s in self.detailWindows, self.matricesWindows, \
				 self.componentsDumpWindows, self.editConstructionWindows:
			for w in s:
				w.onConstructionChanged()
	
	
	def run(self):
		self.mainWindow.mainloop()
	
	
	def about(self):
		return "Версия: %s, %s\n\n" \
			   "Куковинец Дмитрий Валерьевич\nd1021976@gmail.com\n\n" \
			   "ФГБОУ ВО \"МГТУ \"СТАНКИН\"\nКафедра УИТС" \
			   % (self.version, self.timestamp)
