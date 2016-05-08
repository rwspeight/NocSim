import factories as f
import generators as g
import visualize as v
import analyze as a
import math
import inout as io

def simulate(params):

	# Get the selected distribution
	dist = dict(g.get_distributions())[params.distribution]		
	wire_drop_counts = range(params.wire_range[0], params.wire_range[1], params.step)

	#lg = g.get_exponential_decay_length_generator(math.e, 2, max_length, min_length)
	lengths = dist( *(params.length_range + params.distribution_parameters) )
	positions = g.get_uniform_position_generator(params.grid_width)
	angles = g.get_uniform_angle_generator()
	factory = f.NocFactory(f.WireFactory(lengths, positions, angles))

	trials = []
	for trial in range(0, params.trials):
		results = []

		for drop_count in wire_drop_counts:	
			noc = factory.create(drop_count)
			noc.create_graph()
				
			result = a.get_stats(noc, drop_count, trial)
			results.append(result)

		trials.append(results)


	# Save results if requested
	if params.output_file != None:
		for trial in trials:
			io.export_to_csv(trial, params.output_file, mode="a+")

	# Display the results
	if params.visualize:
		v.visualize(trials)