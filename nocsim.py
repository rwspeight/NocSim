#!/usr/bin/python

import math
from math import tan
from random import random
from bisect import bisect
import networkx as nx

# http://matplotlib.org/1.5.1/contents.html
import matplotlib.pyplot as plt
from wire import Wire
from wire import Helpers


def generate(graph_size, wire_count, min_length, max_length):
	# Defines the equation for finding the point of intersection.
	target = wire_count
	count = 0
	limit = 1000
	wires = []
	size = graph_size
	g = nx.Graph()
	h = Helpers()

	#w = h.generate_grid(10, 10, 9)	

	#target = len(w) - 1
	while count <= target:
		count += 1
		angle = random() * 2 * math.pi	
		length = min_length + (random() * (max_length - min_length))
		x = random() * size
		y = random() * size
		
		new = Wire(angle, x, y, length)
		
		#new = w[count - 1]		
		wires.append(new)
		
		# Roll through each preexisting wire and check for intersection.
		
		
		for old in wires:
			

			if old == new:
				continue
			
			node = new.get_intersection(old)			
			
			if node != None:
				print "."*40
				print new
				print old
				print node

				g.add_node(node)
				new.add_node(node)
				old.add_node(node)
				
				# When two wires intersect there's a potential for zero to four nodes to be connected
				for neighbor in old.get_neighbor_nodes(node):
					
					g.add_edge(node, neighbor, length=new.get_distance_between(node, neighbor))		
				for neighbor in new.get_neighbor_nodes(node):
					
					g.add_edge(node, neighbor, length=new.get_distance_between(node, neighbor))		

	

	average_length = 0
	disconnect_count = 0
	largest_size = 0
	no_result = (0,0,0)
	large = None
	
	sub_graphs = list(nx.connected_component_subgraphs(g))
	
	if sub_graphs and len(sub_graphs) > 0:
		large = max(sub_graphs, key=len)

		if len(nx.nodes(large)) < 2:
			return no_result

		average_length = nx.average_shortest_path_length(large, weight="length")
		largest_size = nx.number_of_nodes(large)

		sub_graphs.remove(large)
		if len(sub_graphs) > 0:
			union = nx.union_all(sub_graphs)
			disconnect_count = nx.number_of_nodes(union)

	
	
	if large:
		g2 = h.graph_wires(wires)
		positions = {i: i for i in nx.nodes(g2)}
		nx.draw(large, {i: i for i in nx.nodes(large)}, ax=plt.subplot(122), node_size=30)
		plt.show()

	#plt.plot([a.x for a in wires], [a.y for a in wires], 'ro')
	#plt.show()
	return (average_length, disconnect_count, largest_size)


##################
min_count = 0 
max_count = 100
count_step = 1

min_length = 10
max_length = 15
length_step = 1

print "="*80
lengths = [l * length_step for l in range(min_length, max_length)]
counts = range(min_count, max_count, count_step)
#counts = range(900, 1000, 10)
grid_size = min_length * 2
print "wire count,average shortest path,disconnect count,largest graph"
#for length in lengths:
for count in counts:
	t = generate(grid_size, count, min_length, max_length)		
	#print "{0},{1},{2},{3}".format(count, *t[0:3])
	print "o"*10

print "="*80
