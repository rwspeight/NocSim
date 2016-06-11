import networkx as nx
import matplotlib.pyplot as plt
import analyze as a
import statistics as s
from math import sqrt
import matplotlib.animation as animation

def draw_noc(noc, axes = None, node_size = 10):
	draw_graph(noc.graph, axes, node_size)

def draw_graph(graph, axes = None, node_size = 10):
	if not axes:
		axes = plt.subplot(111);

	positions = {xy: xy for xy in nx.nodes(graph)}		
	nx.draw(graph, positions, ax=axes, node_size=node_size)

def save_noc_image(noc, path, title=None):
	
	# Reset the global plot
	plt.close()
	if not title:
		title = path

	draw_noc_and_largest_graph(noc, title=title)
	plt.savefig(path)
	plt.close()

def draw_noc_and_largest_graph(noc, node_size = 10, title=None):
	if title:
		fig = plt.figure()
		fig.suptitle(title)

	axes = plt.subplot(121)
	axes.set_title("All NoC Connected Graphs")
	draw_noc(noc, axes, node_size)

	axes = plt.subplot(122)
	axes.set_title("Largest NoC Connected Graph")
	sub_graphs = a.get_sub_graphs(noc.graph)
	largest = a.get_largest_sub_graph(sub_graphs)	
	if largest:		
		draw_graph(largest, axes, node_size)

def plot_data(criteria):
	c = criteria
	get_figure = lambda: plt.figure()
	set_super_title = lambda f: f.suptitle("")
	get_x_axis = lambda: plt.subplot(111).get_xaxis()
	set_x_axis_label = lambda axis: None

	get_y_axis = lambda: plt.subplot(111).get_yaxis()
	set_y_axis_label = lambda axis: None

	get_x_values = lambda: []
	get_y_values = lambda: []
	plot_values = lambda xs, ys, format: plt.plot(xs, ys, format)
	get_plot_format = lambda: "ok"
	get_errorbar_data = lambda: []
	plot_errorbars = lambda xs, ys, error: plt.errorbar(xs, ys, yerr=error, color="black", fmt=None)
	present_plot = lambda: plt.show()

	figure = try_to_call(c.get_figure).then(get_figure).go()
	try_to_call(c.set_super_title, figure).then(set_super_title, figure).go()
	
	x_axis = try_to_call(c.get_x_axis).then(get_x_axis).go()
	try_to_call(c.set_x_axis_label, x_axis).then(set_x_axis_label, x_axis).go()

	y_axis = try_to_call(c.get_y_axis).then(get_y_axis).go()
	try_to_call(c.set_y_axis_label, y_axis).then(set_y_axis_label, y_axis).go()
	
	xs = try_to_call(c.get_x_values).then(get_x_values).go()
	ys = try_to_call(c.get_y_values).then(get_y_values).go()

	format = try_to_call(c.get_plot_format).then(get_plot_format).go()
	try_to_call(c.plot_values, xs, ys, format).then(plot_values, xs, ys, format).go()
	
	error = try_to_call(c.get_errorbar_data).then(get_errorbar_data).go()
	try_to_call(c.plot_errorbars, xs, ys, error).then(plot_errorbars, xs, ys, error).go()

	try_to_call(c.present_plot).then(present_plot).go()


def test(trials):
	c = PlotCriteria()
	c.set_super_title = lambda fig: fig.suptitle('Disconnected Ratio vs Wire Count')
	c.set_x_axis_label = lambda axis: axis.label.set_text('Wire Count')
	c.set_y_axis_label = lambda axis: axis.label.set_text('Disconnected Nodes')
	c.get_x_values = lambda: [r.wire_count for r in trials[0]]
	
	data_points = len(trials[0])
	transpose = [ [t[n].disconnected_node_count for t in trials] for n in range(data_points)]
	
	ys = [s.mean(x) for x in transpose]
	print([r.wire_count for r in trials[0]])
	c.get_y_values = lambda: ys
	
	trial_count = len(trials)
	if trial_count >= 2:
		data_points_root = sqrt(trial_count)
		stdev = [s.stdev(x) for x in transpose]
		stderr = [x / data_points_root for x in stdev]
		c.get_errorbar_data = lambda: stderr		

	plot_data(c)

class PlotCriteria:
	def __init__(self):
		self.get_figure = None
		self.set_super_title  = None
		self.get_x_axis = None
		self.set_x_axis_label = None
		self.get_y_axis = None
		self.set_y_axis_label = None
		self.get_x_values = None
		self.get_y_values = None
		self.get_plot_format = None
		self.plot_values = None
		self.get_errorbar_data = None
		self.plot_errorbars = None
		self.present_plot = None

