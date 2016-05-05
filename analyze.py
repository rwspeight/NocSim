import networkx as nx

def get_largest_sub_graph(sub_graphs):
	
	if sub_graphs and len(sub_graphs) > 0:
		largest = max(sub_graphs, key=len)

		if len(nx.nodes(largest)) >= 2:
			return largest

def get_average_shortest_path(graph):
	return nx.average_shortest_path_length(graph, weight="length")

def get_sub_graphs(graph):
	return list(nx.connected_component_subgraphs(graph))

def get_disconnected_node_count(prime_graph, sub_graphs):	

	if prime_graph and prime_graph in sub_graphs:
		sub_graphs.remove(prime_graph)

	return sum([nx.number_of_nodes(n) for n in sub_graphs])

def get_stats(noc):
	result = AnalysisResult()
	result.wire_count = len(noc.wires)

	sub_graphs = get_sub_graphs(noc.graph)
	largest = get_largest_sub_graph(sub_graphs)
	
	asp = 0
	largest_size = 0
	if largest:
		result.average_shortest_path_length = get_average_shortest_path(largest)
		result.largest_graph_node_count = nx.number_of_nodes(largest)

	
	result.disconnected_node_count = get_disconnected_node_count(largest, sub_graphs)
	result.total_wire_length = sum(e[2]["length"] for e in noc.edges)
	print result
	return result

class AnalysisResult:
	def __init__(self):
		self.wire_count = 0
		self.largest_graph_node_count = 0
		self.average_shortest_path_length = 0
		self.disconnected_node_count = 0
		self.total_wire_length = 0		

	def __str__(self):
		return self.to_csv()

	def to_csv(self):		
		return "{0},{1},{2},{3},{4}".format(
			self.wire_count,
			self.largest_graph_node_count,
			self.average_shortest_path_length,
			self.disconnected_node_count,
			self.total_wire_length)	

	def from_csv(self, line):
		values = line.split(",")

		self.wire_count = values[0]
		self.largest_graph_node_count = values[1]
		self.average_shortest_path_length = values[2]
		self.disconnected_node_count = values[3]
		self.total_wire_length = values[4]

