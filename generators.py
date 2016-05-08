from math import pi
from math import exp
from math import log
from random import random

def get_uniform_angle_generator(max_angle = 2 * pi):
	while True:
		yield random() * max_angle

def get_uniform_position_generator(max_x, max_y = None):
	if max_y == None:
		max_y = max_x

	while True:
		yield (random() * max_x, random() * max_y)

def get_uniform_length_generator(min_length, max_length):
	delta = max_length - min_length

	while True:
		yield min_length + random() * delta

def get_exponential_decay_length_generator(min_length, max_length, base, time_constant):
	# Ensure the passed parameters are the correct types
	max_length = float(max_length)
	min_length = float(min_length)
	base = float(base)
	time_constant = float(time_constant)

	# We calculate the length interval so as to map it 
	# to the interval between 0 and the x point corresponding
	# to 0.5% of the passed power parameters.
	control_curve = lambda x: pow(base, -x/time_constant)
	max_x = -time_constant * log(0.005)/log(base)
	conversion = (max_length - min_length) / max_x

	while True:
		x = random() * max_x
		if random() <= control_curve(x):
			yield x * conversion + min_length

def get_distributions():
	yield ("uniform", get_uniform_length_generator)
	yield ("exponential", get_exponential_decay_length_generator)
	yield ("gaussian", get_gaussian_length_distribution)

def get_gaussian_length_distribution(min_length, max_length, mean, stdev):
	mean = float(mean)
	stdev = float(stdev)
	max_length = float(max_length)
	min_length = float(min_length)
	delta = max_length - min_length
	control_curve = lambda x: exp(-(x-mean)**2/(2*stdev**2))

	while True:
		length = delta * random() + min_length
		
		if random() <= control_curve(length):
			yield length



