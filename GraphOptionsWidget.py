#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *


class GraphOptionsWidget(Frame):
	def __init__(self, parent, optionsDesc = [], command = None, **kwargs):
		Frame.__init__(self, parent, **kwargs)
		
		self.options = { name: self.createElement(text, value, cbState) \
						 for name, text, value, cbState in optionsDesc }
		
		# Будет вызвано при изменении состояния пользователем
		self.command = command
	
	
	def createElement(self, text, value, cbState):
		var = IntVar()
		if value is not None and bool(value): var.set(1)
		
		cb = Checkbutton(self, text = text, variable = var, command = self.onCBClicked)
		if cbState in (NORMAL, DISABLED, ACTIVE): cb["state"] = cbState
		cb.pack(fill = X)
		
		return (text, var, cb)
	
	
	def onCBClicked(self):
		# Уведомляем получателя об изменениях
		if self.command is not None: self.command()
	
	
	def get(self):
		def toBool(text, var, cb):
			return True if var.get() == 1 and cb["state"] != DISABLED else False
		
		return { name: toBool(*self.options[name]) for name in self.options }
	
	
	def set(self, **state):
		for name in state:
			(var, cb) = state[name]
			
			if var is not None:
				self.options[name][1].set(1 if var == True else 0)
			
			if cb is not None:
				self.options[name][2]["state"] = cb if cb in (NORMAL, DISABLED, ACTIVE) \
													else DISABLED
