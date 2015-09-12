#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from MainWindow import *
from Logic import *


class Application:
	def __init__(self):
		self.logic = Logic()
		self.mainWindow = MainWindow(self,
									 offsetWFunc = self.logic.offsetWEFunc,
									 offsetNFunc = self.logic.offsetNSFunc,
									 offsetEFunc = self.logic.offsetWEFunc,
									 offsetSFunc = self.logic.offsetNSFunc)
	
	
	def run(self):
		self.mainWindow.mainloop()
