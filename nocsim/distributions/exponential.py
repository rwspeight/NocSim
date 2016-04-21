from random import random
from math import exp

class Decay:

	curveScalar = 0
	maxWireLength = 0

	def __init__(self, maxWireLength, curveScalar = 5):
		self.curveScalar = curveScalar
		self.maxWireLength = maxWireLength

	def curveEquation(self, x):
		return self.maxWireLength * exp(-x / (self.maxWireLength / self.curveScalar))

	def isAboveControl(self, length):
		return self.curveEquation(length) <= random() * self.maxWireLength



