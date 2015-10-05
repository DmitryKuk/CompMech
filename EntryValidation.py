#!/usr/bin/env python3

# Author: Dmitry Kukovinets (d1021976@gmail.com)


def validateInt(s):
	try:
		int(s)
		return True
	except ValueError:
		return False


def validateFloat(s):
	try:
		float(s)
		return True
	except ValueError:
		return False
