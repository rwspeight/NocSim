from noc import Noc
from wire import Wire

class WireFactory:

	def __init__(self, length_generator, position_generator, angle_generator):
		self.length_generator = length_generator
		self.position_generator = position_generator
		self.angle_generator = angle_generator

	def create(self):

		angle = next(self.angle_generator)
		position = next(self.position_generator)
		length = next(self.length_generator)
		
		return Wire(angle, *position, length = length)

class NocFactory:
	def __init__(self, wire_factory, before_add=None, after_add=None):
		self.wire_factory = wire_factory
		self.before_add = before_add
		self.after_add = after_add

	def create(self, wire_count):				
		noc = Noc()

		
		for index in range(0, wire_count):
			wire = self.wire_factory.create()

			# Allow the caller to control the wire add process, if desired.
			if callable(self.before_add):
				skip = self.before_add(noc, wire, index)
				if skip:
					continue
				
			noc.add_wire(wire)

			# Allow the caller to 
			if callable(self.after_add):
				exit = self.after_add(noc, wire, index)
				if exit:
					break

		return noc
			
			


