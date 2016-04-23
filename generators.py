from math import pi
from random import random

def get_basic_angle_generator(max_angle = 2 * pi):
	while True:
		yield random() * max_angle

def get_basic_position_generator(max_x, max_y):	
	while True:
		yield (random() * max_x, random() * max_y)

def get_basic_length_generator(max_length, min_length = 0):
	delta = max_length - min_length

	while True:
		yield min_length + random() * delta
