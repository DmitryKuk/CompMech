#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *


class GraphOptionsWidget(Frame):
	def __init__(self, parent, command = None, **kwargs):
		Frame.__init__(self, parent, **kwargs)
		
		optionsDesc = [
			("drawConstruction", "Конструкция"),
			("drawLoads",        "Нагрузки"),
			("drawN",            "Эпюра Nx"),
			("drawU",            "Эпюра U"),
			("drawSigma",        "Эпюра σ")
		]
		
		
		self.options = { name: self.newElement(text) for name, text in optionsDesc }
		
		# Будет вызвано при изменении состояния пользователем
		self.command = command
	
	
	def newElement(self, text):
		var = IntVar()
		cb = Checkbutton(self, text = text, variable = var, command = self.onCBClicked)
		cb.pack(fill = X)
		return (text, var, cb)
	
	
	def onCBClicked(self):
		# Уведомляем получателя об изменениях
		if self.command is not None: self.command()
	
	
	def get(self):
		def check(text, var, cb):
			return True if var.get() == 1 and cb["state"] != DISABLED else False
		
		return { name: True if check(*self.options[name]) else False \
				 for name in self.options }
	
	
	def set(self, **state):
		for name in state:
			(var, ch) = state[name]
			
			if var is not None:
				self.options[name][1].set(1 if var == True else 0)
			
			if ch is not None:
				self.options[name][2]["state"] = ch if ch in (NORMAL, DISABLED, ACTIVE) \
													else DISABLED
