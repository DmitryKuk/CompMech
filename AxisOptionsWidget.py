#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *


class AxisOptionsWidget(Frame):
	def __init__(self, parent, optionsDesc = [], command = None, **kwargs):
		Frame.__init__(self, parent, **kwargs)
		
		self.options = { name: self.createElement(text, value, state) \
						 for name, text, value, state in optionsDesc }
		
		# Будет вызвано при изменении состояния пользователем
		self.command = command
	
	
	def createElement(self, text, value, state):
		var = StrVar()
		var.set("0" if value is None else str(int(value)))
		
		lb = Label(self, text = text)
		sb = Spinbox(self, textvariable = var, command = self.onSBChanged)
		if state in (NORMAL, DISABLED, ACTIVE):
			lb["state"] = state
			sb["state"] = state
		lb.pack(fill = X, expand = 1)
		sb.pack(fill = X, expand = 1)
		
		return (text, var, sb)
	
	
	def onSBChanged(self):
		# Уведомляем получателя об изменениях
		if self.command is not None: self.command()
	
	
	def get(self):
		def toInt(text, var, sb):
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
				self.options[name][2]["state"] = sb if sb in (NORMAL, DISABLED, ACTIVE) \
													else DISABLED
