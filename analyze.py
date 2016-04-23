import networkx as nx

def get_largest_sub_graph(graph):
	average_length = 0
	disconnect_count = 0
	largest_size = 0
	no_result = (0,0,0)
	
	
	sub_graphs = list(nx.connected_component_subgraphs(graph))
	
	if sub_graphs and len(sub_graphs) > 0:
		largest = max(sub_graphs, key=len)

		if len(nx.nodes(largest)) >= 2:
			return largest

def get_average_shortest_path(graph):
	return nx.average_shortest_path_length(large, weight="length")

def get_disconnected_nodes(graph, prime_sub_graph):
	sub_graphs = list(nx.connected_component_subgraphs(graph))

	if prime_sub_graph in sub_graphs:
		sub_graphs.remove(large)

	if len(sub_graphs) > 0:
		return nx.union_all(sub_graphs)	
	
	if large:
		g2 = h.graph_wires(wires)
		positions = {i: i for i in nx.nodes(g2)}
		nx.draw(large, {i: i for i in nx.nodes(large)}, ax=plt.subplot(122), node_size=30)
		plt.show()