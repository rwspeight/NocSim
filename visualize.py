import networkx as nx
import matplotlib.pyplot as plt
import analyze as a

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

	largest = a.get_largest_sub_graph(noc.graph)
	if largest:
		axes = plt.subplot(122)
		draw_graph(largest, axes, node_size)	

	plt.show()	
