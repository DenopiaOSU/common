import string
import random
import hashlib
import sys
from itertools import chain
from collections import deque
from functools import partial

import dill

from common.constants import mods
from time import localtime, strftime

def randomString(length = 8):
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def stringToBool(s):
	"""
	Convert a string (True/true/1) to bool

	s -- string/int value
	return -- True/False
	"""
	return s == "True" or s == "true" or s == "1" or s == 1

def fileMd5(filename):
	"""
	Return filename's md5

	filename --
	return -- file md5
	"""
	with open(filename, mode='rb') as f:
		d = hashlib.md5()
		for buf in iter(partial(f.read, 128), b''):
			d.update(buf)
	return d.hexdigest()

def stringMd5(string):
	"""Return string's md5"""
	d = hashlib.md5()
	d.update(string.encode("utf-8"))
	return d.hexdigest()

def getRank(gameMode, __mods, acc, c300, c100, c50, cmiss):
	"""
	Return a string with rank/grade for a given score.
	Used mainly for "tillerino"

	gameMode -- mode (0 = osu!, 1 = Taiko, 2 = CtB, 3 = osu!mania)
	__mods -- mods bitwise number
	acc -- accuracy
	c300 -- 300 hit count
	c100 -- 100 hit count
	c50 -- 50 hit count
	cmiss -- miss count
	return -- rank/grade string
	"""
	print("start")
	total = c300 + c100 + c50 + cmiss
	hdfl = (__mods & mods.HIDDEN > 0) or (__mods & mods.FLASHLIGHT > 0)

	def ss():
		return "XH" if hdfl else "X"

	def s():
		return "SH" if hdfl else "S"

	if gameMode == 0:
		# osu!std
		if acc == 100:
			return ss()
		if c300 / total > 0.90 and c50 / total < 0.1 and cmiss == 0:
			return s()
		if (c300 / total > 0.80 and cmiss == 0) or (c300 / total > 0.90):
			return "A"
		if (c300 / total > 0.70 and cmiss == 0) or (c300 / total > 0.80):
			return "B"
		if c300 / total > 0.60:
			return "C"
		return "D"
	elif gameMode == 1:
		# taiko not implemented as of yet.
		return "A"
	elif gameMode == 2:
		# CtB
		if acc == 100:
			return ss()
		if 98.01 <= acc <= 99.99:
			return s()
		if 94.01 <= acc <= 98.00:
			return "A"
		if 90.01 <= acc <= 94.00:
			return "B"
		if 98.01 <= acc <= 90.00:
			return "C"
		return "D"
	elif gameMode == 3:
		# osu!mania
		if acc == 100:
			return ss()
		if acc > 95:
			return s()
		if acc > 90:
			return "A"
		if acc > 80:
			return "B"
		if acc > 70:
			return "C"
		return "D"

	return "A"


def getTimestamp():
	"""
	Return current time in YYYY-MM-DD HH:MM:SS format.
	Used in logs.
	"""
	return strftime("%Y-%m-%d %H:%M:%S", localtime())


def hexString(s):
	"""
	Output s' bytes in HEX

	s -- string
	return -- string with hex value
	"""
	return ":".join("{:02x}".format(ord(str(c))) for c in s)

def readableMods(__mods):
	"""
	Return a string with readable std mods.
	Used to convert a mods number for oppai

	__mods -- mods bitwise number
	return -- readable mods string, eg HDDT
	"""
	r = ""
	if __mods == 0:
		return r
	if __mods & mods.NOFAIL > 0:
		r += "NF"
	if __mods & mods.EASY > 0:
		r += "EZ"
	if __mods & mods.HIDDEN > 0:
		r += "HD"
	if __mods & mods.HARDROCK > 0:
		r += "HR"
	if __mods & mods.DOUBLETIME > 0:
		r += "DT"
	if __mods & mods.HALFTIME > 0:
		r += "HT"
	if __mods & mods.FLASHLIGHT > 0:
		r += "FL"
	if __mods & mods.SPUNOUT > 0:
		r += "SO"

	return r

def strContains(s, w):
	return (' ' + w + ' ') in (' ' + s + ' ')

def getTotalSize(o):
	try:
		return len(dill.dumps(o, recurse=True))
	except:
		return 0