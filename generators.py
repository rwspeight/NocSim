from math import pi
from math import exp
from random import random

def get_uniform_angle_generator(max_angle = 2 * pi):
	while True:
		yield random() * max_angle

def get_uniform_position_generator(max_x, max_y = None):
	if max_y == None:
		max_y = max_x

	while True:
		yield (random() * max_x, random() * max_y)

def get_uniform_length_generator(max_length, min_length = 0):
	delta = max_length - min_length

	while True:
		yield min_length + random() * delta

def get_exponential_decay_length_generator(base, time_constant, max_length, min_length = 0, max_probability = 1):
	delta = max_length - min_length
	control_curve = lambda x: max_probability * pow(base, -x/max_length/time_constant)

	while True:
		length = random() * delta
		threshold = control_curve(length)
		if threshold <= random():
			yield min_length + length	
