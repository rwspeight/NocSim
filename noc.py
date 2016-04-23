import networkx as nx

class Noc:
	def __init__(self):
		self.wires = []
		self.graph = nx.Graph()

	def add_wire(self, new):
		self.wires.append(new)

		# Roll through each preexisting wire and check for intersection.		
		for old in self.wires:

			if old == new:
				continue
			
			node = new.get_intersection(old)			
			
			if node != None:
				self.graph.add_node(node)
				new.add_node(node)
				old.add_node(node)
				
				# When two wires intersect there's a potential for zero to four nodes to be connected
				for neighbor in old.get_neighbor_nodes(node):					
					self.graph.add_edge(node, neighbor, length=new.get_distance_between(node, neighbor))		
				
				for neighbor in new.get_neighbor_nodes(node):					
					self.graph.add_edge(node, neighbor, length=new.get_distance_between(node, neighbor))		


