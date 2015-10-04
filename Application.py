#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from MainWindow import MainWindow
from DetailWindow import DetailWindow
from Logic import *


class Application:
	def __init__(self):
		self.name = "Стержни от Димыча"
		self.nameDelim = " — "
		
		self.version = "1.0"
		self.timestamp = "Октябрь 2015"
		
		self.construction = None
		
		self.logic = Logic(self)
		self.mainWindow = MainWindow(self, offsetFunc = self.logic.offsetFunc)
		self.detailWindows = set()
	
	
	def createDetailWindow(self, barNumber = 0):
		self.detailWindows.add(DetailWindow(self, barNumber = barNumber,
											offsetFunc = self.logic.offsetFunc))
	
	
	def onDetailWindowDestroy(self, window):
		try:
			self.detailWindows.remove(window)
		except KeyError:
			pass
	
	
	def onConstructionChanged(self):
		self.mainWindow.onConstructionChanged()
		for window in self.detailWindows:
			window.onConstructionChanged()
	
	
	def run(self):
		self.mainWindow.mainloop()
	
	
	def about(self):
		return "Версия: %s, %s\n\n" \
			   "Куковинец Дмитрий Валерьевич\nd1021976@gmail.com\n\n" \
			   "ФГБОУ ВО \"МГТУ \"СТАНКИН\"\nКафедра УИТС" \
			   % (self.version, self.timestamp)
