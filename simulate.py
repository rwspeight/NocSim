import factories as f
import generators as g
import visualize as v
import analyze as a
import math

def simulate(params):
	print params
	min_length = params.length_range[0]
	max_length = params.length_range[1]	
	grid_size = params.width[0]
	trials = params.trials[0]
	counts = range(params.wire_range[0], params.wire_range[1], params.step[0])

	#lg = g.get_basic_length_generator(max_length, min_length)
	lg = g.get_exponential_decay_length_generator(math.e, 2, max_length, min_length)
	pg = g.get_uniform_position_generator(grid_size)
	ag = g.get_uniform_angle_generator()
	factory = f.NocFactory(f.WireFactory(lg, pg, ag))

	trials = []
	for trial in range(0,5):
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
		trials.append(results)

	v.plot_disconnected_nodes_vs_wire_count(trials)
	v.plot_largest_graph_vs_wire_count(trials)	
	v.plot_average_shortest_path_vs_wire_count(trials)
		#averages.wire_count = count
		#averages.largest_graph_node_count = sum(t.largest_graph_node_count for t in trials) / len(trials)
		#averages.average_shortest_path_length = sum(t.average_shortest_path_length for t in trials) / len(trials)
		#averages.disconnected_node_count = sum(t.disconnected_node_count for t in trials) / len(trials)
		#averages.total_wire_length = sum(t.total_wire_length for t in trials) / len(trials)



	# Concurrent features
	# https://docs.python.org/dev/library/concurrent.futures.html