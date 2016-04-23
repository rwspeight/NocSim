#!/usr/bin/python
import factories as f
import generators as g
import visualize as v


##################
min_count = 100
max_count = 300
count_step = 10
counts = range(min_count, max_count, count_step)

min_length = 10
max_length = 15
grid_size = min_length * 10

lg = g.get_basic_length_generator(max_length, min_length)
pg = g.get_basic_position_generator(max_x = grid_size, max_y = grid_size)
ag = g.get_basic_angle_generator()
factory = f.NocFactory(f.WireFactory(lg, pg, ag))

for count in counts:
	noc = factory.create(count)
	v.show_noc_and_largest_graph(noc)
	


