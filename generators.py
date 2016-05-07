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

def get_uniform_length_generator(min_length, max_length = 0):
	delta = max_length - min_length

	while True:
		yield min_length + random() * delta

def get_exponential_decay_length_generator(min_length, max_length, base, time_constant, max_probability = 1):
	max_length = float(max_length)
	min_length = float(min_length)
	base = float(base)
	time_constant = float(time_constant)
	max_probability = float(max_probability)

	delta = max_length - min_length
	control_curve = lambda x: max_probability * pow(base, -x/max_length/time_constant)

	while True:
		length = random() * delta
		threshold = control_curve(length)
		if threshold <= random() * max_probability:
			yield min_length + length	

def get_distributions():
	yield ("uniform", get_uniform_length_generator)
	yield ("exponential", get_exponential_decay_length_generator)
	yield ("guassian", get_gaussian_length_distribution)

def get_gaussian_length_distribution(min_length, max_length, mean, stdev):
	mean = float(mean)
	stdev = float(stdev)
	max_length = float(max_length)
	min_length = float(min_length)
	delta = max_length - min_length
	control_curve = lambda x: exp(-(x-mean)**2/(2*stdev**2))

	while True:
		length = delta * random() + min_length
		threshold = control_curve(length)

		if threshold <= random():
			yield length



