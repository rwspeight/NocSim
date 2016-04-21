#!/usr/bin/python

import math
from math import tan
from random import random
from bisect import bisect
import networkx as nx
import matplotlib.pyplot as plt


def generate(graph_size, wire_count, max_wire_length):
	# Defines the equation for finding the point of intersection.
	get_x_intercept = lambda theta1, theta2, x1, x2, y1, y2: (y2 - y1 + tan(theta1)*x1 - tan(theta2)*x2) / (tan(theta1) - tan(theta2))
	get_y_intercept = lambda theta, x, x1, y1: tan(theta)*(x - x1) + y1

	max_length = max_wire_length
	target = wire_count
	count = 0
	limit = 1000
	wires = []
	size = graph_size
	g = nx.Graph()

	while count < target:
		count += 1
		a1 = random() * 2 * math.pi	
		l1 = random()*max_wire_length
		new = (a1, random()*size, random()*size, l1, [])
		node = ()
		
		for old in wires:

			x = get_x_intercept(new[0], old[0], new[1], old[1], new[2], old[2])
			y = get_y_intercept(new[0], x, new[1], new[2])

			length_from_new = math.sqrt((x-new[1])**2 + (y-new[2])**2)
			length_from_old = math.sqrt((x-old[1])**2 + (y-old[2])**2)
			
			if length_from_new <= new[3] and length_from_old <= old[3]:
				
				node = (x,y)
				g.add_node(node)
				#g.add_edge(new, old, length=new[3])
				#g.set_node_attributes(new, {"positions": (x,y)})

				#~ add node to new wire (will need to redefine wire based on this)
				index = bisect(new[4], node)
				new[4].insert(index, node)

				#~ get old wires node list
				oldNodes = old[4]

				#~ bisect node list on x values (only need to x as y function of x)
				index = bisect(oldNodes, node)			

				#~ insert node at bisect index on old wire
				oldNodes.insert(index, node)

				#~ if index-1 exists, get node and add edge between nodes
				if index + 1 <= len(oldNodes) - 1:
					g.add_edge(node, oldNodes[index + 1])

				#~ if index+1 exists, get node and add edge between node_positions
				if index - 1 <= len(oldNodes) - 1:
					g.add_edge(node, oldNodes[index - 1])


				

		wires.append(new)

	average_length = 0
	#nx.draw(g)
	
	sub_graphs = list(nx.connected_component_subgraphs(g))
	
	if sub_graphs and len(sub_graphs) > 0:
		large = max(sub_graphs, key=len)

		if len(nx.nodes(large)) < 2:
			return 0

	#	node_positions = {}
	#	for node in nx.nodes(large):
	#		node_positions[node] = node

		#nx.draw_networkx_nodes(large, node_positions)
		#nx.draw_networkx_edges(large, node_positions)
		#print len(wires)

		average_length = nx.average_shortest_path_length(large)
		#nx.draw(large)
		#plt.show()
		
	#plt.show()

	return average_length

grid_size = 5
min_count = 50
max_count = 80
steps = 600
interval = 1/10.0
for length in [l * interval for l in range(0, 30)]:
	for count in range(min_count, max_count):
		print "{0},{1},{2}".format(length, 10*count, generate(grid_size, count, length))
		pass
pass