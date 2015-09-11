#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from MainWindow import *


class Application:
	def __init__(self):
		self.mainWindow = MainWindow(self)
	
	
	def run(self):
		self.mainWindow.root.mainloop()