def try_to_call(callee, *args):
	class ChainExecution:
		def __init__(self, callee, *args):
			self.value = None
			self.success = False
			self._do_work(callee, *args)

		def _do_work(self, callee, *args):
			if callable(callee):
				self.value = callee(*args)
				self.called = True

		def then(self, callee, *args):
			# If the last callee was not callable 
			# try the next one, otherwise pass forward
			# self holding the value returned form the callee
			if not self.success:
				self._do_work(callee, *args)

			return self

		def go(self):
			return self.value

	return ChainExecution(callee, *args)

def plot_disconnected_nodes_vs_wire_count(trials):
	fig = plt.figure()
	fig.suptitle('Disconnected Ratio vs Wire Count')
	plt.xlabel('Wire Count')
	plt.ylabel('Disconnected Nodes')

	xs = [r.wire_count for r in trials[0]]
	trial_count = len(trials)
	data_points = len(trials[0])

	#if not all()

	transpose = [ [t[n].disconnected_node_count for t in trials] for n in range(data_points)]
	means = [s.mean(x) for x in transpose]

	# There's a bug in errorbar() when called without fmt=None that
	# causes connecting lines to be drawn between data points.  This creates
	# a significant amount of visual noise.  The page below says it was
	# supposed to be fixed in 1.4 and higher, but this doesn't seem to be
	# the cases or I haven't configured the module import correctly.
	# An alternate solution is to draw the data points and the errorbars 
	# separately as is done below.  The error bars seems to be slightly off
	# center, but it's better than the alternative.
	# See:  http://stackoverflow.com/questions/18498742/how-do-you-make-an-errorbar-plot-in-matplotlib-using-linestyle-none-in-rcparams	
	plt.plot(xs, means, "ok")

	# Calculate the standard error for each x's seqence of 
	# y values.  There must be at least two data points or exceptions
	# are thrown.
	# See:  https://en.wikipedia.org/wiki/Standard_error	
	if trial_count >= 2:
		data_points_root = sqrt(trial_count)
		stdev = [s.stdev(x) for x in transpose]
		stderr = [x / data_points_root for x in stdev]
		plt.errorbar(xs, means, yerr=stderr, color="black", fmt=None)
	
	#plt.plot(xs, ys, 'o')
	#plt.savefig('disconnected.png')
	plt.show()

def plot_connectivity_ratio(trials):
	fig = plt.figure()
	fig.suptitle('Connectivity Ratio')
	plt.xlabel('Wire Count')
	plt.ylabel('Connectivity Ratio (largest graph node count / disconnected node count) Nodes')

	xs = [r.wire_count for r in trials[0]]
	trial_count = len(trials)
	data_points = len(trials[0])

	#if not all()

	transpose = [ [t[n].largest_graph_node_count / max(1, t[n].disconnected_node_count) for t in trials] for n in range(data_points)]
	means = [s.mean(x) for x in transpose]

	# There's a bug in errorbar() when called without fmt=None that
	# causes connecting lines to be drawn between data points.  This creates
	# a significant amount of visual noise.  The page below says it was
	# supposed to be fixed in 1.4 and higher, but this doesn't seem to be
	# the cases or I haven't configured the module import correctly.
	# An alternate solution is to draw the data points and the errorbars 
	# separately as is done below.  The error bars seems to be slightly off
	# center, but it's better than the alternative.
	# See:  http://stackoverflow.com/questions/18498742/how-do-you-make-an-errorbar-plot-in-matplotlib-using-linestyle-none-in-rcparams	
	plt.plot(xs, means, "ok")

	# Calculate the standard error for each x's seqence of 
	# y values.  There must be at least two data points or exceptions
	# are thrown.
	# See:  https://en.wikipedia.org/wiki/Standard_error	
	if trial_count >= 2:
		data_points_root = sqrt(trial_count)
		stdev = [s.stdev(x) for x in transpose]
		stderr = [x / data_points_root for x in stdev]
		plt.errorbar(xs, means, yerr=stderr, color="black", fmt=None)
	
	#plt.plot(xs, ys, 'o')
	#plt.savefig('disconnected.png')
	plt.show()	

