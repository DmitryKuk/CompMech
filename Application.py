#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from MainWindow import *
from Logic import *


class Application:
	def __init__(self):
		self.logic = Logic()
		self.mainWindow = MainWindow(self)
	
	
	def run(self):
		self.mainWindow.mainloop()
