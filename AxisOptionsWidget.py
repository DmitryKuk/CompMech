#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *


class AxisOptionsWidget(Frame):
	def __init__(self, parent, label = None, optionsDesc = [], command = None, **kwargs):
		Frame.__init__(self, parent, **kwargs)
		
		# Пустое пространство (растяжимое)
		Label(self, text = "  ").pack(side = LEFT, fill = X, expand = 1)
		
		if label is not None:
			self.label = Label(self, text = label)
			self.label.pack(side = LEFT)
		
		self.options = { name: self.createElement(text, value, state) \
						 for name, text, value, state in optionsDesc }
		
		# Пустое пространство (нерастяжимое)
		Label(self, text = "  ").pack(side = LEFT)#, fill = X, expand = 1)
		
		self.buttonDraw = Button(self, text = "⟳", command = self.onSBChanged)
		self.buttonDraw.pack(side = LEFT)
		
		# Пустое пространство (растяжимое)
		Label(self, text = "  ").pack(side = LEFT, fill = X, expand = 1)
		
		# Будет вызвано при изменении состояния пользователем
		self.command = command
	
	
	def createElement(self, text, value, state):
		var = StringVar()
		var.set("0" if value is None else str(int(value)))
		
		lb = Label(self, text = "  " + text, anchor = E)
		sb = Spinbox(self, textvariable = var, command = self.onSBChanged,
					 justify = RIGHT, width = 3,
					 from_ = 0, to = 999, increment = 1)
		if state in (NORMAL, DISABLED, ACTIVE):
			lb["state"] = state
			sb["state"] = state
		lb.pack(side = LEFT)#, fill = X, expand = 1)
		sb.pack(side = LEFT)
		
		return (text, var, sb, lb)
	
	
	def onSBChanged(self):
		# Уведомляем получателя об изменениях
		if self.command is not None: self.command()
	
	
	def get(self):
		def toInt(text, var, sb, lb):
			try:
				v = int(var.get())
			except:
				v = 0
			return 0 if sb["state"] == DISABLED else v
		
		return { name: toInt(*self.options[name]) for name in self.options }
	
	
	def set(self, **state):
		for name in state:
			(var, sb) = state[name]
			
			if var is not None:
				try:
					v = int(var.get())
				except:
					v = 0
				self.options[name][1].set(v)
			
			if sb is not None:
				st = sb if sb in (NORMAL, DISABLED, ACTIVE) else DISABLED
				
				for x in self.options[name][2], self.options[name][3]:
					x["state"] = st
