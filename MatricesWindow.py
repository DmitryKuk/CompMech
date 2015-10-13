#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *
import tkinter.font


class MatricesWindow(Toplevel):
	def __init__(self, application, barNumber = None, **kwargs):
		Toplevel.__init__(self)
		
		self.application = application
		self.barNumber = barNumber
		self.updateTitle()
		
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
		
		
		(ATitle, bTitle, DeltasTitle) = ("[A] =", "{b} =", "{Δ} =") \
										if self.barNumber is None \
										else ("[K] =", "{Q} =", "{U} =")
		
		
		# A
		self.ATitleLabel = Label(self, text = ATitle, **labelArgs)
		self.ATitleLabel.grid(column = 1, row = 0, sticky = N + S)
		
		self.ALabel = Label(self, textvariable = self.A, **labelArgs)
		self.ALabel.grid(column = 2, row = 0, sticky = N + S)
		
		self.columnconfigure(3, weight = 1, minsize = 20)
		
		
		# b
		self.bTitleLabel = Label(self, text = bTitle, **labelArgs)
		self.bTitleLabel.grid(column = 4, row = 0, sticky = N + S)
		
		self.bLabel = Label(self, textvariable = self.b, **labelArgs)
		self.bLabel.grid(column = 5, row = 0, sticky = N + S)
		
		self.columnconfigure(6, weight = 1, minsize = 20)
		
		
		# Deltas
		self.DeltasTitleLabel = Label(self, text = DeltasTitle, **labelArgs)
		self.DeltasTitleLabel.grid(column = 7, row = 0, sticky = N + S)
		
		self.DeltasLabel = Label(self, textvariable = self.Deltas, **labelArgs)
		self.DeltasLabel.grid(column = 8, row = 0, sticky = N + S)
		
		
		self.columnconfigure(9, weight = 1, minsize = 20)
		self.rowconfigure(0, weight = 1)
		
		
		self.onConstructionChanged()
	
	
	def updateTitle(self):
		self.title(
			"%s%sМатрицы%s" \
			% (self.application.name, self.application.nameDelim,
			   "" if self.barNumber is None else "%sСтержень (%d)" \
												 % (self.application.nameDelim, self.barNumber))
		)
	
	
	def onWindowDestroy(self, event):
		self.application.onWindowDestroy(self)
	
	
	def onConstructionChanged(self):
		if self.barNumber is not None \
			and self.barNumber not in range(0, self.application.logic.barsCount()):
			self.barNumber = 0
			self.updateTitle()
		
		m = self.application.logic.matrices(barNumber = self.barNumber)
		self.A.set(m[0])
		self.b.set(m[1])
		self.Deltas.set(m[2])
