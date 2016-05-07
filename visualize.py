import networkx as nx
import matplotlib.pyplot as plt
import analyze as a
import statistics as s
from math import sqrt

def draw_noc(noc, axes = None, node_size = 10):
	draw_graph(noc.graph, axes, node_size)

def draw_graph(graph, axes = None, node_size = 10):
	if not axes:
		axes = plt.subplot(111);

	positions = {xy: xy for xy in nx.nodes(graph)}		
	nx.draw(graph, positions, ax=axes, node_size=node_size)
	

def show_noc_and_largest_graph(noc, node_size = 10):
	axes = plt.subplot(121)
	draw_noc(noc, axes, node_size)

	sub_graphs = a.get_sub_graphs(noc.graph)
	largest = a.get_largest_sub_graph(sub_graphs)
	if largest:
		axes = plt.subplot(122)
		draw_graph(largest, axes, node_size)	

	plt.show()	

def plot_disconnected_nodes_vs_wire_count(trials):
	fig = plt.figure()
	fig.suptitle('Disconnected Ratio vs Wire Count')
	plt.xlabel('Wire Count')
	plt.ylabel('Disconnected Nodes')

	xs = [r.wire_count for r in trials[0]]
	data_points = len(trials[0])
	data_points_root = sqrt(data_points)
	transpose = [ [t[n].disconnected_node_count for t in trials] for n in range(data_points)]
	means = [s.mean(x) for x in transpose]
	stdev = [s.stdev(x) for x in transpose]
	stderr = [x / data_points_root for x in stdev]

	plt.errorbar(xs, means, yerr=stderr, marker="o", color="black")
	
	#plt.plot(xs, ys, 'o')
	#plt.savefig('disconnected.png')
	plt.show()

def plot_largest_graph_vs_wire_count(trials):
	
	fig = plt.figure()
	fig.suptitle('Largest Graph Nodes vs Wire Count')
	plt.xlabel('Wire Count')
	plt.ylabel('Largest Graph Nodes')	

	for results in trials:
		xs = [r.wire_count for r in results]
		ys = [float(r.largest_graph_node_count) / max(1, r.wire_count) for r in results]

		plt.plot(xs, ys, 'o')	
	
	plt.savefig('largest.png')
	#plt.show()

def plot_average_shortest_path_vs_wire_count(trials):
	fig = plt.figure()
	fig.suptitle('Average Shortest Path vs Wire Count')
	plt.xlabel('Wire Count')
	plt.ylabel('Average Shortest Path')

	for results in trials:
		xs = [r.wire_count for r in results]
		ys = [float(r.average_shortest_path_length) for r in results]
		
		plt.plot(xs, ys, 'o')

	plt.savefig('shortest.png')
	#plt.show()
	