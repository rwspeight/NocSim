import networkx as nx
from wire import WireRegionIndex

class Noc:
	def __init__(self):
		self.wires = []
		self.graph = nx.Graph()
		self.wire_index = WireRegionIndex()
		self.edges = []

	def add_wire(self, new):
		self.wires.append(new)
		self.wire_index.add(new)

		# Roll through each preexisting wire and check for intersection.		
		for old in self.wire_index.get_neighbors(new):

			if old == new:
				continue
			
			node = new.get_intersection(old)			
			
			if node:
				#self.graph.add_node(node)
				new.add_node(node)
				old.add_node(node)
				
				# When two wires intersect there's a potential for zero to four nodes to be connected
				for neighbor in old.get_neighbor_nodes(node) + new.get_neighbor_nodes(node):
					self.edges.append((node, neighbor, {"length":new.get_distance_between(node, neighbor)}))
					#self.graph.add_edge(node, neighbor, length=new.get_distance_between(node, neighbor))		
					pass

	def create_graph(self):
		self.graph = nx.Graph()
		self.graph.add_edges_from(self.edges)



