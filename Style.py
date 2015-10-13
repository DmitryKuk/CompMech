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

XColor					= coordinateAxisColor
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

# Вспомогательные оси
XAxisStyle				= { "fill": XColor,		"dash": (3, 5) }
NAxisStyle				= { "fill": NColor,		"dash": (3, 5) }
UAxisStyle				= { "fill": UColor,		"dash": (3, 5) }
SigmaAxisStyle			= { "fill": SigmaColor,	"dash": (3, 5) }

# Подписи к основным и вспомогательным осям
labelFormat				= "%.3f"

XLabelStyle				= { "fill": XColor }
NLabelStyle				= { "fill": NColor }
ULabelStyle				= { "fill": UColor }
SigmaLabelStyle			= { "fill": SigmaColor }

XLabelOffset			= ( 20, 20)
NLabelOffset			= (-25, 10)
ULabelOffset			= ( 20, 10)
SigmaLabelOffset		= ( 65, 10)


# Макс. компонента / высоту конструкции (макс. нагрузка <=> 80% высоты конструкции)
componentOnHeight		= 0.8


# Фон полей со значениями по умолчанию в редакторе
defaultValueBG			= "#F1F1F1"
