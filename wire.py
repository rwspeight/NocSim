from math import tan
from math import sqrt
from math import cos
from math import sin
from math import degrees
from bisect import bisect
# http://networkx.readthedocs.org/en/stable/index.html
import networkx as nx
# http://matplotlib.org/1.5.1/contents.html
import matplotlib.pyplot as plt
import math

class Wire:
	
	def __init__(self, angle, x, y, length):
		self.angle = angle
		self.x = x
		self.y = y
		self.length = length		
		self.wire_end = self.get_wire_end_point()

		# We currently include the wire ends as nodes.  This could be a configuration param.
		self.nodes = [(x,y), self.wire_end]
		self.nodes.sort()

		
		# We define sorted wire ends to simplify intersection calculations		
		self.absolute_delta_x_to_end = abs(self.x - self.wire_end[0])

		self.x_interval = [self.x, self.wire_end[0]]
		self.x_interval.sort()

		self.y_interval = [self.y, self.wire_end[1]]
		self.y_interval.sort()		
		

	def get_intersection(self, wire):
		
		# There's no intersection if the wires are parallel
		if self.angle == wire.angle:
			return

		# Find the intersection of the infinite lines
		x = (wire.y - self.y + tan(self.angle) * self.x - tan(wire.angle) * wire.x) / (tan(self.angle) - tan(wire.angle))
		# The wires intersect if the distance between the wire start and
		# the intersection of the infinite lines is less than the distance
		# to from the wire start and the wire end.  We only have to check in
		# x due to the linear relationship. 
		#print "{0},{1},{2}".format(self.x, x, self.absolute_delta_x_to_end)
		#delta = round(abs(self.x - x), 9)
		#print "Separation distance {0}".format(delta)
		#print "{0} < {1} or {0} > {2}".format(x, self.x_interval[0], self.x_interval[1])
		if 	x < self.x_interval[0] or x > self.x_interval[1] \
			or x < wire.x_interval[0] or x > wire.x_interval[1]:
		#if delta > self.absolute_delta_x_to_end:
			#print "skipping"
			return

		y = tan(wire.angle) * x + wire.y - tan(wire.angle) * wire.x

		if 	y < self.y_interval[0] or y > self.y_interval[1] \
			or y < wire.y_interval[0] or y > wire.y_interval[1]:
			return

		return(x,y)

		# 
		#length_from_new = sqrt((x - self.x)**2 + (y - self.y)**2)
		#length_from_old = sqrt((x - wire.x)**2 + (y - wire.y)**2)

		#if length_from_new <= self.length and length_from_old <= wire.length:
		#	return (x, y)
		#else:
		#	return None

	def add_node(self, node):
		if node in self.nodes:
			return

		index = bisect(self.nodes, node)
		self.nodes.insert(index, node)
		return index

	def get_neighbor_nodes(self, node):
		if node not in self.nodes:
			return []

		index = self.nodes.index(node)
		neighbors = self.nodes[max(index - 1, 0):index + 2]
		
		neighbors.remove(node)
		return neighbors

	def get_distance_between(self, node1, node2):
		return sqrt((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)

	def __str__(self):
		return "XY:{0}/{1},Angle:{2} rads/{5} degrees,Length:{3},Slope{4}".format(self.x, self.y, self.angle, self.length, tan(self.angle), degrees(self.angle))

	def get_wire_end_point(self):
		x = cos(self.angle) * self.length
		y = sin(self.angle) * self.length
		end = (self.x + x, self.y + y)
		return end

class Helpers:

	def __init__(self):
		pass

	def graph_wires(self, wires):
		g2 = nx.Graph()
	
		for wire in wires:
			g2.add_edge((wire.x, wire.y), wire.get_wire_end_point())
		
		positions = {i: i for i in nx.nodes(g2)}
		#labels1 = {i: "{0}".format(i) for i in nx.nodes(g2)}
		
		nx.draw(g2, positions, ax=plt.subplot(121), node_size=10)
		return g2

	def generate_grid(self, rows, columns, length):
		w = [Wire(0, 0, row, length) for row in range(0, rows)]
		w = w + [Wire(math.pi / 2, column, 0, length) for column in range(0, columns)]
		return w