def coplot_largest_graph_and_disconnected_nodes(trials):
	fig = plt.figure()
	plot = plt.subplot()
	fig.suptitle('Connected & Disconnected Nodes vs. Wire Count')
	plt.xlabel('Wire Count')
	plt.ylabel('Largest graph Node Count')

	xs = [r.wire_count for r in trials[0]]
	trial_count = len(trials)
	data_points = len(trials[0])

	#if not all()

	large_set = [ [t[n].largest_graph_node_count for t in trials] for n in range(data_points)]
	largest = [s.mean(x) for x in large_set]

	discon_set = [ [t[n].disconnected_node_count for t in trials] for n in range(data_points)]
	disconnected = [s.mean(y) for y in discon_set]

	# There's a bug in errorbar() when called without fmt=None that
	# causes connecting lines to be drawn between data points.  This creates
	# a significant amount of visual noise.  The page below says it was
	# supposed to be fixed in 1.4 and higher, but this doesn't seem to be
	# the cases or I haven't configured the module import correctly.
	# An alternate solution is to draw the data points and the errorbars 
	# separately as is done below.  The error bars seems to be slightly off
	# center, but it's better than the alternative.
	# See:  http://stackoverflow.com/questions/18498742/how-do-you-make-an-errorbar-plot-in-matplotlib-using-linestyle-none-in-rcparams	
	
	h1, = plot.plot(xs, largest, "ok", label="Largest")
	

	# Calculate the standard error for each x's seqence of 
	# y values.  There must be at least two data points or exceptions
	# are thrown.
	# See:  https://en.wikipedia.org/wiki/Standard_error	
	if trial_count >= 2:
		data_points_root = sqrt(trial_count)
		stdev = [s.stdev(value) for value in large_set]
		stderr = [x / data_points_root for x in stdev]
		plt.errorbar(xs, largest, yerr=stderr, color="black", fmt=None)
	
	twin = plot.twinx()
	twin.yaxis.label.set_text('Disconnected Node Count')
	h2, = twin.plot(xs, disconnected, "*r", label="Disconnected")
	plt.legend(handles=[h1,h2])

	if trial_count >= 2:
		data_points_root = sqrt(trial_count)
		stdev = [s.stdev(value) for value in discon_set]
		stderr = [x / data_points_root for x in stdev]
		plt.errorbar(xs, disconnected, yerr=stderr, color="black", fmt=None)

	#plt.plot(xs, ys, 'o')
	plt.savefig('connected_vs_disconnected.png')
	#plt.show()		

def coplot_shortest_average_path_and_total_wire_length(trials):
	fig = plt.figure()
	plot = plt.subplot()
	fig.suptitle('Shortest Average Path & Total Wire Length vs. Wire Count')
	plt.xlabel('Wire Count')
	plt.ylabel('Shortest Average Path (units)')

	xs = [r.wire_count for r in trials[0]]
	trial_count = len(trials)
	data_points = len(trials[0])

	#if not all()

	large_set = [ [t[n].average_shortest_path_length for t in trials] for n in range(data_points)]
	largest = [s.mean(x) for x in large_set]

	discon_set = [ [t[n].total_wire_length for t in trials] for n in range(data_points)]
	disconnected = [s.mean(y) for y in discon_set]

	# There's a bug in errorbar() when called without fmt=None that
	# causes connecting lines to be drawn between data points.  This creates
	# a significant amount of visual noise.  The page below says it was
	# supposed to be fixed in 1.4 and higher, but this doesn't seem to be
	# the cases or I haven't configured the module import correctly.
	# An alternate solution is to draw the data points and the errorbars 
	# separately as is done below.  The error bars seems to be slightly off
	# center, but it's better than the alternative.
	# See:  http://stackoverflow.com/questions/18498742/how-do-you-make-an-errorbar-plot-in-matplotlib-using-linestyle-none-in-rcparams	
	
	h1, = plot.plot(xs, largest, "ok", label="Shortest")
	

	# Calculate the standard error for each x's seqence of 
	# y values.  There must be at least two data points or exceptions
	# are thrown.
	# See:  https://en.wikipedia.org/wiki/Standard_error	
	if trial_count >= 2:
		data_points_root = sqrt(trial_count)
		stdev = [s.stdev(value) for value in large_set]
		stderr = [x / data_points_root for x in stdev]
		plt.errorbar(xs, largest, yerr=stderr, color="black", fmt=None)
	
	twin = plot.twinx()
	twin.yaxis.label.set_text('Total Wire Length (units)')
	h2, = twin.plot(xs, disconnected, "*r", label="Total")
	plt.legend(handles=[h1,h2])

	if trial_count >= 2:
		data_points_root = sqrt(trial_count)
		stdev = [s.stdev(value) for value in discon_set]
		stderr = [x / data_points_root for x in stdev]
		plt.errorbar(xs, disconnected, yerr=stderr, color="black", fmt=None)

	#plt.plot(xs, ys, 'o')
	plt.savefig('shortest_vs_total.png')
	plt.show()		

