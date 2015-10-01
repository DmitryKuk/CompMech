#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from MainWindow import *
from Logic import *


class Application:
	def __init__(self):
		self.construction = None
		self.elements = None
		
		self.logic = Logic(self)
		self.mainWindow = MainWindow(self, offsetFunc = self.logic.offsetFunc)
	
	
	def run(self):
		self.mainWindow.mainloop()
