#!/usr/bin/python
import factories as f
import generators as g
import visualize as v
import analyze as a
import math


##################
min_count = 100
max_count = 1000
count_step = 50
counts = range(min_count, max_count, count_step)
trials = 1
min_length = 5
max_length = 15
grid_size = max_length * 10

#lg = g.get_basic_length_generator(max_length, min_length)
lg = g.get_exponential_decay_length_generator(math.e, 2, max_length, min_length)
pg = g.get_uniform_position_generator(grid_size)
ag = g.get_uniform_angle_generator()
factory = f.NocFactory(f.WireFactory(lg, pg, ag))

results = []
for count in counts:	
	noc = factory.create(count)
	noc.create_graph()
		
	result = a.get_stats(noc)
	result.wire_count = count
	print result
	results.append(result)

	averages = a.AnalysisResult()
	results.append(averages)

#v.plot_disconnected_nodes_vs_wire_count(results)
#v.plot_largest_graph_vs_wire_count(results)	
v.plot_average_shortest_path_vs_wire_count(results)
	#averages.wire_count = count
	#averages.largest_graph_node_count = sum(t.largest_graph_node_count for t in trials) / len(trials)
	#averages.average_shortest_path_length = sum(t.average_shortest_path_length for t in trials) / len(trials)
	#averages.disconnected_node_count = sum(t.disconnected_node_count for t in trials) / len(trials)
	#averages.total_wire_length = sum(t.total_wire_length for t in trials) / len(trials)



# Concurrent features
# https://docs.python.org/dev/library/concurrent.futures.html