from noc import Noc
from wire import Wire

class WireFactory:

	def __init__(self, length_generator, position_generator, angle_generator):
		self.length_generator = length_generator
		self.position_generator = position_generator
		self.angle_generator = angle_generator

	def create(self):

		angle = self.angle_generator.next()
		position = self.position_generator.next()
		length = self.length_generator.next()	
		
		return Wire(angle, *position, length = length)

class NocFactory:
	def __init__(self, wire_factory):
		self.wire_factory = wire_factory

	def create(self, wire_count):				
		noc = Noc()
		
		for index in range(0, wire_count):
			noc.add_wire(self.wire_factory.create())

		return noc
			
			


