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
	def __init__(self, wire_factory):
		self.wire_factory = wire_factory

	def create(self, wire_count):				
		noc = Noc()
		
		for index in range(0, wire_count):
			noc.add_wire(self.wire_factory.create())

		return noc
			
			


