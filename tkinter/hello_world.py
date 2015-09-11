#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *


class But_print:
	def __init__(self):
		self.but = Button(root)
		self.but["text"] = "Печать"
		self.but.bind("<Button-1>", self.printer)
		self.but.pack()
	
	
	def printer(self, event):
		print ("Как всегда очередной 'Hello World!'")


root = Tk()
obj = But_print()
root.mainloop()