def coplot_node_density_and_total_wire_length(trials):
	fig = plt.figure()
	plot = plt.subplot()
	fig.suptitle('Node Density & Total Wire Length vs. Wire Count')
	plt.xlabel('Wire Count')
	plt.ylabel('Node Density (node/unit^2)')

	xs = [r.wire_count for r in trials[0]]
	trial_count = len(trials)
	data_points = len(trials[0])

	#if not all()

	large_set = [ [t[n].average_shortest_path_length / 60 for t in trials] for n in range(data_points)]
	largest = [s.mean(x) for x in large_set]

	discon_set = [ [t[n].total_wire_length for t in trials] for n in range(data_points)]
	disconnected = [s.mean(y) for y in discon_set]

	# There's a bug in errorbar() when called without fmt=None that
	# causes connecting lines to be drawn between data points.  This creates
	# a significant amount of visual noise.  The page below says it was
	# supposed to be fixed in 1.4 and higher, but this doesn't seem to be
	# the cases or I haven't configured the module import correctly.
	# An alternate solution is to draw the data points and the errorbars 
	# separately as is done below.  The error bars seems to be slightly off
	# center, but it's better than the alternative.
	# See:  http://stackoverflow.com/questions/18498742/how-do-you-make-an-errorbar-plot-in-matplotlib-using-linestyle-none-in-rcparams	
	
	h1, = plot.plot(xs, largest, "ok", label="Density")
	

	# Calculate the standard error for each x's seqence of 
	# y values.  There must be at least two data points or exceptions
	# are thrown.
	# See:  https://en.wikipedia.org/wiki/Standard_error	
	if trial_count >= 2:
		data_points_root = sqrt(trial_count)
		stdev = [s.stdev(value) for value in large_set]
		stderr = [x / data_points_root for x in stdev]
		plt.errorbar(xs, largest, yerr=stderr, color="black", fmt=None)
	
	twin = plot.twinx()
	twin.yaxis.label.set_text('Total Wire Length (units)')
	h2, = twin.plot(xs, disconnected, "*r", label="Total")
	plt.legend(handles=[h1,h2])

	if trial_count >= 2:
		data_points_root = sqrt(trial_count)
		stdev = [s.stdev(value) for value in discon_set]
		stderr = [x / data_points_root for x in stdev]
		plt.errorbar(xs, disconnected, yerr=stderr, color="black", fmt=None)

	#plt.plot(xs, ys, 'o')
	plt.savefig('density_vs_total.png')
	plt.show()		

def plot_largest_graph_vs_wire_count(trials):
	
	fig = plt.figure()
	fig.suptitle('Largest Graph Nodes vs Wire Count')
	plt.xlabel('Wire Count')
	plt.ylabel('Largest Graph Nodes')	

	for results in trials:
		xs = [r.wire_count for r in results]
		ys = [float(r.largest_graph_node_count) / max(1, r.wire_count) for r in results]

		plt.plot(xs, ys, 'o')	
	
	plt.savefig('largest.png')
	plt.show()

def plot_average_shortest_path_vs_wire_count(trials):
	fig = plt.figure()
	fig.suptitle('Average Shortest Path vs Wire Count')
	plt.xlabel('Wire Count')
	plt.ylabel('Average Shortest Path')

	for results in trials:
		xs = [r.wire_count for r in results]
		ys = [float(r.average_shortest_path_length) for r in results]
		
		plt.plot(xs, ys, 'o')

	plt.savefig('shortest.png')
	plt.show()

def visualize(trials):
	#coplot_largest_graph_and_disconnected_nodes(trials)
	#coplot_shortest_average_path_and_total_wire_length(trials)
	coplot_node_density_and_total_wire_length(trials)
	#plot_connectivity_ratio(trials)
	#plot_disconnected_nodes_vs_wire_count(trials)
	#plot_largest_graph_vs_wire_count(trials)	
	#plot_average_shortest_path_vs_wire_count(trials)


class GraphCreationAnimator:
	def __init__(self):
		self.graphs = []

	def add_graph(self, noc, *args):
		self.graphs.append(noc.create_graph())

	def create_animation(self, save_path):
		fig = plt.figure(figsize=(30,30))

		func = lambda num: nx.draw(self.graphs[num], {xy: xy for xy in nx.nodes(self.graphs[num])}	)
		
		line_ani = animation.FuncAnimation(fig, func, len(self.graphs))

		plt.rcParams['animation.ffmpeg_path'] = '/usr/local/bin/ffmpeg'
		Writer = animation.writers['ffmpeg']
		writer = Writer(metadata=dict(artist='Me'), bitrate=1800)
		line_ani.save(save_path, fps=1, writer=writer)




	