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

def save_noc_image(noc, path, title=None):
	
	# Reset the global plot
	plt.clf()
	if not title:
		title = path

	draw_noc_and_largest_graph(noc, title=title)
	plt.savefig(path)	

def draw_noc_and_largest_graph(noc, node_size = 10, title=None):
	if title:
		fig = plt.figure()
		fig.suptitle(title)

	axes = plt.subplot(121)
	axes.set_title("All NoC Connected Graphs")
	draw_noc(noc, axes, node_size)

	axes = plt.subplot(122)
	axes.set_title("Largest NoC Connected Graph")
	sub_graphs = a.get_sub_graphs(noc.graph)
	largest = a.get_largest_sub_graph(sub_graphs)	
	if largest:		
		draw_graph(largest, axes, node_size)

def plot_disconnected_nodes_vs_wire_count(trials):
	fig = plt.figure()
	fig.suptitle('Disconnected Ratio vs Wire Count')
	plt.xlabel('Wire Count')
	plt.ylabel('Disconnected Nodes')

	xs = [r.wire_count for r in trials[0]]
	trial_count = len(trials)
	data_points = len(trials[0])

	#if not all()

	transpose = [ [t[n].disconnected_node_count for t in trials] for n in range(data_points)]
	means = [s.mean(x) for x in transpose]

	# There's a bug in errorbar() when called without fmt=None that
	# causes connecting lines to be drawn between data points.  This creates
	# a significant amount of visual noise.  The page below says it was
	# supposed to be fixed in 1.4 and higher, but this doesn't seem to be
	# the cases or I haven't configured the module import correctly.
	# An alternate solution is to draw the data points and the errorbars 
	# separately as is done below.  The error bars seems to be slightly off
	# center, but it's better than the alternative.
	# See:  http://stackoverflow.com/questions/18498742/how-do-you-make-an-errorbar-plot-in-matplotlib-using-linestyle-none-in-rcparams	
	plt.plot(xs, means, "ok")

	# Calculate the standard error for each x's seqence of 
	# y values.  There must be at least two data points or exceptions
	# are thrown.
	# See:  https://en.wikipedia.org/wiki/Standard_error	
	if trial_count >= 2:
		data_points_root = sqrt(trial_count)
		stdev = [s.stdev(x) for x in transpose]
		stderr = [x / data_points_root for x in stdev]
		plt.errorbar(xs, means, yerr=stderr, color="black", fmt=None)
	
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

def visualize(trials):
	plot_disconnected_nodes_vs_wire_count(trials)
	plot_largest_graph_vs_wire_count(trials)	
	plot_average_shortest_path_vs_wire_count(trials)
	