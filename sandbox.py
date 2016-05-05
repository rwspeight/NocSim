#!/usr/bin/python

#import math
#from math import tan
#from random import random
#import networkx as nx
#import matplotlib.pyplot as plt
#import wire as w
import analyze as z
from generators import get_distributions

import argparse as ap
p = ap.ArgumentParser(
	prog="sandbox", 
	description="NoC random assembly modeling simulation.",
	epilog="="*60)
p.add_argument("-w", "--wires", help="Wire count range", metavar=("{from}", "{to}"), nargs=2, dest="wire_range", type=int)
p.add_argument("-l", "--lengths", help="Wire length range", metavar=("{from}", "{to}"), nargs=2, dest="length_range")
p.add_argument("-s", "--step", help="Wire count range step size", metavar="{step}", nargs=1, dest="count")
p.add_argument("-W", "--width", help="Width of the N x N chip to simulate", metavar="{width}", nargs=1, dest="width")
p.add_argument("-t", "--trials", help="Number of trials to run with the given parameters", metavar="{trails}", nargs=1, dest="dist")

choices = [k for k in dict(get_distributions())]
p.add_argument("-d", "--dist", help="Wire distribution to use.", choices=choices)
args = p.parse_args()

print args
#wi = w.WireRegionIndex()
#wi.add(w.Wire(math.pi/4, 0, 0, 2))
#wi.add(w.Wire(math.pi*3/4, 4.8, 0, 2))
#wi.add(w.Wire(1, 50, 50, 100))
#print wi.get_neighbors(w.Wire(-math.pi, 3.41, 0, 2))


a = z.AnalysisResult()
a.wire_count = 1
a.largest_graph_node_count = 2
a.average_shortest_path_length = 3
a.disconnected_node_count = 4
a.total_wire_length = 5

b = z.AnalysisResult()
b.from_csv(a.to_csv())

print b