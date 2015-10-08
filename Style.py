#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)

from tkinter import *


# Цвета элементов на графике
barColor				= "yellow"
activeBarColor			= "orange"
nodeColor				= "green"

coordinateAxisColor		= "blue"
FColor					= "red"
qColor					= "green"

NColor					= "red"
UColor					= "green"
SigmaColor				= "blue"


# Стили элементов
barStyle				= { "fill": barColor, "activefill": activeBarColor }
qLineStyle				= { "fill": qColor, "width": 5,
							"arrow": FIRST, "arrowshape": (5, 12, 13) }

NLineStyle				= { "fill": NColor }
ULineStyle				= { "fill": UColor }
SigmaLineStyle			= { "fill": SigmaColor }
SigmaMaxLineStyle		= { "fill": SigmaColor, "dash": (10, 10) }

nodeAxisStyle			= { "fill": nodeColor, "dash": (3, 3) }
FLineStyle				= { "fill": FColor, "width": 11,
							"arrow": LAST, "arrowshape": (5, 12, 13) }
hatchStyle				= {}

coordinateAxisStyle		= { "fill": coordinateAxisColor, "dash": (7, 7),
							"arrow": LAST}

XAxisStyle				= { "fill": coordinateAxisColor,	"dash": (3, 5) }
NAxisStyle				= { "fill": NColor,					"dash": (3, 5) }
UAxisStyle				= { "fill": UColor,					"dash": (3, 5) }
SigmaAxisStyle			= { "fill": SigmaColor,				"dash": (3, 5) }


# Макс. компонента / высоту конструкции (макс. нагрузка <=> 70% высоты конструкции)
componentOnHeight		= 0.8
