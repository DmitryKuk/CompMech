#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *
import tkinter.font
from sympy import pretty


class MatricesWindow(Toplevel):
	def __init__(self, application, **kwargs):
		Toplevel.__init__(self)
		
		self.application = application
		
		self.title("%s%sМатрицы" % (self.application.name, self.application.nameDelim))
		
		self.A = StringVar()
		self.b = StringVar()
		self.Deltas = StringVar()
		
		
		# Подбираем моноширинный шрифт для печати матриц
		fontFamilies = tkinter.font.families()
		labelArgs = {}
		for x in fontFamilies:
			if "Mono" in x:
				labelArgs = { "font": tkinter.font.Font(family = x) }
				print("Выбран моноширинный шрифт: %s" % x)
				break
		
		
		self.columnconfigure(0, weight = 1)
		
		
		# A
		self.ATitleLabel = Label(self, text = "[A] = ", **labelArgs)
		self.ATitleLabel.grid(column = 1, row = 0, sticky = N + S)
		
		self.ALabel = Label(self, textvariable = self.A, **labelArgs)
		self.ALabel.grid(column = 2, row = 0, sticky = N + S)
		
		self.columnconfigure(3, weight = 1)
		
		
		# b
		self.bTitleLabel = Label(self, text = "{b} = ", **labelArgs)
		self.bTitleLabel.grid(column = 4, row = 0, sticky = N + S)
		
		self.bLabel = Label(self, textvariable = self.b, **labelArgs)
		self.bLabel.grid(column = 5, row = 0, sticky = N + S)
		
		self.columnconfigure(6, weight = 1)
		
		
		# Deltas
		self.DeltasTitleLabel = Label(self, text = "{Δ} = ", **labelArgs)
		self.DeltasTitleLabel.grid(column = 7, row = 0, sticky = N + S)
		
		self.DeltasLabel = Label(self, textvariable = self.Deltas, **labelArgs)
		self.DeltasLabel.grid(column = 8, row = 0, sticky = N + S)
		
		
		self.columnconfigure(9, weight = 1)
		self.rowconfigure(0, weight = 1)
		
		
		self.onConstructionChanged()
	
	
	def onWindowDestroy(self, event):
		self.application.onMatricesWindowDestroy(self)
	
	
	def onConstructionChanged(self):
		m = self.application.logic.matrices()
		if m is None:
			self.A.set("<Не рассчитано>")
			self.b.set("<Не рассчитано>")
			self.Deltas.set("<Не рассчитано>")
		
		self.A.set(pretty(m[0]))
		self.b.set(pretty(m[1]))
		self.Deltas.set(pretty(m[2]))
